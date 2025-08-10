''' Aquest programa llegeix les marques de temps i fa un gràfic d'inscripcions cumulatives '''

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Creem la figura
fig, ax = plt.subplots()

# Llegir dades
df = pd.read_csv('Inscripcions_2025.csv')
df.sort_values(by=['Marca de temps'], ascending=True, inplace=True)

# Convertir a datetime
timestamp = pd.to_datetime(df['Marca de temps'], format='%d/%m/%Y %H:%M:%S')

# Data d'inici
time0 = pd.Timestamp('2025-08-08 18:00:00')

# Nombre de gent que ja estaven inscrits abans de time0
n_previous = (timestamp < time0).sum()

# Reescrivim els temps dels qui es van inscriure abans de time0
timestamp = timestamp.where(timestamp >= time0, time0)

# Calculem el temps des de l'inici
diff_time = (timestamp - time0).dt.total_seconds()
diff_time = diff_time[timestamp != time0] # eliminem els qui es van inscriure abans de time0

# Número total de gent inscrita a cada moment (cada vegada 1 persona més)
inscrits = np.arange(n_previous, timestamp.shape[0], 1)

# Gràfic d'inscrits (%) cumulatiu en minuts
ax.plot(diff_time/3600, inscrits / inscrits[-1] *100, label='2025', color='red')

# Gràfic inset
axin = ax.inset_axes([0.45, 0.25, 0.45, 0.45])
axin.plot(diff_time/60, inscrits / inscrits[-1] *100, color='red')
axin.set_xlabel('Temps (min)')
axin.set_ylabel('Inscrits (%)')

# Igual, per dades del 2024
df24 = pd.read_csv('Inscripcions_2024.csv')
df24.sort_values(by=['Marca de temps'], ascending=True, inplace=True)
timestamp24 = pd.to_datetime(df24['Marca de temps'], format='%d/%m/%Y %H:%M:%S')
time0_24 = pd.Timestamp('2024-08-17 15:18:00') # hora a la qual vam obrir el 2024
n_previous24 = (timestamp24 < time0_24).sum()
timestamp24 = timestamp24.where(timestamp24 >= time0_24, time0_24)
time_max = pd.Timestamp('2024-08-18 19:00:00') # hora a la qual es va inscriure l'últim de la llista abans de tancar a 250 (sense comptar repetits)
n_in = (timestamp24 < time_max).sum()
timestamp24 = timestamp24[timestamp24 < time_max]
timestamp24.drop(timestamp24.tail(2).index, inplace=True) # treiem els dos últims punts manualment
diff_time24 = (timestamp24 - time0_24).dt.total_seconds()
diff_time24 = diff_time24[timestamp24 != time0_24]
inscrits24 = np.arange(n_previous24, n_in-2, 1) # -2 per quadrar
ax.plot(diff_time24/3600, inscrits24 / n_in*100, label='2024', color='blue')
print(timestamp24)

# Gràfic general (opcions)
ax.set_xlabel("Temps (h)")
ax.set_ylabel("Inscrits (%)")
plt.legend()

plt.savefig("inscrits_cumulatiu.png", dpi=300, bbox_inches='tight')

plt.show()

