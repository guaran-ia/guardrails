import os
from utils import load_bad_words
from filtering import process_existing_corpora

def main():
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)
    main_directory = os.path.dirname(src_dir) # -> experiments/toxicity_filtering

    input_data_directory = os.path.join(main_directory, 'data', 'existing_corpora', 'data', 'processed')
    output_directory = os.path.join(main_directory, 'data', 'processing_results')
    toxic_terms_path = os.path.join(main_directory, 'data', 'bad_words.txt')

    toxic_terms = load_bad_words(toxic_terms_path)

    print(f"[INFO] Loaded {len(toxic_terms)} bad words")

    process_existing_corpora(input_data_directory, output_directory, toxic_terms)


if __name__ == "__main__":
    main()
