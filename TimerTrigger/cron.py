import datetime
import logging
import os
import urllib.request

import azure.functions as func
from azure.storage.file import FileService

import ssl
import time


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Starting download')

    ssl._create_default_https_context = ssl._create_unverified_context
    response = urllib.request.urlopen("https://www.7-zip.org/a/7za920.zip")
    data = response.read()

    file_service = FileService(connection_string=os.environ['storageglobalsnips_STORAGE'])
    file_service.create_share('myshare')

    final_name = "7zip_%s.zip" % str(int(round(time.time() * 1000)))
    file_service.create_file_from_bytes('myshare', None, final_name, data)
    file_url = file_service.make_file_url('myshare', None, final_name)

    logging.info('New file name = %s and URL = %s at %s' % (final_name, file_url, utc_timestamp))