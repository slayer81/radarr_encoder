import json
import subprocess
from processing.system_tools import logger


SPACER = ' '
MARKER = '#'

########################################################################################################################
def get_video_codec(path: str):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'json',
        path
    ]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        parsed = json.loads(result.stdout)
        return parsed['streams'][0]['codec_name']
    except Exception as e:
        print(f"Error reading codec for: {path}\n{e}")
        return None
########################################################################################################################


########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################

