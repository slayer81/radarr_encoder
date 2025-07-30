import psycopg2
from psycopg2.extras import DictCursor
import os
from processing.system_tools import logger

SPACER = ' '
MARKER = '#'

########################################################################################################################
def get_file_info_by_date(data: str):
    try:
        conn = psycopg2.connect(
            host="192.168.0.99",
            dbname="radarr_main",
            user=os.getenv('PG_username', 'Username not found'),
            password=os.getenv('PG_password', 'Password not found')
        )
        cur = conn.cursor(cursor_factory=DictCursor)

        query = '''
            SELECT DISTINCT s."Path" AS "Root", m."Path" AS "Parent", mf."RelativePath" AS "Filename", mf."Size" AS "Size"
            FROM public."History" h
            JOIN public."Movies" m ON h."MovieId" = m."Id"
            JOIN public."MovieFiles" mf ON m."MovieFileId" = mf."Id"
            JOIN public."RootFolders" s ON POSITION(s."Path" IN m."Path") = 1
            WHERE h."Date"::date = %s;
        '''

        cur.execute(query, (data,))
        results = cur.fetchall()
        cur.close()
        conn.close()

        """  (get_file_info_by_date) Data structure: 
        [
            {'Root': '/Volumes/Primary/Video/Movies/', 'Parent': '/Volumes/Primary/Video/Movies/How.to.Train.Your.Dragon.(2025)', 'Filename': 'How.to.Train.Your.Dragon.2025.mkv', 'Size': 6887867179},
            {'Root': '/Volumes/Primary/Video/Movies/', 'Parent': '/Volumes/Primary/Video/Movies/M3GAN.2.0.(2025)', 'Filename': 'M3GAN.2.0.2025.mkv', 'Size': 6653375076}
        ] """

        # Convert each row to a plain dict. Return dict
        response = [dict(row) for row in results]
        return response
    except Exception as e:
        return f'(get_file_info_by_date) Database error:\t {str(e)}'
########################################################################################################################


########################################################################################################################
########################################################################################################################


########################################################################################################################
########################################################################################################################
