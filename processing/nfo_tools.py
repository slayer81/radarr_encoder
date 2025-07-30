import re
import os
from pathlib import Path
from tools import logger

SPACER = ' '
MARKER = '#'



########################################################################################################################
def find_nfo(logfile_path: str, root_path: str):
    root = Path(root_path)

    if root.is_dir():
        nfo_files = list(root.glob("*.nfo"))
        if len(nfo_files) == 1:
            nfo_path = Path(nfo_files[0])
            if nfo_path.exists():
                return nfo_path
        elif len(nfo_files) > 1:
            print(f"{root_path} contains {len(nfo_files)} .nfo files")
            logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
            logger(logfile_path, 'failure', f"{SPACER * 3} *** TOO MANY NFO FILES FOUND ***")
            logger(logfile_path, 'failure', f"{SPACER * 3} *** EXPECTED 1, FOUND {len(nfo_files)} ***")
            logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
            return len(nfo_files)
        elif not nfo_files:
            print(f"No nfo file found at {root_path}")
            logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
            logger(logfile_path, 'failure', f'{SPACER * 3} *** NO NFO FILE FOUND ***')
            logger(logfile_path, 'failure', f'{SPACER * 3} *** SKIPPING ***')
            logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
            return None
        else:
            return None
########################################################################################################################


########################################################################################################################
def extract_nfo_metadata(file_path):
    field_dict = {
        'year': '  <year>',
        'title': '  <title>',
        'studio': '  <studio>'
    }

    # Initialize a dictionary to store the extracted data
    extracted_data = {key: None for key in field_dict}

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    for field_name, field_tag in field_dict.items():
                        if field_tag in line:
                            raw_match = line.rstrip()
                            match = re.sub(r'<[^>]+>', '', raw_match).strip()
                            if match:
                                extracted_data[field_name] = match
            return extracted_data
        except Exception as e:
            return f'(extract_nfo_data) Error message: {str(e)}'
    else:
        return None
########################################################################################################################


########################################################################################################################
def no_nfo_file(logfile_path: str):
    logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
    logger(logfile_path, 'failure', f'{SPACER * 3} *** NO FOUND NFO FILE! ***')
    logger(logfile_path, 'failure', f'{SPACER * 3} *** Skipping ***')
    logger(logfile_path, 'failure', f'{SPACER * 3} {MARKER * 45}')
########################################################################################################################


########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
