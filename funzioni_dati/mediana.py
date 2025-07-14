import pandas as pd
import os
import datetime as dt

def calc_mediana_e_salva():
    numeri = input("Numeri (separati da virgola): ")
    path = input("Cartella per salvare: ").strip()
    try:
        serie = pd.Series([float(n.strip()) for n in numeri.split(",")])
        mediana = serie.median()
        output = f"# Risultato\n\n**Numeri**: {numeri}\n\n**Mediana**: {mediana:.2f}\n"

        os.makedirs(path, exist_ok=True)
        nome_file = f"mediana_{dt.datetime.now():%Y%m%d_%H%M%S}.md"
        filepath = os.path.join(path, nome_file)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output)

        print(f"Salvato in: {filepath}")
    except Exception as e:
        print("Errore:", e)

calc_mediana_e_salva()
