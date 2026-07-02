import requests
from registry.fii_map import FII_MAP
from core.extractor import deep_extract
from config import FII_BASE_URL


def fetch_fii(fii_id):
    url = FII_BASE_URL.format(fii_id)
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return r.json()


def process_fii(fii_id):

    data = fetch_fii(fii_id)

    dy = deep_extract(data, ["dividend_yield_last_12_months", "dividend_yield"])
    pvp = deep_extract(data, ["p_vp"])
    liq = deep_extract(data, ["daily_liquidity"])
    vac = deep_extract(data, ["occupancy_rate"])
    equity = deep_extract(data, ["equity_value"])

    return {
        "type": "FII",
        "id": fii_id,
        "name": FII_MAP.get(fii_id, "UNKNOWN"),

        "dy_avg": sum(dy)/len(dy) if dy else 0,
        "dy_trend": (dy[-1] - dy[0]) if len(dy) > 1 else 0,

        "pvp_avg": sum(pvp)/len(pvp) if pvp else 0,
        "pvp_trend": (pvp[-1] - pvp[0]) if len(pvp) > 1 else 0,   # ✅ FALTAVA ISSO

        "liq_avg": sum(liq)/len(liq) if liq else 0,
        "vac_avg": sum(vac)/len(vac) if vac else 0,

        "equity_trend": (equity[-1] - equity[0]) if len(equity) > 1 else 0
    }