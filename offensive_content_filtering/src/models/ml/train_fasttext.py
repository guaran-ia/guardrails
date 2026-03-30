import os
import re
import fasttext
import multiprocessing


def normalize_text(text: str):
    text = text.replace("\n", " ")
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def write_txt_file(source_directory: str, output_txt_path: str):
    """
    Converts JSONL dataset into FastText training format.
    One document per line.
    """
    from offensive_content_filtering.src.data.loader import load_jsonl_documents

    with open(output_txt_path, "w", encoding="utf-8") as f:
        for doc in load_jsonl_documents(source_directory):
            text = normalize_text(doc.text)
            if text:
                f.write(text + "\n")


def train_fasttext_model(input_path: str, output_path: str):
    """
    Train FastText embeddings and save model.
    """

    model = fasttext.train_unsupervised(
        input=input_path,
        model="skipgram",
        dim=300,
        epoch=10,
        lr=0.05,
        minn=3,
        maxn=6,
        minCount=2,
        thread=multiprocessing.cpu_count()
    )

    model.save_model(output_path)