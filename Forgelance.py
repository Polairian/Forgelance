
import numpy as np
import pandas as pd
import random as r
import matplotlib.pyplot as plt

# =============
# CONST ZONE
# =============

buffLanceIncendiaire = 4
niveau = 200
PA = 3
doNeutre = 48
terre = np.array([4.5,83]) 
feu = np.array([4.5,74])
eau = np.array([4.6,57])
air =np.array([4.8,109])
elementStat = np.array([terre,feu,eau,air])
puissance = 4.35
crit = 0.84
doCrit = 138
perDist = 14

initial_state = (0, 0, 0, False, 0)
DSorts, Dégats, BuffLanceIncendiaireTotal, Lance, crit = initial_state

# =============

def spellDamage(damage_range, critChance): return(np.average(damage_range[:2])* (1-critChance) + np.average(damage_range[2:])* critChance)

def calculatedMeanDamage(damage_range, critChance, choosenStat): 
    return (spellDamage(damage_range, critChance)* (choosenStat[0] + puissance) + choosenStat[1]  + doCrit* critChance)* (perDist/100 + 1)

def bestElement(): return elementStat[np.argmax(elementStat[:,0])]
def worstElement(): return elementStat[np.argmin(elementStat[:,0])]
def randomElement(): return elementStat[np.random.randint(0,4)]

# =================
# SORTS PAR PAIRES
# =================

def LanceDuLac(): apply_sort([22,25,26,30],0.1, eau)
def EpieuSismique(): apply_sort([26,29,31,36],0.15, terre)

def LancePierre(): apply_sort([25,28,30,34],0.10, terre)
def JavelotFoudre(): apply_sort([28,32,35,39],0.10, eau)

def LanceAIncendie(): apply_sort([23,26,28,31], 0.10, feu, proc=True)
def Degagement(): apply_sort([29,32,35,38], 0.15, air, push = 4)

def JavelyneDeMyr(): apply_sort([26,30,31,36],0.15, air, push = 2)
def FerRouge(): apply_sort([27,30,32,36], 0.20, feu, buffLanceIncendiaire // 2)

def ChargeHeroique(): apply_sort([33,33,40,40],0.20, bestElement(), push = 4)

def Effondrement(): apply_sort([20,22,24,26],0.15, terre)
def PluieDAirain(): apply_sort([19,21,23,25],0.15, air)

def TridenDeLaMer(): apply_sort([21,24,25,29],0.10, eau)
def MoulinRouge(): apply_sort([28,32,34,38], 0.15, feu, buffLanceIncendiaire)

def EstocBrulant(): apply_sort([25,28,30,34], 0.10, feu, buffLanceIncendiaire)
def Octave(): apply_sort([16,18,19,22],0.5, eau)

def VoleeDAirain(): apply_sort([22,25,26,30],0.10, air, push = 2)
def Soulevement(): apply_sort([29,33,35,40],0.15, terre)

def Balestra(): apply_sort([28,31,34,37],0.15, eau)
def MoulinAVent(): apply_sort([29,33,35,40],0.15, air)

def TalonDArgile(): apply_sort([14,16,17,19],0.5, terre)
def Fente(): apply_sort([12*0.85,14*0.85,16*0.85,18*0.85], 0.5, feu, buffLanceIncendiaire)

def Kyrja(): apply_sort([28,32,34,38],0.15, bestElement())
def Varja(): apply_sort([39,44,47,53],0.25, bestElement())

def Maelstom(): apply_sort([29,32,35,38], 0.10, feu, proc=True)
def Ydra(): apply_sort([25,28,30,34],0.15, terre)

def LanceCyclone(): apply_sort([31,33,37,40],0.10, air, push = 3)
def Elding(): apply_sort([32,36,38,43],0.20, eau)

def Jormun(): apply_sort([30,34,36,41],0.5, eau)
def Muspel(): apply_sort([31,35,37,42], 0.20, feu, proc=True, muspel=True)

def TerreDuMilieu(): apply_sort([30,34,36,41],0.15, terre)
def Noa(): apply_sort([20,23,24,28],0.15, air)

#==============

def LanceIncendiaire():
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats
    Lance = False
    DSorts += BuffLanceIncendiaireTotal + 19  # (18+20)/2
    Dégats += (BuffLanceIncendiaireTotal + 19)* (feu[0] + puissance)/ 100
    BuffLanceIncendiaireTotal = 0

# =============    

# =============
# SORTS COMMUNS
# =============

def Flamiche(): apply_sort([8,10,10,12],5, worstElement())
def Flamèche(): apply_sort([8,10,10,12],5, bestElement())
def Ebilition(): apply_sort([21,24,25,29],10, eau, ebilition = True)
def BoomerangDeDiamantine(): apply_sort([26,29,31,31],5, randomElement())

# =============    

def apply_sort(damage_range, critChance, Element, buff=0, proc=False, muspel=False, buff2 = None, push = 0, ebilition = False):
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, crit
    totalCritChance = critChance + crit if critChance + crit < 1 else 1
    DSorts += spellDamage(damage_range, totalCritChance)
    Dégats += calculatedMeanDamage(damage_range, totalCritChance, Element) + push * (niveau/2+32)/4
    BuffLanceIncendiaireTotal += buff
    if proc:
        if Lance:
            LanceIncendiaire()
        elif not muspel:
            Lance = True

    #if ebilition:
    #    crit += 0.1



Sorts = [LanceDuLac,EpieuSismique,LancePierre,JavelotFoudre,LanceAIncendie,Degagement,JavelyneDeMyr,FerRouge,ChargeHeroique,Effondrement,PluieDAirain,TridenDeLaMer,MoulinRouge,EstocBrulant,Octave,VoleeDAirain,Soulevement,Balestra,MoulinAVent,TalonDArgile,Fente,Kyrja,Varja,Maelstom,Ydra,LanceCyclone,Elding,Jormun,Muspel,TerreDuMilieu,Noa, Ebilition]
alternativeID = [1,0,3,2,5,4,7,6,8,10,9,12,11,14,13,16,15,18,17,20,19,22,21,24,23,26,25,28,27,30,29,30]
limits = [3, 2, 3, 2, 4, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2]
pa_costs = [3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3]

def get_seq_from(pa, current_limits: list):
    for i, (f, limit, cost) in enumerate(zip(Sorts, current_limits, pa_costs)):
        if current_limits[i] > 1 and cost <= pa:
            new_limits = current_limits.copy()
            new_limits[i] -= 1
            new_limits[alternativeID[i]] = 0
            yield [i]
            for subseq in get_seq_from(pa - cost, new_limits):
                yield [i, *subseq]

def simulate_turns():
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, crit
    tours = []

    for seq in get_seq_from(PA, limits.copy()):
        DSorts, Dégats, BuffLanceIncendiaireTotal, Lance, crit = initial_state

        for idx in seq:
            Sorts[idx]()
        tours.append((*[Sorts[i].__name__ for i in seq], DSorts, Dégats))

    return tours

tours = simulate_turns()
tours.sort(key=lambda x:-x[-1])
print(*tours[:5], sep='\n')




