import os

from utils import load_bad_words
from filtering import process_existing_corpora

def main():
    # Resolve project directories
    current_file = os.path.abspath(__file__)
    src_dir = os.path.dirname(current_file)
    main_directory = os.path.dirname(src_dir)
    # -> experiments/toxicity_filtering

    # Path to bad words list
    bad_words_path = os.path.join(
        main_directory,
        "data",
        "bad_words.txt",  # adjust if needed
    )

    # Load bad words
    bad_words = load_bad_words(bad_words_path)

    print(f"[INFO] Loaded {len(bad_words)} bad words")

    # Trial run: process only 3 corpora
    process_existing_corpora(
        main_directory=main_directory,
        bad_words=bad_words,
        #max_corpora=3,
    )


if __name__ == "__main__":
    main()
