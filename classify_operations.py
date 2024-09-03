import re

def classify_prediction(oracle_value, gpt_value):
    if oracle_value == True and gpt_value == True:
        return "TP"  # True Positive
    elif oracle_value == False and gpt_value == True:
        return "FP"  # False Positive
    elif oracle_value == False and gpt_value == False:
        return "TN"  # True Negative
    elif oracle_value == True and gpt_value == False:
        return "FN"  # False Negative
    else:
        return ""
    

def change_roman_numerals_to_numbers(roman_numeral: str) -> str:
    roman_numerals = {
        'iv': '4',
        'iii': '3',
        'ii': '2',
        'i': '1'
    }

    return roman_numerals[roman_numeral]

def normalize_clone_type(clone_type: str) -> str:
    number = clone_type.split("-")[-1]
    if number in ['i', 'ii', 'iii', 'iv']:
        number = change_roman_numerals_to_numbers(clone_type.split("-")[-1])
    return "type-" + number

def normalize_matches_clone_type(matches):
    new_matches = [match.lower().strip().replace(" ", "-") for match in matches]
    new_matches = [normalize_clone_type(match) for match in new_matches]
    return new_matches

def get_llm_response_has_true_or_false(has_hallucination, response: str) -> bool | str:
    if has_hallucination:
        return ""
    
    if "True" in response:
        return True
    
    if "False" in response:
        return False
    
    return classify_sentence(response)

def get_llm_response_has_clone_type(has_hallucination, response: str):
    if has_hallucination:
        return ""
    
    pattern = r'\btype[-\s]?(?:1|2|3|4|i|ii|iii|iv)\b'
    matches = re.findall(pattern, response, re.IGNORECASE)

    if matches:
        return normalize_matches_clone_type(matches)[0]

def has_true_or_false_hallucination(response: str):
    if "True" in response and "False" in response:
        return  True
    
    if "True" not in response and "False" not in response:
        return  True
    
    return False

def has_clone_type_hallucination(response: str):
    pattern = r'\btype[-\s]?(?:1|2|3|4|i|ii|iii|iv)\b'
    matches = re.findall(pattern, response, re.IGNORECASE)

    if len(matches) == 0:
        return True

    if len(matches) >= 2:
        new_matches = normalize_matches_clone_type(matches)
        if all(item == new_matches[0] for item in new_matches):
            return False
    
    return False

def check_hallucination(response: str):
    check1 = has_true_or_false_hallucination(response)
    check2 = has_clone_type_hallucination(response)
    return check1, check2


def classify_sentence(sentence):
    affirmative_patterns = [
        r"(yes|certainly|definitely|indeed|surely|they are)\b.*(clones|identical|the same)",
        r"\b(are|is)\b.*(clones|identical|the same)"
    ]

    negative_patterns = [
        r"\b(no|not|aren't|isn't|cannot|can't|never)\b.*(clones|identical|the same)",
        r"\b(none|neither|different|distinct|unique)\b"
    ]

    for pattern in affirmative_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            return True
    
    for pattern in negative_patterns:
        if re.search(pattern, sentence, re.IGNORECASE):
            return False
    
    return ""

sentences = [
    "Yes, they are definitely clones.",
    "No, these are not clones.",
    "They aren't clones at all.",
    "These items are different and unique."
]

for sentence in sentences:
    print(f"Sentence: {sentence}")
    print(f"Classification: {classify_sentence(sentence)}")
    print()
