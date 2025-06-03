import pandas as pd

df = pd.read_csv("sal-lima.csv")
df.columns = df.columns.str.strip()  # elimina espacios
print(df.columns)  # inspeccioná esto

# Asegurate de usar los nombres correctos según lo que imprima
latitudes = df['lat']  # o 'latitude', etc.
