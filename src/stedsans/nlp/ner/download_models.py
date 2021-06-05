#!usr/bin/env python3

import argparse

from transformers import AutoModelForTokenClassification, AutoTokenizer
import nltk


def main(args):

    model_dir = args.md

    DownloadModels(model_dir=model_dir)


class DownloadModels:

    def __init__(self, model_dir='Maltehb/-l-ctra-danish-electra-small-cased-ner-dane'):

        self.model_dir = model_dir

        self.model = AutoModelForTokenClassification.from_pretrained(model_dir)

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, do_lower_case=False, strip_accents=False)

        try:
            nltk.data.find('tokenizers/punkt')

        except LookupError:

            nltk.download('punkt')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--md',
                        metavar="Model Directory",
                        type=str,
                        default=None,
                        help='Path to model directory',
                        required=False)

    parser.add_argument('--NER_tags',
                        metavar="NER_tags",
                        type=list,
                        default=None,
                        help='List of used model-specific entities in BIO-scheme format',
                        required=False)

    main(parser.parse_args())
