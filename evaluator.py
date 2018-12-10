import re
from os import listdir
from os.path import isfile, join

filenames = []


def read_file_names():
    path = 'test_tagged/'
    filenames = [f for f in listdir(path) if isfile(join(path, f))]
    return filenames


def w_tags(text):
    tag = re.compile('<.?>')
    w_tag = re.sub(tag, '', text)
    return w_tag


def untagged(text, tag):
    start = '<' + tag + '>'
    end = '</' + tag + '>'

    pattern = re.compile(start + '(.*?)' + end)

    tagged_text = []

    for tags in re.findall(pattern, text):
        tagged_text.append(w_tags(tags))

    return tagged_text


def values(tagged, test):
    true_pos = 0;
    tags = []

    for tag in tagged:
        if tag in test:
            true_pos += 1
            tags.append(tag)

    for tag in tags:
        if tag in tagged:
            tagged.pop(tagged.index(tag))
        if tag in test:
            test.pop(test.index(tag))

    false_pos = len(test)
    false_neg = len(tagged)

    return true_pos, false_pos, false_neg


if __name__ == '__main__':
    filenames = read_file_names()
    tags = ['sentence', 'paragraph', 'stime', 'etime', 'speaker', 'location']

    map_tags = {}
    for tag in tags:
        map_tags[tag] = {}
        map_tags[tag]['true positive'] = 0
        map_tags[tag]['false positive'] = 0
        map_tags[tag]['false negative'] = 0

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for file in filenames:
        tagged_path = 'tagged/' + file
        test_path = 'test_tagged/' + file

        tagged_file = open(tagged_path, 'r').read()
        test_file = open(test_path, 'r').read()

        tagged_tag = ''
        test_tag = ''

        for tag in tags:
            if tag == 'paragraph':
                for t in tags:
                    tagged_tag = untagged(tagged_file, t)
                    test_tag = untagged(test_file, t)
            else:
                if tag == 'sentence':
                    for t in ['stime', 'etime', 'speaker', 'location', 'sentence']:
                        tagged_tag = untagged(tagged_file, t)
                        test_tag = untagged(test_file, t)
                else:
                    tagged_tag = untagged(tagged_file, tag)
                    test_tag = untagged(test_file, tag)

            # if tag == 'location':
            #     print(file)
            #     print (tagged_tag)
            #     print(test_tag)

            true_pos, false_pos, false_neg = values(tagged_tag, test_tag)
            true_positives += true_pos
            false_positives += false_pos
            false_negatives += false_neg

            map_tags[tag]['true positive'] += true_pos
            map_tags[tag]['false positive'] += false_pos
            map_tags[tag]['false negative'] += false_neg

    accuracy = 0
    precision = 0
    recall = 0
    f1 = 0

    if true_positives + false_positives + false_negatives == 0:
        accuracy = 100
    else:
        accuracy = true_positives / (true_positives + false_positives + false_negatives) * 100

    if true_positives + false_positives == 0:
        precision = 100
    else:
        precision = true_positives / (true_positives + false_positives) * 100

    if true_positives + false_negatives == 0:
        recall = 100
    else:
        recall = true_positives / (true_positives + false_negatives) * 100

    if precision + recall == 0:
        f1 = 100
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    print('TAG                    Accuracy    Precision   Recall      F1 measure')
    print('total' + (10 - len('total')) * ' ' + '             {a:.2f}%      {p:.2f}%      {r:.2f}%      {f:.2f}%'.format(a=accuracy, p=precision, r=recall, f=f1))

    for tag in tags:
        accuracy = 0
        precision = 0
        recall = 0
        f1 = 0

        tp = map_tags[tag]['true positive']
        fp = map_tags[tag]['false positive']
        fn = map_tags[tag]['false negative']

        if tp + fp + fn == 0:
            accuracy = 100
        else:
            accuracy = tp / (tp + fp + fn) * 100

        if tp + fp == 0:
            precision = 100
        else:
            precision = tp / (tp + fp) * 100

        if tp + fn == 0:
            recall = 100
        else:
            recall = tp / (tp + fn) * 100

        if precision + recall == 0:
            f1 = 100
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        print(tag + (10 - len(tag)) * ' ' + '             {a:.2f}%      {p:.2f}%      {r:.2f}%      {f:.2f}%'.format(a=accuracy, p=precision, r=recall, f=f1))
