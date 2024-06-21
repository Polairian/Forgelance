
import numpy as np
import pandas as pd
import random as r
import matplotlib.pyplot as plt

# =============
# CONST ZONE
# =============

BuffLanceIncendiaire = 4
PA = 12
statsIni = pd.DataFrame([[200,'-', 450, 450, 460, 480, 435, 84, 14], ['-',48, 83, 74, 57, 109, '-', 138, '-']], index = ['Characteristics','Do'], columns = ['Level','Neutre','Terre', 'Feu', 'Eau', 'Air','Puissance/Dommages', 'Crit', 'percentDist'])
initial_state = (0, 0, 0, False, statsIni)
DSorts, Dégats, BuffLanceIncendiaireTotal, Lance, stats = initial_state

# =============

def spellDamage(damage_range, critChance): return(np.average(damage_range[:2])* (1-(critChance/100)) + np.average(damage_range[2:])* critChance/100)

def calculatedMeanDamage(damage_range, critChance, Element): 
    return (spellDamage(damage_range, critChance)* (stats.loc['Characteristics',Element] + stats.loc['Characteristics','Puissance/Dommages'])/ 100 +  stats.loc['Do',Element] + stats.loc['Do','Crit']* critChance/ 100)* (stats.loc['Characteristics','percentDist']/100 + 1)

def bestElement(): return stats.iloc[0, 2:6].idxmax()
def worstElement(): return stats.iloc[0, 2:6].idxmin()
def randomElement(): return r.choice(['Terre','Feu','Eau','Air'])

# =================
# SORTS PAR PAIRES
# =================

def LanceDuLac(): apply_sort([22,25,26,30],10, 'Eau')
def EpieuSismique(): apply_sort([26,29,31,36],15, 'Terre')

def LancePierre(): apply_sort([25,28,30,34],10, 'Terre')
def JavelotFoudre(): apply_sort([28,32,35,39],10, 'Eau')

def LanceAIncendie(): apply_sort([23,26,28,31], 10, 'Feu', proc=True)
def Degagement(): apply_sort([29,32,35,38], 15, 'Air', push = 4)

def JavelyneDeMyr(): apply_sort([26,30,31,36],15, 'Air', push = 2)
def FerRouge(): apply_sort([27,30,32,36], 20, 'Feu', BuffLanceIncendiaire // 2)

def ChargeHeroique(): apply_sort([33,33,40,40],20, bestElement(), push = 4)

def Effondrement(): apply_sort([20,22,24,26],15, 'Terre')
def PluieDAirain(): apply_sort([19,21,23,25],15, 'Air')

def TridenDeLaMer(): apply_sort([21,24,25,29],10, 'Eau')
def MoulinRouge(): apply_sort([28,32,34,38], 15, 'Feu', BuffLanceIncendiaire)

def EstocBrulant(): apply_sort([25,28,30,34], 10, 'Feu', BuffLanceIncendiaire)
def Octave(): apply_sort([16,18,19,22],5, 'Eau')

def VoleeDAirain(): apply_sort([22,25,26,30],10, 'Air', push = 2)
def Soulevement(): apply_sort([29,33,35,40],15, 'Terre')

def Balestra(): apply_sort([28,31,34,37],15, 'Eau')
def MoulinAVent(): apply_sort([29,33,35,40],15, 'Air')

def TalonDArgile(): apply_sort([14,16,17,19],5, 'Terre')
def Fente(): apply_sort([12*0.85,14*0.85,16*0.85,18*0.85], 5, 'Feu', BuffLanceIncendiaire)

def Kyrja(): apply_sort([28,32,34,38],15, bestElement())
def Varja(): apply_sort([39,44,47,53],25, bestElement())

def Maelstom(): apply_sort([29,32,35,38], 10, 'Feu', proc=True)
def Ydra(): apply_sort([25,28,30,34],15, 'Terre')

def LanceCyclone(): apply_sort([31,33,37,40],10, 'Air', push = 3)
def Elding(): apply_sort([32,36,38,43],20, 'Eau')

def Jormun(): apply_sort([30,34,36,41],5, 'Eau')
def Muspel(): apply_sort([31,35,37,42], 20, 'Feu', proc=True, muspel=True)

def TerreDuMilieu(): apply_sort([30,34,36,41],15, 'Terre')
def Noa(): apply_sort([20,23,24,28],15, 'Air')

#==============

def LanceIncendiaire():
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats
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
def BoomerangDeDiamantine(): apply_sort([26,29,31,31],5,randomElement())

# =============    

def apply_sort(damage_range, critChance, Element, buff=0, proc=False, muspel=False, buff2 = None, push = 0):
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, stats
    totalCritChance = critChance+stats.loc['Characteristics','Crit'] if critChance+stats.loc['Characteristics','Crit'] < 100 else 100
    DSorts += spellDamage(damage_range, totalCritChance)
    Dégats += calculatedMeanDamage(damage_range, totalCritChance, Element) + push * (stats.loc['Characteristics','Level']/2+32)/4
    BuffLanceIncendiaireTotal += buff
    if proc:
        if Lance:
            LanceIncendiaire()
        elif not muspel:
            Lance = True

    #if buff2:
    #    stats.loc[buff2[0],buff2[1]] += buff2[2]



Sorts = [LanceDuLac,EpieuSismique,LancePierre,JavelotFoudre,LanceAIncendie,Degagement,JavelyneDeMyr,FerRouge,ChargeHeroique,Effondrement,PluieDAirain,TridenDeLaMer,MoulinRouge,EstocBrulant,Octave,VoleeDAirain,Soulevement,Balestra,MoulinAVent,TalonDArgile,Fente,Kyrja,Varja,Maelstom,Ydra,LanceCyclone,Elding,Jormun,Muspel,TerreDuMilieu,Noa]
limits = [3, 2, 3, 2, 4, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2]
pa_costs = [3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4]

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


