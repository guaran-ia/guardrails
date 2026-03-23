import pandas as pd
from offensive_content_filtering.src.data.document import Document
from offensive_content_filtering.src.data.hashing import make_doc_id

def load_documents_from_csv(csv_path: str, text_col="text", label_col="label"):
    """
    Load documents from a CSV using pandas, handling multiline texts and optional filtering.

    Args:
        csv_path (str): Path to CSV file.
        text_col (str): Column name for the text.
        label_col (str): Column name for the label (optional).

    Yields:
        Document objects with metadata.
    """
    df = pd.read_csv(csv_path, engine="python", encoding="utf-8")

    # Drop rows where text is missing
    df = df.dropna(subset=[text_col])

    # Optional: drop rows without labels
    if label_col in df.columns:
        df = df.dropna(subset=[label_col])

    for _, row in df.iterrows():
        text = str(row[text_col])
        label = row[label_col] if label_col in row and pd.notna(row[label_col]) else None

        metadata = {}
        if label is not None:
            metadata["label"] = int(label)  # ensure integer

        # Any other columns are stored in metadata
        for col in df.columns:
            if col not in [text_col, label_col]:
                metadata[col] = row[col]

        doc = Document(
            id=make_doc_id(text),
            text=text,
            corpus=None,  # CSV test set may not have corpus
            num_words_split=None,
            num_words_punct_spacy=None,
            num_words_no_punct_spacy=None,
            num_chars=len(text),
            metadata=metadata
        )

        yield doc