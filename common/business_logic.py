import asyncio

# --- INTERVIEW ASSISTANT LOGIC ---

INTERVIEW_QUESTION_BANK = {
    "software_engineering": [
        {
            "main": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] where 
            nums[i] + nums[j] + nums[k] == 0, and the indices i, j and k are all distinct.
            The output should not contain any duplicate triplets. You may return the output and the triplets in any order.
            For example, if the input is an array 'nums' containing [-1,0,1,2,-1,-4] the output would be [-1,-1,2] and [-1,0,1].
            If the only possible triple does not sum up to 0, the output should be empty""",

            "hints": [
                "You should aim for a solution with O(n^2) time and O(1) space, where n is the size of the input array.",
                "A brute force solution would be to check for every triplet in the array. This would be an O(n^3) solution. Can you think of a better way?",
                """We can iterate through nums with index i and get nums[i] = -(nums[j] + nums[k]) after rearranging the equation, making -nums[i] = nums[j] + 
                nums[k]. For each index i, we should efficiently calculate the j and k pairs without duplicates. Which algorithm is suitable to find j and k pairs?""",
                """To efficiently find the j and k pairs, we run the two pointer approach on the elements to the right of index i as the array is sorted. When we run two 
                pointer algorithm, consider j and k as pointers (j is at left, k is at right) and target = -nums[i], if the current sum num[j] + nums[k] < target then we 
                need to increase the value of current sum by incrementing j pointer. Else if the current sum num[j] + nums[k] > target then we should decrease the value of 
                current sum by decrementing k pointer. How do you deal with duplicates?""",
                """When the current sum nums[j] + nums[k] == target add this pair to the result. We can move j or k pointer until j < k and the pairs are repeated. 
                This ensures that no duplicate pairs are added to the result.""",
            ]
        },
        {
            "main": """Design an algorithm to encode a list of strings to a single string. The encoded string is then decoded back to the original list of strings.
            Please implement encode and decode. For example, if the input is ["neet","code","love","you"] the output would be ["neet","code","love","you"] or if the i
            input is ["we","say",":","yes"] teh output would be ["we","say",":","yes"]""",

            "hints": [
                "You should aim for a solution with O(m) time for each encode() and decode() call and O(m+n) space, where m is the sum of lengths of all the strings and n is the number of strings.",
                "A naive solution would be to use a non-ascii character as a delimiter. Can you think of a better way?",
                "Try to encode and decode the strings using a smart approach based on the lengths of each string. How can you differentiate between the lengths and any numbers that might be present in the strings?",
                """We can use an encoding approach where we start with a number representing the length of the string, followed by a separator character 
                (let's use # for simplicity), and then the string itself. To decode, we read the number until we reach a #, then use that number to read the specified number of characters as the string.""",
            ]
        },
        {
            "main": """You are given an array of length n which was originally sorted in ascending order. It has now been rotated between 1 and n times. For example, the array nums of [1,2,3,4,5,6] might become
            [3,4,5,6,1,2] if it was rotated 4 times or [1,2,3,4,5,6] if it was rotated 6 times. Given the rotated sorted array nums and an integer target, return the index of target within nums, or -1 if it is not present.
            You may assume all elements in the sorted rotated array nums are unique, A solution that runs in O(n) time is trivial, can you write an algorithm that runs in O(log n) time?
            For example, if an array nums contains [3,4,5,6,1,2], and teh traget is one, the output should be 4. Or if nums contains [3,4,5,6,0,1,2] and the target is 4, the output should be -1.""",

            "hints": [
                "You should aim for a solution with O(logn) time and O(1) space, where n is the size of the input array.",
                "A brute force solution would be to do a linear search on the array to find the target element. This would be an O(n) solution. Can you think of a better way? Maybe an efficient searching algorithm is helpful.",
                """Given that the array is rotated after sorting, elements from the right end are moved to the left end one by one, creating two sorted segments separated by a deflection point due to the rotation. 
                For example, consider the array [3, 4, 1, 2], which is rotated twice, resulting in two sorted segments: [3, 4] and [1, 2]. In a fully sorted array, it's easy to find the target. So, if you can identify 
                the deflection point (cut), you can perform a binary search on both segments to find the target element. Can you use binary search to find this cut?""",
                """We perform a binary search on the array with pointers l and r, which belong to two different sorted segments. For example, in [3, 4, 5, 6, 1, 2, 3], l = 0, r = 6, and mid = 3. 
                At least two of l, mid, and r will always be in the same sorted segment. Can you find conditions to eliminate one half and continue the binary search? Perhaps analyzing all possible conditions for l, mid, and r may help.""",
                """There are two cases: l and mid belong to the left sorted segment, or mid and r belong to the right sorted segment. If l and mid are in the same segment, nums[l] < nums[mid], so the pivot index must lie in the right part. 
                If mid and r are in the same segment, nums[mid] < nums[r], so the pivot index must lie in the left part. After the binary search, we eventually find the pivot index. Once the pivot is found, it's straightforward to select the 
                segment where the target lies and perform a binary search on that segement to find its position. If we don't find the target, we return -1.""",
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
