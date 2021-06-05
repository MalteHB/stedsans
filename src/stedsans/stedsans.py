"""Main class for the stedsans package
"""
import pprint

from .geography.geography import Geography

pp = pprint.PrettyPrinter(indent=4)


class stedsans(Geography):

    def __init__(self,
                 sentence=None,
                 file=None,
                 language=None,
                 model_path=None,
                 verbosity=1):

        super().__init__(language=language,
                         model_path=model_path,
                         sentence=sentence,
                         verbosity=verbosity)

        if sentence:
            
            #self.entities = self.extract_loc_and_org(sentence)
            """Due to certain LOC entities being categorized as PER such as
            "H. C. Andersensvej", the current workaround is to extract all entities,
            then find entities with "vej" in it and replace ent with LOC and lastly,
            remove all PER entities.
            """
            self.entities = self.extract_entities(sentence)
            
            no_solvej_entities = []
            
            for _, entities in enumerate(self.entities):
                ent = entities[0]
                tag = entities[1]
                if "vej" in ent:
                    tag = "LOC"
                if tag == "PER":
                    pass
                else:
                    no_solvej_entities.append((ent, tag))
                
            self.entities = no_solvej_entities
                
            

        if file:

            self.entities = self.extract_document_loc_and_org(file)

    def print_entities(self):

        return pp.pprint(self.entities)
