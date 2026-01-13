from utils import read_jsonl, word_counts, write_json, make_markdown_table
import os
from copy import copy
from collections import Counter
import json
from urllib.parse import urlparse


def get_toxic_terms_report():
    toxic_terms_report = {
        'corpus_name':"",
        'total_documents':0,
        'total_documents_by_source': None,
        'total_documents_by_domain': None,
        'affected_documents':0,
        'ratio_affected_documents':0.0,
        'affected_documents_by_source': None,
        'affected_documents_by_domain': None,
        'toxic_terms':0,
        'toxic_term_counts':None,
        'toxic_terms_by_source':None,
        'toxic_terms_by_domain': None,
    }
    return toxic_terms_report


def process_corpus(input_data_directory:str, corpus_name:str, output_directory, toxic_terms):
    corpus_directory = os.path.join(input_data_directory, corpus_name)
    
    #Corpus file path
    corpus_file_path = os.path.join(corpus_directory,f"{corpus_name}.jsonl")

    #Output file paths
    corpus_output_dir = os.path.join(output_directory, corpus_name)
    os.makedirs(corpus_output_dir, exist_ok=True)
    output_file_path = os.path.join(corpus_output_dir,f"{corpus_name}_toxic_term_filtering.jsonl")
    output_report_path = os.path.join(corpus_output_dir,f"{corpus_name}_toxic_term_filtering_report.json")

    #Counters
    total_documents_by_source = Counter()
    total_documents_by_domain = Counter()
    affected_documents_by_source = Counter()
    affected_documents_by_domain = Counter()
    toxic_terms_by_source = Counter()
    toxic_terms_by_domain = Counter()
    toxic_term_counts = Counter()

    #Report dictionary
    toxic_terms_report = get_toxic_terms_report()
    toxic_terms_report["corpus_name"] = corpus_name

    #Stream corpus documents
    documents = read_jsonl(corpus_file_path)

    with open(file=output_file_path, mode="w", encoding="utf-8") as output_file:
        for document in documents:
            source = document['source']

            #Parse the domain
            url = document['url']
            if url != 'unknown':
                domain = urlparse(url).netloc
            else:
                domain = url
            
            toxic_terms_report['total_documents'] += 1
            total_documents_by_source[source] += 1
            total_documents_by_domain[domain] += 1
            toxic_term_counts_document = word_counts(document['text'], toxic_terms)

            if toxic_term_counts_document:
                doc = copy(document)
                doc['toxic_term_counts'] = toxic_term_counts_document

                toxic_terms_report['affected_documents'] +=1
                affected_documents_by_source[source] += 1
                affected_documents_by_domain[domain] += 1
                toxic_term_counts.update(toxic_term_counts_document)
                toxic_terms_document = sum(toxic_term_counts_document.values())
                toxic_terms_report['toxic_terms'] += toxic_terms_document
                toxic_terms_by_source[source] += toxic_terms_document
                toxic_terms_by_domain[domain] += toxic_terms_document

                output_file.write(json.dumps(doc, ensure_ascii=False) + "\n")

    if toxic_terms_report['affected_documents'] > 0:
        toxic_terms_report['ratio_affected_documents'] = (
            toxic_terms_report['affected_documents']
            / toxic_terms_report['total_documents']
        )

    toxic_terms_report['total_documents_by_source'] = dict(total_documents_by_source)
    toxic_terms_report['total_documents_by_domain'] = dict(total_documents_by_domain)
    toxic_terms_report['affected_documents_by_source'] = dict(affected_documents_by_source)
    toxic_terms_report['affected_documents_by_domain'] = dict(affected_documents_by_domain)
    toxic_terms_report['toxic_terms_by_source'] = dict(toxic_terms_by_source)
    toxic_terms_report['toxic_terms_by_domain'] = dict(toxic_terms_by_domain)
    toxic_terms_report['toxic_term_counts'] = dict(toxic_term_counts)

    write_json(toxic_terms_report, output_report_path)


def process_existing_corpora(input_data_directory:str, output_directory:str, toxic_terms: list):
    for corpus_name in os.listdir(input_data_directory):
        print(f"[INFO] Processing corpus: {corpus_name}")
        process_corpus(input_data_directory, corpus_name, output_directory, toxic_terms)


def create_report(filtering_data_directory:str, output_directory:str, data:dict[str,]):
    markdown_parts = []

    #Main Title
    main_title = "# Toxicity Filtering Experiments Report🤬📋"
    markdown_parts.append(main_title)

    #Introduction
    introduction_text = \
    "This report presents and analyses the results of a keyword-based toxicity filtering experiment conducted across multiple text corpora. The goal of the experiment is to evaluate the performance of the filtering method. "

    #Methodology
    methodology_text = f"""## Methodology⚙️
    This section describes the datasets, toxic term list, and filtering procedure used throughout the experiment.

    ### Source Data

    The source data (**`📁data`**)[{data['relative_data_directory']}]consist on **{data['number_of_corpora']} corpora** sourced from the Existing Corpora Repository, which compiles available Guarani corpora into files of a standardised form. For more information on the contents, read their report.

    ### Toxic Term List

    The words and phrases used for filtering, hereafter referred to as **toxic terms**, were manually copied from the SPL's list of *Palabras Vulgares u Ofensivas en Guarani*, which includes both single-word and multi-word expressions. 

    ### Filtering Criterion

    A document is considered an **affected document** if it contains **at least one term** from the list. 

    Toxic terms are identified using regular expression matching with word boundaries to reduce false positives from partial matches. Matching is performed on lowercased text using the following pattern:

    ```python
    def word_counts(text: str, words: list):
    text_lower = text.lower()
    counts = Counter()

    for phrase in words:
        phrase = phrase.lower()
        # Match whole words, even for multi-word phrases
        pattern = rf"\\b{re.escape(phrase)}\\b"
        matches = re.findall(pattern, text_lower)
        if matches:
            counts[phrase] = len(matches)

    return dict(counts)
    ```
    """

    #Corpus-level Analysis
    corpus_level_intro = "This section analyses the results at the corpus level"