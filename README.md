# ```stedsans```
`stedsans` is a Danish and English geoparsing toolkit utilizing Transformer-based models (Vaswani et al, 2017), including the Danish [Ælæctra](https://huggingface.co/Maltehb/-l-ctra-danish-electra-small-cased-ner-dane) and the English [BERT](https://huggingface.co/dslim/bert-base-NER) fine-tuned for Named Entity Recognition, to allow for an efficient and intuitive geospatial analyses of text.


## Demonstration of `stedsans`
For a demonstration of the current tools, we heavily suggest you to use the Google Colab notebook: 

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MalteHB/stedsans/blob/main/notebooks/stedsans_demo.ipynb)
## Installation
`stedsans` is developed and tested on Python 3.7+.
### Windows
Since `stedsans` requires the package `geopandas`, and the dependencies can cause several issues when using Windows, it is recommended to first install [Anaconda](https://docs.anaconda.com/anaconda/install/), which comes with pre-built binaries for `geopandas`. 

After having install Anaconda, create a conda environment and then install `stedsans` using `pip` and `geopandas` using `conda`.

```bash 
pip install stedsans
```

```bash 
conda install geopandas==0.9.0
```

### MacOS and Linux
For MacOS and Linus `stedsans` and `geopandas` can be installed directly by using `pip`.

```bash 
pip install stedsans
```
```bash 
pip install geopandas==0.9.0
```

## Usage
To use `stedsans` start by importing `stedsans`.
```python
from stedsans import stedsans
```
We can then initialize a `stedsans` instance on a pre-defined example text, and print the extracted entities.
```python
>>> example_text = "Hello my name is Malte and i live in Aarhus C. I love watching Randers FC, a football team from Randers, beat Brøndby IF, a football team from the devils island of Sjælland."

>>> my_stedsans = stedsans(example_text, language="english")

>>> my_stedsans.print_entities()

[   ('Aarhus C', 'LOC'),
    ('Randers FC', 'ORG'),
    ('Randers', 'LOC'),
    ('Brøndby IF', 'ORG'),
    ('Sjælland', 'LOC')]
```

These locations can then be vizualised using the `plot_coordinates()` function, and we can specify it to limit the locations to only coming from Denmark. This results in an interactive map.
```python
>>> my_stedsans.plot_locations(limit="country", limit_area="Denmark")
```
<div align="center">
  <img width="100%" alt="DINO illustration" src="img/plot_locations.gif">
</div>


<br />

You can also plot an interactive heatmap with `plot_heatmap()`.
```python
>>> my_stedsans.plot_heatmap(limit="country", limit_area="Denmark")
```
<div align="center">
  <img width="100%" alt="DINO illustration" src="img/plot_heatmap.gif">
</div>

<br />

`stedsans` provides lots of other features and tools and these are very thoroughly demonstrated in the Google Colab (if it wasn't obvious already - we really want you to use the colab:grinning:):

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/MalteHB/stedsans/blob/main/notebooks/stedsans_demo.ipynb)

(if it wasn't obvious already - we really want you to use the colab :grinning:)
## References

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is All you Need. In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, & R. Garnett (Eds.), Advances in Neural Information Processing Systems 30 (pp. 5998–6008). Curran Associates, Inc. http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf


---
## Contact

For help or further information feel free to connect with either of the main developers:

**Malte Højmark-Bertelsen**
<br />
[hjb@kmd.dk](mailto:hjb@kmd.dk?subject=[GitHub]%20stedsans)


[<img align="left" alt="MalteHB | Twitter" width="30px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" />][twitter]
[<img align="left" alt="MalteHB | LinkedIn" width="30px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />][linkedin]

<br />

</details>

[twitter]: https://twitter.com/malteH_B
[linkedin]: https://www.linkedin.com/in/maltehb

<br />

**Jakob Grøhn Damgaard** 
<br />
[bokajgd@gmail.com](mailto:bokajgd@gmail.com?subject=[GitHub]%20stedsans)


[<img align="left" alt="Jakob Grøhn Damgaard | Twitter" width="30px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/twitter.svg" />][twitter]
[<img align="left" alt="Jakob Grøhn Damgaard | LinkedIn" width="30px" src="https://cdn.jsdelivr.net/npm/simple-icons@v3/icons/linkedin.svg" />][linkedin]

<br />

</details>

[twitter]: https://twitter.com/JakobGroehn
[linkedin]: https://www.linkedin.com/in/jakob-gr%C3%B8hn-damgaard-04ba51144/
