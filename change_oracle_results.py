import pandas as pd
from classify_operations import classify_prediction

df = pd.read_csv('oracle_results.csv')
df['class_result'] = df.apply(lambda row: classify_prediction(row['oracle_result'], row['gpt_result']), axis=1)
df.to_csv('oracle_results_updated.csv', index=False)

print("O arquivo 'oracle_results_updated.csv' foi criado com as alterações.")
