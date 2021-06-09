#!usr/bin/env python
# python src/nlp/ner/ner.py --s "Jakob bor i Aarhus"

import argparse

import torch
import torch.nn.functional as F

from .model import NERModel


def main(args):

    model = args.md

    tokenizer = args.tk

    sentence = args.s

    if sentence is None:

        sentence = "Jakob bor i Aarhus og er FC Midtjylland fan, imens Malte bor i Aarhus og er Randers FC fan"

    NER_instance = NamedEntityRecognition(model=model, tokenizer=tokenizer)

    NER_instance.tag_sentence(sentence=sentence)


class NamedEntityRecognition(NERModel):
    """Named Entity Recognition
    """

    def __init__(self,
                 language=None,
                 tokenizer=None,
                 model_path=None,
                 verbosity=1):

        super().__init__(model_path=model_path, language=language, verbosity=verbosity)

    def __repr__(self):

        return f"{self.__class__.__name__}(model_path={self.model_path})"


    def tag_sentence(self, sentence):
        """Tags sentence with Named Entity Recognition labels using a Transformer-based Language model

        Args:
            sentence (str): Input sentece

        Returns:
            dict: Dictionary containing the tokens and their corresponding predictions and prediction probabilities.
        """
        # For GPU use only.
        # self.model.cuda()

        # Preprocessing sentence
        tokenized_sentence = self.tokenizer.encode(sentence, add_special_tokens=True)

        input_ids = torch.tensor([tokenized_sentence])  # If using GPU add '.cuda()'

        # Getting predictions from the model
        with torch.no_grad():

            logits = self.model(input_ids)

        logits = F.softmax(logits[0], dim=2)

        logits_label = torch.argmax(logits, dim=2)

        logits_label = logits_label.detach().cpu().numpy().tolist()[0]

        logits_confidence = [values[label].item() for values, label in zip(logits[0], logits_label)]


        # Joining tokens, tags and confidence probabilities of the model
        tokens = self.tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])

        new_tokens, new_labels, new_probs = [], [], []

        for token, label_idx, probs in zip(tokens, logits_label, logits_confidence):

            label = self.model.config.id2label[label_idx]

            # If word piece tokenized: append word piece to last token
            if token.startswith("##"):

                new_tokens[-1] = new_tokens[-1] + token[2:]

            elif token.startswith("."):

                pass

            elif token.startswith(","):

                pass

            else:

                if token != "[CLS]":

                    if token != "[SEP]":

                        if new_tokens:

                            # If token is a hyphen: append to last token
                            if token.startswith("-"):

                                new_tokens[-1] = new_tokens[-1] + token

                            # If last token ends with a hypen: append current token to last token
                            elif new_tokens[-1].endswith("-"):

                                new_tokens[-1] = new_tokens[-1] + token

                            # If token is an apostrophe: append to last token
                            elif token.startswith("'"):

                                new_tokens[-1] = new_tokens[-1] + token

                            else:

                                new_labels.append(label)

                                new_tokens.append(token)

                                new_probs.append(probs)

                        else:

                            new_labels.append(label)

                            new_tokens.append(token)

                            new_probs.append(probs)

        preds_dict = {"word": new_tokens,
                      "tag": new_labels,
                      "probability": new_probs}

        return preds_dict


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--md',
                        metavar="Model Directory",
                        type=str,
                        default=None,
                        help='Path to model directory',
                        required=False)

    parser.add_argument('--tk',
                        metavar="Model Tokenizer",
                        type=str,
                        default=None,
                        help='Path to tokenizer directory',
                        required=False)

    parser.add_argument('--NER_tags',
                        metavar="NER_tags",
                        type=list,
                        default=None,
                        help='List of used model-specific entities in BIO-scheme format',
                        required=False)

    parser.add_argument('--s',
                        metavar="sentence",
                        type=str,
                        default=None,
                        help='String: Sentence to recognize entities from.',
                        required=False)

    main(parser.parse_args())
