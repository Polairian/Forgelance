import numpy as np

# La voie feu de la forgelance fonctionne autour du sort Lance Incendiaire, 3 des sorts permettent de poser et/ou retirer un état aux ennemis, lorsqu'on le retire, l'ennemi subit le sort Lance Incendiaire
# Les dégats de Lance incendiaire sont augmenté par les autres sorts de la voie, et sont réinitialisé une fois que le sort à proc
# La variable "Lance" correspond à cet état, si Lance = False, l'ennemi n'a pas l'état


# =============
# CONST ZONE
# =============

# Nombre d'ennemis*4 que vous touchez avec les sorts de buff de la forgelance (pour chaque ennemis touché, Lanceincendiaire a ses dégats de bases augmentés de 4 jusqu'au prochain proc) 
BUFFLANCEINCENDIAIRE = 4
MINSPELLCOST = 2
Lance = False
BuffLanceIncendiaireTotal = 0
nbraff = 3


# =============

class Step:
    def __init__(self, dmg, name,paRem,lancerTrack):
        self.name = name
        self.dmg = dmg
        self.paRem = paRem
        self.children = []
        self.lancerTrack = list(lancerTrack)

    def add_child(self, child_node):
        self.children.append(child_node)


def print_tree(node, currDmg, level=0):
    print(' ' * level * 2 + node.name +" : " + str(node.dmg + currDmg) + " : " + str(node.paRem))
    for child in node.children:
        print_tree(child,currDmg+node.dmg,level + 1)


# Definition des différents sorts de la Forgelance

#Passive proc : 
def LanceIncendiaire():
    global Lance, BUFFLANCEINCENDIAIRE, BuffLanceIncendiaireTotal
    Lance = False
    tmp = BuffLanceIncendiaireTotal + np.average([18,20])
    BuffLanceIncendiaireTotal = 0
    return tmp

#ça pourrait être moins lourd ? de ne passer que la moyenne en param et pas une liste, mais beaucoup moins lisible

def apply_spell(dmg_range,buffCoef=1,Muspel=False):
    global Lance, BuffLanceIncendiaireTotal
    currDmg = np.average(dmg_range)
    if buffCoef == 0 and Lance:
        currDmg+=LanceIncendiaire()
    elif not Lance and not Muspel:
        Lance = True
    BuffLanceIncendiaireTotal += BUFFLANCEINCENDIAIRE*buffCoef
    return currDmg
        
#0
def LanceAIncendie(): #proc
    return apply_spell([23,26],0)
    
def MoulinRouge(): #B1
    return apply_spell([28,32])
  
def Fente(): #B1
    return apply_spell([12,14])

def FerRouge(): #B0.5
    return apply_spell([27,30],0.5)

def EstocBrulant():#B1
    return apply_spell([25,28])

#Muspel proc mais n'applique pas
def Muspel():
    return apply_spell([31,35],0,Muspel=True)

#6
def Maelstom(): #Proc
    return apply_spell([16,19],0)

def buildTree(currStep):
    #On regarde quel(s) sorts on peut lancer PA/lancer max
    toBeLaunch = []
    for key,value in SPELLREQ.items():
        if currStep.paRem >= value["pa"] and currStep.lancerTrack[key] < value["max"]:
            toBeLaunch.append(value)
    #On lance les sorts possibles
    for spell in toBeLaunch:
        #On a lancé un sort, du coup on le prépare et on ajoute
        thisSpell = spell
        spellDmg = thisSpell["fct"]()
        name = thisSpell["name"]
        paRem = currStep.paRem - thisSpell["pa"]
        lancerTrack = currStep.lancerTrack
        lancerTrack[thisSpell["id"]]+=1
        thisStep = Step(spellDmg,name,paRem,lancerTrack)
        #On ajoute ce choix au noeud actuel
        currStep.add_child(thisStep)
        
        #On regarde si on pourra en lancer au prochain tour à partir de ce step la
        #(Il est vrai que même si seul un est possible on fait un for/if sur 7 index mais blc)
        if not (paRem < MINSPELLCOST):
            buildTree(thisStep) #build tree from this step
        
def meilleurChemin(currNode): 
    global nbraff
    if not currNode.children: return [(currNode.dmg, [currNode.name])]
    best_paths = []
    for child in currNode.children:
        for child_sum, child_path in meilleurChemin(child): best_paths.append((child_sum, [currNode.name] + child_path))
    best_paths = sorted(best_paths, key=lambda x: x[0], reverse=True)[:nbraff]
    return [(currNode.dmg + s, p) for s, p in best_paths]

# =============
# Main
# =============

SPELLREQ = {0 :{"id" : 0, "fct" :LanceAIncendie, "name" : "LanceAIncendie","pa" : 3 ,"max" : 3 },\
            1 :{"id" : 1, "fct" :MoulinRouge, "name" : "MoulinRouge","pa" : 3,"max" :1},\
            2 :{"id" : 2, "fct" :Fente, "name" : "Fente","pa" : 2,"max" :1},\
            3 :{"id" : 3, "fct" :FerRouge, "name" : "FerRouge","pa" : 3,"max" :2},\
            4 :{"id" : 4, "fct" :EstocBrulant, "name" : "EstocBrulant","pa" : 3,"max" :2},\
            5 :{"id" : 5, "fct" :Muspel, "name" : "Muspel","pa" : 4,"max" :1},\
            6 :{"id" : 6, "fct" :Maelstom, "name" : "Maelstom","pa" : 3,"max" :2},\
            }


pa = input("Nombre de PA ce tour : ")
aff = input("Affichage simple(s) ou complet (c) : ")
if aff == 'c':
    nbraff = int(input("Combien de meilleur score : "))
strat = Step(0,"Start",int(pa),[0,0,0,0,0,0,0])
buildTree(strat)
if aff == 'c':
    print_tree(strat,0)
print(meilleurChemin(strat))

