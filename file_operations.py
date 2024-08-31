import os

def read_file(directory_path, file_name, start_line, end_line):
    full_path = os.path.join(directory_path, file_name)
    if os.path.exists(full_path):
        with open(full_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        start_line = max(0, start_line - 1)  # Linha inicial (convertida para índice de lista)
        end_line = min(len(lines), end_line)  # Linha final (não precisa de -1 porque o final é exclusivo)

        selected_lines = lines[start_line:end_line]
        return ''.join(selected_lines)
    else:
        return None
    
def write_metrics(output_txt_path, all_metrics):
    with open(output_txt_path, 'w') as f:
        f.write(f"Precision: {all_metrics['precision']:.4f}\n")
        f.write(f"Accuracy: {all_metrics['accuracy']:.4f}\n")
        f.write(f"F1-Score: {all_metrics['f1_score']:.4f}\n")
        f.write(f"True Positives (TP): {all_metrics['true_positives']}\n")
        f.write(f"False Positives (FP): {all_metrics['false_positives']}\n")
        f.write(f"True Negatives (TN): {all_metrics['true_negatives']}\n")
        f.write(f"False Negatives (FN): {all_metrics['false_negatives']}\n")

        print(f"Summary metrics have been exported to {output_txt_path}")

def export_results(results_df):
    output_excel_path = 'oracle_results.xlsx'
    results_df.to_excel(output_excel_path, index=False)

    output_csv_path = 'oracle_results.csv'
    results_df.to_csv(output_csv_path, index=False, encoding='utf-8')

    output_json_path = 'oracle_results.json'
    results_df.to_json(output_json_path, orient='records', indent=4, force_ascii=False)

    print(f"Results have been exported to {output_excel_path}, {output_csv_path}, and {output_json_path}")