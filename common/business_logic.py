import random
import logging

logger = logging.getLogger(__name__)

# Interview question bank organized by industry
INTERVIEW_QUESTION_BANK = {
    "software_engineering": [
        {
            "main": """Given an integer array nums, return all the triplets nums i, nums j, and nums k where 
            nums i plus nums j plus nums k equal 0, and the indices i, j and k are all distinct.
            The output should not contain any duplicate triplets. You may return the output and the triplets in any order.
            For example, if the input is an array 'nums' containing negative 1 , 0, 1, 2, negative 1, and negative 4 the output would be negative 1, negative 1, 2 and negative 1, 0, 1.
            If the only possible triple does not sum up to 0, the output should be empty""",
            "hints": [
                "You should aim for a solution with O of n squared time and O of 1 space, where n is the size of the input array.",
                "A brute force solution would be to check for every triplet in the array. This would be an O of n cubed solution. Can you think of a better way?",
                """We can iterate through nums with index i and get nums i equals negative nums j plus nums k after rearranging the equation, making negative nums i equal nums j plus 
                nums k. For each index i, we should efficiently calculate the j and k pairs without duplicates. Which algorithm is suitable to find j and k pairs?""",
                """To efficiently find the j and k pairs, we run the two pointer approach on the elements to the right of index i as the array is sorted. When we run two 
                pointer algorithm, consider j and k as pointers (j is at left, k is at right) and target equals negative nums i, if the current sum num j plus nums k is less than the target then we 
                need to increase the value of current sum by incrementing j pointer. Else if the current sum num j plus nums k is greater than the target then we should decrease the value of 
                current sum by decrementing k pointer. How do you deal with duplicates?""",
                """When the current sum nums j plus nums k equals the target add this pair to the result. We can move j or k pointer until j is less than k and the pairs are repeated. 
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
            "case": """The client is a manufacturer and distributor of infant formula. They sell their product nationwide, and are in the middle 
                        of the pack in terms of market share. They are currently trying to boost their market share while maintaining profitability.
                        There is a government welfare program called WIC (Women, Infants, Children) that allows individuals living below the poverty level to receive vouchers
                        for infant formula for their children. Unlike most welfare programs, this one is subsidized by the actual producers of infant formula. On a state-by-state
                        basis, infant formula producers bid for the right to be the sole supplier of infant formula to welfare recipients in that state.
                        In addition to paying the government for the WIC contract, the client also provides rebates to retailers for WIC sales. As a result, income received from
                        WIC sales is substantially less than that received from normal formula sales. In fact, sales to mothers that remain in the WIC program for more than 12
                        months result in a net loss.
                        In trying to determine how much to bid on a WIC contract for a given state, what factors should you consider?""",
            "follow_ups": [
                """Sure. Obviously the typical WIC customer is poor, since this is a form of welfare. But some things you might not know are that 1) the
                    average WIC recipient stays in the program for less than 12 months, 2) mothers typically remain loyal to a brand through infancy for their
                    first child, but for subsequent children recipients often switch back and forth between brands, and 3) infants typically require formula the
                    first 22 months of their life.""",
                "For the purposes of this interview, let's assume that the rebates average an additional 10% (off of the retail price).",
                "For the most part, your logic is correct. But is there anything else that might be a factor in determining profit?",
                "Contracts typically last several years.",
                """Good. I'm not going to make you go through the math on it, because we're about out of time, but you're right. There are 1.2 million WIC
                    recipients in the state, and shelf-space is awarded based on volume sales. So for this company to get the contract, it can help them have
                    more sales volume, and thus more shelf-space, and hopefully then more market share.""",
                """Real world situation is that synergies are strong, and WIC recipients bounce in and out of program but stay loyal to product for first-borns. Not only are the
                    synergies positive, but also on average WIC recipients are profitable because they pay retail for nearly half of the formula that they purchase over the first
                    22 months of their child's life.""",
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
            "template_answer": """Retail banking provides services to individual consumers, such as
             savings accounts and loans, while investment banking focuses on services like underwriting,
              mergers and acquisitions, and raising capital for corporations."""
        },
        {
            "question": "Explain the concept of fractional reserve banking.",
            "template_answer": """Fractional reserve banking is a system where banks keep a fraction of deposits 
            as reserves and lend out the rest, allowing money creation through the lending process."""
        },
        {
            "question": "What is Basel III and why is it important?",
            "template_answer": """Basel III is a set of international banking regulations developed to strengthen 
            regulation, supervision, and risk management within the banking sector, focusing on capital adequacy, 
            stress testing, and market liquidity risk."""
        },
        {
            "question": "How do banks manage credit risk?",
            "template_answer": """Banks manage credit risk by assessing borrowers' creditworthiness, setting 
            lending limits, requiring collateral, and diversifying their loan portfolios."""
        },
        {
            "question": "What is the role of the Federal Reserve?",
            "template_answer": """The Federal Reserve is the central bank of the United States, responsible for setting 
            monetary policy, regulating banks, maintaining financial stability, and providing financial services to the government and other banks."""
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


async def get_next_interview_question(industry, asked_questions):
    """
    Get the next unasked interview question for the specified industry.
    
    Args:
        industry (str): The interview industry (e.g., 'software_engineering')
        asked_questions (list): List of previously asked questions
    
    Returns:
        dict: Next question data or None if no questions available
    """
    logger.info(f"Getting next question for industry={industry}, {len(asked_questions)} already asked")
    
    available_questions = INTERVIEW_QUESTION_BANK.get(industry, [])
    if not available_questions:
        return {"question": None}
    
    # Find unasked questions based on industry-specific key
    unasked_questions = _filter_unasked_questions(available_questions, asked_questions, industry)
    
    if not unasked_questions:
        return {"question": None}
    
    # Select random question from unasked ones
    selected_question = random.choice(unasked_questions)
    return _format_question_response(selected_question, industry)


def _filter_unasked_questions(available_questions, asked_questions, industry):
    """
    Filter out questions that have already been asked.
    
    Args:
        available_questions (list): All available questions for the industry
        asked_questions (list): Previously asked questions
        industry (str): The interview industry
    
    Returns:
        list: Questions that haven't been asked yet
    """
    # Get the appropriate key for this industry
    question_key = _get_question_key(industry)
    
    # Extract asked question texts
    asked_texts = {q.get(question_key) for q in asked_questions if q.get(question_key)}
    
    # Filter out already asked questions
    unasked = [q for q in available_questions if q.get(question_key) not in asked_texts]
    return unasked


def _get_question_key(industry):
    """
    Get the appropriate key for accessing questions in different industries.
    
    Args:
        industry (str): The interview industry
    
    Returns:
        str: The key to use for accessing questions
    """
    key_mapping = {
        "software_engineering": "main",
        "consulting": "case",
        "default": "question"
    }
    return key_mapping.get(industry, key_mapping["default"])


def _format_question_response(question_data, industry):
    """
    Format the question response based on industry requirements.
    
    Args:
        question_data (dict): The selected question data
        industry (str): The interview industry
    
    Returns:
        dict: Formatted question response
    """
    question_key = _get_question_key(industry)
    
    response = {"question": question_data[question_key]}
    
    # Add industry-specific additional data
    if industry == "software_engineering" and "hints" in question_data:
        response["hints"] = question_data["hints"]
    elif industry == "consulting" and "follow_ups" in question_data:
        response["follow_ups"] = question_data["follow_ups"]
    
    return response


async def get_template_answer(industry, question):
    """
    Get the template answer for a specific question in the given industry.
    
    Args:
        industry (str): The interview industry
        question (str): The question text
    
    Returns:
        str: Template answer or empty string if not found
    """
    available_questions = INTERVIEW_QUESTION_BANK.get(industry, [])
    question_key = _get_question_key(industry)
    
    # Find the question and return its template answer
    for q in available_questions:
        if q.get(question_key) == question and "template_answer" in q:
            return q["template_answer"]
    
    return ""


async def rate_answer(user_answer, template_answer):
    """
    Rate a user's answer compared to the template answer.
    
    Args:
        user_answer (str): User's response
        template_answer (str): Expected/template answer
    
    Returns:
        dict: Rating with score (1-5) and summary
    """
    if not user_answer or not user_answer.strip():
        return {"score": 1, "summary": "No answer provided. Please try to answer the question."}
    
    if not template_answer:
        return {"score": 3, "summary": "Answer received but no template available for comparison."}
    
    # Calculate score based on length and keyword overlap
    user_words = user_answer.lower().split()
    template_words = template_answer.lower().split()
    
    # Base score
    score = 2
    
    # Length factor (reasonable length gets bonus)
    if len(user_words) >= 15:
        score += 1
    
    # Keyword overlap factor
    template_keywords = set(template_words[:10])  # First 10 words are usually key concepts
    user_keywords = set(user_words)
    overlap_ratio = len(template_keywords & user_keywords) / len(template_keywords) if template_keywords else 0
    
    if overlap_ratio >= 0.3:  # 30% overlap
        score += 1
    if overlap_ratio >= 0.5:  # 50% overlap
        score += 1
    
    # Generate summary based on score
    summaries = {
        1: "Answer is too short or off-topic. Try to elaborate more.",
        2: "Basic answer provided. Could use more detail and relevance.",
        3: "Decent answer with some good points. Consider adding more depth.",
        4: "Good answer! You covered most key points effectively.",
        5: "Excellent answer! Comprehensive and well-structured."
    }
    
    return {"score": min(score, 5), "summary": summaries.get(score, summaries[3])}


async def get_feedback(user_answer, template_answer):
    """
    Provide specific, actionable feedback on the user's answer.
    
    Args:
        user_answer (str): User's response
        template_answer (str): Expected/template answer
    
    Returns:
        str: Constructive feedback message
    """
    if not user_answer or not user_answer.strip():
        return "Please provide an answer so I can give you specific feedback."
    
    if not template_answer:
        return "I can see you provided an answer. Try to be more specific and structured in your response."
    
    user_words = user_answer.lower().split()
    template_words = template_answer.lower().split()
    
    # Check answer length
    if len(user_words) < 10:
        return "Your answer is quite brief. Try to provide more detail and explanation to fully address the question."
    
    # Check for keyword overlap
    template_keywords = set(template_words[:10])
    user_keywords = set(user_words)
    common_keywords = template_keywords & user_keywords
    
    if common_keywords:
        key_terms = ", ".join(list(common_keywords)[:3])
        return f"Good start! You mentioned key terms like '{key_terms}'. Consider expanding on these concepts with more detail and examples."
    else:
        return "Your answer covers some points, but try to focus more directly on the core concepts the question is asking about."
