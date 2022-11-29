# -*- coding: utf-8 -*-
import ce_basic.market_data as market_data
import ce_basic.functions as ce_functions
import requests
import logging
from bs4 import BeautifulSoup
import re

URL = 'http://www.chinatcx.com.cn/list/13.html?page=1'
EXCHANGE_CODE = 'TJEA'
EXCHANGE_NAME = 'TJEA:天津碳排放权交易所'
DEFAULT_INSTRUMENT_CODE = 'TJEA'


logger = logging.getLogger()


def scrap_current_mds():
    text = ce_functions.get_html_using_httpx(URL)
    
    lines = []
    soup = BeautifulSoup(text, 'lxml')
    x = soup.select('.transData tr')
    for index, node in enumerate(x):
        line = _parse_data_node(node)
        lines.append(line)
   
    mds = _parse_market_data_list(lines)
    return mds


def _parse_header_node(s):
    headers = []
    for n in s.find_all('td'):
        headers.append(n.text)
    return headers


def _parse_data_node(s):
    line = []
    for n in s.find_all('td'):
        line.append(n.text)
    return line

def _parse_market_data_list(lines):
    md_list = []
    for line in lines:
        flag, mds = _parse_market_data(line)
        if flag:
            md_list.extend(mds)
    for md in md_list:
        md.exchange_code = EXCHANGE_CODE
        md.exchange_name = EXCHANGE_NAME
    return md_list

def _parse_market_data(line):
    if len(line) < 8:
        return False, []
    md_auction = market_data.MarketData()
    md_contract = market_data.MarketData()
    md_auction.trade_type = market_data.TRADE_TYPE_AUCTION
    md_contract.trade_type = market_data.TRADE_TYPE_CONTRACT
    md_auction.trade_date = _convert_trade_date_data(line[0])
    md_auction.instrument_code = _convert_instrument_code_data(line[1])
    md_contract.trade_date = md_auction.trade_date
    md_contract.instrument_code = md_auction.instrument_code
    md_auction.trade_volume = _convert_trade_volume_data(line[2])
    md_contract.trade_volume = _convert_trade_volume_data(line[3])
    md_auction.trade_amount = _convert_trade_amount_data(line[4])
    md_contract.trade_amount = _convert_trade_amount_data(line[5])
    md_auction.avg_price = _convert_price_data(line[6])
    md_contract.avg_price = _convert_price_data(line[7])
    return True, [md_auction, md_contract]

def _convert_trade_date_data(data):
    return data

def _convert_trade_volume_data(data):
    if data == '-':
        return 0
    return int(data.replace(',', ''))

def _convert_price_data(data):
    if data == '-':
        return 0.0
    return   float(data.replace(',', ''))

def _convert_trade_amount_data(data):
    if data == '-':
        return 0.0
    return float(data.replace(',', ''))

def _convert_instrument_code_data(data):
    return data