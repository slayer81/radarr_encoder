import datetime as dt
from humanize import precisedelta as hpd
import os
from pathlib import Path
# import shutil
import pprint
import subprocess
import json
import sys
from db.query import get_file_info_by_date
from processing.conversion_utils import human_but_smaller
from processing.nfo_tools import extract_nfo_metadata, find_nfo
from processing.ff_utils import get_video_codec
from processing.encoder import reencode_video
from processing.system_tools import load_shell_environment, construct_encoder_fs_parts, get_bin_path, file_event
from processing.tools import logger, create_notification_content, encoding_failed, premature_exit, initial_setup
import logging
from config import MEDIA_PATH

profile = os.path.join(os.path.expanduser("~"), '.bash_profile')
load_shell_environment(profile)

########################################################################################################################
# Global variables
FILE_STUB = os.path.basename(__file__).replace('.py', '')
START_TIME = dt.datetime.now()
MARKER = '#'
SPACER = ' '
HOME_PATH = os.path.expanduser("~")

# TODAY_DATESTAMP = dt.date.today().strftime("%Y-%m-%d")
TODAY_DATESTAMP = '2025-07-16'
YESTERDAY_DATESTAMP = (dt.datetime.strptime(TODAY_DATESTAMP, "%Y-%m-%d").date() - dt.timedelta(days=1)).strftime("%Y-%m-%d")

# Define Trash Directory
TRASH_DIR = f'{HOME_PATH}/.Trash/'

# Logging Parameters
LOG_DATESTAMP = dt.date.today().strftime("%Y-%m-%d")
LOG_DIR = f'{HOME_PATH}/Logs/radarr_encoder/{FILE_STUB}'
LOG_NAME = f'{LOG_DATESTAMP}.log'
LOGFILE_FULL_PATH = os.path.join(LOG_DIR, LOG_NAME)

# Create "LOG_DIR" if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

TARGET_CODECS = ['h264', 'h.264', 'x264', 'x.264', 'vp9']
METADATA_CODECS = ['h265', 'h.265', 'x265', 'x.265', 'hevc']
pp = pprint.PrettyPrinter(indent=3)
# End Globals
########################################################################################################################


########################################################################################################################
def main():
    # logging.basicConfig(level=logging.INFO)
    # logging.info("Starting Radarr encoding job")

    bin_paths_dict = initial_setup(LOGFILE_FULL_PATH, profile)
    if not all(value is not None for value in bin_paths_dict.values()):
        premature_exit(bin_paths_dict, 'Required binary missing', START_TIME, FILE_STUB)


    movies = get_file_info_by_date(TODAY_DATESTAMP)
    for movie_path in movies:
        logging.info(f"Processing: {movie_path}")
        nfo_data = extract_nfo_metadata(movie_path)
        codec = get_video_codec(movie_path)
        reencode_video(movie_path, codec, nfo_data)
########################################################################################################################


########################################################################################################################
if __name__ == '__main__':
    main()




"""
from db.query import get_recent_movies
from processing.nfo_parser import parse_nfo
from processing.ffprobe_util import get_video_codec
from processing.encoder import reencode_video
import logging
from config import MEDIA_PATH

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Radarr encoding job")

    movies = get_recent_movies()
    for movie_path in movies:
        logging.info(f"Processing: {movie_path}")
        nfo_data = parse_nfo(movie_path)
        codec = get_video_codec(movie_path)
        reencode_video(movie_path, codec, nfo_data)

if __name__ == "__main__":
    main()
"""
