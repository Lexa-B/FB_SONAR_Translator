# Sonar Translator

## Overview

This project is a simple translator that uses the Sonar concept-level auto-encoder to translate text from Japanese to English.

## Installation

### Install the dependencies
```bash
uv sync
```

### Activate the virtual environment
```bash
source .venv/bin/activate
```

## Usage

### Arguments

* `-i`: Input file to translate.
  * The input file should be a text file in the `2_InputData` directory.
* `-s`: Language to translate from (FLORES-200 code) (e.g., jpn_Jpan, eng_Latn).
* `-t`: Language to translate to (FLORES-200 code) (e.g., deu_Latn, zho_Hans).
* `-v`: Enable verbose output.
* `-q`: Process sentences sequentially.

### Example

```bash
python Translator.py -i 松山鏡ーThe_Mirror_of_Matsuyamaー日本語_Clean.txt -s jpn_Jpan -t eng_Latn
```


