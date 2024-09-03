from llm_operations import compare_oracle_with_gpt
from llm_connection import get_client_lm_studio
import pandas as pd

oracle_csv = 'clones.csv'
cut_stackoverflow_path = 'projects/stackoverflow_formatted/'
qualitas_corpus_path = 'projects/qualitas_corpus_clean/'

oracle_df = pd.read_csv(oracle_csv)
oracle_df = oracle_df[~oracle_df['classification'].isin(['AC', 'BP', 'IC'])]
print('oracle rows:', oracle_df.shape[0])
print('oracle columns:', oracle_df.shape[1])

execution_context = {
    'client': get_client_lm_studio,
    'model': "TheBloke/CodeLlama-7B-Instruct-GGUF"
}

compare_oracle_with_gpt(execution_context,
                        oracle_df,
                        cut_stackoverflow_path,
                        qualitas_corpus_path)
