import random
import config


# fonction de nourritur renvoi la quantitté de faim et la mort si faim=0
def nourriture() -> tuple[str, int]:
    if config.faim < 1:
        config.tuer("mort de faim!")
        return ("Faim :", config.faim)
    
    digerer()
    return ("Faim :", config.faim)


def digerer():
    malade = config.malade
    if malade:
        config.faim -= random.randint(1, 5)
    else :
        config.faim -= 1

def vomir():
    print("Bleurg !")
    config.faim = config.faim - random.randint(30, 50)


def nourrir():
    quantite = random.randint(30, 40)
    malade = config.malade
    if config.faim > 130 and config.faim < 150 and not malade:
        print("Trop manger !")
        config.faim += quantite
    if config.faim > 150:
        vomir()
    elif malade and config.faim > 50 :
        vomir()
    else:
        config.faim += quantite

