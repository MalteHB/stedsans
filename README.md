# ```stedsans```
This repository is for an exam project for the course Spatial Analytics at Aarhus University during the spring of 2021. 

It is made by Jakob Grøhn Damgaard and Malte Højmark-Bertelsen.

The purpose of it is to build a PyPI-package capable of plotting a map of any location in a Danish sentence. To do so we employ the Natural Language Processing (NLP) technique Named Entity Recognition (NER)

**NER** is a task consisting of finding words in text that constitute a specific entities and tagging them with specific labels. The most common entities are person names (PER), locations (LOC) and organizations (ORG) (Ruder, 2019).
The way the named entities are tagged follows a tagging scheme called BIO-tagging, where the different words are separated as either being the beginning (B) of an entity, inside an entity (I), or other (O), meaning that a word is not part of the defined entities. 
An illustration of the aforementioned entities can be seen in *Table 1*.

__Table 1:__
| __NER-tag__ | __Meaning__ |
| --- | --- |
| B-PER | Beginning of person name |
| I-PER | Inside a person name |
| B-LOC | Beginning of location |
| I-LOC | Inside a location |
| B-ORG | Beginning of organization |
| I-ORG | Inside an organization |
| O | Other |
---

### Instructions
To use the code locally, start off by cloning the repository and install [Anaconda](https://docs.anaconda.com/anaconda/install/) for your OS. Afterwards create a conda environment and install the requirements.
```bash 
# From the directory of this repository
conda create -n [env_name] python=3.8  # Create conda environment
conda activate [env_name]  # Activate conda environment
pip install -r requirements.txt  # Install required packages
```

Afterwards install `geopandas`using the pre-build binaries from Anaconda:
```bash
conda install geopandas
```

### Usage
To see an example of usage see the Google Colab demo: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MalteHB/stedsans/blob/main/notebooks/stedsans_demo.ipynb)


### References
Ruder, S. (2019). Neural transfer learning for natural language processing (Doctoral dissertation, NUI Galway).

---

#### Contact
For help or further information feel free to reach out to Jakob Grøhn Damgaard on [bokajgd@gmail.com](mailto:bokajgd@gmail.com?subject=stedsans) or Malte Højmark-Bertelsen on [hjb@kmd.dk](mailto:hjb@kmd.dk?subject=stedsans).
