from gpt_operation import compare_oracle_with_gpt
from file_operations import create_result_directory
import pandas as pd
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
create_result_directory(timestamp)

oracle_csv = 'mini_clones.csv'
cut_stackoverflow_path = 'projects/stackoverflow_formatted/'
qualitas_corpus_path = 'projects/qualitas_corpus_clean/'

oracle_df = pd.read_csv(oracle_csv)
print('oracle shape:', oracle_df.shape)
print('oracle columns:', oracle_df.columns)

compare_oracle_with_gpt(timestamp, oracle_df, cut_stackoverflow_path, qualitas_corpus_path)
