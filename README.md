# Taiwan Equity Multi-Factor Research  
A complete, reproducible multi-factor model research pipeline for Taiwan equities.

This project implements a real quantitative research workflow including:

- Data pipeline for building Taiwan stock universe
- Factor construction (Value, Quality, Momentum, Risk)
- Cross-sectional normalization (Winsorize + Z-score)
- IC / IR computation for factor evaluation
- Portfolio construction and monthly rebalancing
- Backtesting engine (long-only equal-weight)
- Performance analytics & visualization

This repository is designed to be:
✔ Reproducible  
✔ Ready for interview portfolio  
✔ Easy to extend (add custom factors, new pipelines, new backtests)
