# Taiwan Equity Multi-Factor Research

A complete, reproducible multi-factor research pipeline for Taiwan equities.
This repository provides a minimal but functional workflow for building a **multi-factor stock selection model** tailored to the Taiwan market.

---

## 1. Project Overview

This project demonstrates a practical multi-factor modeling process, including:

* Construction of the Taiwan equity universe
* Integration of daily price data and fundamental indicators
* Factor engineering (Value, Quality, Momentum, Risk)
* Cross-sectional standardization (Winsorization + Z-score)
* Factor IC / IR evaluation for predictive effectiveness
* Simple equal-weight portfolio backtesting framework

The goal is to provide a clean, reproducible pipeline—similar to what is used in professional quant research environments—to evaluate and validate factor performance in the Taiwan stock market.

---

## 2. Repository Structure

```
Taiwan-equity-multi-factor-model
├─ data/                       
│   └─ (place raw data files here)
│
├─ build_taiwan_prices_fundamentals.py  
│   → Data pipeline script: downloads / merges price & fundamental data
│
├─ tej_multi_factor_model.ipynb
│   → Main research notebook: factor construction, IC/IR analysis, backtesting
│
└─ README.md
```

* `data/`
  Contains input datasets such as daily prices, fundamentals, market cap, etc.
  (Files not included in repo; users should place data manually.)

* `build_taiwan_prices_fundamentals.py`
  Automates data building and preprocessing.

* `tej_multi_factor_model.ipynb`
  Main notebook implementing the complete multi-factor workflow.

---

## 3. Workflow Summary

### Step 1. Build Dataset

Run the data pipeline to construct a merged dataset containing:

* OHLCV price series
* Basic fundamentals (EPS, ROE, PB, PE, etc.)
* Market cap & liquidity filters

```
python build_taiwan_prices_fundamentals.py
```

---

### Step 2. Factor Construction

Implements standard quant factors:

* **Value** (e.g., B/M, E/P)
* **Quality** (e.g., ROE, margin metrics)
* **Momentum** (e.g., 12-1 return)
* **Risk** (e.g., volatility, beta)

Each factor is cleaned and normalized using:

* Outlier removal (tail winsorize)
* Cross-sectional Z-score standardization

---

### Step 3. Factor Performance Evaluation

The notebook computes:

* **IC (Information Coefficient)**
* **IR (Information Ratio)**
* Monthly or daily factor predictive power
* Factor correlation & diversification benefit

---

### Step 4. Simple Portfolio Backtest

A transparent long-only backtesting framework:

* Rank stocks by composite multi-factor score
* Select top quantile
* Equal-weight allocation
* Cost-aware performance metrics

This is intentionally kept simple to highlight factor effectiveness without complex portfolio engineering.

---

## 4. Requirements

Recommended Python version: **3.9+**

Install dependencies:

```
pip install pandas numpy scipy statsmodels tqdm matplotlib seaborn
```

(Optional) For TEJ users, additional API clients may be required.

---

## 5. Notes

* This repository does **not** include raw TEJ or TWSE data.
  Place your data files under `data/` according to instructions in the code.
* This project is for educational and research purposes only.

---

## 6. Future Extensions (Optional)

If needed, the following modules can be added:

* `src/` folder for cleaner factor modules
* Orthogonalized factor models (Barra-style)
* Enhanced portfolio construction (risk parity, ERC, optimization)
* Live data ingest pipeline
* Alpha combination models (ML-based weighting)

These can be incorporated without modifying the current folder layout.
