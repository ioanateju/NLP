import nltk
import numpy
from os import listdir
from os.path import isfile, join
from nltk.tokenize import word_tokenize
from nltk import ne_chunk

mapFiles = {}
madHeaders = {}
mapContent = {}
mapTags = {}


def readContents():

    myPath = "wsj_untagged/"

    onlyfiles = [f for f in listdir(myPath) if isfile(join (myPath, f))]


    for fileName in onlyfiles:
        filePath = myPath + fileName
        file = open(filePath, "r")
        fileContent = file.read()

        mapFiles[fileName] = fileContent


    print(mapFiles['wsj_0017.txt'])
    print(word_tokenize(mapFiles['wsj_0017.txt']))
    print(ne_chunk(nltk.pos_tag(word_tokenize(mapFiles['wsj_0017.txt'])), binary=False))

readContents()

