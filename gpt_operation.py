from file_operations import read_file
from classify_operations import classify_prediction, string_to_bool
from prompts import system_prompt, get_prompt_to_compare_two_codes
from time_calc import time_it

@time_it
def compare_oracle_with_gpt(oracle_df, cut_stackoverflow_path, qualitas_corpus_path, client):
    results = []

    for index, row in oracle_df.iterrows():
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
            open('error.txt', 'w').write(f'index: {index} - {gpt_result}\n')
            continue
        oracle_result = True if row['classification'] in ['QS', 'EX', 'UD'] else False

        class_result = classify_prediction(oracle_result, gpt_result)

        results.append({
            "class_result": class_result,
            "gpt_result": gpt_result,
            "oracle_result": oracle_result,
            "so_clone": so_clone,
            "qc_clone": qc_clone,
        })

        if index == 5:
            return results