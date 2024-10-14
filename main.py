#ccxt 用于访问加密货币交易所的API
import ccxt
import json
#pandas 用于数据处理和分析。
import pandas as pd

#time 用于时间相关的操作。
import time

#打印ccxt里面的所有交易所
print(ccxt.exchanges)

# 从配置文件加载 API 密钥
with open('config.json') as f:
    config = json.load(f)

#通过ccxt接入交易所（需要科学上网).这里因为不需要查看自己的数据，所以不需要输入接口密码。
#为了防止访问交易所的频率太过频繁，所以要增加访问速度限制
exchange=ccxt.binance({
    "apiKey": config['apiKey'],
    "secret": config['secret'],  # 注意这里是 'secret' 而不是 'secrete'
    "timeout":3000,
    "enableRateLimit":True,
})

#载入交易所的数据
#markets=exchange.load_markets()
#print(markets)

#获取盘口信息,盘口的信息其实是个字典，所以我们可以用使用字典的方法来调出盘口的某类信息
symbol="BTC/USDT"
#orderbook=exchange.fetch_order_book(symbol)
#print("bids",orderbook["bids"])
#print("asks",orderbook["asks"])

#获取price ticker数据
#if (exchange.has["fetchTicker"]):
#print("ticker",exchange.fetch_ticker(symbol))

#获取1日k线数据
kline=exchange.fetch_ohlcv(symbol,"1d")
#print(kline)

#获取公共交易数据
#public_trade=exchange.fetch_trades(symbol)
#print(public_trade)

# 先将获取的k线数据转成一个二维数组，它们的列名称是'time', 'open', 'high', 'low', 'close', 'vol'
kline_df = pd.DataFrame(kline, columns=['time', 'open', 'high', 'low', 'close', 'vol'])

#将 'time' 列从毫秒级时间戳转换为Pandas的datetime对象，并设置为kline_df的索引。
kline_df.index = pd.to_datetime(kline_df['time'], unit='ms')

# 使用 time.localtime() 将毫秒级时间戳转换为本地时间，
# 并将这些本地时间作为新列 'localminute' 添加到kline_df中。
kline_df.loc[:, "localminute"] = kline_df['time'].apply(lambda x: time.localtime(int(x/1000)))

# 将本地时间分钟转换为可读的字符串格式时间戳
kline_df.loc[:, 'timestamp'] = kline_df['localminute'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", x))

# 显示结果
print(kline_df)