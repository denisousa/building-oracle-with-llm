from sklearn.metrics import precision_score, accuracy_score, f1_score, confusion_matrix
from file_operations import write_metrics

def generate_metrics(timestamp, results):
    oracle_results = [result['oracle_result'] for result in results]
    gpt_results = [result['gpt_result'] for result in results]

    precision = precision_score(oracle_results, gpt_results)
    accuracy = accuracy_score(oracle_results, gpt_results)
    f1 = f1_score(oracle_results, gpt_results)
    tn, fp, fn, tp = confusion_matrix(oracle_results, gpt_results).ravel()
    
    all_metrics = {
        "precision": precision,
        "accuracy": accuracy,
        "f1_score": f1,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn
    }

    try:
        write_metrics(f'results/{timestamp}/results_summary.txt', all_metrics)
    except:
        print('Error: Too little data for the confusion matrix')