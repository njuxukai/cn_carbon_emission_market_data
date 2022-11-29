create_md_table_sql = '''create table t_market_data
(trade_date char(10),
exchange_code varchar(6),
instrument_code varchar(20),
trade_type varchar(20),
avg_price decimal(12,4),
close decimal(12,4),
trade_volume int,
trade_amount decimal(19,2),
exchange_name varchar2(40),
primary key(trade_date, exchange_code, instrument_code, trade_type));'''

select_md_sql_fmt = """select 
trade_date,
exchange_code,
instrument_code,
trade_type,
avg_price,
close,
trade_volume,
trade_amount,
exchange_name
from t_market_data
where trade_date between '%s' and '%s' ;"""


insert_or_replace_md_sql = """insert or replace into t_market_data( 
trade_date,
exchange_code,
instrument_code,
trade_type,
avg_price,
close,
trade_volume,
trade_amount,
exchange_name)
values(?, ?, ?, ?, ?, ?, ?, ?, ?);"""


stat_sql = """select  
exchange_code,
count(1),
min(trade_date),
max(trade_date)
from t_market_data
group by exchange_code
order by 1;"""
