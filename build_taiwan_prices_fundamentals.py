import time
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from typing import List

# ========= 使用者設定 =========

# 要抓哪些台股代碼（自行修改／加減）
STOCK_LIST: List[str] = [
    "2330",  # 台積電
    "2317",  # 鴻海
    "2454",  # 聯發科
]

# 期間（含）
START_DATE = "2019-01-01"
END_DATE   = "2024-12-31"

# 輸出檔名（給你的 Notebook 使用）
OUTPUT_CSV = "prices_fundamentals_taiwan.csv"

# ========= yfinance 抓取函數 =========

def fetch_stock_data_yf(stock_no: str, start: str, end: str) -> pd.DataFrame:
    """
    使用 yfinance 抓取台股資料 (OHLCV)
    """
    ticker = f"{stock_no}.TW"
    print(f"Fetching {ticker} from yfinance...")
    
    try:
        # yfinance 的 end date 是 exclusive，所以如果想要包含 12/31，通常要 +1 天
        # 但這裡簡單處理，直接用傳入的日期
        df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
        
        if df.empty:
            print(f"[WARN] {ticker} yfinance returned empty data.")
            return pd.DataFrame()

        # yfinance 回傳的 index 是 DatetimeIndex，columns 是 MultiIndex (Price, Ticker)
        # 我們需要把它攤平
        df = df.reset_index()
        
        # 處理 MultiIndex columns (如果有)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
            
        # 重新命名欄位以符合後續處理需求
        # yfinance columns: Date, Open, High, Low, Close, Adj Close, Volume
        df = df.rename(columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        })
        
        # 轉換日期格式為字串 YYYY-MM-DD
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df["stock_id"] = stock_no
        
        # 確保數值型態
        cols = ["open", "high", "low", "close", "volume"]
        for c in cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
        
        # 選擇需要的欄位
        final_cols = ["date", "stock_id", "open", "high", "low", "close", "volume"]
        # 確保所有欄位都存在
        for c in final_cols:
            if c not in df.columns:
                df[c] = np.nan
                
        return df[final_cols]
        
    except Exception as e:
        print(f"[ERROR] Fetching {ticker} failed: {e}")
        return pd.DataFrame()

# ========= 主流程：組成 prices_fundamentals.csv =========

def build_prices_fundamentals():
    all_df = []

    for stock_no in STOCK_LIST:
        print(f"=== 處理股票 {stock_no} ===")
        
        # 改用 yfinance 抓取
        df = fetch_stock_data_yf(stock_no, START_DATE, END_DATE)
        
        if df.empty:
            print(f"[WARN] {stock_no} 沒有資料，略過。")
            continue

        # yfinance 免費版不提供歷史 PE/PB，這裡先填 NaN
        # 如果需要 PE/PB，可能需要另外爬蟲或計算 (PE = Close / EPS)
        df["pe"] = np.nan
        df["pb"] = np.nan
        
        # 先保留欄位：roe / gross_margin（目前 NaN）
        df["roe"] = np.nan
        df["gross_margin"] = np.nan

        all_df.append(df)

    if not all_df:
        print("沒有任何股票資料，請檢查 STOCK_LIST / 日期範圍。")
        return

    full = pd.concat(all_df, ignore_index=True)
    # 按股票、日期排序
    full = full.sort_values(["stock_id", "date"]).reset_index(drop=True)

    # 確保欄位順序符合 Notebook 需求
    cols = [
        "date",
        "stock_id",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "pe",
        "pb",
        "roe",
        "gross_margin",
    ]
    full = full[cols]

    full.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    print(f"已輸出 {len(full)} 筆資料到 {OUTPUT_CSV}")


if __name__ == "__main__":
    build_prices_fundamentals()
