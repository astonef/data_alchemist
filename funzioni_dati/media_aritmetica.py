import pandas as pd
import os
from datetime import datetime

def calc_media_e_salva(numeri: str, path: str) -> str:
    now = datetime.now()
    data_file = now.strftime("%y%m%d")      # es: 250725
    data_str = now.strftime("%d/%m/%y")      # es: 25/07/25
    ora_str = now.strftime("%H:%M")          # es: 13:42

    serie = pd.Series([float(n.strip()) for n in numeri.split(",")])
    media = serie.mean()

    output = (
        f"# Risultato\n\n"
        f"**Data**: {data_str}\n"
        f"**Ora di stampa**: {ora_str}\n\n"
        f"**Numeri**: {numeri}\n"
        f"**Media**: {media:.2f}\n"
    )

    os.makedirs(path, exist_ok=True)
    filename = f"media_output_{data_file}.md"
    filepath = os.path.join(path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)

    return filepath  # ✅ ora torna il percorso del file
