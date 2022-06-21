import datetime
import calendar
import os
import time
from logging import critical
import numpy as np
import pandas

from . import constants as c


class RunRequirements:
    def __init__(self, download_path, list_run=None, list_not_run=None, list_run_group=None, replace=True, *args, **kwargs):
        if list_run is None:
            list_run = []
        if list_not_run is None:
            list_not_run = []
        if list_run_group is None:
            list_run_group = []

        self.download_path = download_path
        self.replace = replace

        if list_run:
            self.list_run = list_run
        elif list_not_run:
            self.list_run = [_ for _ in c.DF_LINK.index if _ not in list_not_run]
        elif list_run_group:
            self.list_run = [_ for _ in c.DF_LINK.index if c.DF_LINK.loc[_]['group'] in list_run_group]
        else:
            self.list_run = list(c.DF_LINK.index)

        self.today = datetime.date.today()
        self.yesterday = self.today + datetime.timedelta(-1)
        self.n_2 = self.yesterday + datetime.timedelta(-1)
        self.n_3 = self.yesterday + datetime.timedelta(-2)
        self.n_5 = self.yesterday + datetime.timedelta(-4)
        self.n_plus_1 = self.yesterday + datetime.timedelta(1)

        for _ in self.list_run:
            setattr(self, _, False)
        self.check_status()
        self.all_done = False
        self.check_done()
        critical(f'Done __init__, list run = {self.list_run}')

    def check_done(self):
        self.all_done = all(getattr(self, _) for _ in self.list_run)

    @staticmethod
    def _get_date_modified(filepath):
        date_modified = os.path.getmtime(filepath)
        # Convert seconds since epoch to readable timestamp
        return time.strftime('%Y-%m-%d', time.localtime(date_modified))

    @staticmethod
    def _get_begin_date_str(end_date):
        year = end_date.year
        month = end_date.month
        return f'{year}-{str(month).zfill(2)}-01'

    @staticmethod
    def _get_start_month_str(end_date):
        year = end_date.year
        month = end_date.month
        return f'{year}-{str(month).zfill(2)}'

    @staticmethod
    def _get_end_month_str(end_date):
        year = end_date.year
        month = end_date.month
        return f'{year}-{str(month).zfill(2)}-{str(calendar.monthrange(year, month)[1])}'

    @staticmethod
    def str_date(date):
        return datetime.datetime.strftime(date, '%Y-%m-%d')

    def _get_done_list(self):
        return [
            f
            for f in os.listdir(c.TARGETED_PATH)
        ]

    def _get_success_list(self):
        nrl = self._get_done_list()
        return [
            _
            for _ in self.list_run
            if f'{self._get_export_name(_)}.csv' in nrl
        ]

    # Check thêm cả những code chị Linh chạy tay
    def check_status(self):
        nrl = self._get_success_list()
        # critical(f'Check status, success list = {nrl}')
        for _ in nrl:
            if not getattr(self, _):
                setattr(self, _, True)
                print(f'{_} done')
        self.check_done()

    def get_link(self, code_name):
        group = c.DF_LINK.loc[code_name]['group']
        if code_name == 'vn-rts-kpi-salary-calculation':
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.today)).replace('end_date_',
                                                                                                    RunRequirements._get_end_month_str(self.today))
        elif code_name == 'vn-rts-kpi-order-details':
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.yesterday)).replace('end_date_',
                                                                                                    RunRequirements.str_date(self.yesterday))
        elif code_name == 'fm njbiz':
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.n_2)).replace('end_date_',
                                                                                                    RunRequirements.str_date(self.n_2))
        elif group in ['fm', 'fsr', 'nshopee', 'njbiz']:
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.yesterday)).replace('end_date_',
                                                                                                    RunRequirements.str_date(self.yesterday))
        elif group == 'lm':
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.n_3)).replace('end_date_',
                                                                                                    RunRequirements.str_date(self.n_3))
        elif group in ['wh', 'wh_nshopee']:
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.n_2)).replace('end_date_',
                                                                                                    RunRequirements.str_date(self.n_2))
        elif group == 'dailylm':
            return c.DF_LINK.loc[code_name]['link'].replace('start_date_', RunRequirements._get_begin_date_str(self.yesterday)).replace('end_date_',
                                                                                                  RunRequirements.str_date(self.yesterday))

    def _get_export_name(self, code_name):
        group = c.DF_LINK.loc[code_name]['group']
        if code_name == 'vn-rts-kpi-salary-calculation':
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.today).replace('-', '_')}-{RunRequirements._get_end_month_str(self.today)[-2:]}"
        elif code_name == 'vn-rts-kpi-order-details':
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.yesterday).replace('-', '_')}-{RunRequirements.str_date(self.yesterday)[-2:]}"
        elif code_name == 'fm njbiz':
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.n_2).replace('-', '_')}-{RunRequirements.str_date(self.n_2)[-2:]}"
        elif group in ['fm', 'fsr', 'nshopee', 'njbiz']:
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.yesterday).replace('-', '_')}-{RunRequirements.str_date(self.yesterday)[-2:]}"
        elif group == 'lm':
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.n_3).replace('-', '_')}-{RunRequirements.str_date(self.n_3)[-2:]}"
        elif group in ['wh', 'wh_nshopee']:
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.n_2).replace('-', '_')}-{RunRequirements.str_date(self.n_2)[-2:]}"
        elif group == 'dailylm':
            return f"{c.DF_LINK.loc[code_name]['export_name']}_{RunRequirements._get_begin_date_str(self.yesterday).replace('-', '_')}-{RunRequirements.str_date(self.yesterday)[-2:]}"

    @staticmethod
    def _get_export_folder(code_name):
        return c.DF_LINK.loc[code_name]['export_folder']

    def _get_old_file_name(self, code_name):
        group = c.DF_LINK.loc[code_name]['group']
        if code_name == 'vn-rts-kpi-salary-calculation':
            check = RunRequirements._get_begin_date_str(self.today).replace('-', '_')
        elif code_name == 'vn-rts-kpi-order-details':
            check = RunRequirements._get_begin_date_str(self.today).replace('-', '_')
        elif code_name == 'fm njbiz':
            check = RunRequirements._get_begin_date_str(self.n_2).replace('-', '_')
        elif group in ['fm', 'fsr', 'nshopee', 'njbiz']:
            check = RunRequirements._get_begin_date_str(self.yesterday).replace('-', '_')
        elif group == 'lm':
            check = RunRequirements._get_begin_date_str(self.n_3).replace('-', '_')
        elif group in ['wh', 'wh_nshopee']:
            check = RunRequirements._get_begin_date_str(self.n_2).replace('-', '_')
        elif group == 'dailylm':
            check = RunRequirements._get_begin_date_str(self.yesterday).replace('-', '_')

        list_file = [f for f in os.listdir(c.DF_LINK.loc[code_name]['export_folder'])
                     if check in f and 'crdownload' not in f]
        if not isinstance(list_file, list) or list_file == []:
            critical(code_name)
            return ""
        if len(list_file) == 1:
            return list_file[0]

    def check_download(self):
        for code_name in self.list_run:
            if getattr(self, code_name):
                continue

            # Fix lỗi 2 code WH vừa Shopee vừa Non Shopee
            # Bằng cách chạy riêng, set default download folder của chrome là folder khác

            list_file = [f for f in os.listdir(self.download_path) if
                         c.DF_LINK.loc[code_name]['file_name'] in f and RunRequirements.str_date(self.today) in f and 'crdownload' not in f]

            if not list_file:
                continue

            list_file.sort(reverse=True)
            
            for _ in list_file:
                try:
                    df = pandas.read_csv(f'{self.download_path}/{_}', low_memory=False)
                except:
                    os.remove(f'{self.download_path}/{_}')
                    continue
                if '{' not in str(df.iloc[0:, 0]) and 'xception' not in str(df.iloc[0:, 0]):  # Kiểm tra cả cột sẽ chính xác hơn
                    df.to_csv(
                        f'{c.TARGETED_PATH}/{self._get_export_name(code_name)}.csv',
                        index=False)
                    # Tự động thay thế file trong folder chính
                    if RunRequirements._get_export_folder(code_name) is not np.nan and self.replace:
                        old_name = self._get_old_file_name(code_name)
                        df.to_csv(
                            f'{RunRequirements._get_export_folder(code_name)}/{self._get_export_name(code_name)}.csv',
                            index=False)
                        if old_name != "" and old_name is not None:
                            os.remove(
                                f'{RunRequirements._get_export_folder(code_name)}/{old_name}')
                    critical(f'Run {code_name} Success')
                    break
