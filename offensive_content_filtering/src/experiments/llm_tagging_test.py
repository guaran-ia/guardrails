# offensive_content_filtering/src/experiments/run_llm_csv_test.py
import os
from tqdm import tqdm
from dotenv import load_dotenv

from offensive_content_filtering.src.data.csv_loader import load_documents_from_csv
from offensive_content_filtering.src.models.llm_classifier import LLMClassifier
from offensive_content_filtering.src.models.llm_providers.openai_provider import OpenAIProvider
from offensive_content_filtering.src.models.llm_providers.azure_openai_provider import AzureOpenAIProvider
from offensive_content_filtering.src.utils.prediction_writer import PredictionWriter
from offensive_content_filtering.src.utils.metrics import evaluate_binary


#Helper directories
CURRENT_FILE_PATH = os.path.dirname(__file__)
REPO_ROOT_DIRECTORY = os.path.abspath(os.path.join(CURRENT_FILE_PATH, '..', '..', '..'))
OFFENSIVE_CONTENT_FILTERING_DIRECTORY = os.path.join(REPO_ROOT_DIRECTORY, 'offensive_content_filtering')

#Environment Variables
load_dotenv(dotenv_path=os.path.join(REPO_ROOT_DIRECTORY, ".env"))  # load .env if exists
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
DEFAULT_TEMPERATURE = os.getenv("DEFAULT_TEMPERATURE")

#print([AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, DEFAULT_TEMPERATURE])

if not all([AZURE_API_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, DEFAULT_TEMPERATURE]):
    raise ValueError("Missing one or more environment variables for OpenAI/Azure")

#Input and output directories
DATA_DIRECTORY = os.path.join(OFFENSIVE_CONTENT_FILTERING_DIRECTORY, 'data')
OUTPUTS_DIRECTORY = os.path.join(OFFENSIVE_CONTENT_FILTERING_DIRECTORY, 'outputs')

#Test results directory
TEST_LLM_DIRECTORY = os.path.join(OUTPUTS_DIRECTORY, "tests", "llms")

os.makedirs(TEST_LLM_DIRECTORY, exist_ok=True)

INPUT_FILE = os.path.join(DATA_DIRECTORY, 'toxicity_evaluation.csv')

# Azure models
azure_models = ["gpt-4o", "gpt-4.1"]

# OpenAI models
openai_models = ["grok-4-fast-non-reasoning", "Mistral-Large-3", "Llama-3.3-70B-Instruct"]


#Documents
# Load documents once
documents = list(load_documents_from_csv(INPUT_FILE, 'text', "Offensive"))

for model_name in azure_models:
    print(f"\n--- Running Azure OpenAI Model: {model_name} ---")
    provider = AzureOpenAIProvider(
        endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        deployment=model_name,
        temperature=DEFAULT_TEMPERATURE
    )
    classifier = LLMClassifier(provider)

    output_path = os.path.join(TEST_LLM_DIRECTORY, "", f"azure_openai_{model_name}_predictions.jsonl")
    y_true, y_pred = [], []

    with PredictionWriter(output_path, mode="w") as writer:
        for doc in tqdm(documents, desc=f"{model_name} Predictions"):
            prediction = classifier.predict_document(doc)
            writer.write(prediction)

            # Collect metrics if label exists
            label = doc.metadata.get("label") if doc.metadata else None
            if label is not None:
                y_true.append(label)
                y_pred.append(int(prediction.score))

    # Compute metrics
    if y_true:
        metrics = evaluate_binary(y_true, y_pred)
        print(f"Metrics for {model_name}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")

for model_name in openai_models:
    print(f"\n--- Running OpenAI Model: {model_name} ---")
    provider = OpenAIProvider(
        endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        deployment=model_name
    )
    classifier = LLMClassifier(provider)

    output_path = os.path.join(TEST_LLM_DIRECTORY, f"openai_{model_name}_predictions.jsonl")
    y_true, y_pred = [], []

    with PredictionWriter(output_path, mode="w") as writer:
        for doc in tqdm(documents, desc=f"{model_name} Predictions"):
            prediction = classifier.predict_document(doc)
            writer.write(prediction)

            label = doc.metadata.get("label") if doc.metadata else None
            if label is not None:
                y_true.append(label)
                y_pred.append(int(prediction.score))

    if y_true:
        metrics = evaluate_binary(y_true, y_pred)
        print(f"Metrics for {model_name}:")
        for k, v in metrics.items():
            print(f"  {k}: {v:.4f}")