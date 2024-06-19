import numpy as np

# La voie feu de la forgelance fonctionne autour du sort Lance Incendiaire, 3 des sorts permettent de poser et/ou retirer un état aux ennemis, lorsqu'on le retire, l'ennemi subit le sort Lance Incendiaire
# Les dégats de Lance incendiaire sont augmenté par les autres sorts de la voie, et sont réinitialisé une fois que le sort à proc
# La variable "Lance" correspond à cet état, si Lance = False, l'ennemi n'a pas l'état

# Nombre d'ennemis*4 que vous touchez avec les sorts de buff de la forgelance (pour chaque ennemis touché, Lanceincendiaire a ses dégats de bases augmentés de 4 jusqu'au prochain proc) 
BUFFLANCEINCENDIAIRE = 4

class Spell:
    #Le coup en PA pour savoir si on continue
    #L'id du sort
    #Les dmg
    #Les enfants
    def __init__(self, dmg, cost, name):
        self.name = name
        self.dmg = dmg
        self.cost = cost
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)


class Tour:
    def __init__(self, root):
        self.root = root

def print_tree(node, level=0):
    print(' ' * level+ node.name)
    for child in node.children:
        print_tree(child, level + 1)


def max_value(inputlist):
    return max([sublist[-1] for sublist in inputlist])

# Definition des différents sorts de la Forgelance

#Passive proc : 
def LanceIncendiaire():
    global Lance, DSorts, BUFFLANCEINCENDIAIRE, BuffLanceIncendiaireTotal, PA
    
    Lance = False
    tmp = BuffLanceIncendiaireTotal + np.average([18,20])
    BuffLanceIncendiaireTotal = 0
    return tmp

#ça pourrait être moins lourd ? de ne passer que la moyenne en param et pas une liste, mais beaucoup moins lisible

def apply_spell(pa_cost,dmg_range,buffCoef=1,Muspel=False):
    global Lance, DSorts, BuffLanceIncendiaireTotal, PA
    if pa_cost >= PA:
        #Add damage
        DSorts += np.average(dmg_range)
        
        #On proc que si on est à buff = 0
        if buffCoef == 0 and Lance:
            DSorts+=LanceIncendiaire()
        elif not Lance and not Muspel:
            Lance = True
        
        #Buff the lanceBuff if needed, sometime it can be 0 but anyway
        BuffLanceIncendiaireTotal += BUFFLANCEINCENDIAIRE*buffCoef
        #Sub PA cost
        PA -= pa_cost
        
def LanceAIncendie(): #proc
    apply_spell(3,[23,26],0)
    
def MoulinRouge(): #B1
   apply_spell(3,[28,32])
   #I don't like returning nothing but if we keep this struct...

def Fente(): #B1
    apply_spell(2,[12,14])

def FerRouge(): #B0.5
    apply_spell(3,[27,30],0.5)

def EstocBrulant():#B1
    apply_spell(3,[25,28])

#Muspel proc mais n'applique pas
def Muspel():
    apply_spell(3,[31,35],0,Muspel=True)

# Sort Numéro 6
def Maelstom(): #Proc
    apply_spell(3,[16,19],0)


# =============
# Main
# =============
Tour1 = []
TourFiltre = []

# Liste de fonctions correspondantes aux sorts feu de la Forgelance
Sorts = (LanceAIncendie,MoulinRouge,Fente,FerRouge,EstocBrulant,Muspel,Maelstom)


# 4 Boucle pour itérer à travers les sorts et tester toutes les combinaison possibles
# Problèmes majeurs: 
# Besoin de "sauvegarder" les Pa, Dégat, les Buff et l'état de la Lance à un moment donné
# Besoin de faire une boucle par sorts lancé, serait plus pratique si ça détectait, avec les PA restants, s'il est possible de lancer un sort (utile si on se fait Re Pa)



# Nouveau format de sortie:

# Une grande liste

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
                        Tour1.append((i,j,k,l,DSorts))
                    else:
                        Tour1.append((i,j,k,DSortsE3))

            elif PA == 0:

                Tour1.append((i,j,k,DSorts))

# Sert a retirer les séquences de sorts où un sort a plus d'utilisation que sa limite par tour
for sublist in Tour1:
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


root = Spell("Root")
child_a = Spell("A")
child_b = Spell("B")
child_a1 = Spell("A1")
child_a2 = Spell("A2")
child_b1 = Spell("B1")
child_a1_1 = Spell("A1.1")
child_a1_2 = Spell("A1.2")
child_a2_1 = Spell("A2.1")
child_b1_1 = Spell("B1.1")

root.add_child(child_a)
root.add_child(child_b)
child_a.add_child(child_a1)
child_a.add_child(child_a2)
child_b.add_child(child_b1)
child_a1.add_child(child_a1_1)
child_a1.add_child(child_a1_2)
child_a2.add_child(child_a2_1)
child_b1.add_child(child_b1_1)

tree = Tour(root)

print_tree(tree.root)

