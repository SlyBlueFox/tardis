# Torrented Anime Renaming Download Induced Sorter
import csv
import os
import string
import logging


# Compare text of 2 strings ignoring punctuation whitespace and numbers
def compare(s1, s2):
        remove = string.punctuation + string.whitespace + string.digits
        return s1.translate(None, remove) == s2.translate(None, remove)


# Scans for found video in provided list of known shows
def find_show(video, array):
    for i, elmt in enumerate(array):
        if compare(video, elmt[0]):
            logging.info('Show Found!')
            logging.info("Found MKV: %s" % video)
            logging.info("Matched Template: %s" % elmt[0])
            logging.info("Location Template: %s" % elmt[1])
            return i


# Scans found show template for location of '##' wildcard
def find_wildcard(templates, show_number):
    return templates[show_number][0].index('##')


def move_mkv(src, dst):
    #os.renames(src,dst)
    logging.info("Source: %s"% src)
    logging.info("Destination: %s" % dst)
    logging.info("MOVED SUCCESSFULLY\n")


def main():
    # Logger config
    logging.basicConfig(filename='tardis.log', level=logging.DEBUG,
                        format='%(asctime)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("--- STARTING SCAN ---\n")

    # Reads csv into array for processing
    shows = list(csv.reader(open('test.csv')))

    # Loads default.cfg with source and destination paths
    config = [line.rstrip('\n') for line in open('default.cfg')]

    # Scan directory for mkv files and load into array
    mkvs = []
    for root, dirs, files in os.walk("."):
        for scanned_file in files:
            if scanned_file.endswith('.mkv'):
                mkvs.append(scanned_file)

    for i, elmt in enumerate(mkvs):
        logging.info("Processing Video: %s" % str(elmt))

        show_index = find_show(elmt, shows)
        if show_index is None:
            logging.info("NO MATCH FOUND\n")
        else:
            logging.info("Show Index: %d" % show_index)

            show_wildcard = find_wildcard(shows, show_index)
            logging.info("Wildcard Location: %d" % show_wildcard)

            episode_number = elmt[show_wildcard] + elmt[show_wildcard+1]
            logging.info("Episode Number: %s" % episode_number)

            source_path = config[0] + elmt
            destination_path = config[1] + shows[show_index][1].replace('##', episode_number)
            move_mkv(source_path, destination_path)
    logging.info("--- SCAN COMPLETE ---\n\n")

main()
