from sklearn.metrics import precision_score, accuracy_score, f1_score, confusion_matrix


def get_metric(oracle_results, gpt_results):
    precision = precision_score(oracle_results, gpt_results)
    accuracy = accuracy_score(oracle_results, gpt_results)
    f1 = f1_score(oracle_results, gpt_results)
    tn, fp, fn, tp = confusion_matrix(oracle_results, gpt_results).ravel()
    
    return {
        "precision": precision,
        "accuracy": accuracy,
        "f1_score": f1,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn
    }