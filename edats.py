import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Anys definits per fer les gràfiques
any_actual = 2025
any_vells = 1985
edicions_correbars = [2024, 2025]
any_limit_max = np.max(edicions_correbars) - 21

# Colors barres
colors = {'2024' : 'blue',
          '2025' : 'red'}

# Creem la figura
fig, ax = plt.subplots(figsize=(7,5))

# Creem els ticks amb el número de la generació
xticks = ["<'"+str(any_vells)[-2:]]
for i in range((any_limit_max - any_vells)+1):
    any = any_vells + i
    xtick = "'" + str(any)[-2:]
    xticks.append(xtick)

anys_llista = np.arange(any_vells-1, any_limit_max+1) # llista d'edats (-1 pel <85 i +1 per incloure any_limit)

# Creació del gràfic per cada edició
for any_actual in edicions_correbars:
    # Any límit dels participants
    any_limit = any_actual - 21

    # Llegim les dades
    filename = "Inscripcions_" + str(any_actual) + ".csv"
    correbars = pd.read_csv(filename)

    ## Trobem els duplicats
    duplicats = correbars['DNI'].duplicated()
    #print("Nombre de duplicats: ", len(correbars['DNI'][duplicats]))

    ## Anàlisi d'edat
    dates = pd.to_datetime(correbars['Data de naixement'], format='%d/%m/%Y')  # Convertim a datetime

    # Extraiem els anys
    anys = dates.dt.year
    #print("Nombre de participants no admesos (2025): ", np.sum(anys>any_limit))
    anys = anys[anys <= any_limit] # treiem els que no compleixen l'edat

    # Comptem quants participants tenim de cada any
    barres_valors = anys.value_counts().sort_index()

    # Agrupem els participants de <1985 en una sola barra (l'interval d'anys és el mateix per totes les edicions!)
    vells = np.sum(anys < any_vells) # quants vells tenim
    joves = anys[anys>=any_vells] # triem els joves (>1990)
    barres_valors = joves.value_counts().sort_index() # comptem quants joves tenim de cada any
    barres_valors = barres_valors.reindex(np.arange(any_vells, any_limit_max+1), fill_value=0) # reindexem per tenir tots els anys (si no hi ha cap participant d'algun any, s'hi posa un 0)
    barres_valors = pd.concat([pd.Series([vells]), barres_valors], ignore_index=True) # afegim el recompte de vells a davant

    # Gràfic de barres
    ax.bar(anys_llista, barres_valors, facecolor = 'none', edgecolor =colors[str(any_actual)], label = str(any_actual))

    print("Participants " + str(any_actual) + ": " + str(dates.shape[0]))

ax.set_xticks(ticks=anys_llista, labels=xticks, rotation = 45)
ax.set_yticks([]) # treiem yticks
#plt.title("De quin any som?")


plt.legend(loc = 'upper left')
plt.savefig('edats_2025.png', dpi=300, bbox_inches='tight')
plt.show()

print("Mitjana d'edat (2025): ", np.mean(any_actual-anys), "anys")