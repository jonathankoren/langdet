#!/usr/bin/env python3

import argparse
import html
import sys



# Wikipedia abstracts can be downloaded from https://dumps.wikimedia.org/enwiki/latest/
# and at other apporpriate language codes

def unwikify(line):
    '''Attempts to unwikify text. Mainly this is dropping [] and {}, and
    attempting to handle |.'''
    escaped = False
    out = ''
    for i in range(0, len(line)):
        if escaped:
            out += line[i]
            escaped = False
        else:
            if line[i] == '[' or line[i] == ']' \
               or line[i] == '{' or line[i] == '}':
               pass
            elif line[i] == '|':
                out += ' '
            elif line[i] == '\\':
                escaped = True
            else:
                out += line[i]
    return out

parser = argparse.ArgumentParser(description='Process Wikipedia abstracts.')
parser.add_argument('abstracts', metavar='XML', type=str, nargs='+',
                    help='XML files to process')
args = parser.parse_args()

for filename in args.abstracts:
    with open(filename, 'r') as infile:
        for line in infile:
            if line.startswith('<abstract>'):
                line = line[10:-12]
                if line[0] == '|':
                    # some infobox junk
                    continue
                print(unwikify(html.unescape(line)))
