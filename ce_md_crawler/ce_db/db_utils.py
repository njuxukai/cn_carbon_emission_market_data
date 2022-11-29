# -*- coding: utf-8 -*-

import ce_db.db_sqls  as db_sqls
import ce_basic.market_data as market_data
import os
import sqlite3
import logging


def get_target_db_fpath():
    return 'ce_db/db.sqlite3'

def create_db_file_if_not_exist():
    target_fpath = get_target_db_fpath()
    if  os.path.exists(target_fpath)  and os.path.isfile(target_fpath):
        return target_fpath
    conn = sqlite3.connect(target_fpath)
    cur = conn.cursor()
    cur.execute(db_sqls.create_md_table_sql)
    conn.commit()
    conn.close()
    return target_fpath


def query_market_data(begin_date, end_date):
    target_fpath = get_target_db_fpath()
    if  not os.path.exists(target_fpath) or not os.path.isfile(target_fpath):
        logging.error('%s数据库文件错误', target_fpath)
        return []
    md_list = []
    conn = sqlite3.connect(target_fpath)
    cur = conn.cursor()
    cur.execute(db_sqls.select_md_sql_fmt % (begin_date, end_date))
    rows = cur.fetchall()
    for row in rows:
        md = market_data.MarketData        
        md.trade_date = row[0]
        md.exchange_code = row[1]
        md.instrument_code = row[2]
        md.trade_type = row[3]
        md.avg_price = float(row[4])
        md.close = float(row[5])
        md.trade_volume = int(row[6])
        md.trade_amount = float(row[7])
        md.exchange_name = row[8]
        md_list.append(md)
    conn.commit()
    conn.close()
    return md_list



def save_market_data(market_data_list):
    target_fpath = create_db_file_if_not_exist()
    md_tuples = []
    for md in market_data_list:
        value_tuple = ( md.trade_date ,
                        md.exchange_code ,
                        md.instrument_code ,
                        md.trade_type ,
                        md.avg_price ,
                        md.close ,
                        md.trade_volume,
                        md.trade_amount ,
                        md.exchange_name)
        md_tuples.append(value_tuple)

    conn = sqlite3.connect(target_fpath)
    cur = conn.cursor()
    cur.executemany(db_sqls.insert_or_replace_md_sql, md_tuples)
    conn.commit()
    conn.close()
    return True

def get_db_stat_lines():
    target_fpath = get_target_db_fpath()
    if  not os.path.exists(target_fpath) or not os.path.isfile(target_fpath):
        logging.error('%s数据库文件错误', target_fpath)
        return []
    lines = []
    conn = sqlite3.connect(target_fpath)
    cur = conn.cursor()
    cur.execute(db_sqls.stat_sql)
    rows = cur.fetchall()
    for row in rows:
        line = 'exchange=%s,md_count=%s,min_trade_date=%s,max_trade_date=%s' % (row[0],row[1],row[2],row[3])
        lines.append(line)
    conn.commit()
    conn.close()
    return lines
