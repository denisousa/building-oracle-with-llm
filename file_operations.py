import os

def create_result_directory(timestamp):
    output_dir = f'results/{timestamp}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

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

def export_results(timestamp, results_df):
    output_dir = f'results/{timestamp}'
    output_excel_path = os.path.join(output_dir, 'oracle_results.xlsx')
    output_csv_path = os.path.join(output_dir, 'oracle_results.csv')
    output_json_path = os.path.join(output_dir, 'oracle_results.json')

    results_df.to_excel(output_excel_path, index=False)
    results_df.to_csv(output_csv_path, index=False, encoding='utf-8')
    results_df.to_json(output_json_path, orient='records', indent=4, force_ascii=False)
