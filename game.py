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

elements: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []

# Obligé pour écrire texte
pg.font.init()


def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    ecran = pg.display.set_mode(fenetre)
    return ecran


def charger_arriere_plan(ecran: pg.Surface, nom: str) -> None:
    """Charge l'arrière plan de jeu"""
    fenetre = (ecran.get_width(), ecran.get_height())

    background = pg.image.load(f"images/{nom}").convert()
    background = pg.transform.scale(background, fenetre)

    # coller le rectangle par dessus en (0,0)
    ecran.blit(background, (0, 0))


# --- MODIFICATION ICI : Ajout du paramètre 'texte' ---
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


def actionner_boutons(pos: tuple[int, int]):
    """Actionne les boutons en fonction de la position de la souris"""
    for element in elements:
        position, taille, action = element
        if (position[0] <= pos[0] < position[0] + taille[0]) and (
            position[1] <= pos[1] < position[1] + taille[1]
        ):
            action()
            break


async def game_loop():
    """La boucle de jeu asynchrone"""
    pg.init()
    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)

    pg.display.flip()

    jouer = True
    while jouer:
        # Les évènements
        for event in pg.event.get():
            if event.type == QUIT:
                jouer = False
            if event.type == MOUSEBUTTONDOWN:
                actionner_boutons(event.pos)

        arriere_plan = main.obtenir_resultat("Temps :")

        if arriere_plan == None:
            arriere_plan = "background.jpg"

        charger_arriere_plan(ecran, arriere_plan)
        charger_bouton(ecran, (20, 30), (100, 50), "Manger", nourriture.nourrir)
        charger_bouton(ecran, (130, 30), (100, 50), "Boire", eau.boire)
        charger_bouton(ecran, (240, 30), (100, 50), "Soigner", sante.guerir)
        charger_bouton(ecran, (350, 30), (100, 50), "Sport", sport.sport)

        # Mettre à jour rendu
        pg.display.update()

        # Attente pour être avec la boucle principale
        await main.attente_ms()

    pg.quit()


async def run_all():
    """Lance tout en parallèle"""
    await asyncio.gather(main.main(), game_loop())


if __name__ == "__main__":
    asyncio.run(run_all())
