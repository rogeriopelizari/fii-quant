import numpy as np

def calculate_score(m):

    return (
        m.get("dy_avg", 0) * 0.5 +
        m.get("dy_trend", 0) * 0.3 +
        -m.get("pvp_avg", 0) * 5 +
        -m.get("pvp_trend", 0) * 2 +   # opcional
        -m.get("vac_avg", 0) * 0.2 +
        (m.get("liq_avg", 0) / 1e6) * 0.1 +
        (m.get("equity_trend", 0) / 1e9) * 0.2
    )