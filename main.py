from os import listdir
from os.path import isfile, join

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

    for content in mapFiles:

        print(mapFiles[content])

readContents()

