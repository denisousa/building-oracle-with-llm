from gpt_operation import compare_oracle_with_gpt
from file_operations import write_metrics, export_results
from llm_operations import get_client_openai, get_client_azure_openai
from metrics import get_metric
import pandas as pd

oracle_csv = 'mini_clones.csv'
cut_stackoverflow_path = 'projects/stackoverflow_formatted/'
qualitas_corpus_path = 'projects/qualitas_corpus_clean/'

oracle_df = pd.read_csv(oracle_csv)
client = get_client_azure_openai()

print('oracle shape:', oracle_df.shape)
print('oracle columns:', oracle_df.columns)

results = compare_oracle_with_gpt(oracle_df, cut_stackoverflow_path, qualitas_corpus_path, client)

results_df = pd.DataFrame(results)
export_results(results_df)

oracle_results = [result['oracle_result'] for result in results]
gpt_results = [result['gpt_result'] for result in results]

try:
    all_metrics = get_metric(oracle_results, gpt_results)
    write_metrics('results_summary.txt', all_metrics)
except:
    print('Error: Too little data for the confusion matrix')
