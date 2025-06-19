import json
from datetime import datetime, timedelta
import asyncio
from common.business_logic import (
    get_next_interview_question as get_next_interview_question_logic,
    rate_answer,
    get_template_answer,
    get_feedback
)
import groq


async def get_next_interview_question(params):
    # Get the next interview question for the given industry/role
    industry = params.get("industry", "behavioral")
    asked_questions = params.get("asked_questions", [])
    question = await get_next_interview_question_logic(industry, asked_questions)
    return question

async def receive_interview_answer(params):
    # Placeholder: In practice, the answer is received as transcript/audio elsewhere
    return {"status": "received", "answer": params.get("answer", "")}

async def rate_answer(params):
    # Rate the user's answer against a template answer
    question = params.get("question")
    user_answer = params.get("user_answer")
    industry = params.get("industry", "behavioral")
    template_answer = await get_template_answer(industry, question)
    rating = await rate_answer(user_answer, template_answer)
    return rating

async def give_feedback(params):
    # Generate feedback for the user's answer
    question = params.get("question")
    user_answer = params.get("user_answer")
    industry = params.get("industry", "behavioral")
    template_answer = await get_template_answer(industry, question)
    feedback = await get_feedback(user_answer, template_answer)
    return feedback

async def get_software_engineering_hint(params):
    # Use Groq LLM to select the most contextually relevant hint
    user_answer = params.get("user_answer", "")
    question = params.get("question", "")
    # Get the hints for the question
    from common.business_logic import INTERVIEW_QUESTION_BANK
    hints = []
    for q in INTERVIEW_QUESTION_BANK["software_engineering"]:
        if q["main"].strip() == question.strip():
            hints = q.get("hints", [])
            break
    if not hints:
        return {"hint": None}
    # Compose the LLM prompt
    prompt = f"""
        You are an expert technical interview coach. Here is the interview question:
        """
    prompt += f"\nQuestion: {question}\n"
    prompt += f"\nHere is the user's answer so far:\n{user_answer}\n"
    prompt += "\nHere are some hints you can give to help the user progress if they are stuck:\n"
    for i, hint in enumerate(hints):
        prompt += f"{i+1}. {hint}\n"
    prompt += "\nBased on the user's answer and the question, select the single most helpful hint from the list above that would best help the user move forward. Only return the hint text, not the number or any extra explanation."

    # Call the Groq LLM API
    response = await groq.ChatCompletion.acreate(
        model="mixtral-8x7b-32768",
        messages=[{"role": "system", "content": "You are a helpful technical interview coach."},
                  {"role": "user", "content": prompt}]
    )
    selected_hint = response.choices[0].message.content.strip()
    # Ensure the selected hint is one of the provided hints
    for hint in hints:
        if selected_hint.lower() in hint.lower() or hint.lower() in selected_hint.lower():
            return {"hint": hint}
    # Fallback: just return the LLM's output
    return {"hint": selected_hint}

# function definitions that will be sent to the voice agent api
FUNCTION_DEFINITIONS = [
    {
        "name": "get_next_interview_question",
        "description": "Get the next interview question for the user based on the selected industry/role. Pass a list of already asked questions to avoid repeats.",
        "parameters": {
            "type": "object",
            "properties": {
                "industry": {"type": "string", "description": "Industry or role for the interview (e.g., 'software_engineering')."},
                "asked_questions": {"type": "array", "items": {"type": "string"}, "description": "List of questions already asked."}
            },
            "required": ["industry", "asked_questions"]
        }
    },
    {
        "name": "receive_interview_answer",
        "description": "Receive the user's answer to the current interview question.",
        "parameters": {
            "type": "object",
            "properties": {
                "answer": {"type": "string", "description": "The user's answer as text."}
            },
            "required": ["answer"]
        }
    },
    {
        "name": "rate_answer",
        "description": "Rate the user's answer to the interview question compared to a template answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The interview question."},
                "user_answer": {"type": "string", "description": "The user's answer."},
                "industry": {"type": "string", "description": "Industry or role for the interview."}
            },
            "required": ["question", "user_answer", "industry"]
        }
    },
    {
        "name": "give_feedback",
        "description": "Provide constructive feedback on the user's answer, highlighting strengths and areas for improvement.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The interview question."},
                "user_answer": {"type": "string", "description": "The user's answer."},
                "industry": {"type": "string", "description": "Industry or role for the interview."}
            },
            "required": ["question", "user_answer", "industry"]
        }
    },
    {
        "name": "get_software_engineering_hint",
        "description": "Get a hint for the user's answer to the interview question.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_answer": {"type": "string", "description": "The user's answer."},
                "question": {"type": "string", "description": "The interview question."}
            },
            "required": ["user_answer", "question"]
        }
    }
]

# map function names to their implementations
FUNCTION_MAP = {
    "get_next_interview_question": get_next_interview_question,
    "receive_interview_answer": receive_interview_answer,
    "rate_answer": rate_answer,
    "give_feedback": give_feedback,
    "get_software_engineering_hint": get_software_engineering_hint
}




