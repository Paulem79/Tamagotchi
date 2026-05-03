import random, time

faim = 100


def nourriture():
    digerer()
    print(f"Faim: {faim}")


def digerer():
    global faim
    faim -= 1
    if faim < 0:
        print("Mort")


def nourrir():
    quantite = random.randint(30, 40)
    global faim
    if faim > 130 and faim < 150:
        print("Trop manger !")
        faim += quantite
    if faim > 150:
        print("Bleurg !")
        faim = faim - random.randint(30, 50)
    else:
        faim += quantite
