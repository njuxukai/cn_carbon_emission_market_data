# -*- coding: utf-8 -*-
import ce_basic.market_data as market_data
import ce_basic.functions as ce_functions
import requests
import logging
from bs4 import BeautifulSoup
import re




#子查询获得页面链接列表
AJAX_QRY_URL = 'https://www.cqggzy.com/interface/rest/esinteligentsearch/getFullTextDataNew'

#另一个主页
QRY_URL = 'https://www.cqggzy.com/xxhz/014006/carbonEmission.html'
BASE_URL = 'https://www.cqggzy.com/'


EXCHANGE_CODE = 'CQEA'
EXCHANGE_NAME = 'CQEA:重庆碳排放权交易中心'
DEFAULT_INSTRUMENT_CODE = 'CQEA'
DEFAULT_TRADE_TYPE = market_data.TRADE_TYPE_AUCTION

logger = logging.getLogger()

MOCK_HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}

def scrap_current_mds():
    md_list = []
    hrefs = get_recent_page_urls()
    for href in hrefs:
        flag, mds = scrap_mds_from_single_url(BASE_URL, href)
        if flag:
            md_list.extend(mds)
    return md_list

def scrap_mds_from_single_url(url, href):
    url = '%s%s' % (url, href)
    logger.info('解析重庆行情网页%s', url)
    t = ce_functions.get_html_with_headers(url, MOCK_HEADERS)
    soup = BeautifulSoup(t, 'lxml')
    x = soup.select('table tbody tr')
    lines = []
    for idx, node in enumerate(x):
        if idx <= 1:
            continue
        line = _parse_data_node(node)
        lines.append(line)
    md_list = []
    for line in lines:
        flag, mds =  _parse_market_data_list(line)
        if flag:
            md_list.extend(mds)
    return True, md_list


def get_recent_page_urls():
    hrefs = set()
    
    t =  ce_functions.get_html_with_headers(QRY_URL, MOCK_HEADERS)
    soup = BeautifulSoup(t, 'lxml')
    x = soup.select('.clearfix a')
    for index, node in enumerate(x):
        if node.text.find('成交信息') >= 0 and node.text.find('碳排') >= 0 and 'href' in node.attrs:
            hrefs.add(node.attrs['href'])
    return hrefs





def _parse_data_node(s):
    line = []
    for n in s.find_all('td'):
        line.append(n.text.strip())
    return line

def _parse_market_data_list(line):
    if len(line) != 11:
        return False, []
    md_auction = market_data.MarketData()
    #定价申报
    md_contract = market_data.MarketData()
    md_auction.exchange_code = EXCHANGE_CODE
    md_auction.exchange_name = EXCHANGE_NAME
    md_auction.trade_type = market_data.TRADE_TYPE_AUCTION
    md_contract.exchange_code = EXCHANGE_CODE
    md_contract.exchange_name = EXCHANGE_NAME
    md_contract.trade_type = market_data.TRADE_TYPE_CONTRACT

    #parse data
    md_auction.trade_date = _convert_trade_date_data(line[0])
    md_auction.instrument_code = _convert_instrument_code_data(line[1])
    md_auction.trade_volume = _convert_trade_volume_data(line[9])
    md_auction.trade_amount = _convert_trade_amount_data(line[10])

    md_contract.trade_date = md_auction.trade_date
    md_contract.instrument_code = md_auction.instrument_code
    md_contract.trade_volume = _convert_trade_volume_data(line[7])
    md_contract.trade_amount = _convert_trade_amount_data(line[8])

    md_auction.avg_price = 0.0 if md_auction.trade_volume == 0 else  round(md_auction.trade_amount / md_auction.trade_volume,4)
    md_auction.close = md_auction.avg_price
    md_contract.avg_price = 0.0 if md_contract.trade_volume == 0 else  round(md_contract.trade_amount / md_contract.trade_volume,4)
    md_contract.close = md_contract.avg_price
    return True, [md_auction, md_contract]



def _convert_trade_date_data(data):
    nodes = data.split('/')
    year = int(nodes[0])
    month = int(nodes[1])
    day = int(nodes[2])
    return  '%d-%02d-%02d' % (year, month, day)

def _convert_trade_volume_data(data):
    if data == '-':
        return 0
    return int(data)

def _convert_price_data(data):
    return   float(data)

def _convert_trade_amount_data(data):
    if data == '-':
        return 0.0
    return float(data) * 10000

def _convert_instrument_code_data(data):
    return data