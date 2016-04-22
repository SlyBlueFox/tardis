# Torrented Anime Renaming Download Induced Sorter
import csv
import os
import string
import logging
import shutil
import sys


# Compare text of 2 strings ignoring punctuation whitespace and numbers
def compare(s1, s2):
        remove = string.punctuation + string.whitespace + string.digits
        return s1.lower().translate(None, remove) == s2.lower().translate(None, remove)


# Scans for found video in provided list of known shows
def find_show(video, array):
    for i, elmt in enumerate(array):
        if compare(video, elmt[0]):
            logging.info('Show Found!')
            logging.debug("Matched Template: %s" % elmt[0])
            logging.debug("Location Template: %s" % elmt[1])
            return i


# Scans found show template for location of '##' wildcard
def find_wildcard(templates, show_number):
    return templates[show_number][0].index('##')


# Moves and Renames video file
def move_mkv(src, dst):
    logging.info("Source: %s"% src)
    logging.info("Destination: %s" % dst)
    (filepath, filename) = os.path.split(dst)
    try:
        os.makedirs(filepath)
        logging.info("Missing Directory has been created")
    except OSError:
        if not os.path.isdir(filepath):
            raise
        else:
            logging.debug("Directory already exists")
#    shutil.move(src, dst)
    logging.info("MOVED SUCCESSFULLY\n")


def main():
    # Config Vars
    src_cfg = "/mnt/vol1/downloads/transmission/complete/"
    dst_cfg = "/mnt/vol1/Video/Anime/"
    swd_cfg = "/mnt/vol1/scripts/tardis/"
    log_cfg = "doctor.log"
    lst_cfg = "animelist.csv"

    # Logger config
    logging.basicConfig(filename=swd_cfg+log_cfg, 
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("--- STARTING SCAN ---\n")

    # Reads csv into array for processing
    try:
        shows = list(csv.reader(open(swd_cfg+lst_cfg)))
    except (OSError, IOError) as e:
        logging.critical('--- CRITICAL ERROR --- ' + str(e) + '\n')
        sys.exit(1)
    shows = filter(None, shows)

    # Loads default.cfg with source and destination paths
    #config = [line.rstrip('\n') for line in open('default.cfg')]

    # Scan directory for mkv files and load into array
    mkvs = []
    for scanned_file in os.listdir(src_cfg):
        if scanned_file.endswith('.mkv'):
            mkvs.append(scanned_file)

    # Processes each found MKV file
    import_count = 0
    for i, elmt in enumerate(mkvs):
        logging.info("Processing Video: %s" % str(elmt))

        show_index = find_show(elmt, shows)

        # Only processes matched MKVs
        if show_index is None:
            logging.info("NO MATCH FOUND\n")
        else:
            logging.debug("Show Index: %d" % show_index)

            show_wildcard = find_wildcard(shows, show_index)
            logging.debug("Wildcard Location: %d" % show_wildcard)

            episode_number = elmt[show_wildcard] + elmt[show_wildcard+1]
            logging.debug("Episode Number: %s" % episode_number)

            source_path = src_cfg + elmt
            destination_path = dst_cfg + shows[show_index][1].replace('##', episode_number)
            move_mkv(source_path, destination_path)
            import_count += 1

#    if import_count > 0:
#        os.system("http://IPHERE:32400/library/sections/5/refresh?X-Plex-Token=TOKENHERE")
    logging.info("Imported %d episodes\n" % import_count)
    logging.info("--- SCAN COMPLETE ---\n\n")

main()
