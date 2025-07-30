import subprocess
import os
from pathlib import Path
from tools import logger


SPACER = ' '
MARKER = '#'

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

    # Optionally, check if input file exists
    # if not os.path.isfile(in_file_full_path):
    #     raise FileNotFoundError(f"Input file not found: {in_file_full_path}")

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
def encode(logfile_path: str, bin_paths: dict, data: dict):
    # Assemble metadata components
    m_title = ''.join(['title="', data['title'], '"'])
    m_year = ''.join(['Year="', data['year'], '"'])
    m_studio = ''.join(['Studio="', data['studio'], '"'])

    # ffmpeg Parameters
    ff_params = [bin_paths['ffmpeg_bin'], '-hide_banner', '-i']
    video_params = ['-c:v', 'hevc_videotoolbox', '-tag:v', 'hvc1', '-b:v', '1500k', '-pix_fmt', 'yuv420p']
    audio_params = ['-c:a', 'aac_at', '-b:a', '192k']
    ff_switches = [*video_params, *audio_params, '-map_metadata', '-1', '-movflags', 'use_metadata_tags', '-metadata', m_title, '-metadata', m_studio, '-metadata', m_year]

    # ffmpeg command
    convert_cmd = [
        *ff_params,
        data['in_file_full_path'],
        *ff_switches,  # Correct: Unpacks the list into separate arguments
        data['temp_file_full_path']
    ]

    # Convert File
    logger(logfile_path, 'info', f'{SPACER * 3} Begin encoding of target file....')
    status_dict = {}
    try:
        subprocess.run(convert_cmd, shell=False, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Downgraded successfully
        logger(logfile_path, 'success', f'{SPACER * 3} File encoded successfully')

        # Compare before and after file sizes
        status_dict['temp_file_size'] = os.path.getsize(data['temp_file_full_path'])
        status_dict['percent_gained'] = CU.percentage_decrease(status_dict['temp_file_size'], data['Size'])

        if status_dict['percent_gained'] <= 0:
            # Poor result, so delete temp file
            logger(logfile_path, 'failure', f'{SPACER * 6} *** RESULTANT FILE SIZE NOT ACCEPTABLE *** PERCENTAGE GAINED: {status_dict["percent_gained"]}%')
            logger(logfile_path, 'info', f'{SPACER * 3} Deleting TEMP file')
            # move_result = SU.file_event(logfile_path, data['temp_file_full_path'], TRASH_DIR, 'delete')
            # status_dict['delete_temp_file'] = move_result
            status_dict['delete_temp_file'] = SU.file_event(logfile_path, data['temp_file_full_path'], TRASH_DIR, 'delete')

        # else:
        #     status_dict['after_size'] = after_size_raw

    except Exception as e:
        # Encoding process failed. Log event
        SU.encoding_failed(logfile_path, str(e))

        # Delete temp file
        logger(logfile_path, 'info', f'{SPACER * 3} Deleting TEMP file')

        try:
            shutil.move(data['temp_file_full_path'], TRASH_DIR)
            SU.file_event(logfile_path, data['temp_file_full_path'], TRASH_DIR, 'delete')
            logger(logfile_path, 'success', f'{SPACER * 3} Successfully deleted TEMP file')
        except Exception as e:
            logger(logfile_path, 'failure', f'{SPACER * 3} Failed to delete TEMP file. Please perform manually')
            logger(logfile_path, 'failure', f'{SPACER * 3} Response:\t {str(e)}')
########################################################################################################################

