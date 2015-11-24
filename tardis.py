# Torrented Anime Renaming Download Induced Sorter
import csv
import os
import string


# Compare text of 2 strings ignoring punctuation whitespace and numbers
def compare(s1, s2):
        remove = string.punctuation + string.whitespace + string.digits
        return s1.translate(None, remove) == s2.translate(None, remove)


# Scans for found video in provided list of known shows
def find_show(video, csv):
    for i, elmt in enumerate(csv):
        if compare(video, csv[i][0]):
            print(video, csv[i][0])
            print('Show Found')
            return i


# Scans found show template for location of '##' wildcard
def find_wildcard(templates, show_number):
    return templates[show_number][0].index('##')


def main():
    # Reads csv into array for processing
    shows = list(csv.reader(open(r'test.csv')))

    # Scan directory for mkv files and load into array
    mkvs = []
    for root, dirs, files in os.walk("."):
        for scanned_file in files:
            if scanned_file.endswith('.mkv'):
                mkvs.append(scanned_file)

    show_index = find_show(mkvs[0], shows)
    print("Show Index: %d" % show_index)

    show_wildcard = find_wildcard(shows, show_index)
    print("Wildcard Location: %d" % show_wildcard)

    '''
            lulz = shows[i][0].replace('##', '02')
            print(lulz)
            print(mkvs[0][28], mkvs[0][29])
    '''
main()
