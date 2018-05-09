# langdet
Language detector. Returns scores identifying a human language from a sample text.

This is a vary simple KNN language classifier that uses character shingles to determine which language a piece
of text is written in. Can be used in multilingual documents.

# Usage
`train-langdet.py` is the model trainer. It reads in a file containing text from a known language and the outputs a JSON file containing the corresponding detection model. Various options configure the model, but `--ngramSize 3` is suggested, as classification using single characters, and unicode code planes are not currently supported.

`test-langdet.py` is a sample script for identifying a language. It is very simple, and can be used as an example for integrating language detection into another codebase.

`processWikiAbstracts.py` is a utility function for converting Wikipedia pages into usable text corpora for training purposes. Wikipedia abstracts can be obtained from
`https://dumps.wikimedia.org/enwiki/latest/`, or by running `download-abstracts.sh <lang>`
