import random
import modules.nourriture as nourriture
import modules.eau as water

etat_de_sante: int = 100


def sport_decompte():
    global etat_de_sante
    etat_de_sante = etat_de_sante - 1
    print("etat de sante :", etat_de_sante)


def sport():
    global etat_de_sante
    etat_de_sante = etat_de_sante + random.randint(1, 30)
    nourriture.faim-=random.randint(10,20)
    water.eau-=random.randint(5,10)
    
