import os
from utils import load_bad_words
from filtering import process_existing_corpora
from report_generation import create_report

def main():
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file) #-> experiments/toxicity_filtering/src/
    toxicity_filtering_directory = os.path.dirname(src_dir) # -> experiments/toxicity_filtering/
    experiments_directory = os.path.dirname(toxicity_filtering_directory) # -> experiments/
    corpora_data_directory = os.path.join(experiments_directory, 'data', 'existing_corpora', 'data', 'processed')

    data_directory = os.path.join(toxicity_filtering_directory, 'data')
    output_directory = os.path.join(toxicity_filtering_directory, 'data', 'processing_results')
    toxic_terms_path = os.path.join(toxicity_filtering_directory, 'data', 'toxic_terms.txt')
    report_template_path = os.path.join(toxicity_filtering_directory, 'data', 'report_template.md')

    # toxic_terms = load_bad_words(toxic_terms_path)

    # print(f"[INFO] Loaded {len(toxic_terms)} toxic terms")

    # process_existing_corpora(corpora_data_directory, output_directory, toxic_terms)

    processing_paths = {
        'relative_data_directory': os.path.relpath(corpora_data_directory, toxicity_filtering_directory),
        'toxic_term_path': os.path.relpath(toxic_terms_path, toxicity_filtering_directory),
        'utils_path': os.path.relpath(os.path.join(src_dir, 'utils.py'), toxicity_filtering_directory)
    }

    create_report(data_path=data_directory, output_path=toxicity_filtering_directory, filename="toxicity_report.md", processing_paths = processing_paths)


if __name__ == "__main__":
    main()
