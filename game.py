# Créé par paulem, le 12/05/2026 en Python 3.7
import asyncio
from typing import Callable
import pygame as pg
from pygame.locals import *

import main
import modules.config as config
import modules.eau as eau
import modules.nourriture as nourriture
import modules.sante as sante
import modules.sport as sport
import modules.DAE as DAE

# Contient la liste des éléments cliquables, avec leur position, taille et action associée
elements: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []


def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    # Dire qu'on veut cette taille de fenêtre
    ecran = pg.display.set_mode(fenetre)
    return ecran


"""
aspect_scale.py - Scaling surfaces keeping their aspect ratio
Raiser, Frank - Sep 6, 2k++
crashchaos at gmx.net

This is a pretty simple and basic function that is a kind of
enhancement to pygame.transform.scale. It scales a surface
(using pygame.transform.scale) but keeps the surface's aspect
ratio intact. So you will not get distorted images after scaling.
A pretty basic functionality indeed but also a pretty useful one.

Usage:
is straightforward.. just create your surface and pass it as
first parameter. Then pass the width and height of the box to
which size your surface shall be scaled as a tuple in the second
parameter. The aspect_scale method will then return you the scaled
surface (which does not neccessarily have the size of the specified
box of course)

Dependency:
a pygame version supporting pygame.transform (pygame-1.1+)
"""
# Vous en occupez pas, c'est importé d'internet
def aspect_scale(img: pg.Surface, bx: int, by: int):
    """Scales 'img' to fit into box bx/by.
    This method will retain the original image's aspect ratio"""
    ix, iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx / float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by / float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by / float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx / float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pg.transform.scale(img, (sx, sy))


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
    police = pg.font.SysFont("Arial", 20)
    # Rendu texte en noir + anti aliasing
    texte_surface = police.render(texte, True, (0, 0, 0))

    # Récupérer dimensions texte
    texte_rect = texte_surface.get_rect()
    # Placer centre texte sur centre bouton
    texte_rect.center = (taille[0] // 2, taille[1] // 2)

    # Mettre texte sur bouton
    button.blit(texte_surface, texte_rect)

    # Mettre image + texte sur ecran
    ecran.blit(button, position)

    # Enregistrer pour détection clics
    elements.append((position, taille, action))

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
    for element in elements:
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
    """La boucle de jeu asynchrone"""
    pg.init
    # Obligé pour écrire texte
    pg.font.init()
    
    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)

    pg.display.flip()

    jouer = True
    while jouer:
        # Vider les éléments pour plus détruire les performances
        elements.clear()
    
        # Les évènements
        for event in pg.event.get():
            # Si on ferme la fenêtre, on arrête le jeu
            if event.type == QUIT:
                jouer = False
            # Si on clique, on actionne les boutons sous la souris
            if event.type == MOUSEBUTTONDOWN:
                actionner_boutons(event.pos)

        # L'arrière plan se basera sur ce que nous renvoie le module de météo
        arriere_plan = main.obtenir_resultat("Temps :")

        # Si la météo ne s'est pas encore exécutée, on met une image par défaut
        if arriere_plan == None:
            arriere_plan = "background.jpg"

        charger_arriere_plan(ecran, arriere_plan)
        charger_personnage(ecran, config.mort)
        charger_bouton(ecran, (20, 30), (100, 50), "Manger", nourriture.nourrir)
        charger_bouton(ecran, (130, 30), (100, 50), "Boire", eau.boire)
        charger_bouton(ecran, (240, 30), (100, 50), "Soigner", sante.guerir)
        charger_bouton(ecran, (350, 30), (100, 50), "Sport", sport.sport)
        # Si le jeu demande le défibrilatteur, on le met
        if DAE.demande_defibrilatteur:
            charger_bouton(ecran, (460, 30), (100, 50), "Défibrilatteur", DAE.actionner)

        # On met les barres d'état
        barre_etat(ecran, (750, 300), sport.etat_de_sante, (0, 255, 0), (0, 150, 0), (255, 0, 0))
        barre_etat(ecran, (700, 300), nourriture.faim, (200, 150, 0), (255, 255, 0), (255, 0, 0))
        barre_etat(ecran, (650, 300), eau.eau, (0, 0, 255), (0, 255, 255), (255, 10, 60))

        # Mettre à jour rendu
        pg.display.update()

        # Attente pour être avec la boucle principale
        await main.attente_ms()

    pg.quit()


async def run_all():
    """Lance tout en parallèle"""
    await asyncio.gather(main.main(), game_loop())


# Tout exécuter si on est le fichier principal (python game.py)
if __name__ == "__main__":
    asyncio.run(run_all())