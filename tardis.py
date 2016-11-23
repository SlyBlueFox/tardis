# Torrented Anime Renaming Download Induced Sorter
import csv
import os
import string
import logging
import shutil
import sys
import ConfigParser

# Creates default config file
def createConfig(name):
    config = ConfigParser.ConfigParser()
    config.add_section('General')
    config.set('General', 'script path', os.path.dirname(os.path.realpath(__file__))+'/')
    config.set('General', 'source path', '/mnt/vol1/downloads/transmission/complete/anime/')
    config.set('General', 'destination path', '/mnt/vol1/Video/Anime/')
    config.set('General', 'list file', 'animelist.csv')
    config.set('General', 'log file', 'doctor.log')

    with open(name, 'wb') as config_file:
        config.write(config_file)


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
    shutil.move(src, dst)
    logging.info("MOVED SUCCESSFULLY\n")


def main():

    # Checks if config file exists, if not then creates one
    cfg_file = os.path.dirname(os.path.realpath(__file__))+"/settings.cfg"
    if not os.path.exists(cfg_file):
        createConfig(cfg_file)
    
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)

    # Logger config
    logging.basicConfig(filename=config._sections['General']['script path']+config._sections['General']['log file'], 
                        level=logging.INFO,
                        format='%(asctime)s - %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info("--- STARTING SCAN ---\n")

    # Reads csv into array for processing
    try:
        shows = list(csv.reader(open(config._sections['General']['script path']+config._sections['General']['list file'])))
    except (OSError, IOError) as e:
        logging.critical('--- CRITICAL ERROR --- ' + str(e) + '\n')
        sys.exit(1)
    shows = filter(None, shows)

    # Scan directory for mkv files and load into array
    mkvs = []
    for scanned_file in os.listdir(config._sections['General']['source path']):
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

            source_path = config._sections['General']['source path'] + elmt
            destination_path = config._sections['General']['destination path'] + shows[show_index][1].replace('##', episode_number)
            move_mkv(source_path, destination_path)
            import_count += 1

    logging.info("Imported %d episodes\n" % import_count)
    logging.info("--- SCAN COMPLETE ---\n\n")

main()
