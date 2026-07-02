import os
import pandas as pd
from modules.fii import process_fii
from modules.stocks import process_stock
from core.score import calculate_score

from registry.stock_map import STOCK_MAP
from registry.fii_map import FII_MAP

FII_IDS = [10, 24, 28, 48, 56, 85, 552, 697]
STOCK_IDS = [5, 18, 42, 44, 308]

def main():

    results = []

    for fid in FII_IDS:
        r = process_fii(fid)

        if r is None:
            continue

        r["score"] = calculate_score(r)
        results.append(r)

    for sid in STOCK_IDS:
        r = process_stock(sid)

        if r is None:
            continue

        r["score"] = calculate_score(r)
        results.append(r)

    df = pd.DataFrame(results)
    df = df.sort_values("score", ascending=False)

    os.makedirs("data", exist_ok=True)

    df = df.copy()

    # opcional: arredondar
    df = df.round(4)

    # salvar
    df.to_csv("data/screener.csv", index=False, sep=";", decimal=",", encoding="utf-8-sig")
    

    print(df)

if __name__ == "__main__":
    main()