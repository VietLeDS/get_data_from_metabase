import os, time, datetime

path = r'G:\My Drive\Ninjavan Data\Fleet\Bot data\Metabase Downloads'


def get_date_modified(filepath):
    date_modified = os.path.getmtime(filepath)
    # Convert seconds since epoch to readable timestamp
    return time.strftime('%Y-%m-%d', time.localtime(date_modified))


today_str = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
ls = [_ for _ in os.listdir(path) if '.csv' in _ and '2022' in _ and 'T' in _ and 'Z' in _]
for _ in ls:
    os.remove(f'{path}/{_}')
