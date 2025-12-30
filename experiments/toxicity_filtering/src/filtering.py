from utils import read_jsonl, word_counts, read_json, write_json
import os
from copy import copy
from collections import Counter
import json


DATA_DIRECTORY = 'data'
BAD_WORDS_FILENAME = 'bad_words.txt'
EXISTING_CORPORA_DATA = 'existing_corpora/data/processed'
OUTPUT_DIRECTORY = 'data/processing_results'

def get_empty_bad_word_report():
    bad_words_report = {
        'corpus_name':"",
        'total_documents':0,
        'documents_with_bad_words':0,
        'percentage_documents_with_bad_words':0.0,
        'total_bad_words':0,
        'bad_word_counts':None,
        'sources_counts':None,
        'bad_words_by_source': None,
        'url_counts':None,
        'bad_words_by_url':None
    }
    return bad_words_report

def process_file(file_path:str, bad_words:list):
    documents = read_jsonl(file_path=file_path)
    for document in documents:
        bad_word_counts = word_counts(document['text'], bad_words)
        if bad_word_counts:
            result = copy(document)
            result['bad_word_counts'] = bad_word_counts
            yield result

def create_report(data, output_data_dir: str, corpus_name: str, corpus_report_path: str):
    corpus_output_dir = os.path.join(output_data_dir, corpus_name)
    os.makedirs(corpus_output_dir, exist_ok=True)
    output_jsonl_path = os.path.join(corpus_output_dir,f"{corpus_name}_bad_words.jsonl")
    output_report_path = os.path.join(corpus_output_dir,f"{corpus_name}_bad_words_report.json")

    bad_word_counts = Counter()
    url_counts = Counter()
    source_counts = Counter()
    bad_words_by_source = Counter()
    bad_words_by_url = Counter()

    bad_words_report = get_empty_bad_word_report()
    bad_words_report["corpus_name"] = corpus_name

    #Read corpus metadata (small → safe to load fully)
    corpus_report = read_json(corpus_report_path)

    with open(output_jsonl_path, "w", encoding="utf-8") as out_f:
        for document in data:
            bad_words_report["documents_with_bad_words"] += 1
            bad_word_counts.update(document["bad_word_counts"])
            doc_bad_word_total = sum(document["bad_word_counts"].values())
            source_counts[document["source"]] += 1
            bad_words_by_source[document["source"]] += doc_bad_word_total
            url_counts[document["url"]] += 1
            bad_words_by_url[document["url"]] += doc_bad_word_total
            out_f.write(json.dumps(document, ensure_ascii=False) + "\n")

    # Finalize report
    bad_words_report["total_documents"] = corpus_report["num_docs"]

    if bad_words_report["total_documents"] > 0:
        bad_words_report["percentage_documents_with_bad_words"] = (
            bad_words_report["documents_with_bad_words"]
            / bad_words_report["total_documents"]
        )

    bad_words_report["total_bad_words"] = sum(bad_word_counts.values())
    bad_words_report["bad_word_counts"] = dict(bad_word_counts)
    bad_words_report["sources_counts"] = dict(source_counts)
    bad_words_report["url_counts"] = dict(url_counts)
    bad_words_report["bad_words_by_source"] = dict(bad_words_by_source)
    bad_words_report["bad_words_by_url"] = dict(bad_words_by_url)

    write_json(bad_words_report, output_report_path)

def process_existing_corpora(main_directory: str, bad_words: list):
    data_path = os.path.join(main_directory,DATA_DIRECTORY,EXISTING_CORPORA_DATA)

    output_data_dir = os.path.join(main_directory,OUTPUT_DIRECTORY)

    for corpus_name in os.listdir(data_path):
        corpus_dir = os.path.join(data_path, corpus_name)

        if not os.path.isdir(corpus_dir):
            continue

        corpus_file_path = os.path.join(corpus_dir,f"{corpus_name}.jsonl")
        corpus_report_path = os.path.join(corpus_dir,f"{corpus_name}_report.json")

        if not os.path.isfile(corpus_file_path):
            continue
        print(f"[INFO] Processing corpus: {corpus_name}")
        results = process_file(corpus_file_path, bad_words)
        create_report(data=results,output_data_dir=output_data_dir,corpus_name=corpus_name,corpus_report_path=corpus_report_path)


# def process_existing_corpora(
#     main_directory: str,
#     bad_words: list,
#     max_corpora: int | None = None,
# ):
#     data_path = os.path.join(
#         main_directory,
#         DATA_DIRECTORY,
#         EXISTING_CORPORA_DATA,
#     )

#     output_data_dir = os.path.join(
#         main_directory,
#         OUTPUT_DIRECTORY,
#     )

#     processed = 0

#     for corpus_name in os.listdir(data_path):
#         if max_corpora is not None and processed >= max_corpora:
#             break

#         corpus_dir = os.path.join(data_path, corpus_name)

#         if not os.path.isdir(corpus_dir):
#             continue

#         corpus_file_path = os.path.join(
#             corpus_dir,
#             f"{corpus_name}.jsonl"
#         )

#         corpus_report_path = os.path.join(
#             corpus_dir,
#             f"{corpus_name}_report.json"
#         )

#         if not os.path.isfile(corpus_file_path):
#             continue

#         print(f"[INFO] Processing corpus: {corpus_name}")

#         results = process_file(corpus_file_path, bad_words)

#         create_report(
#             data=results,
#             output_data_dir=output_data_dir,
#             corpus_name=corpus_name,
#             corpus_report_path=corpus_report_path,
#         )

#         processed += 1



