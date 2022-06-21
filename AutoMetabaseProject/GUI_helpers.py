from logging import critical

import pyautogui
import pyperclip
from pywinauto import Application
import time


def open_chrome():
    # Chrome always open
    return Application(backend="uia").connect(title_re=r".*Google Chrome.*").window(title_re=".*Google Chrome.*")


def reset(chrome):
    try:
        chrome.ShowAll.click_input()
        critical('Reset success')
    except:
        pass


def run_metabase_once(r_status_, chrome, link):
    try:
        chrome.restore().maximize()
        chrome.NewTabButton.click_input()
        time.sleep(0.5)
        pyperclip.copy(link)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        timeout = 6 * 12
        for _ in range(timeout):
            try:
                chrome.DownloadIcon.click_input()
                chrome['.csv'].click_input()
                break
            except:
                continue
            break
    except Exception as e:
        critical(f'Error = {e}')


def run_metabase_once_not_download(chrome, link):
    try:
        chrome.NewTab.click_input()
        pyperclip.copy(link)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
    except Exception as e:
        critical(f'Error = {e}')
