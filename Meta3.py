import logging
import sys
import threading
import time
import schedule

from AutoMetabaseProject.Auto_Metabase_v2 import run_meta
from AutoMetabaseProject import constants as c

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL, stream=sys.stdout, format="%(asctime)s %(funcName)s:%(message)s")
    run_meta(c.NEW_DOWNLOAD_PATH, list_run_group=['fsr', 'nshopee'])
    schedule.every().day.at("09:00").do(run_meta, c.NEW_DOWNLOAD_PATH, list_run_group=['fsr', 'nshopee'])
    while True:
        schedule.run_pending()
        time.sleep(60)
