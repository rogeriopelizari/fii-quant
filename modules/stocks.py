import requests
from registry.stock_map import STOCK_MAP
from core.extractor import deep_extract
from config import STOCK_BASE_URL

def fetch_stock(stock_id):

    url = STOCK_BASE_URL.format(stock_id)

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    print("URL:", url)
    print("STATUS:", r.status_code)

    # ❌ bloqueia qualquer coisa que não seja 200
    if r.status_code != 200:
        print(f"⚠ ignorando stock_id inválido: {stock_id}")
        return None

    # ❌ protege JSON quebrado
    try:
        return r.json()
    except Exception:
        print("⚠ resposta não JSON:", r.text[:200])
        return None


def process_stock(stock_id):

    data = fetch_stock(stock_id)

    if not data:
        return None

    dy   = deep_extract(data, ["dividend_yield"])
    pl   = deep_extract(data, ["p_l"])
    pvp  = deep_extract(data, ["p_vp"])
    roe  = deep_extract(data, ["roe"])
    roic = deep_extract(data, ["roic"])

    return {
        "type": "STOCK",
        "id": stock_id,
        "name": STOCK_MAP.get(stock_id, "UNKNOWN"),

        "dy_avg": sum(dy) / len(dy) if dy else 0,
        "dy_trend": (dy[-1] - dy[0]) if len(dy) > 1 else 0,

        "pvp_avg": sum(pvp) / len(pvp) if pvp else 0,
        "pvp_trend": (pvp[-1] - pvp[0]) if len(pvp) > 1 else 0,

        # Não existem para ações, mas mantêm compatibilidade com o DataFrame
        "liq_avg": 0,
        "vac_avg": 0,
        "equity_trend": 0,

        # Indicadores específicos das ações
        "pl_avg": sum(pl) / len(pl) if pl else 0,
        "roe_avg": sum(roe) / len(roe) if roe else 0,
        "roic_avg": sum(roic) / len(roic) if roic else 0,
    }