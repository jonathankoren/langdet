#!/usr/bin/env python3

import argparse
import json
import sys

import langdet

parser = argparse.ArgumentParser(description='Create language detection models')
parser.add_argument('filename', type=str,
                    help='Text file to process')
parser.add_argument('--ngramSize', type=int, default=3,
                    help='character ngram size')
parser.add_argument('--maxNgrams', type=int, default=sys.maxsize,
                    help='maximum number of ngrams in model')
parser.add_argument('--threshNgrams', type=int, default=0,
                    help='minimum frequency of ngram in model')
parser.add_argument('--percentNgrams', type=float, default=0.0,
                    help='minimum percentage ngrams must reach in model')

args = parser.parse_args()

# make config
config = {}
if args.ngramSize > 0:
    config = {
        'ngramSize': args.ngramSize,
        'maxValues': args.maxNgrams,
        'freqThresh': args.threshNgrams,
        'percentThresh': args.percentNgrams,
    }

model = None
with open(args.filename, 'r') as infile:
    model = langdet.train(infile, config)
if model is not None:
    with open(args.filename + '-model.json', 'w') as outfile:
        json.dump(model, outfile)
