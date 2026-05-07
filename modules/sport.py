import random

etat_de_sante = 100


def sport_decompte():
    global etat_de_sante
    etat_de_sante = etat_de_sante - 1
    print("etat de sante :", etat_de_sante)


def sport():
    global etat_de_sante
    etat_de_sante = etat_de_sante + random.randint(1, 50)
