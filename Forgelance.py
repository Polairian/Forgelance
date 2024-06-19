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
PA = 12
Lance = False
BuffLanceIncendiaireTotal = 0


# =============

class Step:
    def __init__(self, dmg, name,paRem,lancerTrack):
        self.name = name
        self.dmg = dmg
        self.paRem = paRem
        self.children = []
        self.lancerTrack = lancerTrack

    def add_child(self, child_node):
        self.children.append(child_node)

class Racine:
    def __init__(self, name,paRem,lancerTrack):
        self.name = name
        self.paRem = paRem
        self.lancerTrack = lancerTrack

def print_tree(node, currDmg, level=0):
    print(' ' * level * 2 + node.name +" : " + str(currDmg))
    for child in node.children:
        print_tree(child,currDmg+node.dmg,level + 1)


# Definition des différents sorts de la Forgelance

#Passive proc : 
def LanceIncendiaire():
    global Lance, DSorts, BUFFLANCEINCENDIAIRE, BuffLanceIncendiaireTotal, PA
    
    Lance = False
    tmp = BuffLanceIncendiaireTotal + np.average([18,20])
    BuffLanceIncendiaireTotal = 0
    return tmp

#ça pourrait être moins lourd ? de ne passer que la moyenne en param et pas une liste, mais beaucoup moins lisible

def apply_spell(dmg_range,buffCoef=1,Muspel=False):
    global Lance, BuffLanceIncendiaireTotal
    Lance = Lance
    #On sait déjà que si on est la c'est qu'on a les PA
    currDmg = 0
    #Add damage
    currDmg += np.average(dmg_range)
    
    #On proc que si on est à buff = 0
    if buffCoef == 0 and Lance:
        currDmg+=LanceIncendiaire()
    elif not Lance and not Muspel:
        Lance = True
    
    #Buff the lanceBuff if needed, sometime it can be 0 but anyway
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


# =============
# Main
# =============

SPELLREQ = {0 :{"id" : 0, "fct" :LanceAIncendie, "name" : "LanceAIncendie","pa" : 3 ,"max" : 3 },\
            1 :{"id" : 1, "fct" : MoulinRouge, "name" : "MoulinRouge","pa" : 3,"max" :1},\
            2 :{"id" : 2, "fct" : Fente, "name" : "Fente","pa" : 2,"max" :1},\
            3 :{"id" : 3, "fct" : FerRouge, "name" : "FerRouge","pa" : 3,"max" :2},\
            4 :{"id" : 4, "fct" : EstocBrulant, "name" : "EstocBrulant","pa" : 3,"max" :2},\
            5 :{"id" : 5, "fct" : Muspel, "name" : "Muspel","pa" : 4,"max" :1},\
            6 :{"id" : 6, "fct" : Maelstom, "name" : "Maelstom","pa" : 3,"max" :2},\
            }



def stillLaunch(currStep):
    if currStep.paRem < MINSPELLCOST:
        return False
    #Pas besoin de regarder les cumuls max
    #ça aurait été une condition d'arrêt s'il était possible de lancer tout les sorts avec encore des PA
    return True
    
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
        if stillLaunch(thisStep):
            buildTree(thisStep) #build tree from this step
        
    

#Il faudra juste compare les plus gros résulats
strat = Step(0,"Start",PA,[0,0,0,0,0,0,0])
buildTree(strat)
print_tree(strat,0)

