#!/bin/sh

url='https://dumps.wikimedia.org/'$1'wiki/latest/'$1'wiki-latest-abstract.xml.gz'
url1='https://dumps.wikimedia.org/'$1'wiki/latest/'$1'wiki-latest-abstract1.xml.gz'

wget $url1 || wget $url
