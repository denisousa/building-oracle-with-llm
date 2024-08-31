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
        return "Invalid Input"
    
def string_to_bool(s):
    if s == "True":
        return True
    elif s == "False":
        return False
    else:
        raise ValueError("Invalid input: the string must be 'True' or 'False'")