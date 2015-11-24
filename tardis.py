# Torrented Anime Renaming Download Induced Sorter
import csv
import os
import string


# Compare text of 2 strings ignoring punctuation whitespace and numbers
def compare(s1, s2):
        remove = string.punctuation + string.whitespace + string.digits
        return s1.translate(None, remove) == s2.translate(None, remove)


# Scans for found video in provided list of known shows
def find_show(video, array):
    for i, elmt in enumerate(array):
        if compare(video, elmt[0]):
            print('Show Found!\n')
            print("Found MKV: %s\nMatched Template: %s\nLocation Template: %s\n" % (video, elmt[0], elmt[1]))

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

    episode_number = mkvs[0][show_wildcard] + mkvs[0][show_wildcard+1]
    print("Episode Number: %s\n" % episode_number)

    lulz = shows[show_index][1].replace('##', episode_number)
    print("Output Filename: %s" % lulz)

main()
