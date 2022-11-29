# -*- coding: utf-8 -*-
import ce_basic.market_data as market_data
import ce_basic.functions as ce_functions
import requests
import logging
from bs4 import BeautifulSoup
import re

URL = 'https://ets.cnemission.com/carbon/portalIndex/markethistory'
EXCHANGE_CODE = 'GDEA'
EXCHANGE_NAME = 'GDEA:广州碳排放权交易所'
DEFAULT_INSTRUMENT_CODE = 'GDEA'
DEFAULT_TRADE_TYPE = market_data.TRADE_TYPE_AUCTION

logger = logging.getLogger()


def scrap_current_mds():
    text = ce_functions.get_html(URL)
    
    headers = []
    lines = []
    soup = BeautifulSoup(text, 'lxml')
    x = soup.select('.lh_baseTable tr')
    for index, node in enumerate(x):
        if index == 0:
            headers = _parse_header_node(node)
        else:
            line = _parse_data_node(node)
            lines.append(line)

    
    mds = _parse_market_data_list(headers, lines)
    return mds




def _parse_header_node(s):
    headers = []
    for n in s.find_all('td'):
        headers.append(n.text.strip())
    return headers


def _parse_data_node(s):
    line = []
    for n in s.find_all('td'):
        line.append(n.text.strip())
    return line

def _parse_market_data_list(header, lines):
    trade_date_index = -1
    trade_amount_index = -1
    trade_volume_index = -1
    instrument_code_index = -1
    for index, h in enumerate(header):
        if h.startswith('日期'):
            trade_date_index = index
        elif h.startswith('成交数量'):
            trade_volume_index = index
        elif h.startswith('成交金额'):
            trade_amount_index = index
        elif h.startswith('品种'):
            instrument_code_index = index
    if trade_date_index == -1:
        logger.error('日期列无法定位')
    if trade_amount_index == -1:
        logger.error('成交金额列无法定位')
    if trade_volume_index == -1:
        logger.error('成交数量列无法定位')
    if instrument_code_index == -1:
        logger.error('品种列无法定位')
    mds = []
    for line in lines:
        md = market_data.MarketData()
        md.exchange_code = EXCHANGE_CODE
        md.exchange_name = EXCHANGE_NAME
        md.trade_type = DEFAULT_TRADE_TYPE
        for index, data in enumerate(line):
            if index ==  trade_date_index:
                md.trade_date = _convert_trade_date_data(data)
            if index == trade_volume_index:
                md.trade_volume = _convert_trade_volume_data(data)
            if index == trade_amount_index:
                md.trade_amount = _convert_trade_amount_data(data)
            if index == instrument_code_index:
                md.instrument_code = _convert_instrument_code_data(data)
        md.avg_price = 0.0 if md.trade_volume == 0 else  round(md.trade_amount / md.trade_volume,4)
        md.close = md.avg_price
        mds.append(md)
    return mds


def _convert_trade_date_data(data):
    return '%s-%s-%s' % (data[0:4], data[4:6], data[6:])

def _convert_trade_volume_data(data):
    return int(data)

def _convert_price_data(data):
    return   float(data)

def _convert_trade_amount_data(data):
    return float(data)

def _convert_instrument_code_data(data):
    return data