import pandas as pd
from datetime import datetime

def calc_media(numeri: str) -> str:
    now = datetime.now()
    data_str = now.strftime("%d/%m/%y")
    ora_str = now.strftime("%H:%M")

    serie = pd.Series([float(n.strip()) for n in numeri.split(",")])
    media = serie.mean()

    output = (
        f"Data: {data_str}\n"
        f"Ora di stampa: {ora_str}\n"
        f"Numeri: {numeri}\n"
        f"Media: {media:.2f}"
    )

    return output
