import numpy as np

# La voie feu de la forgelance fonctionne autour du sort Lance Incendiaire, 3 des sorts permettent de poser et/ou retirer un état aux ennemis, lorsqu'on le retire, l'ennemi subit le sort Lance Incendiaire
# Les dégats de Lance incendiaire sont augmenté par les autres sorts de la voie, et sont réinitialisé une fois que le sort à proc
# La variable "Lance" correspond à cet état, si Lance = False, l'ennemi n'a pas l'état

# Nombre d'ennemis*4 que vous touchez avec les sorts de buff de la forgelance (pour chaque ennemis touché, Lanceincendiaire a ses dégats de bases augmentés de 4 jusqu'au prochain proc) 
BuffLanceIncendiaire = 4

def max_value(inputlist):
    return max([sublist[-1] for sublist in inputlist])

# Definition des différents sorts de la Forgelance

#Passive proc : 
def LanceIncendiaire():
    
    global Lance, DSorts, BuffLanceIncendiaire, BuffLanceIncendiaireTotal, PA
    Lance = False
    BuffLanceIncendiaireTotal = 0
    return BuffLanceIncendiaireTotal + (18+20)/2

#ça pourrait être moins lourd ? de ne passer que la moyenne en param et pas une liste, mais beaucoup moins lisible

def apply_spell(pa_cost,dmg_range,buffCoef=1,Muspel=False):
    global Lance, DSorts, BuffLanceIncendiaire, BuffLanceIncendiaireTotal, PA
    if pa_cost >= PA:
        #Add damage
        DSorts += np.average(dmg_range)
        
        #Proc if lance or give it (not for Muspel)
        if not Lance and not Muspel: Lance = True
        elif Lance: DSorts+=LanceIncendiaire()
        
        #Buff the lanceBuff
        BuffLanceIncendiaireTotal += BuffLanceIncendiaireTotal*buffCoef
        #Sub PA cost
        PA -= pa_cost
        
        
    

# Sort Numéro 0
def LanceAIncendie():

    global Lance, DSorts, BuffLanceIncendiaire, BuffLanceIncendiaireTotal, PA

    if PA >= 3:
        
        DSorts += (23+26)/2 # moyenne
        if not Lance:
            Lance = True
        elif Lance:
            LanceIncendiaire()
    PA -= 3
    return
    
# Sort Numéro 1
def MoulinRouge():
   apply_spell(3,[28,32])
   #I don't like returning nothing but if we keep this struct...

# Sort Numéro 2
def Fente():
    apply_spell(2,[12,14])

# Sort Numéro 3
def FerRouge():
    apply_spell(3,[27,30],0.5)


# Sort Numéro 4
def EstocBrulant():
    apply_spell(3,[25,28])


# Sort Numéro 5
#Muspel proc mais n'applique pas
def Muspel():
    apply_spell(3,[31,35],0,Muspel=True)

# Sort Numéro 6
def Maelstom():
    apply_spell(3,[16,19],0)



# =============
# Main
# =============
Tour = []
TourFiltre = []

# Liste de fonctions correspondantes aux sorts feu de la Forgelance
Sorts = (LanceAIncendie,MoulinRouge,Fente,FerRouge,EstocBrulant,Muspel,Maelstom)


# 4 Boucle pour itérer à travers les sorts et tester toutes les combinaison possibles
# Problèmes majeurs: 
# Besoin de "sauvegarder" les Pa, Dégat, les Buff et l'état de la Lance à un moment donné
# Besoin de faire une boucle par sorts lancé, serait plus pratique si ça détectait, avec les PA restants, s'il est possible de lancer un sort (utile si on se fait Re Pa)

for i in range(0,len(Sorts)):

    PA = 12
    BuffLanceIncendiaireTotal = 0
    Lance = False
    DSorts = 0

    Sorts[i]()

    PAE1 = PA
    DSortsE1 = DSorts
    BuffLanceIncendiaireTotalE1 = BuffLanceIncendiaireTotal
    LanceE1 = Lance
    
    for j in range(0,len(Sorts)):

        PA = PAE1
        BuffLanceIncendiaireTotal = BuffLanceIncendiaireTotalE1
        Lance = LanceE1
        DSorts = DSortsE1

        Sorts[j]()

        PAE2 = PA
        DSortsE2 = DSorts
        BuffLanceIncendiaireTotalE2 = BuffLanceIncendiaireTotal
        LanceE2 = Lance

        for k in range(0,len(Sorts)):

            PA = PAE2
            BuffLanceIncendiaireTotal = BuffLanceIncendiaireTotalE2
            Lance = LanceE2
            DSorts = DSortsE2

            Sorts[k]()

            PAE3 = PA
            DSortsE3 = DSorts
            BuffLanceIncendiaireTotalE3 = BuffLanceIncendiaireTotal
            LanceE3 = Lance

            if PA>0:
                for l in range(0,len(Sorts)):

                    PA = PAE3
                    BuffLanceIncendiaireTotal = BuffLanceIncendiaireTotalE3
                    Lance = LanceE3
                    DSorts = DSortsE3
                    
                    Sorts[l]()

                    if PA>=0:
                        Tour.append((i,j,k,l,DSorts))
                    else:
                        Tour.append((i,j,k,DSortsE3))

            elif PA == 0:

                Tour.append((i,j,k,DSorts))

# Sert a retirer les séquences de sorts où un sort a plus d'utilisation que sa limite par tour
for sublist in Tour:
    NBLAI = sublist.count(0)
    NBMORO = sublist.count(1)
    NBFENT = sublist.count(2)
    NBFERO = sublist.count(3)
    NBESTC = sublist.count(4)
    NBMUS = sublist.count(5)
    NBMAEL = sublist.count(6)
    if NBLAI < 3 and NBFERO < 3 and NBESTC < 3 and NBMAEL < 3 and NBMORO < 2 and NBFENT < 2 and NBMUS < 2:
        TourFiltre.append(sublist)

# Détermine le maximum de dégats de sorts dans les conditions données
GrosDégat = max_value(TourFiltre)

# Print les séquences obtenant ce résultat
for sublist in TourFiltre:
    if GrosDégat in sublist:
        print(sublist)

