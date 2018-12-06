import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
from os import listdir
from os.path import isfile, join
import re

# Maps for files
files = {}
headers = {}
contents = {}
tagged = {}

# Read files contents
def read():
    path = 'untagged/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    # Read files
    for file_name in onlyfiles:
        file_path = path + file_name
        file = open(file_path, 'r')
        content = file.read()
        files[file_name] = content

# Check is text is a sentence
def isSentence(text):
    tagged = nltk.pos_tag(text.split())
    for tag in tagged:
        if 'VB' in tag[1]:
            return True
    return False

# Check if text is a paragraph
def isParagraph(paragraph):
    if '<sentence>' in paragraph:
        return True
    return False

# Tag a sentence
def tagSent(sentence):
    return '<sentence>' + sentence[0 : len(sentence) - 1] + '</sentence>' + '.'

# Tag a paragraph
def tagPar(paragraph):
    return '<paragraph>' + paragraph + '</paragraph>'

# Tag a paragraph
def tagParagraph(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    tagged = ''
    for sentence in sentences:
        if 'where:' not in sentence.lower() and 'when:' not in sentence.lower() and 'speaker:' not in sentence.lower() and 'title' not in sentence.lower():
            if isSentence(sentence):
                paragraph = paragraph.replace(sentence, tagSent(sentence))
                tagged = tagged + tagSent(sentence)
            else:
                tagged = tagged + sentence
        else:
            tagged = tagged + sentence

    if(isParagraph(tagged)):
        paragraph = paragraph.replace(paragraph, tagPar(paragraph))

    return paragraph

# Tag all paragraphs in a text
def tagParagraphs(text):
    paragraphs = text.split('\n\n')
    for i in range (0, len(paragraphs) - 1):
        text = text.replace(paragraphs[i], tagParagraph(paragraphs[i]), 1)
    return text

# Tag start time and end time
def tagTime(text):

    time_format = re.compile(r'\b((0?[1-9]|1[012])([:][0-5][0-9])?(\s?[apAP][Mm])|([01]?[0-9]|2[0-3])([:][0-5][0-9]))\b')
    times = time_format.findall(text)
    if len(times) > 0:
        time1 = '<stime>' + times[0][0] + '</stime>'
        text = text.replace(times[0][0], time1)
    if len(times) > 1:
        time2 = '<etime>' + times[1][0] + '</etime>'
        text = text.replace(times[1][0], time2)

    return text

def tagTimeHeader(text):
    time = 'time'
    posted = text.lower().find("postedby")
    time_header = text.lower().find(time)
    if time_header != -1:
        if posted != -1:
            toreplace = text[time_header:posted]
        else:
            toreplace = text[time_header:]

        text = text.replace(toreplace, tagTime(toreplace))
    return text

# Tag speaker in text
# def tagSpeaker(text):
#     stanfordClassifier = '/Users/ioanateju/nltk_data/taggers/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz'
#     stanfordNerPath = '/Users/ioanateju/nltk_data/taggers/stanford-ner-2018-10-16/stanford-ner.jar'
#     st = StanfordNERTagger(stanfordClassifier, stanfordNerPath, encoding='utf8')
#     result = st.tag(word_tokenize(text))
#     res = []
#     for r in result:
#         if r[1] == "PERSON":
#             res.append(r[0])
#
#     if len(res) > 1:
#         tagged = "<speaker>" + res[0] + " " + res[1] + "</speaker>"
#         text = text.replace(res[0] + " " + res[1], tagged)
#     else:
#         if len(res) > 0:
#             tagged = "<speaker>" + res[0] + "</speaker>"
#             text = text.replace(res[0] + res[1], tagged)
#
#     return text

def map():
    for file in files:
        f = files[file]
        if 'Abstract:' in f:
            temp = f.split('Abstract:')
            header = temp[0]
            text = temp[1]
            headers[file] = header
            contents[file] = text
            tagged[file] = tagTimeHeader(headers[file]) + '\n Abstract:' + tagTime(tagParagraphs(contents[file]))

# main
if __name__ == '__main__':

    # Read files
    read()

    # Map files
    map()

    print(tagged['303.txt'])