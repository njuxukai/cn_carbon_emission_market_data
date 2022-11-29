# -*- coding: utf-8 -*-


import logging 
import logging.config 
import ce_db.db_utils as db_utils
import ce_basic.functions as ce_functions


def test():
    #北京
    #modules = ['ce_exchanges/bea.py',]
    #深圳
    #modules = ['ce_exchanges/szea.py',]
    #天津
    #modules = ['ce_exchanges/tjea.py',]
    #湖北
    #modules = ['ce_exchanges/hbea.py',]
    #福建
    #modules = ['ce_exchanges/fjea.py',]
    #广东
    #modules = ['ce_exchanges/gdea.py',]
    #上海
    #modules = ['ce_exchanges/shea.py',]
    #重庆
    modules = ['ce_exchanges/cqea.py',]
    for fpath in modules:
        f = ce_functions.get_scrap_function(fpath)
        if f is not None:
            mds = f()
            for md in mds:
                print(md)


if __name__ == '__main__':
    logging.config.fileConfig('log/ce_logger.conf')

    test()

    

    
