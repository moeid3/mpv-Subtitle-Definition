import glob
import os
import sys
import re

from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith("J"):
        return wn.ADJ
    elif treebank_tag.startswith("V"):
        return wn.VERB
    elif treebank_tag.startswith("N"):
        return wn.NOUN
    elif treebank_tag.startswith("R"):
        return wn.ADV
    else:
        return wn.NOUN


def clean_word(word):
    word = word.lower()
    word = re.sub(r"^[^\w]+|[^\w]+$", "", word)

    tokens = word.split()
    lemmatizer = WordNetLemmatizer()
    tagged_tokens = pos_tag(tokens)

    cleaned_tokens = []

    for token, tag in tagged_tokens:
        wn_tag = get_wordnet_pos(tag)
        lemma = lemmatizer.lemmatize(token, pos=wn_tag)

        if token.endswith("ss") and lemma == token[:-1]:
            lemma = token

        cleaned_tokens.append(lemma)

    return " ".join(cleaned_tokens)


def define_words(words, original_words):
    definitions = []

    for word, original in zip(words, original_words):
        # Detect POS from the original word
        tagged = pos_tag([original])
        wn_pos = get_wordnet_pos(tagged[0][1])

        # First try the exact surface form
        synsets = wn.synsets(original.lower(), pos=wn_pos)

        if not synsets:
            synsets = wn.synsets(word, pos=wn_pos)

        # Final fallback: ignore POS restriction
        if not synsets:
            synsets = wn.synsets(original.lower())

        if not synsets:
            synsets = wn.synsets(word)

        if not synsets:
            definitions.append(
                f"{original}\n  Definition not found."
            )
            continue

        synset = synsets[0]

        result = f"{original}\n  {synset.definition()}"

        examples = synset.examples()
        if examples:
            result += f"\n  Example: {examples[0]}"

        definitions.append(result)

    return "\n\n".join(definitions)


def find_obscure_words(input_string, known_words_dir=None):
    if known_words_dir is None:
        known_words_dir = os.path.join(
            os.path.dirname(__file__),
            "word-lists"
        )

    words = input_string.split()
    processed_words = []
    original_words = []

    for word in words:
        cleaned = clean_word(word)

        if cleaned:
            processed_words.append(cleaned)
            original_words.append(
                re.sub(r"^[^\w]+|[^\w]+$", "", word).lower()
            )

    known_words = set()

    pattern = os.path.join(known_words_dir, "*.txt")
    txt_files = glob.glob(pattern)

    if not txt_files:
        print(
            f"Error: No .txt files found in directory "
            f"'{known_words_dir}'."
        )
        sys.exit(1)

    for filepath in txt_files:
        try:
            with open(filepath, "r") as f:
                for line in f:
                    word_from_file = line.strip().lower()

                    if word_from_file:
                        known_words.add(word_from_file)

        except Exception as e:
            print(f"Error reading file '{filepath}': {e}")
            sys.exit(1)

    obscure_words = []
    obscure_originals = []

    for word, original in zip(processed_words, original_words):
        if (
            word.lower() not in known_words
            and "'" not in word
            and word not in obscure_words
        ):
            obscure_words.append(word)
            obscure_originals.append(original)

    return obscure_words, obscure_originals


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py 'input string'")
        sys.exit(1)

    input_string = sys.argv[1]

    obscure_words, original_words = find_obscure_words(input_string)

    if obscure_words:
        print(define_words(obscure_words, original_words))
    else:
        print("KNOWN")


if __name__ == "__main__":
    main()
