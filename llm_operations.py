from classify_operations import (
    classify_prediction,
    get_llm_response_has_true_or_false,
    get_llm_response_has_clone_type,
    check_hallucination
)
from prompts import get_chat_simple_prompt, get_prompt_to_compare_two_codes
from file_operations import create_result_directory
from file_operations import export_results
from file_operations import read_file
from metrics import generate_metrics
from print_operations import print_progress
from transformers import GPT2Tokenizer
from time_calc import time_it
from datetime import datetime
import pandas as pd
import gc


@time_it
def compare_oracle_with_gpt(
    execution_context, oracle_df, cut_stackoverflow_path, qualitas_corpus_path
):
    output_folder = create_result_directory(execution_context["model"])
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    results = []
    for index, row in oracle_df.iterrows():
        print_progress(index)

        so_clone = read_file(cut_stackoverflow_path, row["file1"], row["start1"], row["end1"])
        qc_clone = read_file(qualitas_corpus_path, row["file2"], row["start2"], row["end2"])
        user_prompt = get_prompt_to_compare_two_codes(so_clone, qc_clone)

        client = execution_context["client"]()

        start_time = datetime.now()
        completion = client.chat.completions.create(
            model=execution_context["model"],
            messages=get_chat_simple_prompt(user_prompt),
            temperature=0.7,
        )
        end_time = datetime.now()

        llm_complete_result = completion.choices[0].message.content

        check1, check2 = check_hallucination(llm_complete_result)
        if check1 or check2:
            error_msg = f"index: {index} - {llm_complete_result}\n"
            open(f"{output_folder}/error.txt", "a").write(error_msg)

        llm_result = get_llm_response_has_true_or_false(check1, llm_complete_result)
        clone_type = get_llm_response_has_clone_type(check2, llm_complete_result)

        oracle_result = True
        class_result = classify_prediction(oracle_result, llm_result)
        class_result = "" if check1 or check2 else class_result

        comparative_result = {
            "class_result": class_result,
            "oracle_result": oracle_result,
            "llm_result": llm_result,
            "clone_type_result": clone_type,
            "true_or_false_hallucionation": check1,
            "clone_type_hallucionation": check2,
            "so_clone": so_clone,
            "qc_clone": qc_clone,
            "llm_complete_result": llm_complete_result,
            "user_prompt_tokens": len(tokenizer.encode(user_prompt)),
            "llm_complete_results_tokens": len(tokenizer.encode(llm_complete_result)),
            "time": str(end_time - start_time),
        }

        comparative_result.update(row.to_dict())
        results.append(comparative_result)

        results_df = pd.DataFrame(results)
        export_results(output_folder, results_df)

        generate_metrics(output_folder, results)

        del client, completion, llm_result, user_prompt, so_clone, qc_clone
        gc.collect()

    return results
