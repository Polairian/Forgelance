
import numpy as np
import pandas as pd

# =============
# CONST ZONE
# =============

BuffLanceIncendiaire = 4
PA = 12
statsIni = pd.DataFrame([['-', 450, 450, 460, 480, 435, 84], [48, 83, 74, 57, 109, '-', 138]], index = ['Characteristics','Do'], columns = ['Neutre','Terre', 'Feu', 'Eau', 'Air','Puissance/Dommages', 'Crit'])
initial_state = (0, 0, 0, False, statsIni)
DSorts, Dégats, BuffLanceIncendiaireTotal, Lance, stats = initial_state

# =============

def spellDamage(damage_range, critChance): return(np.average(damage_range[:2])* (1-(critChance/100)) + np.average(damage_range[2:])* critChance/100)

def calculatedMeanDamage(damage_range, critChance, Element):
    global stats
    return spellDamage(damage_range, critChance)* (stats.loc['Characteristics',Element] + stats.loc['Characteristics','Puissance/Dommages'])/ 100 +  stats.loc['Do',Element] + stats.loc['Do','Crit']* critChance/ 100

def bestElement():
    global stats
    return stats.iloc[0, 1:5].idxmax()

def worstElement():
    global stats
    return stats.iloc[0, 1:5].idxmin()

# =============
# SORTS FEUX
# =============

def LanceAIncendie(): apply_sort([23,26,28,31], 10, 'Feu', proc=True)
def MoulinRouge(): apply_sort([28,32,34,38], 15, 'Feu', BuffLanceIncendiaire)
def Fente(): apply_sort([12,14,16,18], 5, 'Feu', BuffLanceIncendiaire)
def FerRouge(): apply_sort([27,30,32,36], 20, 'Feu', BuffLanceIncendiaire // 2)
def EstocBrulant(): apply_sort([25,28,30,34], 10, 'Feu', BuffLanceIncendiaire)
def Muspel(): apply_sort([31,35,37,42], 20, 'Feu', proc=True, muspel=True)
def Maelstom(): apply_sort([29,32,35,38], 10, 'Feu', proc=True)

def LanceIncendiaire():
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, stats
    Lance = False
    DSorts += BuffLanceIncendiaireTotal + 19  # (18+20)/2
    Dégats += (BuffLanceIncendiaireTotal + 19)* (stats.loc['Characteristics','Feu'] + stats.loc['Characteristics','Puissance/Dommages'])/ 100
    BuffLanceIncendiaireTotal = 0

# =============    

# =============
# SORTS COMMUNS
# =============

def Flamiche(): apply_sort([8,10,10,12],5, worstElement())
def Flamèche(): apply_sort([8,10,10,12],5, bestElement())
def Ebilition(): apply_sort([21,24,25,29],10,'Eau',buff2 = ('Characteristics','Crit',10))

# =============    

def apply_sort(damage_range, critChance, Element, buff=0, proc=False, muspel=False, buff2 = None):
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, stats
    totalCritChance = critChance+stats.loc['Characteristics','Crit'] if critChance+stats.loc['Characteristics','Crit'] < 100 else 100
    DSorts += spellDamage(damage_range, totalCritChance)
    Dégats += calculatedMeanDamage(damage_range, totalCritChance, Element)
    BuffLanceIncendiaireTotal += buff
    if proc:
        if Lance:
            LanceIncendiaire()
        elif not muspel:
            Lance = True

Sorts = [LanceAIncendie, MoulinRouge, Fente, FerRouge, EstocBrulant, Muspel, Maelstom, Flamiche, Flamèche, Ebilition]
limits = [3, 2, 2, 3, 3, 2, 3, 3, 5, 2]
pa_costs = [3, 3, 2, 3, 3, 4, 3, 2, 2, 3]

def get_seq_from(pa, current_limits: list):
    for i, (f, limit, cost) in enumerate(zip(Sorts, current_limits, pa_costs)):
        if current_limits[i] > 1 and cost <= pa:
            new_limits = current_limits.copy()
            new_limits[i] -= 1
            yield [i]
            for subseq in get_seq_from(pa - cost, new_limits):
                yield [i, *subseq]

def simulate_turns():
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, stats
    tours = []

    for seq in get_seq_from(PA, limits.copy()):
        DSorts, Dégats, BuffLanceIncendiaireTotal, Lance, stats = initial_state

        for idx in seq:
            Sorts[idx]()
        tours.append((*[Sorts[i].__name__ for i in seq], DSorts, Dégats))

    return tours

tours = simulate_turns()
tours.sort(key=lambda x:-x[-1])
print(*tours[:5], sep='\n')
