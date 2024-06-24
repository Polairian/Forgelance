
import numpy as np
import pandas as pd
import random as r
import matplotlib.pyplot as plt
import functools

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
elementStat = [terre,feu,eau,air]
TERRE, FEU, EAU, AIR = 0, 1, 2, 3
puissance = 4.35
crit = 0.84
doCrit = 138
perDist = 14

initial_state = (0, 0, 0, False)
DSorts, Dégats, BuffLanceIncendiaireTotal, Lance = initial_state

# =============

@functools.lru_cache(maxsize=None)
def spellDamage(totalCritChance, *damage_range): 
    return(np.average(damage_range[:2])* (1-totalCritChance) + np.average(damage_range[2:])* totalCritChance)

@functools.lru_cache(maxsize=None)
def calculatedMeanDamage(critChance, choosenStatIndex, *damage_range, push=0):
    chosenStat = elementStat[choosenStatIndex]
    return (spellDamage(critChance, *damage_range)* (chosenStat[0] + puissance) + chosenStat[1]  + doCrit* critChance)* (perDist/100 + 1)  + push * (niveau/2+32)/4

def bestElement(): return int(np.argmax(np.array(elementStat)[:,0]))
def worstElement(): return int(np.argmin(np.array(elementStat)[:,0]))
def randomElement(): return np.random.randint(0,4)

# =================
# SORTS PAR PAIRES
# =================

def LanceDuLac(): apply_sort([22,25,26,30],0.1, EAU)
def EpieuSismique(): apply_sort([26,29,31,36],0.15, TERRE)

def LancePierre(): apply_sort([25,28,30,34],0.10, TERRE)
def JavelotFoudre(): apply_sort([28,32,35,39],0.10, EAU)

def LanceAIncendie(): apply_sort([23,26,28,31], 0.10, FEU, proc=True)
def Degagement(): apply_sort([29,32,35,38], 0.15, AIR, push = 4)

def JavelyneDeMyr(): apply_sort([26,30,31,36],0.15, AIR, push = 2)
def FerRouge(): apply_sort([27,30,32,36], 0.20, FEU, buffLanceIncendiaire // 2)

def ChargeHeroique(): apply_sort([33,33,40,40],0.20, bestElement(), push = 4)

def Effondrement(): apply_sort([20,22,24,26],0.15, TERRE)
def PluieDAirain(): apply_sort([19,21,23,25],0.15, AIR)

def TridenDeLaMer(): apply_sort([21,24,25,29],0.10, EAU)
def MoulinRouge(): apply_sort([28,32,34,38], 0.15, FEU, buffLanceIncendiaire)

def EstocBrulant(): apply_sort([25,28,30,34], 0.10, FEU, buffLanceIncendiaire)
def Octave(): apply_sort([16,18,19,22],0.5, EAU)

def VoleeDAirain(): apply_sort([22,25,26,30],0.10, AIR, push = 2)
def Soulevement(): apply_sort([29,33,35,40],0.15, TERRE)

def Balestra(): apply_sort([28,31,34,37],0.15, EAU)
def MoulinAVent(): apply_sort([29,33,35,40],0.15, AIR)

def TalonDArgile(): apply_sort([14,16,17,19],0.5, TERRE)
def Fente(): apply_sort([12*0.85,14*0.85,16*0.85,18*0.85], 0.5, FEU, buffLanceIncendiaire)

def Kyrja(): apply_sort([28,32,34,38],0.15, bestElement())
def Varja(): apply_sort([39,44,47,53],0.25, bestElement())

def Maelstom(): apply_sort([29,32,35,38], 0.10, FEU, proc=True)
def Ydra(): apply_sort([25,28,30,34],0.15, TERRE)

def LanceCyclone(): apply_sort([31,33,37,40],0.10, AIR, push = 3)
def Elding(): apply_sort([32,36,38,43],0.20, EAU)

def Jormun(): apply_sort([30,34,36,41],0.5, EAU)
def Muspel(): apply_sort([31,35,37,42], 0.20, FEU, proc=True, muspel=True)

def TerreDuMilieu(): apply_sort([30,34,36,41],0.15, TERRE)
def Noa(): apply_sort([20,23,24,28],0.15, AIR)

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
def Ebilition(): apply_sort([21,24,25,29],10, EAU, ebilition = True)
def BoomerangDeDiamantine(): apply_sort([26,29,31,31],5, randomElement())

# =============

def apply_sort(damage_range, critChance, Element: int, buff=0, proc=False, muspel=False, buff2 = None, push = 0, ebilition = False):
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats, crit
    totalCritChance = critChance + crit if critChance + crit < 1 else 1
    DSorts += spellDamage(totalCritChance, *damage_range)
    Dégats += calculatedMeanDamage(totalCritChance, Element, *damage_range, push)
    BuffLanceIncendiaireTotal += buff
    if proc:
        if Lance:
            LanceIncendiaire()
        elif not muspel:
            Lance = True

    if ebilition:
        crit += 0.1



Sorts = [LanceDuLac,EpieuSismique,LancePierre,JavelotFoudre,LanceAIncendie,Degagement,JavelyneDeMyr,FerRouge,ChargeHeroique,Effondrement,PluieDAirain,TridenDeLaMer,MoulinRouge,EstocBrulant,Octave,VoleeDAirain,Soulevement,Balestra,MoulinAVent,TalonDArgile,Fente,Kyrja,Varja,Maelstom,Ydra,LanceCyclone,Elding,Jormun,Muspel,TerreDuMilieu,Noa]
alternativeID = [1,0,3,2,5,4,7,6,8,10,9,12,11,14,13,16,15,18,17,20,19,22,21,24,23,26,25,28,27,30,29]
limits = [3, 2, 3, 2, 4, 2, 3, 3, 2, 2, 2, 3, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 2, 3, 2, 2, 2, 2]
pa_costs = [3, 3, 3, 3, 3, 4, 3, 3, 3, 3, 2, 3, 3, 3, 2, 3, 3, 3, 3, 2, 2, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4]

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
    global Lance, DSorts, BuffLanceIncendiaireTotal, Dégats
    tours = []

    for seq in get_seq_from(PA, limits.copy()):
        DSorts, Dégats, BuffLanceIncendiaireTotal, Lance = initial_state

        for idx in seq:
            Sorts[idx]()
        tours.append((*seq, DSorts, Dégats))

    return tours

tours = simulate_turns()
tours.sort(key=lambda x:-x[-1])
for tour in tours[:5]:
    print(*[Sorts[i].__name__ for i in tour[:-2]], tour[-2], tour[-1], sep=' ')
