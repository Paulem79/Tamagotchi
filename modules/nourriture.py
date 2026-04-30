import random, time

faim = 100


def nourriture():
    digerer()
    print(f"Faim: {faim}")


def digerer():
    global faim
    faim -= 1


def nourrir(quantite: int):
    global faim
    faim += quantite
