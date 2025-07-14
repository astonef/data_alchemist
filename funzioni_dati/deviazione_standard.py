import pandas as pd
import os
import datetime as dt

def calc_std_e_salva():
    numeri = input("Numeri (separati da virgola): ")
    path = input("Cartella per salvare: ").strip()
    try:
        serie = pd.Series([float(n.strip()) for n in numeri.split(",")])
        std = serie.std()
        output = f"# Risultato\n\n**Numeri**: {numeri}\n\n**Deviazione standard**: {std:.2f}\n"

        os.makedirs(path, exist_ok=True)
        nome_file = f"std_{dt.datetime.now():%Y%m%d_%H%M%S}.md"
        filepath = os.path.join(path, nome_file)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"Salvato in: {filepath}")
    except Exception as e:
        print("Errore:", e)

calc_std_e_salva()
