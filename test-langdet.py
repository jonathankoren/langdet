#!/usr/bin/env python3

import argparse
import json
import sys

import langdet

parser = argparse.ArgumentParser(description='Create language detection models')
parser.add_argument('models', type=str, nargs='+', #metavar='filename',
                    help='Models to load to load')
parser.add_argument('--test', type=str,
                    help='file to test')

args = parser.parse_args()

models = {}
for filename in args.models:
    with open(filename, 'r') as infile:
        models[filename[:2]] = json.load(infile)
with open(args.test, 'r') as infile:
    print(langdet.classify(infile, models))
