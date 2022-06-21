import logging
import sys
import threading
import time
import numpy as np

from AutoMetabaseProject.Auto_Metabase_v2 import RunRequirements
from AutoMetabaseProject import constants as c


def meta_check(r_status):
    r_status.check_download()
    r_status.check_status()
    print("Don't success list")
    for _ in r_status.list_run:
        if not getattr(r_status, _):
            print(_)

    # Check file in folder
    print('\n\n100% Success list')
    fleet = 0
    for _ in r_status.list_run:
        path = RunRequirements._get_export_folder(_)
        if path is not np.nan:
            file_name = f'{r_status._get_export_name(_)}.csv'
            ls = [f for f in os.listdir(path) if RunRequirements._get_start_month_str(r_status.today).replace('-', '_') in f]
            if file_name in ls:
                print(file_name)
                fleet += 1
    print(f"Progress Fleet: {fleet}/{len([f for f in r_status.list_run if c.DF_LINK.loc[f]['group'] not in ('wh', 'wh_nshopee')])}")

    print('\n\n99% Success list')
    # Đã chạy thành công nhưng không có trong folder chính
    for _ in r_status.list_run:
        path = RunRequirements._get_export_folder(_)
        if path is not np.nan:
            file_name = f'{r_status._get_export_name(_)}.csv'
            ls = [f for f in os.listdir(path) if RunRequirements._get_start_month_str(r_status.today).replace('-', '_') in f]
            if file_name not in ls and getattr(r_status, _):
                print(file_name)

    # Check overall
    print('\n\nOverall')
    for _ in r_status.list_run:
        path = RunRequirements._get_export_folder(_)
        if path is not np.nan:
            ls = [f for f in os.listdir(path) if RunRequirements._get_start_month_str(r_status.today).replace('-', '_') in f]
            print(ls)


if __name__ == '__main__':
    import os
    import datetime

    with open(r'H:\My Drive\Viet_Project\PythonProject\runHistory.csv', 'a') as f0:
        now = datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d_%H_%M_%S")
        f0.write(f'{now},{os.getpid()},{__file__}\n')
        print(f'{now},{os.getpid()},{__file__}\n')

    logging.basicConfig(level=logging.CRITICAL, stream=sys.stdout, format="%(asctime)s %(funcName)s:%(message)s")
    r_status_ = RunRequirements(c.NEW_DOWNLOAD_PATH, list_run_group=['fsr', 'fm', 'lm', 'wh', 'wh_nshopee', 'nshopee', 'njbiz'])
    meta_check(r_status_)
