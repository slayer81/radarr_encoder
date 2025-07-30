import os
import datetime as dt
from datetime import datetime
import sys
import shutil
import subprocess
from humanize import precisedelta as hpd
from processing.conversion_utils import human_but_smaller as hbs
from processing.system_tools import get_bin_path
from pathlib import Path

SPACER = ' '
MARKER = '#'


########################################################################################################################
def create_notification_content(file_stub: str, log_name: str, total_count: int, failed_list: list, body_str: str):
    msg_title = f'({dt.datetime.now().strftime("%H:%M")})\t{file_stub.replace("_", " ")}'
    message_content_list = [msg_title]
    msg_body = ''

    if len(failed_list) > 0:
        msg_subtitle = f'FAILED to encode {len(failed_list)} of {total_count} files'
        msg_body += f'Filenames in log: "{log_name}"\n'
    else:
        msg_subtitle = f'All {total_count} files were encoded successfully'

    msg_body += f'{body_str}'
    message_content_list.extend([msg_subtitle, body_str])

    if len(message_content_list) == 3:
        message_content = '|'.join(message_content_list)
    else:
        message_content = f' Automator Task Completed With Errors | Check Log File For More Detail | {log_name} '
    return message_content
########################################################################################################################


########################################################################################################################
def encoding_failed(logfile_path: str, message: str):
    logger(logfile_path, 'failure', f'{SPACER * 3}')
    logger(logfile_path, 'failure', f'{SPACER * 6} *** ENCODING FAILED ***')
    logger(logfile_path, 'failure', f'{SPACER * 3} *** RESPONSE:\t {message}')
    logger(logfile_path, 'failure', f'{SPACER * 6} *** CLEANING UP ***')
    logger(logfile_path, 'failure', f'{SPACER * 3}')
########################################################################################################################


########################################################################################################################
def premature_exit(logfile_path: str, data, reason, start_time: datetime, file_stub: str):
    logger(logfile_path, 'failure', f' *** EXITING ***')
    logger(logfile_path, 'failure', f' *** {reason.upper()} ***')
    logger(logfile_path, 'info', f'{MARKER * 102}')

    execution_time = hpd(dt.datetime.now() - start_time)
    msg_title = f'({dt.datetime.now().strftime("%H:%M")})\t{file_stub.replace("_", " ")}'
    # message_content = f' Automator Task Completed | {msg_title} | Nothing found to encode\nTotal runtime: {CU.human_but_smaller(execution_time)} '
    message_content = f' Automator Task Completed | {msg_title} | {reason}\nTotal runtime: {hbs(execution_time)} '
    logger(logfile_path, 'info', f'Display Notification data:\t"{message_content[20:]}"...')
    logger(logfile_path, 'info', '{:<62} {:>16}'.format(f'Execution completed. Total runtime:', hbs(execution_time)))
    logger(logfile_path, 'none', f'{MARKER * 140}\n')
    print(message_content)

    # Make sure to flush stdout to ensure immediate output
    sys.stdout.flush()
    exit(0)
########################################################################################################################


########################################################################################################################
def get_fs_objects(source_dir: str):
    print('{:<28}{:<60}'.format('Action:', 'Fetching source filesystem objects'))
    objects = []
    try:
        objects = os.listdir(source_dir)
        objects = [o for o in objects if not o.endswith('.DS_Store')]
    except Exception as e:
        print(f'Error reading source filesystem:\t {str(e)}')

    if not objects:
        # This is the end
        print('{:<28}"{:<60}"'.format('No file system objects fetched   ...Exiting...', ''))
    return objects
########################################################################################################################


########################################################################################################################
def logger(logfile_path: str, status: str, data: str):
    status_list = ['none', 'info', 'success', 'warning', 'failure']
    if status.lower() not in status_list:
        status_key = 'UNKNOWN'
    else:
        status_key = status.upper()

    # Write to logfile
    with open(logfile_path, "a") as log_pipe:
        log_timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        if status_key == 'NONE':
            log_data = data
        else:
            log_data = '{:23} || {:^7} || {:<80}\n'.format(log_timestamp, status_key, data)
        log_pipe.write(f'{log_data}')
########################################################################################################################


########################################################################################################################
def initial_setup(logfile_path: str, profile: str):
    logger(logfile_path, 'none', f'\n\n{MARKER * 155}\n')
    logger(logfile_path, 'info', f'Executing script:\t {__file__}')
    logger(logfile_path, 'none', f'{MARKER * 155}\n')

    # Verify local environment dependencies are ready
    ###############################################################################################
    logger(logfile_path, 'info', 'Checking environment dependencies ....')

    # Load path to active shell profile
    logger(logfile_path, 'info', f'Using shell profile:\t {profile}')

    # Get filesystem path of ffmpeg
    ffmpeg_path = str(get_bin_path('ffmpeg'))
    logger(logfile_path, 'info', '{:>20}\t {:<}'.format('Path to ffmpeg binary:', ffmpeg_path))

    # Get filesystem path of ffprobe
    ffprobe_path = str(get_bin_path('ffprobe'))
    logger(logfile_path, 'info', '{:>20}\t {:<}'.format('Path to ffprobe binary:', ffprobe_path))
    ###############################################################################################
    # Local environment checks completed

    logger(logfile_path, 'none', f'{MARKER * 155}\n')
    return {'ffmpeg_bin': ffmpeg_path, 'ffprobe_bin': ffprobe_path}
########################################################################################################################

########################################################################################################################
########################################################################################################################
########################################################################################################################
