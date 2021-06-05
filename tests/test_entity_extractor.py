import unittest

from stedsans.nlp.ner.entity_extractor import EntityExtractor

from parameterized import parameterized


class TestEntityExtractor(unittest.TestCase):

    @parameterized.expand([
                          ("H.C. Andersensvej, København er Mads' yndlingsgade og han arbejder på KMD.", None, 0.90),
                          ("H.C. Andersensvej, København er Mads' yndlingsgade og han arbejder på KMD.", None),
                          ("H.C. Andersensvej København er Mads' yndlingsgade og han arbejder på KMD.", None),
                          ("Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena", "danish"),
                          ("Adela Sobotkova is a teacher at Aarhus University and so is her colleague Ross Deans Kristensen-McLachlan", "english"),
                          "KMD Aarhus Universitet Randersvej",
                          "Malte tænker på en tankestreg - eller gør han?"
                          ]
                          )
    def test_extract_entities(self, sentence=None, language=None, threshold=0.00):

        sentence = sentence

        language = language

        threshold = threshold

        EE = EntityExtractor(language=language)

        extracted_entities = EE.extract_entities(sentence=sentence, threshold=threshold)

        print(extracted_entities)

        self.assertIsInstance(extracted_entities, list)

    @parameterized.expand([
                          "Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena",
                          "KMD Aarhus Universitet Randersvej"
                          ]
                          )
    def test_extract_loc(self, sentence):

        test_entity = "LOC"

        sentence = sentence

        EE = EntityExtractor()

        extracted_entities = EE.extract_loc(sentence)

        print(extracted_entities)

        tags = [entity[1] for entity in extracted_entities]

        for tag in tags:

            self.assertEqual(tag, test_entity)

    @parameterized.expand([
                          "Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena",
                          "KMD Aarhus Universitet Randersvej"
                          ]
                          )
    def test_extract_org(self, sentence):

        test_entity = "ORG"

        sentence = sentence

        EE = EntityExtractor()

        extracted_entities = EE.extract_org(sentence)

        print(extracted_entities)

        tags = [entity[1] for entity in extracted_entities]

        for tag in tags:

            self.assertEqual(tag, test_entity)

    @parameterized.expand([
                          "Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena",
                          "Jakob Grøhn Damgaard Malte Højmark-Bertelsen"
                          ]
                          )
    def test_extract_per(self, sentence):

        test_entity = "PER"

        sentence = sentence

        EE = EntityExtractor()

        extracted_entities = EE.extract_per(sentence)

        print(extracted_entities)

        tags = [entity[1] for entity in extracted_entities]

        for tag in tags:

            self.assertEqual(tag, test_entity)
    
    @parameterized.expand([
                          "Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena",
                          "Jakob Grøhn Damgaard Malte Højmark-Bertelsen"
                          ]
                          )        
    def test_extract_loc_and_org(self, sentence):
    
        test_entities = ["LOC", "ORG"]

        sentence = sentence

        EE = EntityExtractor()

        extracted_entities = EE.extract_loc_and_org(sentence)

        print(extracted_entities)

        tags = [entity[1] for entity in extracted_entities]

        for tag in tags:

            self.assertIn(tag, test_entities)


if __name__ == '__main__':
    unittest.main()
