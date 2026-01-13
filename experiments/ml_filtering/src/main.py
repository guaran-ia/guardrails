import os
from utils import load_bad_words
from ml_filtering import process_existing_corpora

def main():
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)
    main_directory = os.path.dirname(src_dir) # -> experiments/ml_filtering
    experiments_directory = os.path.dirname(main_directory)

    input_data_directory = os.path.join(experiments_directory, 'data', 'existing_corpora', 'data', 'processed')
    
    model_path = "mmaguero/toxic-multilingual-bert-gn-base-cased"
    model_name = model_path.split('/')[-1]
    output_directory = os.path.join(main_directory, 'data', 'processing_results', model_name)

    print(f"Starting Processing with model {model_name}")

    process_existing_corpora(input_data_directory, output_directory, model_path, model_name)


if __name__ == "__main__":
    main()
