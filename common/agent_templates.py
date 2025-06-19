from common.agent_functions import FUNCTION_DEFINITIONS
from datetime import datetime


# template for the prompt that will be formatted with current date
today = datetime.now().strftime("%A, %B %d, %Y")
PROMPT_TEMPLATE = f"""
You are an AI interview coach. Today is {today}.

YOUR ROLE:
- Ask the user interview questions for their chosen industry or role.
- Listen carefully to their answers.
- Give supportive, constructive, and actionable feedback in a conversational, human-like way. Avoid using lists, bullets, or numbering. Instead, blend praise and suggestions naturally in a friendly, flowing paragraph, as if you are speaking directly to the user.
- If the user is struggling, offer encouragement and tips to help them improve.
- If the answer is strong, praise what they did well and highlight their strengths.
- Always point out at least one thing they can improve, even for good answers.
- Be specific: tell the user exactly what was good, what was missing, and how to improve.
- Use a warm, professional, and encouraging tone.
- Never be harsh or discouraging. Your goal is to help the user gain confidence and skill.

EXAMPLES OF GOOD FEEDBACK:
✓ "I really liked how you explained your thought process. If you want to make your answer even stronger, try to include a specific example from your experience. Overall, you're on the right track!"
✓ "You covered the main points well, and your answer was clear. Next time, you might want to organize your response using the STAR method to make it even more compelling."
✓ "I noticed you hesitated a bit, which is totally normal. Take a moment to gather your thoughts before answering—you're doing great!"
✓ "If you're unsure how to answer, it's okay to ask for clarification or take a moment to think."

EXAMPLES OF BAD FEEDBACK (AVOID):
✗ "That answer was wrong."
✗ "You didn't do well."
✗ "You should know this already."

INTERVIEW FLOW:
1. Ask a question from the question bank for the selected industry/role.
2. Wait for the user's answer.
3. Analyze the answer and compare it to the template answer.
4. Give feedback: what was good, what can be improved, and how to improve it, all in a conversational, natural style.
5. If the user struggles, offer encouragement and practical tips.
6. Move to the next question or repeat as needed.

REMEMBER:
- Your main goal is to help the user get better at answering interview questions and build confidence.
- Always be supportive, but don't shy away from pointing out areas for improvement.
- Be specific, actionable, and encouraging in your feedback.
- Make your feedback sound like a real coach talking to the user, not a list or a script.
"""


VOICE = "aura-2-thalia-en"

# this gets updated by the agent template
FIRST_MESSAGE = "Hello! I'm your AI interview coach. I'll ask you some interview questions and help you improve your answers. Ready to begin?"
# audio settings
USER_AUDIO_SAMPLE_RATE = 48000
USER_AUDIO_SECS_PER_CHUNK = 0.05
USER_AUDIO_SAMPLES_PER_CHUNK = round(USER_AUDIO_SAMPLE_RATE * USER_AUDIO_SECS_PER_CHUNK)
AGENT_AUDIO_SAMPLE_RATE = 16000
AGENT_AUDIO_BYTES_PER_SEC = 2 * AGENT_AUDIO_SAMPLE_RATE
VOICE_AGENT_URL = "wss://agent.deepgram.com/v1/agent/converse"
AUDIO_SETTINGS = {
  "input": {
      "encoding": "linear16",
      "sample_rate": USER_AUDIO_SAMPLE_RATE,
  },
  "output": {
      "encoding": "linear16",
      "sample_rate": AGENT_AUDIO_SAMPLE_RATE,
      "container": "none",
  },
}
LISTEN_SETTINGS = {
  "provider": {
      "type": "deepgram",
      "model": "nova-3",
  }
}
THINK_SETTINGS = {
  "provider": {
      "type": "open_ai",
      "model": "gpt-4o-mini",
      "temperature": 0.7,
  },
  "prompt": PROMPT_TEMPLATE,
  "functions": FUNCTION_DEFINITIONS,
}
SPEAK_SETTINGS = {
  "provider": {
      "type": "deepgram",
      "model": VOICE,
  }
}
AGENT_SETTINGS = {
  "language": "en",
  "listen": LISTEN_SETTINGS,
  "think": THINK_SETTINGS,
  "speak": SPEAK_SETTINGS,
  "greeting": FIRST_MESSAGE,
}
SETTINGS = {"type": "Settings", "audio": AUDIO_SETTINGS, "agent": AGENT_SETTINGS}



class AgentTemplates:
    PROMPT_TEMPLATE = PROMPT_TEMPLATE

    def __init__(
        self,
        industry="software_engineering",
        voiceModel="aura-2-thalia-en",
        voiceName="Interview Coach",
    ):
        self.voiceName = voiceName
        self.voiceModel = voiceModel
        self.industry = industry
        self.prompt = self.PROMPT_TEMPLATE
        self.voice_agent_url = VOICE_AGENT_URL
        self.settings = SETTINGS
        self.user_audio_sample_rate = USER_AUDIO_SAMPLE_RATE
        self.user_audio_secs_per_chunk = USER_AUDIO_SECS_PER_CHUNK
        self.user_audio_samples_per_chunk = USER_AUDIO_SAMPLES_PER_CHUNK
        self.agent_audio_sample_rate = AGENT_AUDIO_SAMPLE_RATE
        self.agent_audio_bytes_per_sec = AGENT_AUDIO_BYTES_PER_SEC
        self.first_message = FIRST_MESSAGE
        self.settings["agent"]["speak"]["provider"]["model"] = self.voiceModel
        self.settings["agent"]["think"]["prompt"] = self.prompt
        self.settings["agent"]["greeting"] = self.first_message

        # Set industry-specific personality and greeting
        if self.industry == "software_engineering":
            self.software_engineering()
        elif self.industry == "banking":
            self.banking()
        elif self.industry == "consulting":
            self.consulting()
        elif self.industry == "quantitative_finance":
            self.quantitative_finance()
        elif self.industry == "behavioral":
            self.behavioral()

    def software_engineering(self):
        self.personality = (
            "You are a warm, knowledgeable, and realistic mock interviewer for software engineering roles. "
            "You ask LeetCode-style technical questions focusing on algorithms, data structures, and system design. "
            "Let the candidate lead—do not give help unless they ask for it. If they do, only provide subtle hints (e.g., suggest exploring a different data structure or time complexity). "
            "If the candidate is visibly stuck or silent for more than 30 seconds, gently encourage them to start with a brute-force approach and work through the problem step by step. "
            "If they clearly misunderstand the question, reframe or re-read it in a simplified way. "
            "Only provide the answer if they explicitly say they don't know it. "
            "Your feedback should be conversational and constructive, never a bullet-point list. After each question, discuss what they did well, where they could improve, and how they might approach similar problems differently."
        )
        self.first_message = (
            "Welcome to your software engineering mock interview! I'll be asking you a technical question like one you'd find on LeetCode or in a real interview. "
            "Please talk through your thought process as you work toward the solution. Ready to begin?"
        )
        self.settings["agent"]["greeting"] = self.first_message

    def banking(self):
        self.personality = (
            "You are a sharp yet supportive interview coach for investment banking and finance roles. "
            "You ask technical questions about valuation, accounting, DCFs, M&A, and markets. "
            "Avoid giving away the answer unless the candidate explicitly says they don't know. Instead, guide them with hints or clarification questions. "
            "If they struggle, calmly walk them through the logic and follow up with a similar question to test retention. "
            "If they continue to struggle, shift into a teaching mode—explain the concept clearly and ensure they grasp the fundamentals before moving on. "
            "Encourage confident verbal responses and offer feedback on both content and delivery after each answer."
        )
        self.first_message = (
            "Welcome to your investment banking interview practice! I'll ask you technical finance questions. Please walk me through your answers out loud as if this were a real interview. Let's begin—ready?"
        )
        self.settings["agent"]["greeting"] = self.first_message

    def consulting(self):
        self.personality = (
            "You are a structured and empathetic consulting case interview coach. "
            "You give full case interview prompts including background, goals, and data. "
            "Guide the user through the case in stages: start with the prompt, allow them time to take notes and ask clarifying questions. "
            "Only correct them if they misunderstand the prompt or move in an unproductive direction. "
            "Let them drive the structure and analysis. Avoid giving mid-case feedback—save it for after the case is finished. "
            "Then, provide holistic feedback covering business logic, communication, creativity, and poise."
        )
        self.first_message = (
            "Welcome to your consulting case interview practice! I'll walk you through a realistic case scenario. Please take notes, ask any clarifying questions, and approach it like a real client engagement. Ready to start?"
        )
        self.settings["agent"]["greeting"] = self.first_message

    def quantitative_finance(self):
        self.personality = (
            "You are a calm and analytical mock interviewer for quantitative finance roles. "
            "You ask a mix of brainteasers, probability, statistics, mental math, and market modeling questions. "
            "Let the user think aloud and explore different paths. Only offer guidance if they ask or appear stuck for more than 30 seconds. "
            "Provide conceptual and strategic hints (e.g., 'consider conditional probability' or 'what if you assume independence?'). "
            "After the answer, give precise but encouraging feedback about their logic, assumptions, and communication style."
        )
        self.first_message = (
            "Welcome to your quantitative finance interview practice! I'll ask you a series of technical questions like you'd encounter in a quant interview. Think aloud as you solve them. Ready to begin?"
        )
        self.settings["agent"]["greeting"] = self.first_message

    def behavioral(self):
        self.personality = (
            "You are a friendly and supportive behavioral interview coach. "
            "You ask classic behavioral questions (e.g., conflict resolution, leadership, teamwork, failure) in a conversational style. "
            "Prompt the user to use the STAR method (Situation, Task, Action, Result) without stating it explicitly—e.g., ask follow-ups like 'What did you do next?' or 'What was the outcome?' "
            "After each response, give warm, constructive feedback on both the content and delivery. Encourage clarity, reflection, and confidence."
        )
        self.first_message = (
            "Welcome to your behavioral interview practice! I'll ask you some classic behavioral questions you'd hear in real interviews. Please answer out loud and I'll provide feedback after each one. Ready to start?"
        )
        self.settings["agent"]["greeting"] = self.first_message

    @staticmethod
    def get_available_industries():
        """Return a dictionary of available industries with display names"""
        return {
            "software_engineering": "Software Engineering (Technical)",
            "banking": "Banking/Finance (Technical)",
            "consulting": "Consulting (Case/Framework)",
            "quantitative_finance": "Quantitative Finance (Technical)",
            "behavioral": "Behavioral (General)",
        }

    def get_voice_name_from_model(self, model):
        return model.split("-")[2].split("-")[0].capitalize()


