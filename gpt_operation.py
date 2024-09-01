from file_operations import read_file
from metrics import generate_metrics
from classify_operations import classify_prediction, string_to_bool
from prompts import system_prompt, get_prompt_to_compare_two_codes
from llm_operations import get_client_azure_openai
from file_operations import export_results
from time_calc import time_it
from time import sleep
import pandas as pd

@time_it
def compare_oracle_with_gpt(timestamp, oracle_df, cut_stackoverflow_path, qualitas_corpus_path):
    client = get_client_azure_openai()
    results = []

    for index, row in oracle_df.iterrows():
        if index % 20 == 0 and index > 0:
            sleep(3)
            print(f"Processing row {index}...")
        
        so_clone = read_file(cut_stackoverflow_path, row['file1'], row["start1"], row["end1"])
        qc_clone = read_file(qualitas_corpus_path, row['file2'], row['start2'], row['end2'])
        user_prompt = get_prompt_to_compare_two_codes(so_clone, qc_clone)

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "assistant", "content": "I will answer only True or False"},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )

        gpt_result = completion.choices[0].message.content
        try:
            gpt_result = string_to_bool(gpt_result)
        except:
            open(f'results/{timestamp}/error.txt', 'a').write(f'index: {index} - {gpt_result}\n')
            continue

        oracle_result = True
        class_result = classify_prediction(oracle_result, gpt_result)

        comparative_result = {
            "class_result": class_result,
            "gpt_result": gpt_result,
            "oracle_result": oracle_result,
            "so_clone": so_clone,
            "qc_clone": qc_clone,
        }

        comparative_result.update(row.to_dict())
        results.append(comparative_result)

        results_df = pd.DataFrame(results)
        export_results(timestamp, results_df)
        generate_metrics(timestamp, results)

    return results
        