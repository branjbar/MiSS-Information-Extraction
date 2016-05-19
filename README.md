# MiSS Information Extraction
The code provided here allows for extraction of names and household relationships from notarial acts written in Dutch language.

## How to use this code

Using this code is as easy as download the complete package an running the main file 'nerd_main.py' in python:
```
python nerd_main.py
```

### more details
* `nerd_main.py` contains the main class `NERD(.)` that can be used as
```python
nerd = Nerd(a_piece_of_text)
```
Then, the references can be extracted by
```python
nerd.get_references()
```
and the relations can be extracted by
```python
nerd.get_relations()
```
Also, a highlighted html text can be exported by using the following code
```python
nerd.get_highlighted_text()
```

* `module_preprocess.py` contains the code for preprocessing the text and removing/correcting the bad text patterns
* `module_names.py` contains the code for tagging words
* `module_refs` contains the code for using the tagged words to extract relations
* `module_rels` contains the code for detecting the husband-wife relationships
* `/db`-folder contains some dictionaries required to extract the names from text
..* `first_name.txt`: list of frequent first names in Dutch
..* `last_name_multiple.txt`: list of commong last names that consist of more than one word
..* `starting_words.py` list of the words that start a sentence and can be problematic in detecting the correct pattern of names


## Evaluations
according to the first evaluations on 48 notarial acts that contain 309 individual names, 278 names are extracted precisely 
and 31 names are undetected: Recall: 90%, Precision: 91%

## Terms of Use
This code is developed within the MiSS project (http://swarmlab.unimaas.nl/catch/), funded by NWO. This code is free to use. 
However, it will be highly appreciated if the developer gets notified in case of use (email: bij.ranjbar@gmail.com).

