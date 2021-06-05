"""Class for extracting entities from a given sentence
"""

import nltk
import numpy as np

from tqdm import tqdm

from .predict import NamedEntityRecognition


class EntityExtractor(NamedEntityRecognition):

    def __init__(self, **kwargs):

        super().__init__(model_path=kwargs.get("model_path"),
                         language=kwargs.get("language"),
                         verbosity=kwargs.get("verbosity"))

        try:

            self.sentence = kwargs["sentence"]

        except Exception:

            self.sentence = None

        try:

            self.file = kwargs["file"]

        except Exception:

            self.file = None

    def extract_entities(self, sentence=None, entity=None, threshold=0.00) -> list:
        """Extracting the entities of an input sentence.

        Args:
            sentence (str): Sentence to extract entities from.
            entity (Optional, str): LOC, PER or ORG. Specific entity to extract.

        Raises:
            ValueError: Invalid tag order.

        Returns:
            list: List of tuples with extracted entities and entity type.
        """

        if sentence:

            NER_dict = self.tag_sentence(sentence=sentence)

        else:

            NER_dict = self.tag_sentence(self.sentence)

        extracted_result = []

        current_entity_tokens = []  # Named entity instances will go here.

        current_entity = []  # Tokens that are part of the current entity will go here.

        current_probabilities = []

        for idx, tag in enumerate(NER_dict.get("tag")):

            token = NER_dict.get("word")[idx]

            if entity is None:

                if tag == 'O':	 # We've reached the end of the current entity.
                    continue
                
                else:
                    current_probabilities.append(NER_dict.get("probability")[idx])

                if tag.startswith("B-"):

                    if current_entity:

                        if np.mean(current_probabilities) >= threshold:

                            extracted_result.append((" ".join(current_entity_tokens), current_entity))

                            current_probabilities = []

                    current_entity = tag[2:]  # Removing the 'B-' or 'I-'

                    current_entity_tokens = [token]
                    
                    current_probabilities = [NER_dict.get("probability")[idx]]

                elif "I-" in tag:

                    current_entity_tokens.append(token)
                    
                    current_probabilities.append(NER_dict.get("probability")[idx])

                else:

                    raise ValueError("Invalid tag order.")

            else:

                if entity in tag:  # If the tag has the specified entity
                                      
                    if tag.startswith("B-"):

                        if current_entity:

                            if np.mean(current_probabilities) >= threshold:

                                extracted_result.append((" ".join(current_entity_tokens), current_entity))

                                current_probabilities = []

                        current_entity = tag[2:]  # Removing the 'B-' or 'I-'

                        current_entity_tokens = [token]
                        
                        current_probabilities = [NER_dict.get("probability")[idx]]

                    elif "I-" in tag:

                        current_entity_tokens.append(token)
                        
                        current_probabilities.append(NER_dict.get("probability")[idx])

                    else:

                        raise ValueError("Invalid tag order.")

        if current_entity and current_probabilities:

            if np.mean(current_probabilities) >= threshold:

                extracted_result.append((" ".join(current_entity_tokens), current_entity))

                current_probabilities = []

        return extracted_result

    def extract_loc(self, sentence=None) -> list:
        """Extracting the location entities of an input sentence.

        Args:
            sentence (str): Sentence to extract entities from.

        Returns:
            list: List of tuples with extracted entities and entity type.
        """

        return self.extract_entities(sentence, entity="LOC")

    def extract_org(self, sentence: str) -> list:
        """Extracting the organization entities of an input sentence.

        Args:
            sentence (str): Sentence to extract entities from.

        Returns:
            list: List of tuples with extracted entities and entity type.
        """

        return self.extract_entities(sentence, entity="ORG")

    def extract_per(self, sentence=None) -> list:
        """Extracting the person entities of an input sentence.

        Args:
            sentence (str): Sentence to extract entities from.

        Returns:
            list: List of tuples with extracted entities and entity type.
        """

        return self.extract_entities(sentence, entity="PER")

    def extract_loc_and_org(self, sentence=None) -> list:
        """Extracting the location and organization entities of an input sentence.

        Args:
            sentence (str): Sentence to extract entities from.

        Returns:
            list: List of tuples with extracted entities and entity type.
        """

        entities = self.extract_loc(sentence)

        entities.extend(self.extract_org(sentence))

        return entities

    def extract_document_entities(self, file=None, language="danish"):

        if file:

            text = file.read_text(encoding="utf-8")

        else:

            text = self.file.read_text(encoding="utf-8")

        try:

            nltk.data.find('tokenizers/punkt')

        except LookupError:

            print("Downloading sentence tokenizer")

            nltk.download('punkt')

        token_text = nltk.sent_tokenize(text, language=language)

        document_entities = []

        print("Predicting entities for file: '{file}'")

        for sentence in tqdm(token_text):

            sentence_entities = self.extract_entities(sentence=sentence)
            
            """Due to certain LOC entities being categorized as PER such as 
            "H. C. Andersensvej", the current workaround is to extract all entities,
            then find entities with "vej" in it and replace ent with LOC and lastly,
            remove all PER entities.
            """
            no_solvej_entities = []
            for _, entities in enumerate(sentence_entities):
                ent = entities[0]
                tag = entities[1]
                if "vej" in ent:
                    tag = "LOC"
                if tag == "PER":
                    pass
                else:
                    no_solvej_entities.append((ent, tag))
                
            sentence_entities = no_solvej_entities

            document_entities.extend(sentence_entities)

        return document_entities

    def extract_document_loc_and_org(self, file=None, language="danish"):
    
        if file:

            text = file.read_text(encoding="utf-8")

        else:

            text = self.file.read_text(encoding="utf-8")

        try:

            nltk.data.find('tokenizers/punkt')

        except LookupError:

            print("Downloading sentence tokenizer")

            nltk.download('punkt')

        token_text = nltk.sent_tokenize(text, language=language)

        document_entities = []

        print(f"Predicting entities for file: '{file}'")

        for sentence in tqdm(token_text):

            sentence_entities = self.extract_loc(sentence)

            sentence_entities.extend(self.extract_org(sentence))

            document_entities.extend(sentence_entities)

        return document_entities
