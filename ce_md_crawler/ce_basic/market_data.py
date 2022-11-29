

TRADE_TYPE_AUCTION = '竞价交易'
TRADE_TYPE_CONTRACT = '协议交易'

class MarketData(object):
    def __init__(self):
        self.trade_date = ''
        self.instrument_code = ''
        self.trade_type = ''
        self.avg_price = 0.0
        self.close = 0.0
        self.trade_volume = 0
        self.trade_amount = 0.0
        self.exchange_code = ''
        self.exchange_name = ''

    def __str__(self):
        return ('trade_date=%s,instrument_code=%s,trade_type=%s,avg_price=%.2f,close=%.2f,'
                'trade_volume=%d,trade_amount=%.2f,exchange_name=%s') % (self.trade_date, self.instrument_code,
                self.trade_type,self.avg_price, self.close, self.trade_volume, self.trade_amount, self.exchange_name)