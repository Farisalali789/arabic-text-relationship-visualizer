# arabic-text-relationship-visualizer


This repository contains a Python script that processes Arabic text, extracts subject-verb-object (SVO) triples, and visualizes the relationships as an RDF graph. The script uses the **Stanza NLP library** for text processing and **PyVis** for interactive graph visualization.

## Features
- **Arabic Text Processing**: Tokenization, part-of-speech tagging, lemmatization, and dependency parsing using Stanza.
- **SVO Triple Extraction**: Extracts subject-verb-object relationships from Arabic text.
- **RDF Graph Creation**: Converts extracted triples into an RDF graph using `rdflib`.
- **Interactive Visualization**: Generates an interactive network graph using PyVis and saves it as an HTML file.

## Requirements
- **Libraries**: `stanza`, `rdflib`, `pyvis`, `urllib`
- **Disk Space**: Ensure you have at least **1 GB** of free disk space to accommodate the `stanza_resources` folder.
- **Memory**: The script may require additional memory depending on the size of the input text.
