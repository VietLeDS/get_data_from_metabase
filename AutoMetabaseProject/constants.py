import pandas as pd

COL_META = ['code_name', 'group', 'file_name', 'link', 'export_folder', 'export_name']
DF_LINK = pd.read_csv(r'G:\My Drive\Ninjavan Project\Python code\Meta\AutoMetabaseProject\link_metabase.csv', low_memory=False, usecols=COL_META, index_col='code_name')
MAY_O_NHA = r'C:\Users\Le Hoang Viet\Downloads'
LAPTOP = r'C:\Users\Admin\Downloads'
MAY_CONG_TY = r'C:\Users\bakhi\Downloads'
NEW_DOWNLOAD_PATH = r'G:\My Drive\Ninjavan Data\Fleet\Bot data\Metabase Downloads'
TARGETED_PATH = r'G:\My Drive\Ninjavan Data\Fleet\Daily Task\Metabase auto code'