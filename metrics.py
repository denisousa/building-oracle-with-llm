from sklearn.metrics import precision_score, accuracy_score, f1_score, confusion_matrix
from file_operations import write_metrics

def generate_metrics(output_folder, results):
    if len(results) < 10:
        return 
    
    try:
        filtered_results = [item for item in results if item['llm_result'] in [True, False]]

        oracle_results = [result['oracle_result'] for result in filtered_results]
        llm_results = [result['llm_result'] for result in filtered_results]

        precision = precision_score(oracle_results, llm_results)
        accuracy = accuracy_score(oracle_results, llm_results)
        f1 = f1_score(oracle_results, llm_results)
        tn, fp, fn, tp = confusion_matrix(oracle_results, llm_results).ravel()
        
        all_metrics = {
            "precision": precision,
            "accuracy": accuracy,
            "f1_score": f1,
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
            "total": len(filtered_results),
        }

        write_metrics(f'{output_folder}/results_summary.txt', all_metrics)
        print('Error: Too little data for the confusion matrix')
    except:
        pass