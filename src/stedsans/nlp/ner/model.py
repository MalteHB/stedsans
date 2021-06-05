from transformers import AutoModelForTokenClassification, AutoTokenizer


class NERModel:
    """Class for loading a model from Huggingface's model hub.
    """

    def __init__(self,
                 language=None,
                 model_path=None,
                 verbosity=1):

        self.model_path = model_path

        self.language = language

        if self.model_path:

            print(f"Using specified model name: '{self.model_path}'")

        else:

            if self.language == "danish":

                self.model_path = "Maltehb/-l-ctra-danish-electra-small-cased-ner-dane"
                
                if verbosity == 2:

                    print(f"'language' is set to: '{self.language}', but 'model_path' has not been specified. Defaulting to '{self.model_path}'.")

            elif self.language == "english":

                self.model_path = "dslim/bert-base-NER"

                if verbosity == 2:
                        
                    print(f"'language' is set to: '{self.language}', but 'model_path' has not been specified. Defaulting to '{self.model_path}'.")

            else:

                self.language = "danish"

                self.model_path = "Maltehb/-l-ctra-danish-electra-small-cased-ner-dane"

                if verbosity == 2:
                    
                    print(f"Neither 'language' nor 'model_path' has been specified. Defaulting to '{self.language}' and '{self.model_path}'.")

        self._shared_model = {"tokenizer": AutoTokenizer.from_pretrained(self.model_path, do_lower_case=False, strip_accents=False),
                              "model": AutoModelForTokenClassification.from_pretrained(self.model_path),
                              "model_path": self.model_path,
                              "language": self.language
                              }

        self.__dict__ = self._shared_model
