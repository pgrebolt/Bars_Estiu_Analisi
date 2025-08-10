import pandas as pd

# Llegir dades
df = pd.read_csv('Inscripcions_2025.csv')

# Extreiem DNI. El posem en majúscules
dni = df['DNI'].str.upper()

# Treiem els espais en blanc
dni = dni.str.replace(' ', '', regex=False)

# Duplicats
duplicated = dni[dni.duplicated()]

# Llistem els duplicats
print(duplicated)
print("Hi ha ", len(duplicated), " duplicats")

# Gent que ha posat malament la data de naixement
naixement = pd.to_datetime(df['Data de naixement'], format='%d/%m/%Y')
df_canalla = df[naixement > pd.Timestamp('2005-01-01')] # naixements que no compleixen el requisit +21
print(df_canalla)

