#然后正式开始
import ccxt
import json

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
markets=exchange.load_markets()
print(markets)

#获取盘口信息,盘口的信息其实是个字典，所以我们可以用使用字典的方法来调出盘口的某类信息
symbol="BTC/USDT"
orderbook=exchange.fetch_order_book(symbol)
print("bids",orderbook["bids"])
print("asks",orderbook["asks"])

#获取price ticker数据
if (exchange.has["fetchTicker"]):
    print("ticker",exchange.fetch_ticker(symbol))

#获取1日k线数据
kline=exchange.fetch_ohlcv(symbol,"1d")
print(kline)

#获取公共交易数据
public_trade=exchange.fetch_trades(symbol)
print(public_trade)
