import random
import logging

logger = logging.getLogger(__name__)

# Interview question bank organized by industry
INTERVIEW_QUESTION_BANK = {
    "software_engineering": {
        "easy": [
            {
                "main": """Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.
                    For example, if the input is an array nums containing 1, 2, 3, 3, the output should be true.
                    If the input is an array nums containing 1, 2, 3, 4, the output should be false.""",
                "difficulty": "easy",
                "hints": [
                    "You should aim for a solution with O(n) time and O(n) space, where n is the size of the input array.",
                    "A brute force solution would be to check every element against every other element in the array. This would be an O(n^2) solution. Can you think of a better way?",
                    "Is there a way to check if an element is a duplicate without comparing it to every other element? Maybe there's a data structure that is useful here.",
                    "We can use a hash data structure like a hash set or hash map to store elements we've already seen. This will allow us to check if an element is a duplicate in constant time.",
                ]
            },
            {
                "main": """Given two strings s and t, return true if the two strings are anagrams of each other, otherwise return false.
                An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.
                For example, if the input is a string s containing 'racecar' and a string t containing 'carrace', the output should be true.
                If the input is a string s containing 'jar' and a string t containing 'jam', the output should be false.
                s and t consist of lowercase English letters.""",
                "difficulty": "easy",
                "hints": [
                    "You should aim for a solution with big O of (n + m) time and big O of (1) space, where n is the length of the string s and m is the length of the string t.",
                    "A brute force solution would be to sort the given strings and check for their equality. This would be an big O of ( n log n + m log m ) solution. Though this solution is acceptable, can you think of a better way without sorting the given strings?",
                    "By the definition of the anagram, we can rearrange the characters. Does the order of characters matter in both the strings? Then what matters?",
                    "We can just consider maintaining the frequency of each character. We can do this by having two separate hash tables for the two strings. Then, we can check whether the frequency of each character in string s is equal to that in string t and vice versa.",
                ]
            },
            {
                "main": """Given an array of integers nums and an integer target, return the indices i and j such that nums at i + nums at j equals the target and i is not equal to j.
                    You may assume that every input has exactly one pair of indices i and j that satisfy the condition.
                    Return the answer with the smaller index first.
                    If the input is an array nums containing 3, 4, 5, 6, and the target is 7, the output should be 0 and 1.
                    If the input is an array nums containing 4, 5, 6, and the target is 10, the output should be 0 and 2.""",
                "difficulty": "easy",
                "hints": [
                    "You should aim for a solution with big O of (n) time and big O of (n) space, where n is the size of the input array.",
                    "A brute force solution would be to check every pair of numbers in the array. This would be an big O of (n squared) solution. Can you think of a better way? Maybe in terms of mathematical equation?",
                    "Given, we need to find indices i and j such that i is not equal to j and nums at [i] + nums at [j] is equal to the target. Can you rearrange the equation and try to fix any index to iterate on?",
                    "We can iterate through nums with index i. Let difference = target - nums at [i] and check if difference exists in the hash map as we iterate through the array, else store the current element in the hashmap with its index and continue. We use a hashmap for big O of (1) lookups.",
                ]
            },
            {
                "main": """Given a string s, return true if it is a palindrome, otherwise return false.
                    A palindrome is a string that reads the same forward and backward. It is also case-insensitive and ignores all non-alphanumeric characters.
                    Note: Alphanumeric characters consist of letters (capital A through Z and lowercase a through z) and numbers (0 through 9).
                    If the input is a string s containing 'Was it a car or a cat I saw?', the output should be true.
                    If the input is a string s containing 'tab a cat', the output should be false.""",
                "difficulty": "easy",
                "hints": [
                    "You should aim for a solution with big O of (n) time and big O of (1) space, where n is the length of the input string.",
                    "A brute force solution would be to create a copy of the string, reverse it, and then check for equality. This would be an big O of (n) solution with extra space. Can you think of a way to do this without big O of (n) space?",
                    "Can you find the logic by observing the definition of pallindrome or from the brute force solution?",
                    "A palindrome string is a string that is read the same from the start as well as from the end. This means the character at the start should match the character at the end at the same index. We can use the two pointer algorithm to do this efficiently.",
                ]
            },
            {
                "main": """You are given an integer array prices where prices at [i] is the price of NeetCoin on the ith day.
                    You may choose a single day to buy one NeetCoin and choose a different day in the future to sell it.
                    Return the maximum profit you can achieve. You may choose to not make any transactions, in which case the profit would be 0.
                    If the input is an array prices containing 10, 1, 5, 6, 7, 1, the output should be 6.
                    If the input is an array prices containing 10, 8, 7, 5, 2, the output should be 0.""",
                "difficulty": "easy",
                "hints": [
                    "You should aim for a solution with big O of (n) time and big O of (1) space, where n is the size of the input array.",
                    "A brute force solution would be to iterate through the array with index i, considering it as the day to buy, and trying all possible options for selling it on the days to the right of index i. This would be a big O of (n squared) solution. Can you think of a better way?",
                    "You should buy at a price and always sell at a higher price. Can you iterate through the array with index i, considering it as either the buying price or the selling price?",
                    "We can iterate through the array with index i, considering it as the selling value. But what value will it be optimal to consider as buying point on the left of index i?",
                    "We are trying to maximize profit = sell - buy. If the current i is the sell value, we want to choose the minimum buy value to the left of i to maximize the profit. The result will be the maximum profit among all. However, if all profits are negative, we can return 0 since we are allowed to skip doing transaction.",
                ]
            },
        ],
        "medium": [
            {
                "main": """Given an array of strings strs, group all anagrams together into sublists. You may return the output in any order.
                    An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.
                    For example, if the input is an array strs containing 'act', 'pots', 'tops', 'cat', 'stop', 'hat', the output should be [['hat'], ['act', 'cat'], ['stop', 'pots', 'tops']].
                    If the input is an array strs containing 'x', the output should be [['x']].
                    If the input is an array strs containing '', the output should be [['']].""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(m * n) time and O(m) space, where m is the number of strings and n is the length of the longest string.",
                    "A naive solution would be to sort each string and group them using a hash map. This would be an O(m * nlogn) solution. Though this solution is acceptable, can you think of a better way without sorting the strings?",
                    "By the definition of an anagram, we only care about the frequency of each character in a string. How is this helpful in solving the problem?",
                    "We can simply use an array of size O(26), since the character set is a through z (26 continuous characters), to count the frequency of each character in a string. Then, we can use this array as the key in the hash map to group the strings.",
                ]
            },
            {
                "main": """Given an integer array nums and an integer k, return the k most frequent elements within the array.
                    The test cases are generated such that the answer is always unique.
                    You may return the output in any order.
                    If the input is an array nums containing 1, 2, 2, 3, 3, 3, and the k is 2, the output should be 2 and 3.
                    If the input is an array nums containing 7, 7, and the k is 1, the output should be 7.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(n) time and O(n) space, where n is the size of the input array.",
                    "A naive solution would be to count the frequency of each number and then sort the array based on each element's frequency. After that, we would select the top k frequent elements. This would be an O(nlogn) solution. Though this solution is acceptable, can you think of a better way?",
                    "Can you think of an algorithm which involves grouping numbers based on their frequency?",
                    "Use the bucket sort algorithm to create n buckets, grouping numbers based on their frequencies from 1 to n. Then, pick the top k numbers from the buckets, starting from n down to 1.",
                ]
            },
            {
                "main": """Design an algorithm to encode a list of strings to a single string. The encoded string is then decoded back to the original list of strings.
                    Please implement encode and decode.
                    If the input is an array strs containing 'neet', 'code', 'love', 'you', the output should be 'neetcodeloveyou'.
                    If the input is an array strs containing 'we', 'say', ':', 'yes', the output should be 'wesay:yes'.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(m) time for each encode() and decode() call and O(m+n) space, where m is the sum of lengths of all the strings and n is the number of strings.",
                    "A naive solution would be to use a non-ascii character as a delimiter. Can you think of a better way?",
                    "Try to encode and decode the strings using a smart approach based on the lengths of each string. How can you differentiate between the lengths and any numbers that might be present in the strings?",
                    "We can use an encoding approach where we start with a number representing the length of the string, followed by a separator character (let's use # for simplicity), and then the string itself. To decode, we read the number until we reach a #, then use that number to read the specified number of characters as the string.",
                ]
            },
            {
                "main": """Given an integer array nums, return an array output where output[i] is the product of all the elements of nums except nums[i].
                    Each product is guaranteed to fit in a 32-bit integer.
                    If the input is an array nums containing 1, 2, 4, 6, the output should be 48, 24, 12, 8.
                    If the input is an array nums containing -1, 0, 1, 2, 3, the output should be 0, -6, 0, 0, 0.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution as good or better than O(n) time and O(n) space, where n is the size of the input array.",
                    "A brute-force solution would be to iterate through the array with index i and compute the product of the array except for that index element. This would be an O(n^2) solution. Can you think of a better way?",
                    "Is there a way to avoid the repeated work? Maybe we can store the results of the repeated work in an array.",
                    "We can use the prefix and suffix technique. First, we iterate from left to right and store the prefix products for each index in a prefix array, excluding the current index's number. Then, we iterate from right to left and store the suffix products for each index in a suffix array, also excluding the current index's number. Can you figure out the solution from here?",
                    "We can use the stored prefix and suffix products to compute the result array by iterating through the array and simply multiplying the prefix and suffix products at each index.",
                ]
            },
            {
                "main": """Given an array of integers nums, return the length of the longest consecutive sequence of elements that can be formed.
                    A consecutive sequence is a sequence of elements in which each element is exactly 1 greater than the previous element. The elements do not have to be consecutive in the original array.
                    You must write an algorithm that runs in O(n) time.
                    If the input is an array nums containing 2, 20, 4, 10, 3, 4, 5, the output should be 4.
                    If the input is an array nums containing 0, 3, 2, 5, 4, 6, 1, 1, the output should be 7.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution as good or better than O(n) time and O(n) space, where n is the size of the input array.",
                    "A brute force solution would be to consider every element from the array as the start of the sequence and count the length of the sequence formed with that starting element. This would be an O(n^2) solution. Can you think of a better way?",
                    "Is there any way to identify the start of a sequence? For example, in [1, 2, 3, 10, 11, 12], only 1 and 10 are the beginning of a sequence. Instead of trying to form a sequence for every number, we should only consider numbers like 1 and 10.",
                    "We can consider a number num as the start of a sequence if and only if num - 1 does not exist in the given array. We iterate through the array and only start building the sequence if it is the start of a sequence. This avoids repeated work. We can use a hash set for O(1) lookups by converting the array to a hash set.",
                ]
            },
            {
                "main": """Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] where nums[i] + nums[j] + nums[k] == 0, and the indices i, j and k are all distinct.
                    The output should not contain any duplicate triplets. You may return the output and the triplets in any order.
                    If the input is an array nums containing -1, 0, 1, 2, -1, -4, the output should be [[-1, -1, 2], [-1, 0, 1]].
                    If the input is an array nums containing 0, 1, 1, the output should be [].
                    If the input is an array nums containing 0, 0, 0, the output should be [[0, 0, 0]].""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(n^2) time and O(1) space, where n is the size of the input array.",
                    "A brute force solution would be to check for every triplet in the array. This would be an O(n^3) solution. Can you think of a better way?",
                    "Can you think of an algorithm after sorting the input array? What can we observe by rearranging the given equation in the problem?",
                    "We can iterate through nums with index i and get nums[i] = -(nums[j] + nums[k]) after rearranging the equation, making -nums[i] = nums[j] + nums[k]. For each index i, we should efficiently calculate the j and k pairs without duplicates. Which algorithm is suitable to find j and k pairs?",
                    "To efficiently find the j and k pairs, we run the two pointer approach on the elements to the right of index i as the array is sorted. When we run two pointer algorithm, consider j and k as pointers (j is at left, k is at right) and target = -nums[i], if the current sum num[j] + nums[k] < target then we need to increase the value of current sum by incrementing j pointer. Else if the current sum num[j] + nums[k] > target then we should decrease the value of current sum by decrementing k pointer. How do you deal with duplicates?",
                    "When the current sum nums[j] + nums[k] == target add this pair to the result. We can move j or k pointer until j < k and the pairs are repeated. This ensures that no duplicate pairs are added to the result.",
                ]
            },
            {
                "main": """Given a string s, find the length of the longest substring without duplicate characters.
                    A substring is a contiguous sequence of characters within a string.
                    If the input is a string s containing 'zxyzxyz', the output should be 3.
                    If the input is a string s containing 'xxxx', the output should be 1.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(n) time and O(m) space, where n is the length of the string and m is the number of unique characters in the string.",
                    "A brute force solution would be to try the substring starting at index i and try to find the maximum length we can form without duplicates by starting at that index. we can use a hash set to detect duplicates in O(1) time. Can you think of a better way?",
                    "We can use the sliding window algorithm. Since we only care about substrings without duplicate characters, the sliding window can help us maintain valid substring with its dynamic nature.",
                    "We can iterate through the given string with index r as the right boundary and l as the left boundary of the window. We use a hash set to check if the character is present in the window or not. When we encounter a character at index r that is already present in the window, we shrink the window by incrementing the l pointer until the window no longer contains any duplicates. Also, we remove characters from the hash set that are excluded from the window as the l pointer moves. At each iteration, we update the result with the length of the current window, r - l + 1, if this length is greater than the current result.",
                ]
            },
            {
                "main": """You are given a string s consisting of only uppercase english characters and an integer k. You can choose up to k characters of the string and replace them with any other uppercase English character.
                    After performing at most k replacements, return the length of the longest substring which contains only one distinct character.
                    If the input is a string s containing 'XYYX' and k is 2, the output should be 4.
                    If the input is a string s containing 'AAABABB' and k is 1, the output should be 5.""",
                "difficulty": "medium",
                "hints": [
                    "You should aim for a solution with O(n) time and O(m) space, where n is the length of the given string and m is the number of unique characters in the string.",
                    "Which characters would you replace in a string to make all its characters unique? Can you think with respect to the frequency of the characters?",
                    "It is always optimal to replace characters with the most frequent character in the string. Why? Because using the most frequent character minimizes the number of replacements required to make all characters in the string identical. How can you find the number of replacements now?",
                    "The number of replacements is equal to the difference between the length of the string and the frequency of the most frequent character in the string. A brute force solution would be to consider all substrings, use a hash map for frequency counting, and return the maximum length of the substring that has at most k replacements. This would be an O(n^2) solution. Can you think of a better way?",
                    "We can use the sliding window approach. The window size will be dynamic, and we will shrink the window when the number of replacements exceeds k. The result will be the maximum window size observed at each iteration.",
                ]
            },
            {
                "main": """Y.""",
                "difficulty": "medium",
                "hints": [
                    "",
                ]
            },
        ],
        "hard": [
            {
                "main": """Given two strings s and t, return the shortest substring of s such that every character in t, including duplicates, is present in the substring. If such a substring does not exist, return an empty string "".
                    You may assume that the correct output is always unique.
                    If the input is a string s containing 'OUZODYXAZV' and t containing 'XYZ', the output should be 'YXAZ'.
                    If the input is a string s containing 'xyz' and t containing 'xyz', the output should be 'xyz'.
                    If the input is a string s containing 'x' and t containing 'xy', the output should be ''""",
                "difficulty": "hard",
                "hints": [
                    "You should aim for a solution with O(n) time and O(m) space, where n is the length of the string s and m is the number of unique characters in s and t.",
                    "A brute force solution would involve checking every substring of s against t and returning the minimum length valid substring. This would be an O(n^2) solution. Can you think of a better way? Maybe you should think in terms of frequency of characters.",
                    "We need to find substrings in s that should have atleast the characters of t. We can use hash maps to maintain the frequencies of characters. It will be O(1) for lookups. Can you think of an algorithm now?",
                    "We can use a dynamically sized sliding window approach on s. We iterate through s while maintaining a window. If the current window contains at least the frequency of characters from t, we update the result and shrink the window until it is valid.",
                    "We should ensure that we maintain the result substring and only update it if we find a shorter valid substring. Additionally, we need to keep track of the result substring's length so that we can return an empty string if no valid substring is found.",
                ]
            },
        ]
    },
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
    ],
    "banking": [
        {
            "question": "What is the difference between retail banking and investment banking?",
            "template_answer": """Retail banking provides services to individual consumers, such as
             savings accounts and loans, while investment banking focuses on services like underwriting,
              mergers and acquisitions, and raising capital for corporations."""
        },
    ],
    "quantitative_finance": [
        {
            "question": "What is the Black-Scholes model used for?",
            "template_answer": "The Black-Scholes model is used to price European options and calculate theoretical values based on factors like volatility, time, and risk-free rate."
        },
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
    ]
}


async def get_next_interview_question(industry, asked_questions, difficulty=None):
    """
    Get the next unasked interview question for the specified industry and difficulty.
    
    Args:
        industry (str): The interview industry (e.g., 'software_engineering')
        asked_questions (list): List of previously asked questions
        difficulty (str, optional): Question difficulty ('easy', 'medium', 'hard')
    
    Returns:
        dict: Next question data or None if no questions available
    """
    logger.info(f"Getting next question for industry={industry}, difficulty={difficulty}, {len(asked_questions)} already asked")
    
    # Get the industry's question data
    industry_questions = INTERVIEW_QUESTION_BANK.get(industry, [])

    # Check if it's the NEW format (dict with difficulties) or OLD format (list)
    if isinstance(industry_questions, dict):
        # NEW FORMAT (Software Engineering only)
        if difficulty and difficulty in industry_questions:
            # User selected a specific difficulty -> use only those questions
            available_questions = industry_questions[difficulty]  # e.g., industry_questions['easy']
        else:
            # No difficulty selected -> combine ALL difficulty levels
            available_questions = []
            for diff_level in ['easy', 'medium', 'hard']:
                if diff_level in industry_questions:
                    available_questions.extend(industry_questions[diff_level])
    else:
        # OLD FORMAT (Consulting, Banking, Behavioral, etc.)
        available_questions = industry_questions  # Use the list directly
    
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
