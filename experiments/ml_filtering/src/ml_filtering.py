from transformers import pipeline
from utils import read_jsonl, write_json
import os
from urllib.parse import urlparse
from copy import copy
import json
from collections import Counter

def get_ml_filtering_report():
    ml_filtering_report = {
        'corpus_name':"",
        'total_documents':0,
        'classification_model':"",
        'total_documents_by_source': None,
        'total_documents_by_domain': None,
        'affected_documents':0,
        'ratio_affected_documents':0.0,
        'affected_documents_by_source': None,
        'affected_documents_by_domain': None,
        'average_offensiveness_score_total': 0.0,
        'average_offensiveness_score_affected': 0.0
    }

    return ml_filtering_report


def process_corpus(input_data_directory, corpus_name, output_directory, model, model_name):
    corpus_directory = os.path.join(input_data_directory, corpus_name)
    
    #Corpus file path
    corpus_file_path = os.path.join(corpus_directory,f"{corpus_name}.jsonl")

    #Output file paths
    corpus_output_dir = os.path.join(output_directory, corpus_name)
    os.makedirs(corpus_output_dir, exist_ok=True)
    output_file_path = os.path.join(corpus_output_dir,f"{corpus_name}_ml_filtering_{model_name}.jsonl")
    output_report_path = os.path.join(corpus_output_dir,f"{corpus_name}_ml_filtering_{model_name}_report.json")

    total_documents_by_source = Counter()
    total_documents_by_domain = Counter()
    affected_documents_by_source = Counter()
    affected_documents_by_domain = Counter()

    total_offensiveness_score = 0.0

    documents = read_jsonl(corpus_file_path)

    ml_filtering_report = get_ml_filtering_report()

    ml_filtering_report["corpus_name"] = corpus_name
    ml_filtering_report["classification_model"] = model_name

    with open(file=output_file_path, mode="w", encoding="utf-8") as output_file:
        for document in documents:
            source = document['source']

            #Parse the domain
            url = document['url']
            if url != 'unknown':
                domain = urlparse(url).netloc
            else:
                domain = url

            ml_filtering_report['total_documents'] += 1
            total_documents_by_source[source] += 1
            total_documents_by_domain[domain] += 1
            classification_result = model(document['text'])[0]

            if classification_result['label'] == 'OFF':
                doc = copy(document)
                doc['offensiveness_score'] = classification_result['score']
                total_offensiveness_score += classification_result['score']
                ml_filtering_report['affected_documents'] +=1
                affected_documents_by_source[source] += 1
                affected_documents_by_domain[domain] += 1
                output_file.write(json.dumps(doc, ensure_ascii=False) + "\n")
    
    if ml_filtering_report['affected_documents'] > 0:
        ml_filtering_report['ratio_affected_documents'] = (
            ml_filtering_report['affected_documents']
            / ml_filtering_report['total_documents']
        )

    if total_offensiveness_score > 0:
        ml_filtering_report['average_offensiveness_score_total'] = total_offensiveness_score/ml_filtering_report['total_documents']
        ml_filtering_report['average_offensiveness_score_affected'] = total_offensiveness_score/ml_filtering_report['affected_documents']

    ml_filtering_report['total_documents_by_source'] = dict(total_documents_by_source)
    ml_filtering_report['total_documents_by_domain'] = dict(total_documents_by_domain)
    ml_filtering_report['affected_documents_by_source'] = dict(affected_documents_by_source)
    ml_filtering_report['affected_documents_by_domain'] = dict(affected_documents_by_domain)

    write_json(ml_filtering_report, output_report_path)

def process_existing_corpora(input_data_directory:str, output_directory:str, model_path: str, model_name:str):
    for corpus_name in os.listdir(input_data_directory):
        print(f"[INFO] Processing corpus: {corpus_name} with model {model_name}")

        model = pipeline("text-classification", model=model_path)

        process_corpus(input_data_directory, corpus_name, output_directory, model, model_name)