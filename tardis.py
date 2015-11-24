# Torrented Anime Renamer Download Induced Sorter
import csv
import os
import string


def compare(s1, s2):
        remove = string.punctuation + string.whitespace + string.digits
        return s1.translate(None, remove) == s2.translate(None, remove)

array = list(csv.reader(open(r'test.csv')))
mkvs = []
for root, dirs, files in os.walk("."):
    for scanned_file in files:
        if scanned_file.endswith('.mkv'):
            mkvs.append(scanned_file)

for i, elmt in enumerate(array):
    if compare(mkvs[0], array[i][0]):
        print(mkvs[0], array[i][0])
        print('Show Found')
        show_index = i
        print("Show Index: %d" % show_index)
        print("Wildcard Location: %d" % array[i][0].index('##'))
        #lulz = array[i][0].replace('##', '02')
        #print(lulz)
        print(mkvs[0][28], mkvs[0][29])
