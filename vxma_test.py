import time
import timeit
import warnings
from datetime import datetime as dt

import ccxt
import pandas as pd
from vxmapandasta import vxma as pa
from vxmatalib import vxma as ta

exchange = ccxt.binance()

# get OHLC info

ta_table = {
    "atr_p": 12,
    "atr_m": 1.6,
    "ema": 30,
    "linear": 30,
    "smooth": 30,
    "rsi": 14,
    "aol": 30,
    "pivot": 60,
}

warnings.filterwarnings("ignore")
pd.set_option("display.max_rows", None)


def fetchbars(symbol, timeframe, exchange):
    bars = 2000
    print(
        f"Benchmarking new bars for {symbol , timeframe , dt.now().isoformat()}"
    )
    try:
        bars = exchange.fetch_ohlcv(
            symbol, timeframe=timeframe, since=None, limit=bars
        )
    except Exception as e:
        print(e)
        time.sleep(2)
        bars = exchange.fetch_ohlcv(
            symbol, timeframe=timeframe, since=None, limit=bars
        )
    df = pd.DataFrame(
        bars[:-1],
        columns=["timestamp", "Open", "High", "Low", "Close", "Volume"],
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True).map(
        lambda x: x.tz_convert("Asia/Bangkok")
    )
    df = df.set_index("timestamp")
    return df


data = fetchbars("BTC/USDT", "1d", exchange)
# data = pd.read_csv("Bitcoin_1D_2009-2022.csv")
# data = data.set_index("Date")


def bot1():
    bot = ta(data, ta_table)
    data1 = bot.indicator()
    print(data1.tail(1))


def bot2():
    bot2 = pa(data, ta_table)
    data2 = bot2.indicator()
    print(data2.tail(1))


if __name__ == "__main__":
    t1 = timeit.timeit(stmt=bot1, number=1)
    t2 = timeit.timeit(stmt=bot2, number=1)
    print(f"ta-lib : {round(t1,2)}sec. ")
    print(f"pandas_ta : {round(t2,2)}sec.")
