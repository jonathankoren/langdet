# Langdet language detection / classification.
# Jonathan Koren <jonathan@jonathankoren.com>
#
# MIT License
#
# Copyright (c) 2018 Jonathan Koren
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import math
import operator
import sys

def topNValues(x, topN, thresh, minPercent):
    '''Given a dictionary containing keys and counts, returns the subset
    of keys that are:
        - are the topN most frequent keys
        - have a frequency in excess of `thresh`
        - account for more than `minPercent` of all values'''
    totalNum = float(sumValues(x))
    sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    if len(sorted_x) > topN:
        sorted_x = sorted_x[:topN]
    z = {}
    for kvp in sorted_x:
        if kvp[1] > thresh and float(kvp[1]) / totalNum > minPercent:
            z[kvp[0]] = kvp[1]
    return z

def normalize(d):
    '''Takes a dictionary of keys to numeric values, and then rescales all the
    values by the L2 norm (i.e. euclidian distance) of the dictionary.'''
    norm = 0.0
    for kvp in d.items():
        norm += kvp[1] * kvp[1]
    norm = math.sqrt(norm)
    n = {}
    for k in d:
        n[k] = d[k] / norm
    return n

def sumValues(x):
    '''Given a dictionary of keys to numbers, returns the sum of all the
    values in the dictionary.'''
    s = 0
    for (k,v) in x.items():
        s += v
    return s

def processStream(inStream, ngramSize):
    ngramCounts = {}
    for line in inStream:
        if line == '':
            continue
        length = len(line)
        for i in range(0, length):
            c = line[i]

            if ngramSize > 0:
                if i + ngramSize < length:
                    ngram = line[i:i+ngramSize]
                    if ngram not in ngramCounts:
                        ngramCounts[ngram] = 1
                    else:
                        ngramCounts[ngram] = ngramCounts[ngram] + 1
    return ngramCounts

def train(inStream, config):
    '''Processes characters from inStream and returns a dictionary that
    represents the language detection model. The model is defined the `config`
    argument. All keys in the config are optional, but at least one key needs
    to be defined in order to build a model. Config parameters are:
    - ngrams
        - ngramSize         -- size in characters of the ngram
        - maxValues         -- maximum number of ngrams to consider
        - freqThresh        -- consider only ngrams that occur more than this number of times
        - percentThresh     -- consider only ngrams that account for more than this percentage of all ngrams'''

    # setup ngram features
    ngramSize = config.get('ngramSize', 0)
    maxNgrams = config.get('maxValues', sys.maxsize)
    threshNgrams = config.get('freqThresh', 0)
    percentNgrams = config.get('percentThresh', 0.0)

    ngramCounts = processStream(inStream, ngramSize)
    model = {}
    model['ngramSize'] = ngramSize
    model['ngrams'] = normalize(topNValues(ngramCounts, maxNgrams, threshNgrams, percentNgrams))

    return model

def classify(inStream, modelMap):
    '''Takes an input stream and a map of language codes to models, and returns
    the language code that best describes the input stream.

    IMPORTANT: All models must have the same ngramSize.'''
    ngramSize = list(modelMap.items())[0][1].get('ngramSize', 0)

    ngramCounts = processStream(inStream, ngramSize)
    item_ngrams = normalize(ngramCounts)

    bestLang = None
    bestSim = 0.0
    for (lang, model) in modelMap.items():
        sim = 0.0
        for (ngram, score) in model['ngrams'].items():
            try:
                sim += item_ngrams[ngram] * score
            except KeyError:
                pass
        if sim > bestSim:
            bestSim = sim
            bestLang = lang
    return (bestLang, bestSim)
