import os
import datetime as dt
import shutil
import subprocess
from pathlib import Path
from tools import logger

SPACER = ' '
MARKER = '#'


########################################################################################################################
def file_event(logfile_path: str, source: str, destination: str, action: str):
    import shutil
    try:
        shutil.move(source, destination)
        logger(logfile_path, 'success', f'{SPACER * 3} File {action}d successfully')
        return 0
    except Exception as e:
        logger(logfile_path, 'failure', f'{SPACER * 3} *** FAILED TO {action.upper()} FILE ***')
        logger(logfile_path, 'failure', f'{SPACER * 3} *** RESPONSE:\t {str(e)}')
        # return str(e)
        return 1
########################################################################################################################


########################################################################################################################
# profile = os.path.join(os.path.expanduser("~"), '.bash_profile')
# def load_shell_environment(profile_path=profile):
def load_shell_environment(profile: str):
    # Use subprocess to source the shell profile and print the environment variables
    # command = f"source {profile_path} && env"
    command = f"source {profile} && env"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
    for line in proc.stdout:
        (key, _, value) = line.decode("utf-8").partition("=")
        os.environ[key] = value.strip()
########################################################################################################################


########################################################################################################################
def construct_encoder_fs_parts(data):       # Construct encoder filesystem parts
    # Basic required keys
    required_keys = ['Filename', 'Parent']

    # Check for required keys
    for key in required_keys:
        if key not in data:
            raise KeyError(f"Missing required key: '{key}'")
        if not isinstance(data[key], str) or not data[key].strip():
            raise ValueError(f"Value for '{key}' must be a non-empty string")

    filename = data['Filename']
    parent = data['Parent']

    try:
        file_ext = Path(filename).suffix
        in_file_full_path = os.path.join(parent, filename)
        temp_file_name = f"{Path(in_file_full_path).stem}.TEMP{file_ext}"
        temp_file_full_path = os.path.join(parent, temp_file_name)
    except Exception as e:
        raise ValueError(f"Error constructing paths: {e}")

    # Return updated dictionary
    fs_data = {
        'file_ext': file_ext,
        'in_file_full_path': in_file_full_path,
        'temp_file_name': temp_file_name,
        'temp_file_full_path': temp_file_full_path
    }
    return fs_data
########################################################################################################################


########################################################################################################################
def get_bin_path(binary: str):
    command = f'which {binary}'    # Get filesystem path

    bin_path = subprocess.run(
        command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ).stdout.decode('utf-8').strip()
    return bin_path
########################################################################################################################

