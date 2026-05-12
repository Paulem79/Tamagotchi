import random, time
import modules.sante as sante
import modules.config as config

faim: int = 100
# fonction de nourritur renvoi la quantitté de faim et la mort si faim=0
def nourriture() -> tuple[str, int]:
    if faim < 1:
        config.tuer("mort de faim!")
        return ("Faim :", faim)
    
    digerer()
    return ("Faim :", faim)


def digerer():
    global faim
    malade = sante.malade
    if malade==True :
        faim -= random.randint(1, 5)
    else :
        faim -= 1


def nourrir():
    quantite = random.randint(30, 40)
    global faim
    malade = sante.malade
    if faim > 130 and faim < 150 and not malade:
        print("Trop manger !")
        faim += quantite
    if faim > 150:
        print("Bleurg !")
        faim = faim - random.randint(30, 50)
    elif malade and faim > 50 :
        print("Bleurg !")
        faim = faim - random.randint(30, 50)
    else:
        faim += quantite

