from flask import Flask, render_template, jsonify, session, request
from flask_socketio import SocketIO
import pyaudio
import asyncio
import websockets
import os
import json
import threading
import janus
import queue
import sys
import time
import requests
from datetime import datetime
from common.agent_functions import FUNCTION_MAP
from common.agent_templates import AgentTemplates
import logging

from common.log_formatter import CustomFormatter
from flask import copy_current_request_context
import subprocess
import collections


# Configure Flask and SocketIO
app = Flask(__name__, static_folder="./static", static_url_path="/")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")
socketio = SocketIO(app)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with the custom formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(CustomFormatter(socketio=socketio))
logger.addHandler(console_handler)

# Remove any existing handlers from the root logger to avoid duplicate messages
logging.getLogger().handlers = []

# Store the latest code for the current session (single user for now)
current_code = ""


class VoiceAgent:
    def __init__(
        self,
        industry="software_engineering",
        voiceModel="aura-2-thalia-en",
        voiceName="",
        learning_mode=False,
        difficulty=None,
    ):
        self.mic_audio_queue = asyncio.Queue()
        self.speaker = None
        self.ws = None
        self.is_running = False
        self.loop = None
        self.audio = None
        self.stream = None
        self.input_device_id = None
        self.output_device_id = None
        self.learning_mode = learning_mode
        self.difficulty = difficulty
        self.agent_templates = AgentTemplates(industry, voiceModel, voiceName, learning_mode)
        self.log_buffer = collections.deque()
        self.awaiting_audio_done = False
        
        # Push-to-talk state
        self.headphones_mode = True
        self.push_to_talk_active = False

    def set_loop(self, loop):
        self.loop = loop

    async def setup(self):
        dg_api_key = os.environ.get("DEEPGRAM_API_KEY")
        if dg_api_key is None:
            logger.error("DEEPGRAM_API_KEY env var not present")
            return False

        settings = self.agent_templates.settings

        try:
            self.ws = await websockets.connect(
                self.agent_templates.voice_agent_url,
                extra_headers={"Authorization": f"Token {dg_api_key}"},
            )
            await self.ws.send(json.dumps(settings))
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Deepgram: {e}")
            return False

    def audio_callback(self, input_data, frame_count, time_info, status_flag):
        if self.is_running and self.loop and not self.loop.is_closed():
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self.mic_audio_queue.put(input_data), self.loop
                )
                future.result(timeout=1)  # Add timeout to prevent blocking
            except Exception as e:
                logger.error(f"Error in audio callback: {e}")
        return (input_data, pyaudio.paContinue)

    async def start_microphone(self):
        try:
            self.audio = pyaudio.PyAudio()

            # List available input devices
            info = self.audio.get_host_api_info_by_index(0)
            numdevices = info.get("deviceCount")
            logger.info(f"Number of devices: {numdevices}")
            logger.info(
                f"Selected input device index from frontend: {self.input_device_id}"
            )

            # Log all available input devices
            available_devices = []
            for i in range(0, numdevices):
                device_info = self.audio.get_device_info_by_host_api_device_index(0, i)
                if device_info.get("maxInputChannels") > 0:
                    available_devices.append(i)

            # If a specific device index was provided from the frontend, use it
            if self.input_device_id and self.input_device_id.isdigit():
                requested_index = int(self.input_device_id)
                # Verify the requested index is valid
                if requested_index in available_devices:
                    input_device_index = requested_index
                    logger.info(f"Using selected device index: {input_device_index}")
                else:
                    logger.warning(
                        f"Requested device index {requested_index} not available, using default"
                    )

            # If still no device selected, use first available
            if input_device_index is None and available_devices:
                input_device_index = available_devices[0]
                logger.info(f"Using first available device index: {input_device_index}")

            if input_device_index is None:
                raise Exception("No input device found")

            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.agent_templates.user_audio_sample_rate,
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=self.agent_templates.user_audio_samples_per_chunk,
                stream_callback=self.audio_callback,
            )
            self.stream.start_stream()
            logger.info("Microphone started successfully")
            return self.stream, self.audio
        except Exception as e:
            logger.error(f"Error starting microphone: {e}")
            if self.audio:
                self.audio.terminate()
            raise

    def cleanup(self):
        """Clean up audio resources"""
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                logger.error(f"Error closing audio stream: {e}")

        if self.audio:
            try:
                self.audio.terminate()
            except Exception as e:
                logger.error(f"Error terminating audio: {e}")

    async def sender(self):
        try:
            while self.is_running:
                data = await self.mic_audio_queue.get()
                if self.ws and data:
                    # Only send audio if in headphones mode OR push-to-talk is active
                    if self.headphones_mode or self.push_to_talk_active:
                        await self.ws.send(data)
        except Exception as e:
            logger.error(f"Error in sender: {e}")
    
    def set_push_to_talk_mode(self, headphones_mode, push_to_talk_active):
        """Update push-to-talk state"""
        self.headphones_mode = headphones_mode
        self.push_to_talk_active = push_to_talk_active
        logger.info(f"Push-to-talk mode updated: headphones={headphones_mode}, ptt_active={push_to_talk_active}")

    async def receiver(self):
        try:
            self.speaker = Speaker()
            last_user_message = None
            last_function_response_time = None
            in_function_chain = False
            with self.speaker:
                async for message in self.ws:
                    if isinstance(message, str):
                        log_this = False
                        if message.startswith("Server: "):
                            try:
                                json_part = message[message.find("{") : message.rfind("}") + 1]
                                data = json.loads(json_part)
                                if (
                                    (data.get("type") == "ConversationText" and data.get("role") == "assistant")
                                    or data.get("type") == "AgentAudioDone"
                                ):
                                    self.log_buffer.append(message)
                                    log_this = True
                                    if data.get("type") == "AgentAudioDone":
                                        self.awaiting_audio_done = True
                            except Exception:
                                pass
                        message_json = json.loads(message)
                        message_type = message_json.get("type")
                        current_time = time.time()

                        if message_type == "UserStartedSpeaking":
                            self.speaker.stop()
                        elif message_type == "ConversationText":
                            # Emit the conversation text to the client
                            socketio.emit("conversation_update", message_json)

                            if message_json.get("role") == "user":
                                last_user_message = current_time
                                in_function_chain = False
                            elif message_json.get("role") == "assistant":
                                in_function_chain = False

                        elif message_type == "FunctionCalling":
                            if in_function_chain and last_function_response_time:
                                latency = current_time - last_function_response_time
                                logger.info(
                                    f"LLM Decision Latency (chain): {latency:.3f}s"
                                )
                            elif last_user_message:
                                latency = current_time - last_user_message
                                logger.info(
                                    f"LLM Decision Latency (initial): {latency:.3f}s"
                                )
                                in_function_chain = True

                        elif message_type == "FunctionCallRequest":
                            functions = message_json.get("functions")
                            if len(functions) > 1:
                                raise NotImplementedError(
                                    "Multiple functions received in FunctionCallRequest"
                                )
                            function_name = functions[0].get("name")
                            function_call_id = functions[0].get("id")
                            parameters = json.loads(functions[0].get("arguments", {}))

                            # Force the industry to be the one this agent was configured with.
                            if function_name == "get_next_interview_question":
                                parameters["industry"] = self.agent_templates.industry
                                # Only add difficulty for software engineering
                                if self.difficulty and self.agent_templates.industry == "software_engineering":
                                    parameters["difficulty"] = self.difficulty
                                logger.info(
                                    f"Overriding/setting industry for get_next_interview_question to: {parameters['industry']}, difficulty: {self.difficulty if self.agent_templates.industry == 'software_engineering' else 'N/A (not software engineering)'}"
                                )

                            logger.info(f"Function call received: {function_name}")
                            logger.info(f"Parameters: {parameters}")

                            start_time = time.time()
                            try:
                                func = FUNCTION_MAP.get(function_name)
                                if not func:
                                    raise ValueError(
                                        f"Function {function_name} not found"
                                    )

                                # Special handling for functions that need websocket
                                if function_name in ["agent_filler", "end_call"]:
                                    result = await func(self.ws, parameters)

                                    if function_name == "agent_filler":
                                        # Extract messages
                                        inject_message = result["inject_message"]
                                        function_response = result["function_response"]

                                        # First send the function response
                                        response = {
                                            "type": "FunctionCallResponse",
                                            "id": function_call_id,
                                            "name": function_name,
                                            "content": json.dumps(function_response),
                                        }
                                        await self.ws.send(json.dumps(response))
                                        logger.info(
                                            f"Function response sent: {json.dumps(function_response)}"
                                        )

                                        # Update the last function response time
                                        last_function_response_time = time.time()
                                        # Then just inject the message and continue
                                        await inject_agent_message(
                                            self.ws, inject_message
                                        )
                                        continue

                                    elif function_name == "end_call":
                                        # Extract messages
                                        inject_message = result["inject_message"]
                                        function_response = result["function_response"]
                                        close_message = result["close_message"]

                                        # First send the function response
                                        response = {
                                            "type": "FunctionCallResponse",
                                            "id": function_call_id,
                                            "name": function_name,
                                            "content": json.dumps(function_response),
                                        }
                                        await self.ws.send(json.dumps(response))
                                        logger.info(
                                            f"Function response sent: {json.dumps(function_response)}"
                                        )

                                        # Update the last function response time
                                        last_function_response_time = time.time()

                                        # Then wait for farewell sequence to complete
                                        await wait_for_farewell_completion(
                                            self.ws, self.speaker, inject_message
                                        )

                                        # Finally send the close message and exit
                                        logger.info(f"Sending ws close message")
                                        await close_websocket_with_timeout(self.ws)
                                        self.is_running = False
                                        break
                                else:
                                    result = await func(parameters)

                                execution_time = time.time() - start_time
                                logger.info(
                                    f"Function Execution Latency: {execution_time:.3f}s"
                                )

                                # Special handling for score_answer function in learning mode
                                if function_name == "score_answer" and self.learning_mode:
                                    # Emit score event to frontend for display
                                    socketio.emit("answer_score", result)
                                    logger.info(f"Score event emitted: {result}")

                                # Send the response back
                                response = {
                                    "type": "FunctionCallResponse",
                                    "id": function_call_id,
                                    "name": function_name,
                                    "content": json.dumps(result),
                                }
                                await self.ws.send(json.dumps(response))
                                logger.info(
                                    f"Function response sent: {json.dumps(result)}"
                                )

                                # Update the last function response time
                                last_function_response_time = time.time()

                            except Exception as e:
                                logger.error(f"Error executing function: {str(e)}")
                                result = {"error": str(e)}
                                response = {
                                    "type": "FunctionCallResponse",
                                    "id": function_call_id,
                                    "name": function_name,
                                    "content": json.dumps(result),
                                }
                                await self.ws.send(json.dumps(response))

                        elif message_type == "Welcome":
                            logger.info(
                                f"Connected with session ID: {message_json.get('session_id')}"
                            )
                        elif message_type == "CloseConnection":
                            logger.info("Closing connection...")
                            await self.ws.close()
                            break

                    elif isinstance(message, bytes):
                        await self.speaker.play(message)
                    # After all messages, check if we just got AgentAudioDone and flush
                    if getattr(self, "awaiting_audio_done", False):
                        while self.speaker._queue and not self.speaker._queue.sync_q.empty():
                            await asyncio.sleep(0.01)
                        await asyncio.sleep(0.2)  # Artificial delay for testing
                        while self.log_buffer:
                            logger.info(self.log_buffer.popleft())
                        self.awaiting_audio_done = False

        except Exception as e:
            logger.error(f"Error in receiver: {e}")

    async def run(self):
        if not await self.setup():
            return

        self.is_running = True
        try:
            stream, audio = await self.start_microphone()
            await asyncio.gather(
                self.sender(),
                self.receiver(),
            )
        except Exception as e:
            logger.error(f"Error in run: {e}")
        finally:
            self.is_running = False
            self.cleanup()
            if self.ws:
                await self.ws.close()


class Speaker:
    def __init__(self, agent_audio_sample_rate=None):
        self._queue = None
        self._stream = None
        self._thread = None
        self._stop = None
        self.agent_audio_sample_rate = (
            agent_audio_sample_rate if agent_audio_sample_rate else 16000
        )

    def __enter__(self):
        audio = pyaudio.PyAudio()
        self._stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.agent_audio_sample_rate,
            input=False,
            output=True,
        )
        self._queue = janus.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=_play, args=(self._queue, self._stream, self._stop), daemon=True
        )
        self._thread.start()

    def __exit__(self, exc_type, exc_value, traceback):
        self._stop.set()
        self._thread.join()
        self._stream.close()
        self._stream = None
        self._queue = None
        self._thread = None
        self._stop = None

    async def play(self, data):
        return await self._queue.async_q.put(data)

    def stop(self):
        if self._queue and self._queue.async_q:
            while not self._queue.async_q.empty():
                try:
                    self._queue.async_q.get_nowait()
                except janus.QueueEmpty:
                    break


def _play(audio_out, stream, stop):
    while not stop.is_set():
        try:
            data = audio_out.sync_q.get(True, 0.05)
            stream.write(data)
        except queue.Empty:
            pass


async def inject_agent_message(ws, inject_message):
    """Simple helper to inject an agent message."""
    logger.info(f"Sending InjectAgentMessage: {json.dumps(inject_message)}")
    await ws.send(json.dumps(inject_message))


async def close_websocket_with_timeout(ws, timeout=5):
    """Close websocket with timeout to avoid hanging if no close frame is received."""
    try:
        await asyncio.wait_for(ws.close(), timeout=timeout)
    except Exception as e:
        logger.error(f"Error during websocket closure: {e}")


async def wait_for_farewell_completion(ws, speaker, inject_message):
    """Wait for the farewell message to be spoken completely by the agent."""
    # Send the farewell message
    await inject_agent_message(ws, inject_message)

    # First wait for either AgentStartedSpeaking or matching ConversationText
    speaking_started = False
    while not speaking_started:
        message = await ws.recv()
        if isinstance(message, bytes):
            await speaker.play(message)
            continue

        try:
            message_json = json.loads(message)
            logger.info(f"Server: {message}")
            if message_json.get("type") == "AgentStartedSpeaking" or (
                message_json.get("type") == "ConversationText"
                and message_json.get("role") == "assistant"
                and message_json.get("content") == inject_message["message"]
            ):
                speaking_started = True
        except json.JSONDecodeError:
            continue

    # Then wait for AgentAudioDone
    audio_done = False
    while not audio_done:
        message = await ws.recv()
        if isinstance(message, bytes):
            await speaker.play(message)
            continue

        try:
            message_json = json.loads(message)
            logger.info(f"Server: {message}")
            if message_json.get("type") == "AgentAudioDone":
                audio_done = True
        except json.JSONDecodeError:
            continue

    # Give audio time to play completely
    await asyncio.sleep(3.5)


# Get available audio devices
def get_audio_devices():
    try:
        audio = pyaudio.PyAudio()
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get("deviceCount")

        input_devices = []
        for i in range(0, numdevices):
            device_info = audio.get_device_info_by_host_api_device_index(0, i)
            if device_info.get("maxInputChannels") > 0:
                input_devices.append({"index": i, "name": device_info.get("name")})

        audio.terminate()
        return input_devices
    except Exception as e:
        logger.error(f"Error getting audio devices: {e}")
        return []


# Flask routes
@app.route("/")
def index():
    # Sample data for the frontend
    sample_data = [
        {"industry": "software_engineering", "question": "Given an array of integers, return the indices of the two numbers that add up to a specific target."},
        {"industry": "consulting", "case": "A beverage company wants to enter a new market. How would you approach this case?"},
        {"industry": "banking", "question": "What is the difference between retail banking and investment banking?"},
        {"industry": "quantitative_finance", "question": "What is the Black-Scholes model used for?"},
        {"industry": "behavioral", "question": "Can you tell me about yourself?"}
    ]
    return render_template("index.html", sample_data=sample_data)


@app.route("/audio-devices")
def audio_devices():
    # Get available audio devices
    devices = get_audio_devices()
    return {"devices": devices}


@app.route("/industries")
def get_industries():
    # Get available industries from AgentTemplates
    return AgentTemplates.get_available_industries()


@app.route("/tts-models")
def get_tts_models():
    # Get TTS models from Deepgram API
    try:
        dg_api_key = os.environ.get("DEEPGRAM_API_KEY")
        if not dg_api_key:
            return jsonify({"error": "DEEPGRAM_API_KEY not set"}), 500

        response = requests.get(
            "https://api.deepgram.com/v1/models",
            headers={"Authorization": f"Token {dg_api_key}"},
        )

        if response.status_code != 200:
            return (
                jsonify(
                    {"error": f"API request failed with status {response.status_code}"}
                ),
                500,
            )

        data = response.json()

        # Process TTS models
        formatted_models = []

        # Check if 'tts' key exists in the response
        if "tts" in data:
            # Filter for only aura-2 models
            for model in data["tts"]:
                if model.get("architecture") == "aura-2":
                    # Extract language from languages array if available
                    language = "en"
                    if model.get("languages") and len(model.get("languages")) > 0:
                        language = model["languages"][0]

                    # Extract metadata for additional information
                    metadata = model.get("metadata", {})
                    accent = metadata.get("accent", "")
                    tags = ", ".join(metadata.get("tags", []))

                    formatted_models.append(
                        {
                            "name": model.get("canonical_name", model.get("name")),
                            "display_name": model.get("name"),
                            "language": language,
                            "accent": accent,
                            "tags": tags,
                            "description": f"{accent} accent. {tags}",
                        }
                    )

        return jsonify({"models": formatted_models})
    except Exception as e:
        logger.error(f"Error fetching TTS models: {e}")
        return jsonify({"error": str(e)}), 500


voice_agent = None


def run_async_voice_agent():
    try:
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Set the loop in the voice agent
        voice_agent.set_loop(loop)

        try:
            # Run the voice agent
            loop.run_until_complete(voice_agent.run())
        except asyncio.CancelledError:
            logger.info("Voice agent task was cancelled")
        except Exception as e:
            logger.error(f"Error in voice agent thread: {e}")
        finally:
            # Clean up the loop
            try:
                # Cancel all running tasks
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()

                # Allow cancelled tasks to complete
                if pending:
                    loop.run_until_complete(
                        asyncio.gather(*pending, return_exceptions=True)
                    )

                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                loop.close()
    except Exception as e:
        logger.error(f"Error in voice agent thread setup: {e}")


@socketio.on("start_voice_agent")
def handle_start_voice_agent(data=None):
    global voice_agent
    logger.info(f"Starting voice agent with data: {data}")
    if voice_agent is None:
        # Get industry from data or default to behavioral
        industry = data.get("industry", "behavioral") if data else "behavioral"
        voiceModel = (
            data.get("voiceModel", "aura-2-thalia-en") if data else "aura-2-thalia-en"
        )
        # Get voice name from data or default to empty string, which uses the Model's voice name in the backend
        voiceName = data.get("voiceName", "") if data else ""
        # Get learning mode from data or default to False (interview mode)
        learning_mode = data.get("learningMode", False) if data else False
        # Get difficulty from data or default to None (all levels)
        difficulty = data.get("difficulty") if data else None
        
        voice_agent = VoiceAgent(
            industry=industry,
            voiceModel=voiceModel,
            voiceName=voiceName,
            learning_mode=learning_mode,
            difficulty=difficulty,
        )
        if data:
            voice_agent.input_device_id = data.get("inputDeviceId")
            voice_agent.output_device_id = data.get("outputDeviceId")
        # Start the voice agent in a background thread
        socketio.start_background_task(target=run_async_voice_agent)


@socketio.on("stop_voice_agent")
def handle_stop_voice_agent():
    global voice_agent
    if voice_agent:
        voice_agent.is_running = False
        if voice_agent.loop and not voice_agent.loop.is_closed():
            try:
                # Cancel all running tasks
                for task in asyncio.all_tasks(voice_agent.loop):
                    task.cancel()
            except Exception as e:
                logger.error(f"Error stopping voice agent: {e}")
        voice_agent = None


# Store session data for the current user (single user for now)
def get_user_session():
    if 'user_data' not in session:
        session['user_data'] = {
            'current_code': '',
            'current_question': '',
            'transcript': ''
        }
    return session['user_data']


@socketio.on("code_update")
def handle_code_update(data):
    user_data = get_user_session()
    user_data['current_code'] = data.get("code", "")
    session.modified = True


@socketio.on("request_hint")
def handle_request_hint(data):
    user_data = get_user_session()
    from common.agent_functions import get_software_engineering_hint
    import asyncio
    question = user_data.get('current_question', '')
    user_answer = user_data.get('transcript', '')
    code = user_data.get('current_code', '')
    params = {"user_answer": user_answer + "\n" + code, "question": question}
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(get_software_engineering_hint(params))
    socketio.emit("hint_response", result)


# Example: update transcript (user's spoken thoughts)
@socketio.on("transcript_update")
def handle_transcript_update(data):
    user_data = get_user_session()
    user_data['transcript'] = data.get('transcript', '')
    session.modified = True


# Example: set current question when a new one is asked
@socketio.on("set_current_question")
def handle_set_current_question(data):
    user_data = get_user_session()
    user_data['current_question'] = data.get('question', '')
    session.modified = True


@socketio.on("run_code")
def handle_run_code(data):
    code = data.get("code", "")
    try:
        # Run the code in a subprocess with a timeout and capture output
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout
        if result.stderr:
            output += ("\n" if output else "") + result.stderr
        if not output.strip():
            output = "(No output)"
    except Exception as e:
        output = f"Error running code: {e}"
    socketio.emit("code_output", {"output": output})


@socketio.on("toggle_push_to_talk_mode")
def handle_toggle_push_to_talk_mode(data):
    """Handle push-to-talk mode changes from frontend"""
    global voice_agent
    if voice_agent:
        headphones_mode = data.get("headphonesMode", True)
        push_to_talk_active = data.get("isPushToTalkActive", False)
        voice_agent.set_push_to_talk_mode(headphones_mode, push_to_talk_active)


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Interview Assistant Demo Starting!")
    print("=" * 60)
    print("\n1. Open this link in your browser to start the demo:")
    print("   http://127.0.0.1:5000")
    print("\n2. Click 'Start Voice Agent' when the page loads")
    print("\n3. Speak with the agent using your microphone")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")

    socketio.run(app, debug=True)