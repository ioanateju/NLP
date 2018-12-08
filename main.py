import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
from os import listdir
from os.path import isfile, join
import re

# Maps for files
files = {}
headers = {}
contents = {}
tagged = {}
speakers_headers = {}
speakers_contents = {}
locations_headers = {}
locations_contents = {}


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
def is_sentence(sentence):
    if sentence.strip() != '':
        if sentence.strip()[0] == '-' or sentence.strip()[0] == '*' or sentence.strip()[0] == '~':
            return False
    for something in ['type:', 'who:', 'topic:', 'dates:', 'time:', 'place:', 'duration:', 'host:', 'when:', 'where:',
                      'speaker:', 'title:']:
        if something in sentence.lower():
            return False
    tagged = nltk.pos_tag(sentence.split())
    for tag in tagged:
        if 'V' in tag[1]:
            return True
    return False


# Check if text is a paragraph
def is_paragraph(paragraph):
    if paragraph.strip() != '':
        if paragraph.strip()[0] == '-' or paragraph.strip()[0] == '*' or paragraph.strip()[0] == '~':
            return False
    for something in ['type:', 'who:', 'topic:', 'dates:', 'time:', 'place:', 'duration:', 'host:', 'when:', 'where:',
                      'speaker:', 'title:', 'furtherdetails']:
        if something in paragraph.lower():
            return False
    if '<sentence>' in paragraph:
        return True
    return False


# Tag a sentence
def tag_sent(sentence):
    return '<sentence>' + sentence[0 : len(sentence) - 1] + '</sentence>' + '.'


# Tag a paragraph
def tag_par(paragraph):
    return '<paragraph>' + paragraph + '</paragraph>'


# Tag speaker
def tag_spk(speaker):
    return '<speaker>' + speaker + '</speaker>'


# Tag location
def tag_loc(location):
    return '<location>' + location + '</location>'


# Tag speaker and location in header
def tag_speaker_location_header():
    for header in headers:
        speaker = re.search('Who:(.*)', headers[header])
        location = re.search('Place:(.*)', headers[header])
        if speaker is not None:
            line = speaker.group(1).strip()
            line2 = re.split(':|,|/|-|\(', line)
            name = line2[0]
            speakers_headers[header] = name

            headers[header] = headers[header].replace(name, tag_spk(name))
            if name in tagged[header]:
                tagged[header] = tagged[header].replace(name, tag_spk(name))

        if location is not None:
            line = location.group(1).strip()
            line2 = re.split(':|,|/|-|\(', line)
            loc = line2[0]
            locations_headers[header] = loc

            headers[header] = headers[header].replace(loc, tag_loc(loc))
            if loc in tagged[header]:
                tagged[header] = tagged[header].replace(loc, tag_loc(loc))


# Tag speaker and locationin content
def tag_speaker_location_content():
    for content in contents:
        if '<speaker>' not in tagged[content]:
            speaker = re.search('WHO:(.*)|SPEAKER:(.*)', contents[content])
            if speaker is not None:
                line = speaker.group(0).strip()
                line2 = re.split(':|,|/|-|\(', line)
                name = line2[1].strip()
                speakers_contents[content] = name

                contents[content] = contents[content].replace(name, tag_spk(name))
                if name in tagged[content]:
                    tagged[content] = tagged[content].replace(name, tag_spk(name))

        if '<location>' not in tagged[content]:
            location = re.search('WHERE:(.*)', contents[content])
            if location is not None:
                line = location.group(0).strip()
                line2 = re.split(':|,|/|-|\(', line)
                loc = line2[1].strip()
                locations_contents[content] = loc

                contents[content] = contents[content].replace(loc, tag_loc(loc))
                if loc in tagged[content]:
                    tagged[content] = tagged[content].replace(loc, tag_loc(loc))


# Tag a paragraph
def tag_paragraph(paragraph):
    sentences = nltk.sent_tokenize(paragraph)
    tagged = ''
    for sentence in sentences:
        if is_sentence(sentence):
            paragraph = paragraph.replace(sentence, tag_sent(sentence))
            tagged = tagged + tag_sent(sentence)
        else:
            tagged = tagged + sentence

    if is_paragraph(tagged):
        paragraph = paragraph.replace(paragraph, tag_par(paragraph))

    return paragraph


# Tag all paragraphs in a text
def tag_paragraphs(text):
    paragraphs = text.split('\n\n')
    for i in range (0, len(paragraphs)):
        text = text.replace(paragraphs[i], tag_paragraph(paragraphs[i]), 1)
    return text


# Tag start time and end time
def tag_time(text):
    time_format = re.compile(r'\b((0?[1-9]|1[012])([:][0-5][0-9])?(\s?[apAP][.]?[Mm])|([01]?[0-9]|2[0-3])([:][0-5][0-9]))\b')
    times = time_format.findall(text)
    if len(times) > 0:
        time1 = '<stime>' + times[0][0] + '</stime>'
        text = text.replace(times[0][0], time1)
    if len(times) > 1:
        time2 = '<etime>' + times[1][0] + '</etime>'
        text = text.replace(times[1][0], time2)

    return text


# Tag time in header
def tag_time_header(text):
    time = 'time'
    posted = text.lower().find("postedby")
    time_header = text.lower().find(time)
    if time_header != -1:
        if posted != -1:
            toreplace = text[time_header:posted]
        else:
            toreplace = text[time_header:]

        text = text.replace(toreplace, tag_time(toreplace))
    return text


# Map headers, contents and tagged files
def map():
    for file in files:
        f = files[file]
        if 'Abstract:' in f:
            temp = f.split('Abstract:')
            header = temp[0]
            text = temp[1]
            headers[file] = header
            contents[file] = text
            tagged[file] = tag_time_header(headers[file]) + '\nAbstract:' + tag_time(tag_paragraphs(contents[file]))

    tag_speaker_location_header()
    tag_speaker_location_content()


# Write tagged files
def write():
    for tag in tagged:
        file_name = 'tagged/' + tag
        if os.path.exists(file_name):
            os.remove(file_name)
        file = open(file_name, 'w')
        file.write(tagged[tag])
        file.close()


# main
if __name__ == '__main__':

    # Read files
    read()

    # Map files
    map()

    # Write files
    write()
