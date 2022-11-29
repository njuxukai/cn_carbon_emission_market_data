# -*- coding: utf-8 -*-


import logging 
import logging.config 
import ce_db.db_utils as db_utils
import ce_basic.functions as ce_functions

all_modules = ['ce_exchanges/bea.py',
                   'ce_exchanges/szea.py',
                   'ce_exchanges/tjea.py',
                   'ce_exchanges/hbea.py',
                   'ce_exchanges/fjea.py',
                   'ce_exchanges/gdea.py',
                   'ce_exchanges/shea.py',
                   'ce_exchanges/cqea.py',]

def scrap_and_save_recent_market_data():
    md_list = []
    for m in all_modules:
        scrap_function = ce_functions.get_scrap_function(m)
        if scrap_function is not None:
            mds = scrap_function()
            logging.info('[%s]fetch [%d] md', m, len(mds))
            md_list.extend(mds)
    flag = db_utils.save_market_data(md_list)
    if flag:
        logging.info('save md,[%d] entries' % len(md_list))

def query_market_data(begin_date, end_date):
    return db_utils.query_market_data(begin_date, end_date)

def get_db_stat_lines():
    return db_utils.get_db_stat_lines()


def _scrap_demo():
    #before scape
    lines = get_db_stat_lines()
    for line in lines:
        print(line)

    #fetch
    scrap_and_save_recent_market_data()
    
    #stat
    lines = get_db_stat_lines()
    for line in lines:
        print(line)

def _query_demo():
    begin_date = '2022-08-01'
    end_date = '2022-08-15'
    mds = query_market_data(begin_date, end_date)
    print('query begin[%s],end[%s],record_count:[%d]' % (begin_date, end_date, len(mds)))

    begin_date = '2022-08-15'
    end_date = '2022-08-31'
    mds = query_market_data(begin_date, end_date)
    print('query begin[%s],end[%s],record_count:[%d]' % (begin_date, end_date, len(mds)))

if __name__ == '__main__':
    logging.config.fileConfig('log/ce_logger.conf')
    
    _scrap_demo()
    #_query_demo()

    

    

    
