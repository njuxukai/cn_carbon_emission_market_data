# -*- coding: utf-8 -*-
import logging
import requests
import httpx
import importlib.util
import inspect


def get_html(url, encoding='utf-8'):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding=encoding
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException as e:
        logging.error('error occurred while scraping %s', url, exc_info=True)
    return None



def get_html_with_headers(url, headers, encoding='utf-8'):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response.encoding=encoding
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException as e:
        logging.error('error occurred while scraping %s', url, exc_info=True)
    return None

def get_html_using_httpx(url, encoding='utf-8'):
    try:
        response = httpx.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except requests.RequestException as e:
        logging.error('error occurred while scraping %s', url, exc_info=True)
    return None


def get_scrap_function(fpath, func_name = 'scrap_current_mds'):
    spec = importlib.util.spec_from_file_location('', fpath)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    for f in foo.__dict__.values():
        if inspect.isfunction(f) and f.__name__ == func_name:
            return f
    return None
