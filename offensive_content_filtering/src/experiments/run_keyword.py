import os
from offensive_content_filtering.src.models.keyword_classifier import KeywordClassifier
from offensive_content_filtering.src.utils.prediction_writer import PredictionWriter
from offensive_content_filtering.src.data.loader import load_dataset
from tqdm import tqdm

#Helper directories
CURRENT_FILE_PATH = os.path.dirname(__file__)
REPO_ROOT_DIRECTORY = os.path.abspath(os.path.join(CURRENT_FILE_PATH, '..', '..', '..'))
OFFENSIVE_CONTENT_FILTERING_DIRECTORY = os.path.join(REPO_ROOT_DIRECTORY, 'offensive_content_filtering')

#Input and output directories
DATA_DIRECTORY = os.path.join(OFFENSIVE_CONTENT_FILTERING_DIRECTORY, 'data')
OUTPUT_DIRECTORY = os.path.join(OFFENSIVE_CONTENT_FILTERING_DIRECTORY, 'outputs')

DOCUMENTS_DIRECTORY = os.path.join(DATA_DIRECTORY, 'raw', 'data', 'processed')

TOXIC_TERMS_FILE_PATH = os.path.join(DATA_DIRECTORY, 'toxic_terms_severity_score.csv')

OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIRECTORY, "test_keyword_matching.csv")

# -----------------------
# Debug / quick test limit
# -----------------------
DEBUG_LIMIT = 100  # Set None or remove for full run

def main():
    """Run a small test of the KeywordClassifier on a dataset."""
    # Initialize model
    model = KeywordClassifier(TOXIC_TERMS_FILE_PATH)

    # Initialize prediction writer
    writer = PredictionWriter(OUTPUT_FILE_PATH)

    # Load dataset generator
    dataset = load_dataset(DOCUMENTS_DIRECTORY)

    # Iterate over documents with tqdm progress bar
    for i, doc in enumerate(tqdm(dataset, desc="Processing documents")):

        # Debug/test limit
        if DEBUG_LIMIT and i >= DEBUG_LIMIT:
            break

        # Predict and write
        prediction = model.predict_document(doc)
        writer.write(prediction)

    writer.close()
    print(f"Test run complete. Predictions saved to {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    main()