import logging
import sys
import threading
import time
import pandas as pd
import numpy as np

from AutoMetabaseProject.Auto_Metabase_v2 import RunRequirements, run_multi_metabase
from AutoMetabaseProject import constants as c

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL, stream=sys.stdout, format="%(asctime)s %(funcName)s:%(message)s")
    start_date = '2022-05-01'
    end_date = datetime.date.strftime(datetime.date.today() + datetime.timedelta(-1), '%Y-%m-%d')
    special_path = r'C:\Users\vietl\Downloads'
    r_status = RunRequirements(special_path, start_date, end_date, list_run_group=['wh_nshopee'], replace=False)
    run_multi_metabase(r_status)
