# -*- coding: utf-8 -*-
import ce_basic.market_data as market_data
import ce_basic.functions as ce_functions
import requests
import logging
import requests
import json
import re
import datetime

URL = 'https://www.cneeex.com/cneeex/daytrade/detail?SiteID=122#;'
AJAX_URL = 'https://www.cneeex.com/cneeex/daytrade/selectData'

EXCHANGE_CODE = 'SHEA'
EXCHANGE_NAME = 'SHEA:上海环境能源交易所'
DEFAULT_INSTRUMENT_CODE = 'SHEA'
DEFAULT_TRADE_TYPE = market_data.TRADE_TYPE_AUCTION

logger = logging.getLogger()

http_headers = {
'Accept': '*/*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Connection': 'keep-alive',
'host': 'www.cneeex.com',
'Origin' :'https://www.cneeex.com',
'Referer': 'https://www.cneeex.com/cneeex/daytrade/detail?SiteID=122',
'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW 64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
}

def scrap_current_mds():
    now = datetime.datetime.now()
    pre = now - datetime.timedelta(days=15)
    months = set()
    months.add(now.strftime('%Y-%m'))
    months.add(pre.strftime('%Y-%m'))
    mds = []
    for month in months:
        mds.extend(batch_query_by_month(month))
    return mds

def batch_query_by_month(month):
    d = {}
    d['Date'] = month
    d['Type'] = 'MONTH'
    
    j = _get_ajax_result(AJAX_URL, d, http_headers)
    if j is  None:
        return []
    return _parse_json_result(j)



def _get_ajax_result(url, data, headers):
    try:
        r =requests.post(AJAX_URL, data=data, headers=headers)
        if r.status_code == 200:
            return r.text
        else:
            return None
    except Exception as e:
        logger.error(e)
    return None

def _parse_json_result(raw_s):
    md_data_list = json.loads(raw_s)
    mds = []
    for md_data in md_data_list:
        mds.append(_parse_md_data(md_data))
    mds = [md for md in mds if md.instrument_code == DEFAULT_INSTRUMENT_CODE]
    return mds



def _parse_md_data(md_data):
    md = market_data.MarketData()
    md.exchange_code = EXCHANGE_CODE
    md.exchange_name = EXCHANGE_NAME
    md.trade_type = DEFAULT_TRADE_TYPE
    md.trade_date = _convert_trade_date_data(md_data[0])
    md.instrument_code = _convert_instrument_code_data(md_data[1])
    md.trade_volume = _convert_trade_volume_data(md_data[2])
    md.trade_amount = _convert_trade_amount_data(md_data[3])
    md.avg_price = 0.0 if md.trade_volume == 0 else round(md.trade_amount / md.trade_volume, 4)
    md.close = md.avg_price
    return md

def _parse_header_node(s):
    headers = []
    for n in s.find_all('li'):
        headers.append(n.text)
    return headers


def _parse_data_node(s):
    line = []
    for n in s.find_all('li'):
        line.append(n.text)
    return line



def _convert_trade_date_data(data):
    return data

def _convert_trade_volume_data(data):
    if data == '-':
        return 0
    return int(data.replace(',', ''))

def _convert_price_data(data):
    return   float(data)

def _convert_trade_amount_data(data):
    if data == '-':
        return 0.0
    return float(data.replace(',', ''))

def _convert_instrument_code_data(data):
    return data