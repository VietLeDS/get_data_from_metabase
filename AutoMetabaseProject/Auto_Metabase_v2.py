import logging
import sys
import threading
import pandas
import datetime

from .GUI_helpers import *
from .Main_helpers import *


def loop(f):
    def inner(*args, **kwarg):
        now = datetime.datetime.now()
        while not locals()['kwarg']['r_status_'].all_done and now.hour >= 9 and now.hour <= 22:
            f(*args, **kwarg)
            now = datetime.datetime.now()
    return inner


def clear_chrome(chrome):
    now = datetime.datetime.now()
    for _ in range(5):
        try:
            chrome.restore().maximize()
            chrome.NewTabButton.click_input(button='left')
            chrome.NewTab0Item.click_input(button='left')
            chrome.NewTab0Item.click_input(button='right')
            chrome.CloseOtherTab.click_input()
            break
        except:
            continue


@loop
def thread_run_meta(r_status_=None, chrome=None):
    clear_chrome(chrome)
    list_run = r_status_.list_run
    for _ in list_run:
        if not getattr(r_status_, _):
            critical(f'Run {_}')
            run_metabase_once(r_status_, chrome, r_status_.get_link(_))

@loop
def thread_check_status(r_status_=None):
    r_status_.check_status()
    time.sleep(60)


def run_multi_metabase(r_status_=None):
    chrome = open_chrome()
    chrome.restore().maximize()

    thread = {
        "thread_0": threading.Thread(target=thread_run_meta,
                                     kwargs={'r_status_': r_status_, 'chrome': chrome}),
        "thread_1": threading.Thread(target=thread_check_status,
                                     kwargs={'r_status_': r_status_}),
    }

    for _ in range(2):
        thread[f'thread_{_}'].start()
    for _ in range(2):
        thread[f'thread_{_}'].join()

    critical('Finish')
    # reset(chrome)
    chrome.minimize()


def run_meta(*args, **kwargs):
    r_status = RunRequirements(*args, **kwargs)
    run_multi_metabase(r_status)
