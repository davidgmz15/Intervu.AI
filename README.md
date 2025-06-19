# PrepPal AI

## Overview

PrepPal AI is a web-based application that simulates real interview scenarios for a variety of industries, including behavioral, software engineering, consulting, banking/finance, and quantitative finance. It uses voice interaction and AI-driven feedback to help users practice and improve their interview skills in a realistic, supportive environment.

## Features
- **Voice-based Interview Practice:** Speak your answers and interact with the AI agent in real time.
- **Industry-Specific Questions:** Choose from behavioral, technical, consulting, finance, and quant interviews.
- **Conversational Feedback:** Receive concise, actionable feedback on your answers, tailored to the question and your response.
- **Hints for Technical Questions:** For software engineering, the agent can provide context-aware hints if you get stuck.
- **Customizable Agent:** Easily modify the agent's logic, feedback style, and question bank.
- **Modern Web UI:** Clean, responsive interface with adjustable log/conversation panels and dark mode.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd interview_assistant
```

### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
- **DEEPGRAM_API_KEY:** Required for voice-to-text and text-to-speech.
- **(Optional) OpenAI or Groq API Key:** If using LLM-based hint selection, set the appropriate API key as an environment variable (e.g., `OPENAI_API_KEY` or `GROQ_API_KEY`).

You can set these in your shell or in a `.env` file (if using a tool like `python-dotenv`).

### 5. Run the Application
```bash
python client.py
```
- Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000)
- Click "Start Interview" to begin.

## Customization & Extending the Agent

You can easily modify the agent's logic, feedback, and question bank by editing the following files:

- **`common/agent_functions.py`:**
  - Add or modify the agent's high-level logic, function definitions, and how the agent interacts with the user.
- **`common/business_logic.py`:**
  - Add, remove, or edit interview questions for any industry in the `INTERVIEW_QUESTION_BANK` dictionary.
  - Adjust how questions, hints, and feedback are selected and generated.
- **`common/agent_templates.py`:**
  - Change the agent's personality, greeting, and prompt style for each industry.
  - Adjust the system prompt and example feedback for the LLM.

**To add your own questions:**
- Open `common/business_logic.py`.
- Find the `INTERVIEW_QUESTION_BANK` dictionary.
- Add your question(s) under the appropriate industry key, following the existing format.
- For software engineering, you can add a `hints` list to each question.
- For consulting, add `follow_ups` for multi-step cases.

## Contributing
- Please only modify the files listed above for logic, feedback, or question changes.
- For UI or server changes, edit the corresponding HTML/CSS/JS or Flask server code.

## Support
If you encounter issues or have questions, please open an issue or contact the maintainer.

---

Enjoy practicing your interviews and improving your skills with the AI Interview Assistant! 