import setuptools

with open("requirements.txt", encoding='utf-8') as f:
    requirements = f.read()

setuptools.setup(
    install_requires=requirements,
    keywords="Geospatial Analysis NLP Danish English",
)
