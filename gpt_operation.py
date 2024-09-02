from classify_operations import classify_prediction, string_to_bool
from prompts import get_chat_simple_prompt, get_prompt_to_compare_two_codes
from hallucination_operation import fix_hallucination
from file_operations import create_result_directory
from file_operations import export_results
from file_operations import read_file
from metrics import generate_metrics
from time_calc import time_it
from time import sleep
import pandas as pd
import gc


@time_it
def compare_oracle_with_gpt(execution_context, oracle_df, cut_stackoverflow_path, qualitas_corpus_path):
    output_folder = create_result_directory(execution_context['model'])

    results = []
    for index, row in oracle_df.iterrows():
        client = execution_context['client']()

        if index % 20 == 0 and index > 0:
            sleep(3)
            print(f"Processing row {index}...")
        
        so_clone = read_file(cut_stackoverflow_path, row['file1'], row["start1"], row["end1"])
        qc_clone = read_file(qualitas_corpus_path, row['file2'], row['start2'], row['end2'])
        user_prompt = get_prompt_to_compare_two_codes(so_clone, qc_clone)

        completion = client.chat.completions.create(
            model=execution_context['model'],
            messages=get_chat_simple_prompt(user_prompt),
            temperature=0.0
        )

        gpt_result = completion.choices[0].message.content
        try:
            gpt_result = string_to_bool(gpt_result)
        except:
            gpt_result = fix_hallucination(output_folder,
                                           index,
                                           gpt_result,
                                           client,
                                           execution_context,
                                           user_prompt)

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
        export_results(output_folder, results_df)

        if index >= 10:
            generate_metrics(output_folder, results)

        del client, completion, gpt_result, user_prompt, so_clone, qc_clone
        gc.collect()

    return results
