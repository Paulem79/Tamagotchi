"""
Note: La manière dont l'interface de jeu a été faite n'a pas été conçu pour être optimisée et efficace, au contraire,
en termes de performances, on pourrait avoir eu mieux. Elle a surtout été conçue pour être facilement modifiable par
nous trois, sinon ça aurait été une anarchie de classes dans tous les sens, et ce n'était pas le but.
"""

import asyncio
from typing import Callable

import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN, QUIT

import config
from interface.aspect_scale import aspect_scale
import main
import modules.DAE as DAE
import modules.eau as eau
import modules.nourriture as nourriture
import modules.sante as sante
import modules.sport as sport

# Contient la liste des boutons, avec leur position, taille et action associée
boutons: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []


def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    # Dire qu'on veut cette taille de fenêtre
    ecran = pg.display.set_mode(fenetre)
    return ecran


def charger_arriere_plan(ecran: pg.Surface, nom: str) -> None:
    """Charge l'arrière plan de jeu"""
    # Obtenir les dimensions de l'écran
    fenetre = (ecran.get_width(), ecran.get_height())

    # Charger l'image et la redimensionner aux dimensions de la fenêtre
    background = pg.image.load(f"images/{nom}").convert()
    background = pg.transform.scale(background, fenetre)

    # coller l'arrière plan sur toute la fenêtre
    ecran.blit(background, (0, 0))


def charger_personnage(ecran: pg.Surface, mort: bool) -> None:
    """Charge le personnage de jeu"""
    # Si mort, on charge l'image de mort
    image = "poyo_Idle.png"
    if mort:
        image = "poyo_dead.png"

    # Charger l'image et la redimensionner
    personnage = pg.image.load(f"images/{image}").convert_alpha()
    personnage = aspect_scale(personnage, 400, 400)
    # coller le personnage sur l'écran
    ecran.blit(personnage, (200, 300))


def charger_bouton(
    ecran: pg.Surface,
    position: tuple[int, int],
    taille: tuple[int, int],
    texte: str,
    action: Callable[[], None],
):
    """Charge un bouton avec du texte centré sur l'écran"""
    # Charger et redimensionner bouton
    button = pg.image.load("images/button.png").convert_alpha()
    button = pg.transform.scale(button, taille)

    # Créer texte Arial 20px
    police = pg.font.Font('polices/Minecraft.ttf', 20)
    # Rendu texte en noir
    texte_surface = police.render(texte, False, (0, 0, 0))

    # Récupérer dimensions texte
    texte_rect = texte_surface.get_rect()
    # Placer centre texte sur centre bouton
    texte_rect.center = (taille[0] // 2, taille[1] // 2)

    # Mettre texte sur bouton
    button.blit(texte_surface, texte_rect)

    # Mettre image + texte sur ecran
    ecran.blit(button, position)

    # Enregistrer pour détection clics
    boutons.append((position, taille, action))

def barre_etat(ecran: pg.Surface, position: tuple[int, int], valeur: int, cbase:tuple[int,int,int], cmilieu: tuple[int, int, int], cfin:tuple[int,int,int]):
    # Position x et y de la jauge depuis le tuple
    jauge_x, jauge_y = position
    # Largeur de la jauge (en x)
    jauge_largeur = 30
    # Hauteur de la jauge (en y)
    jauge_hauteur = 300
    # Contenu de la jauge, entre 0 et 100 en général
    # TODO: On laisse déborder les jauges car c'est drôle ? sinon, mettre min(valeur / 100, 1)
    ratio = valeur / 100
    # Hauteur du contenu de la jauge
    hauteur_dynamique = jauge_hauteur * ratio
    # Couleur de la jauge, si > 60%, si > 30%, autre couleur sinon
    couleur_jauge = cbase if ratio > 0.6 else cmilieu if ratio > 0.3 else cfin

    # Position y du contenu de la jauge, un offset pour que la jauge soit en bas
    jauge_y_dynamique = jauge_y + (jauge_hauteur - hauteur_dynamique)

    # Dessiner le fond de la jauge
    pg.draw.rect(ecran, (0, 0, 0), (jauge_x, jauge_y, jauge_largeur, jauge_hauteur))
    # Dessiner le contenu de la jauge
    pg.draw.rect(ecran, couleur_jauge, (jauge_x,jauge_y_dynamique, jauge_largeur, hauteur_dynamique))
    # Dessiner le contour de la jauge
    pg.draw.rect(ecran, (0, 0, 0), (jauge_x, jauge_y, jauge_largeur, jauge_hauteur), 2)


def actionner_boutons(pos: tuple[int, int]):
    """Actionne les boutons en fonction de la position de la souris"""
    for element in boutons:
        # Récupérer la position, la taille et l'action de l'élément
        position, taille, action = element
        # Vérifier si la position de la souris est dans l'élément
        if (position[0] <= pos[0] < position[0] + taille[0]) and (
            position[1] <= pos[1] < position[1] + taille[1]
        ):
            # Exécuter l'action
            action()
            break


async def game_loop():
    """boucle de jeu en asynchrone (parallèle)"""
    pg.init()
    # Obligé pour écrire texte
    pg.font.init()
    
    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)

    pg.display.flip()
    config.fenetre_ouverte = True

    while config.fenetre_ouverte:
        # Détruit les boutons existants pour éviter de les dupliquer
        boutons.clear()

        # L'arrière plan se basera sur ce que nous renvoie le module de météo
        arriere_plan = main.obtenir_resultat("Temps :")

        # Si la météo ne s'est pas encore exécutée, on met une image par défaut
        if arriere_plan is None:
            arriere_plan = "background.jpg"

        charger_arriere_plan(ecran, arriere_plan)
        charger_personnage(ecran, config.mort)

        if config.jeu_en_cours:
            charger_bouton(ecran, (20, 30), (100, 50), "Manger", nourriture.nourrir)
            charger_bouton(ecran, (130, 30), (100, 50), "Boire", eau.boire)
            charger_bouton(ecran, (240, 30), (100, 50), "Soigner", sante.guerir)
            charger_bouton(ecran, (350, 30), (100, 50), "Sport", sport.sport)
            # Si le jeu demande le défibrilatteur, on le met
            if config.demande_defibrillateur and config.mort:
                charger_bouton(ecran, (460, 30), (100, 50), "Defibrilatteur", DAE.actionner)

            # On met les barres d'état
            barre_etat(ecran, (750, 300), config.etat_de_sante, (0, 255, 0), (0, 150, 0), (255, 0, 0))
            barre_etat(ecran, (700, 300), config.faim, (200, 150, 0), (255, 255, 0), (255, 0, 0))
            barre_etat(ecran, (650, 300), config.eau, (0, 0, 255), (0, 255, 255), (255, 10, 60))

        # Mettre à jour rendu
        pg.display.update()

        # Evenements
        for event in pg.event.get():
            # Si on ferme la fenêtre, on arrête le jeu
            if event.type == QUIT:
                config.stopper_tout()
            # Si on clique, on actionne les boutons sous la souris
            if event.type == MOUSEBUTTONDOWN:
                actionner_boutons(event.pos)

        # Attente pour être avec la boucle principale
        await main.attente_ms()

    pg.quit()


async def run_all():
    """Lance tout en parallèle"""
    await asyncio.gather(main.main(), game_loop())


# Tout exécuter si on est le fichier principal (python game.py)
if __name__ == "__main__":
    asyncio.run(run_all())