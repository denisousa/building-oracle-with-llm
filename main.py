from gpt_operation import compare_oracle_with_gpt
from file_operations import write_metrics, export_results
from metrics import get_metric
import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

oracle_csv = 'mini_clones.csv'
cut_stackoverflow_path = 'projects/stackoverflow_formatted/'
qualitas_corpus_path = 'projects/qualitas_corpus_clean/'

oracle_df = pd.read_csv(oracle_csv)
print('oracle shape:', oracle_df.shape)
print('oracle columns:', oracle_df.columns)

results = compare_oracle_with_gpt(oracle_df, cut_stackoverflow_path, qualitas_corpus_path)

results_df = pd.DataFrame(results)
export_results(timestamp, results_df)

oracle_results = [result['oracle_result'] for result in results]
gpt_results = [result['gpt_result'] for result in results]

try:
    all_metrics = get_metric(oracle_results, gpt_results)
    write_metrics(f'results/{timestamp}/results_summary.txt', all_metrics)
except:
    print('Error: Too little data for the confusion matrix')
