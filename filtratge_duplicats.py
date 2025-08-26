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
print("Hi ha ", len(duplicated), " duplicats a la inscripció")

# Gent que ha posat malament la data de naixement
naixement = pd.to_datetime(df['Data de naixement'], format='%d/%m/%Y')
df_canalla = df[naixement > pd.Timestamp('2005-01-01')] # naixements que no compleixen el requisit +21
print("Dates de naixements incorrectes (menors de 21 anys): ", len(df_canalla))
print(df_canalla[['Cognoms', 'Nom', 'Data de naixement']])

#### Duplicats de la llista de correus de confirmació
from collections import Counter

# Llegim la llista de correus
with open('../2025/correus_confirmacio.txt', 'r') as f:
    correus = f.readlines()
correus = [x.strip() for x in correus] # treiem els salts de línia
correus = [x.lower() for x in correus] # posem en minúscules
correus = [x.replace(' ', '') for x in correus] # treiem els espais en blanc
correus = [x for x in correus if x != ''] # treiem els buits
correus_counts = Counter(correus) # comptem quants n'hi ha de cada
correus_duplicats = [[correu, repeticions] for correu, repeticions in correus_counts.items() if repeticions > 1] # filtrem els que estan repetits
print(correus_duplicats)
print("Hi ha ", len(correus_duplicats), " correus duplicats")



