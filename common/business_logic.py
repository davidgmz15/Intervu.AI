import asyncio

# --- INTERVIEW ASSISTANT LOGIC ---

INTERVIEW_QUESTION_BANK = {
    "software_engineering": [
        {
            "main": """Given an input string s, reverse the order of the words.cA word is defined as a sequence of non-space characters. 
            The words in s will be separated by at least one space. Return a string of the words in reverse order concatenated by a single space.
            Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single 
            space separating the words. Do not include any extra spaces.
            For example, if you input "the sky is blue", the output should be "blue is the sky", or if you input "  hello    world   ", the output should be "world hello", removing all the spaces.""",

            "hints": [
                "What is the brute-force solution?",
                "What data structure would you use to solve this efficiently?",
                "What is the time and space complexity of your solution?",
                "How would you handle edge cases?",
            ]
        },
        
    ],
    "consulting": [
        {
            "case": "A beverage company wants to enter a new market. How would you approach this case?",
            "follow_ups": [
                "What clarifying questions would you ask?",
                "What framework would you use to structure your analysis?",
                "Suppose the market size is 10 million people and the average consumption is 20 liters per year. What is the total addressable market?",
                "If the company expects to capture 5% market share in 3 years, what is the expected annual revenue at a price of $2 per liter?",
                "What risks or barriers should the company consider before entering?",
                "What is your final recommendation?"
            ]
        },
        {
            "case": "A retail chain is experiencing declining profits. How would you diagnose the problem?",
            "follow_ups": [
                "What data would you request first?",
                "What are the main drivers of profitability in retail?",
                "Suppose costs have increased by 10% but revenue is flat. What would you investigate next?",
                "If you find that one region is underperforming, how would you analyze the cause?",
                "What recommendations would you make to improve profitability?"
            ]
        },
        {
            "case": "A tech startup wants to double its user base in one year. How would you help them achieve this?",
            "follow_ups": [
                "What growth levers would you consider?",
                "How would you prioritize between marketing, product, and partnerships?",
                "Suppose the current user base is 100,000 and the average monthly growth rate is 5%. What growth rate is needed to reach the goal?",
                "What risks or challenges might the company face?",
                "What is your final recommendation?"
            ]
        }
    ],
    "banking": [
        {
            "question": "What is the difference between retail banking and investment banking?",
            "template_answer": "Retail banking provides services to individual consumers, such as savings accounts and loans, while investment banking focuses on services like underwriting, mergers and acquisitions, and raising capital for corporations."
        },
        {
            "question": "Explain the concept of fractional reserve banking.",
            "template_answer": "Fractional reserve banking is a system where banks keep a fraction of deposits as reserves and lend out the rest, allowing money creation through the lending process."
        },
        {
            "question": "What is Basel III and why is it important?",
            "template_answer": "Basel III is a set of international banking regulations developed to strengthen regulation, supervision, and risk management within the banking sector, focusing on capital adequacy, stress testing, and market liquidity risk."
        },
        {
            "question": "How do banks manage credit risk?",
            "template_answer": "Banks manage credit risk by assessing borrowers' creditworthiness, setting lending limits, requiring collateral, and diversifying their loan portfolios."
        },
        {
            "question": "What is the role of the Federal Reserve?",
            "template_answer": "The Federal Reserve is the central bank of the United States, responsible for setting monetary policy, regulating banks, maintaining financial stability, and providing financial services to the government and other banks."
        }
    ],
    "quantitative_finance": [
        {
            "question": "What is the Black-Scholes model used for?",
            "template_answer": "The Black-Scholes model is used to price European options and calculate theoretical values based on factors like volatility, time, and risk-free rate."
        },
        {
            "question": "Explain the concept of Value at Risk (VaR).",
            "template_answer": "Value at Risk (VaR) is a risk measure that estimates the maximum potential loss of a portfolio over a given time period at a certain confidence level."
        },
        {
            "question": "What is a martingale process in finance?",
            "template_answer": "A martingale is a stochastic process where the expected value of the next observation is equal to the present value, given all prior information. It's used in modeling fair games and financial markets."
        },
        {
            "question": "How do you simulate a random walk in Python?",
            "template_answer": "You can simulate a random walk using numpy by cumulatively summing random steps, e.g., np.cumsum(np.random.randn(n))."
        },
        {
            "question": "What is the difference between correlation and cointegration?",
            "template_answer": "Correlation measures the linear relationship between two variables, while cointegration indicates a long-term equilibrium relationship between two or more time series."
        }
    ],
    "behavioral": [
        {
            "question": "Can you tell me about yourself?",
            "template_answer": "A concise summary of your background, key skills, and what motivates you."
        },
        {
            "question": "Why do you want to work at this company?",
            "template_answer": "Show you've researched the company and connect your goals/values to theirs."
        },
        {
            "question": "Describe a time you faced a challenge at work and how you handled it.",
            "template_answer": "Describe the situation, your actions, and the outcome, focusing on problem-solving and resilience."
        },
        {
            "question": "Tell me about a time you worked on a team project.",
            "template_answer": "Describe your role, how you collaborated, and what the team achieved."
        },
        {
            "question": "What are your greatest strengths and weaknesses?",
            "template_answer": "Identify a key strength with an example, and a real weakness with steps you are taking to improve."
        }
    ]
}

async def get_next_interview_question(industry, asked_questions, step=0):
    """
    For software_engineering, return the main question and the list of hints.
    For consulting, return the main case and follow-up prompts based on 'step'.
    For banking, quantitative_finance, and behavioral, return the next unasked question.
    'asked_questions' should be a list of dicts with 'main' or 'case' for multi-step, or 'question' for single-step.
    """
    questions = INTERVIEW_QUESTION_BANK.get(industry, [])
    if industry == "software_engineering":
        for q in questions:
            key = "main"
            if not any(a.get(key) == q[key] for a in asked_questions):
                return {"question": q[key], "hints": q.get("hints", [])}
        return {"question": None}
    elif industry == "consulting":
        for q in questions:
            key = "case"
            if not any(a.get(key) == q[key] for a in asked_questions):
                # If step is 0, return the main/case question
                if step == 0:
                    return {"question": q[key], "follow_up": q["follow_ups"][0] if q["follow_ups"] else None, "step": 0}
                # If step > 0, return the next follow-up
                elif step < len(q["follow_ups"]):
                    return {"question": q[key], "follow_up": q["follow_ups"][step], "step": step}
                else:
                    return {"question": None}  # All follow-ups done
        return {"question": None}  # No more questions
    else:
        for q in questions:
            if not any(a.get("question") == q["question"] for a in asked_questions):
                return {"question": q["question"]}
        return {"question": None}  # No more questions

async def get_template_answer(industry, question):
    """Return the template answer for a given question and industry."""
    questions = INTERVIEW_QUESTION_BANK.get(industry, [])
    for q in questions:
        if q["question"] == question:
            return q["template_answer"]
    return ""

async def rate_answer(user_answer, template_answer):
    """Basic rule-based rating: returns a score and summary."""
    if not user_answer or not template_answer:
        return {"score": 0, "summary": "No answer provided."}
    # Simple scoring: check for length and keyword overlap
    score = 1
    feedback = "Answer is too short. Try to elaborate more."
    if len(user_answer.split()) > 20:
        score += 1
    if any(word in user_answer.lower() for word in template_answer.lower().split()[:5]):
        score += 1
    if score == 3:
        feedback = "Good answer! You covered the main points."
    elif score == 2:
        feedback = "Decent answer, but could use more detail or relevance."
    return {"score": score, "summary": feedback}

async def get_feedback(user_answer, template_answer):
    """Provide concise, actionable feedback based on the answer and template."""
    if not user_answer:
        return "Please try to answer the question so I can give you feedback."
    if not template_answer:
        return "No template answer available for this question."

    short = len(user_answer.split()) < 15
    template_keywords = set(template_answer.lower().split())
    user_keywords = set(user_answer.lower().split())
    overlap = template_keywords & user_keywords

    if short:
        return "Try to give a more detailed answer with a specific example."
    if overlap:
        return f"Good start. You mentioned: {', '.join(list(overlap)[:2])}. Focus on being clear and direct."
    return "Address the main points of the question more directly and keep your answer focused."

# Sample data for use in the client
MOCK_DATA = {
    "sample_data": [
        {"industry": "software_engineering", "question": "Given an array of integers, return the indices of the two numbers that add up to a specific target."},
        {"industry": "consulting", "case": "A beverage company wants to enter a new market. How would you approach this case?"},
        {"industry": "banking", "question": "What is the difference between retail banking and investment banking?"},
        {"industry": "quantitative_finance", "question": "What is the Black-Scholes model used for?"},
        {"industry": "behavioral", "question": "Can you tell me about yourself?"}
    ]
}
