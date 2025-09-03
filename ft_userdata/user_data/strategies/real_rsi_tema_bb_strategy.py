from freqtrade.strategy import IStrategy, IntParameter
import talib.abstract as ta
import numpy as np
from pandas import DataFrame
from technical import qtpylib


class RealRSIThemeBBStrategy(IStrategy):
    INTERFACE_VERSION = 3
    can_short: bool = False

    timeframe = "5m"
    startup_candle_count: int = 200
    process_only_new_candles = True

    # ROI dan stoploss
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04,
    }
    stoploss = -0.10
    trailing_stop = False

    # Parameter untuk Hyperopt
    buy_rsi = IntParameter(1, 50, default=30, space="buy", optimize=True, load=True)
    sell_rsi = IntParameter(50, 100, default=70, space="sell", optimize=True, load=True)

    # Konfigurasi plot
    plot_config = {
        "main_plot": {
            "tema": {},
            "sar": {"color": "white"},
        },
        "subplots": {
            "MACD": {
                "macd": {"color": "blue"},
                "macdsignal": {"color": "orange"},
            },
            "RSI": {
                "rsi": {"color": "red"},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe)
        dataframe["tema"] = ta.TEMA(dataframe, timeperiod=9)
        dataframe["sar"] = ta.SAR(dataframe)

        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]

        dataframe["volume_mean_slow"] = dataframe["volume"].rolling(window=30).mean()
        dataframe["volume_mean_fast"] = dataframe["volume"].rolling(window=5).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.buy_rsi.value)) &
                (dataframe["tema"] <= dataframe["bb_middleband"]) &
                (dataframe["tema"] > dataframe["tema"].shift(1)) &
                (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], self.sell_rsi.value)) &
                (dataframe["tema"] > dataframe["bb_middleband"]) &
                (dataframe["tema"] < dataframe["tema"].shift(1)) &
                (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1
        return dataframe

