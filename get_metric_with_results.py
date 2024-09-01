import pandas as pd
from metrics import get_metric
from file_operations import write_metrics

directory_path = 'results/XXXXXX'

file_path = 'oracle_results_updated.csv'
df = pd.read_csv(file_path)
results = df.to_dict('records')

oracle_results = [result['oracle_result'] for result in results]
gpt_results = [result['gpt_result'] for result in results]

try:
    all_metrics = get_metric(oracle_results, gpt_results)
    write_metrics(f'{directory_path}/results_summary.txt', all_metrics)
except:
    print('Error: Too little data for the confusion matrix')
