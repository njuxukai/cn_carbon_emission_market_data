# 1 需求

从北京等碳排放权交易所（详见下方数据源）每日日终（上海T+1日日初）爬取各交易所碳排放行情数据，行情数据格式如下：

 

| 字段名（中文） | 备注                                                         |
| -------------- | ------------------------------------------------------------ |
| 日期           | YYYY-MM-DD                                                   |
| 交易品种       | BEA:北京碳排放权；  SHEA:上海碳排放权;  SZA:深圳碳排放权;  TJEA22:天津2022年碳排放权;...  CQEA-1:重庆碳排放权;  HBEA:湖北碳排放权;  GDEA:广东碳排放权;  FJEA:福建碳排放权; |
| 交易方式       | 竞价交易；                                                   |
| 成交均价       | 单位：元                                                     |
| 收盘价         | 单位：元（深圳、广东、福建有收盘价则取收盘价，无收盘价则取成交均价） |
| 成交量         | 单位：吨                                                     |
| 成交额         | 单位：元                                                     |
| 交易所         | BEA:北京绿色交易所;  SHEA:上海环境能源交易所;  SZA:深圳碳排放权交易所;  TJEA:天津碳排放权交易所;  CQEA:重庆碳排放权交易中心;  HBEA:湖北碳排放权;  GDEA:广州碳排放权交易所;  FJEA:海峡股权交易中心环境能源交易平台; |

 

数据源

BEA：https://www.bjets.com.cn/article/jyxx/
SZA:http://www.cerx.cn/dailynewsCN/index.htm
TJEA:http://www.chinatcx.com.cn/list/13.html
HBEA:https://www.hbets.cn/list/13.html
FJEA:https://carbon.hxee.com.cn/
GDEA:https://www.cnemission.com/

SHEA：https://www.cneeex.com/cneeex/daytrade/detail?SiteID=122#;

# 2 解决方案

为各交易所开发一个python模块

比较特殊的是：

1 重庆 从https://www.cqggzy.com/xxhz/014006/carbonEmission.html抓取最近的行情页面URL后分别抓取

2 上海  直接模仿ajax，调用http post接口查询数据

3 天津  网站使用html2，抓取网页需用httpx

## 2.1依赖包

pip install requests

pip install beautifulsoup4

pip install httpx[html2]

## 2.2 ce_md_crawler.py函数列表

**scrap_and_save_recent_market_data()**

使用所有市场模块抓取最近的行情数据,并保存本地文件数据库



**query_market_data(begin_date, end_date)**

从本地文件数据库中读取行情



**get_db_stat_lines()**

打印本地文件数据库中行情统计信息

交易所+记录数+最早日期+最晚日期









