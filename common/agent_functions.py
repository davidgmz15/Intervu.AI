import os
import re
import difflib
import logging
from common.business_logic import (
    get_next_interview_question as get_next_interview_question_logic,
    rate_answer as rate_answer_logic,
    get_template_answer,
    get_feedback as get_feedback_logic
)
import openai

# Configure OpenAI client to use Groq API
openai.api_key = os.environ.get("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

logger = logging.getLogger(__name__)


async def get_next_interview_question(params):
    """
    Get the next interview question based on industry and previously asked questions.
    
    Args:
        params (dict): Contains 'industry' and 'asked_questions'
    
    Returns:
        dict: The next question data
    """
    # Get industry with default fallback
    industry = params.get("industry", "behavioral")
    
    # Validate industry
    valid_industries = [
        "software_engineering", "consulting", "banking", 
        "quantitative_finance", "behavioral"
    ]
    if industry not in valid_industries:
        industry = "behavioral"
    
    # Map alternate industry names
    industry_mapping = {
        "investment_banking": "banking",
        "quant_finance": "quantitative_finance",
    }
    industry = industry_mapping.get(industry, industry)
    
    # Get asked questions and normalize format
    asked_questions = params.get("asked_questions", [])
    asked_questions = [_normalize_question_format(q, industry) for q in asked_questions]
    
    logger.info(f"Getting next question for industry={industry}, {len(asked_questions)} already asked")
    
    # Get question from business logic
    question = await get_next_interview_question_logic(industry, asked_questions)
    return question


def _normalize_question_format(question, industry):
    """
    Normalize question format based on industry requirements.
    
    Args:
        question: Question in various formats (string or dict)
        industry: The interview industry
    
    Returns:
        dict: Normalized question format
    """
    if isinstance(question, dict):
        # Already in dict format - ensure correct key structure
        if industry == "behavioral" and "question" not in question and len(question) == 1:
            return {"question": list(question.values())[0]}
        return question
    
    # Convert string to appropriate dict format
    key_mapping = {
        "software_engineering": "main",
        "consulting": "case",
        "default": "question"
    }
    key = key_mapping.get(industry, key_mapping["default"])
    return {key: question}


async def rate_user_answer(params):
    """
    Rate a user's answer against the template answer for the question.
    
    Args:
        params (dict): Contains 'question', 'user_answer', and 'industry'
    
    Returns:
        dict: Rating information
    """
    question = params.get("question")
    user_answer = params.get("user_answer")
    industry = params.get("industry", "behavioral")
    
    # Get template answer and rate user's response
    template_answer = await get_template_answer(industry, question)
    rating = await rate_answer_logic(user_answer, template_answer)
    return rating


async def provide_feedback(params):
    """
    Generate constructive feedback for a user's answer.
    
    Args:
        params (dict): Contains 'question', 'user_answer', and 'industry'
    
    Returns:
        dict: Feedback information
    """
    question = params.get("question")
    user_answer = params.get("user_answer")
    industry = params.get("industry", "behavioral")
    
    # Get template answer and generate feedback
    template_answer = await get_template_answer(industry, question)
    feedback = await get_feedback_logic(user_answer, template_answer)
    return feedback


async def get_software_engineering_hint(params):
    """
    Get a contextually relevant hint for software engineering questions using LLM.
    
    Args:
        params (dict): Contains 'user_answer' and 'question'
    
    Returns:
        dict: Contains selected hint or None if no hints available
    """
    user_answer = params.get("user_answer", "")
    question = params.get("question", "")
    
    # Find hints for the question
    hints = _find_question_hints(question)
    if not hints:
        return {"hint": None}
    
    # Use LLM to select most appropriate hint
    try:
        selected_hint = await _select_contextual_hint(question, user_answer, hints)
        return {"hint": selected_hint}
    except Exception as e:
        logger.error(f"Error selecting hint: {e}")
        # Fallback to first hint if LLM fails
        return {"hint": hints[0]}


def _find_question_hints(question):
    """
    Find hints for a software engineering question using exact and fuzzy matching.
    
    Args:
        question (str): The interview question
    
    Returns:
        list: Available hints for the question
    """
    from common.business_logic import INTERVIEW_QUESTION_BANK
    
    def normalize_text(text):
        return re.sub(r"\s+", " ", text.strip().lower())
    
    normalized_question = normalize_text(question)
    software_questions = INTERVIEW_QUESTION_BANK.get("software_engineering", [])
    
    # Try exact matching first
    for q in software_questions:
        normalized_main = normalize_text(q["main"])
        if (normalized_main == normalized_question or 
            normalized_main in normalized_question or 
            normalized_question in normalized_main):
            return q.get("hints", [])
    
    # Try fuzzy matching if exact match fails
    all_questions = [normalize_text(q["main"]) for q in software_questions]
    matches = difflib.get_close_matches(normalized_question, all_questions, n=1, cutoff=0.6)
    
    if matches:
        for q in software_questions:
            if normalize_text(q["main"]) == matches[0]:
                return q.get("hints", [])
    
    return []


async def _select_contextual_hint(question, user_answer, hints):
    """
    Use LLM to select the most contextually appropriate hint.
    
    Args:
        question (str): The interview question
        user_answer (str): User's current answer
        hints (list): Available hints
    
    Returns:
        str: Selected hint
    """
    # Create clear, concise prompt
    prompt = f"""You are a technical interview coach. 

Question: {question}

User's answer so far: {user_answer}

Available hints:
{chr(10).join(f"{i+1}. {hint}" for i, hint in enumerate(hints))}

Select the single most helpful hint from the list above. Return only the hint text, no additional commentary."""

    # Call LLM API
    response = await openai.ChatCompletion.acreate(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are a helpful technical interview coach. Return only the selected hint text."},
            {"role": "user", "content": prompt}
        ]
    )
    
    selected_hint = response.choices[0].message.content.strip()
    
    # Validate response is one of the provided hints (fuzzy match)
    for hint in hints:
        if (selected_hint.lower() in hint.lower() or 
            hint.lower() in selected_hint.lower()):
            return hint
    
    # Fallback to truncated LLM response
    sentences = [s.strip() for s in selected_hint.split('.') if s.strip()]
    truncated = '. '.join(sentences[:2])
    return truncated + '.' if truncated and not truncated.endswith('.') else truncated


# Function definitions for voice agent API
FUNCTION_DEFINITIONS = [
    {
        "name": "get_next_interview_question",
        "description": "Get the next interview question based on industry and avoid repeats.",
        "parameters": {
            "type": "object",
            "properties": {
                "industry": {
                    "type": "string", 
                    "description": "Industry for interview (e.g., 'software_engineering')"
                },
                "asked_questions": {
                    "type": "array", 
                    "items": {"type": "string"}, 
                    "description": "List of already asked questions"
                }
            },
            "required": ["industry", "asked_questions"]
        }
    },
    {
        "name": "rate_user_answer",
        "description": "Rate user's answer compared to template answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The interview question"},
                "user_answer": {"type": "string", "description": "User's answer"},
                "industry": {"type": "string", "description": "Interview industry"}
            },
            "required": ["question", "user_answer", "industry"]
        }
    },
    {
        "name": "provide_feedback",
        "description": "Provide constructive feedback on user's answer.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The interview question"},
                "user_answer": {"type": "string", "description": "User's answer"},
                "industry": {"type": "string", "description": "Interview industry"}
            },
            "required": ["question", "user_answer", "industry"]
        }
    },
    {
        "name": "get_software_engineering_hint",
        "description": "Get contextual hint for software engineering questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_answer": {"type": "string", "description": "User's current answer"},
                "question": {"type": "string", "description": "The interview question"}
            },
            "required": ["user_answer", "question"]
        }
    }
]

# Map function names to implementations
FUNCTION_MAP = {
    "get_next_interview_question": get_next_interview_question,
    "rate_user_answer": rate_user_answer,
    "provide_feedback": provide_feedback,
    "get_software_engineering_hint": get_software_engineering_hint
}