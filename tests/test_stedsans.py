from pathlib import Path

import unittest

from parameterized import parameterized

from stedsans import stedsans


class TestStedsans(unittest.TestCase):

    @parameterized.expand([
        "H.C. Andersensvej, København er Mads' yndlingsgade og han arbejder på KMD.",
        ("Malte Højmark-Bertelsen bor på Testvej 13, Testby C som ligger tæt på Jakob Grøhn Damgaards yndlingssted: MCH Arena", "danish"),
        ("Adela Sobotkova is a teacher at Aarhus University and so is her colleague Ross Deans Kristensen-McLachlan", "english"),
        "KMD Aarhus Universitet Randersvej",
        "Malte tænker på en tankestreg - eller gør han?"
    ]
    )
    def test_stedsans_sentence(self, sentence=None, language=None):

        sentence = sentence

        language = language

        my_stedsans = stedsans(sentence=sentence, language=language)

        my_stedsans.print_entities()

        self.assertIsInstance(my_stedsans.entities, list)
        
    @parameterized.expand([
        "`stedsans` er en python-pakke, udviklet af Jakob Grøhn Damgaard, Aarhus Universitet, og Malte Højmark-Bertelsen, KMD, som kan bruges til at skabe geografiske visualiseringer og analyser ud fra tekster. `stedsans` kan udtrække addresser, organisationer og personnavne fra både sætninger og tekstfiler, ved bruge af den nyeste sprogteknologi - herunder kontekstbaserede sprogmodeller som Ælæctra og BERT. Hoveddelen af pakken er udviklet henholdsvist fra et dejligt sommerhus på Mols og fra to fantastiske hjem i Aarhus. Hvis man ønsker at bruge pakken i sin løsning, og/eller har spørgsmål er man velkommen til at kontakte fra oplysningerne, som er tilgængelig på https://github.com/MalteHB/stedsans#readme"
    ]
    )
    def test_stedsans_file(self, text=None):

        text = text
        
        file = Path() / "tmp.txt"

        file.write_text(text, encoding="utf-8")

        my_stedsans = stedsans(file=file)

        file.unlink()

        my_stedsans.print_entities()

        self.assertIsInstance(my_stedsans.entities, list)


if __name__ == '__main__':
    unittest.main()
