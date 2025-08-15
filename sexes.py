import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

# Anys definits per fer les gràfiques
any_actual = 2025
any_vells = 1985
edicions_correbars = [2024, 2025]
any_limit_max = np.max(edicions_correbars) - 21

# Colors barres
colors = {'2024' : 'blue',
          '2025' : 'red'}

# Ordre per la llista de sexes
sexes_order = ['H', 'D']

# Creem la figura
fig_as, ax_as = plt.subplots(figsize=(10,5)) # anys i sexes
fig_s, ax_s = plt.subplots(figsize=(7,5)) # sexes

# Creem els ticks amb el número de la generació
xticks = ["<'"+str(any_vells)[-2:]]
for i in range((any_limit_max - any_vells)+1):
    any = any_vells + i
    xtick = "'" + str(any)[-2:]
    xticks.append(xtick)

anys_llista = np.arange(2*(any_vells-1), 2*(any_limit_max+1), 2) # llista d'edats (-1 pel <85 i +1 per incloure any_limit). Ho fem de 2 en 2 per les barres H/D

# Creació del gràfic per cada edició
for any_actual in edicions_correbars:
    # Any límit dels participants
    any_limit = any_actual - 21

    # Llegim les dades
    filename = "Inscripcions_" + str(any_actual) + ".csv"
    print(any_actual)
    correbars = pd.read_csv(filename)

    ## Trobem els duplicats
    duplicats = correbars['DNI'].duplicated()
    #print("Nombre de duplicats: ", len(correbars['DNI'][duplicats]))

    ## Anàlisi d'edat
    dates = pd.to_datetime(correbars['Data de naixement'], format='%d/%m/%Y')  # Convertim a datetime

    # Extraiem els anys
    anys = dates.dt.year
    mask_anys = anys <= any_limit # fem una màscara per treure els que no compleixen l'edat
    anys = anys[mask_anys] # treiem els que no compleixen l'edat

    # Extraiem els sexes dels participants
    sexes = correbars['Sexe']
    sexes = sexes[mask_anys] # treiem els que no compleixen l'edat
    sexes_valors = sexes.count()

    # Filtrem les dades per només tenir les que són d'edat vàlida
    correbars = correbars[mask_anys]

    # Per cada any, comptar quants H i quants D hi ha (ordenats per l'ordre de sexe sexe)
    any_sex_counts = correbars.groupby([anys, sexes]).size().unstack(fill_value=0).reindex(columns=sexes_order, fill_value=0)

    # Comptem, en total, quants H i quantes D hi ha de qualsevol any
    sexes_counts = any_sex_counts.sum().reindex(sexes_order)

    # Agrupem els participants de <1985 en una sola barra (l'interval d'anys és el mateix per totes les edicions!)
    vells_s = any_sex_counts[any_sex_counts.index < any_vells].sum() # quants vells tenim (per sexe)
    joves_s = any_sex_counts[any_sex_counts.index > any_vells] # triem els joves (per sexe)
    barres_valors = joves_s.reindex(np.arange(any_vells-1, any_limit_max+1), fill_value=0) # reindexem per tenir tots els anys (si no hi ha cap participant d'algun any, s'hi posa un 0)
    barres_valors.iloc[0] = vells_s # afegim el recompte de vells a davant (per sexe)

    # Gràfic de barres
    if any_actual == 2025:
        linestyle = '-'
    else:
        linestyle = '-.'
    ax_as.bar(anys_llista-0.4, barres_valors['H'], width = 0.8, linestyle = linestyle, facecolor = 'none', edgecolor ='cornflowerblue')
    ax_as.bar(anys_llista+0.4, barres_valors['D'], width = 0.8, linestyle = linestyle, facecolor = 'none', edgecolor ='fuchsia')

    ax_s.bar(sexes_order, sexes_counts / sexes_counts.sum(), facecolor = 'none', edgecolor = colors[str(any_actual)], label = str(any_actual)) # % homes / dones

    print("Participants " + str(any_actual) + ": " + str(dates.shape[0]))

# Opcions Sexe-Any
# Primera llegenda: edicions correbars
linetype_legend = [Line2D([0], [0], color='black', linestyle='-', label='2025'),
                   Line2D([0], [0], color='black', linestyle='-.', label='2024')] # definim els tipus de línia per les edicions
legend1 = ax_as.legend(handles=linetype_legend, loc='upper left', title='Edició') # Defineix la llegenda per les edicions
ax_as.add_artist(legend1)  # afegim la primera llegenda al gràfic
pos = legend1.get_bbox_to_anchor().bounds
print(pos)

# Segona llegenda: colors pels sexes
color_legend = [Line2D([0], [0], color='cornflowerblue', lw=4, label='H'),
                Line2D([0], [0], color='fuchsia', lw=4, label='D')] # definim els colors per les barres de sexe
legend2 = ax_as.legend(handles=color_legend, loc='upper left', bbox_to_anchor=(0.12, 1.), title='Sexe') # definim la llegenda per sexe
ax_as.add_artist(legend2)  # afegim la segona llegenda al gràfic
# altres opcions
ax_as.set_xticks(ticks=anys_llista, labels=xticks, rotation = 45)
ax_as.set_yticks([]) # treiem yticks
fig_as.savefig('sexes_any_2025.png', dpi=300, bbox_inches='tight')
fig_as.show()
fig_as.clf()

# Opcions Sexe
ax_s.set_xticks(ticks=[0, 1], labels=sexes_order, rotation = 0)
ax_s.legend()
fig_s.savefig('sexes_2025.png', dpi=300, bbox_inches='tight')