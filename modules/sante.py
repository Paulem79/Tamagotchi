import random
#import modules.sport as sport

malade: bool = False


# fonction de santé
# TODO: Rajouter la possibilité de se soigner
def maladie() -> tuple[str, bool]:
    # TODO: Régler circular import par migration dans config.py
    #etat_de_sante = sport.etat_de_sante
    #if random.randint(0, etat_de_sante) == 0:
    #    global malade
    #    malade = True
    return ("Malade :", malade)


def guerir():
    global malade
    malade = False
