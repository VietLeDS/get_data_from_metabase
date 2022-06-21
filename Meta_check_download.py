import logging
import sys
import threading
import time
import numpy as np
import schedule

from AutoMetabaseProject.Auto_Metabase_v2 import RunRequirements, loop
from AutoMetabaseProject import constants as c

import os
import datetime


def meta_remove():
    path = r'G:\My Drive\Ninjavan Data\Fleet\Bot data\Metabase Downloads'
    ls = [_ for _ in os.listdir(path) if '.csv' in _ and 'T' in _ and 'Z' in _]
    for _ in ls:
        os.remove(f'{path}/{_}')


def check_download():
    r_status_ = RunRequirements(c.NEW_DOWNLOAD_PATH, list_run_group=['fsr', 'fm', 'lm', 'wh', 'wh_nshopee', 'nshopee', 'njbiz'])
    _check_download(r_status_=r_status_)


@loop
def _check_download(r_status_=None):
    r_status_.check_download()
    r_status_.check_status()


if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL, stream=sys.stdout, format="%(asctime)s %(funcName)s:%(message)s")
    meta_remove()
    check_download()
    schedule.every().day.at("09:00").do(check_download)
    schedule.every().day.at("23:05").do(meta_remove)
    while True:
        schedule.run_pending()
        time.sleep(60)
