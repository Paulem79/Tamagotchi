# Créé par paulem, le 12/05/2026 en Python 3.7
import pygame as pg
from pygame.locals import *
from typing import Callable
import asyncio
from main import main
import modules.nourriture as nourriture
import modules.config as config

elements: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []

def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    ecran = pg.display.set_mode(fenetre)
    return ecran

def charger_arriere_plan(ecran: pg.Surface) -> None:
    """Charge l'arrière plan de jeu"""
    fenetre = (ecran.get_width(), ecran.get_height())
    
    background = pg.image.load("images/pluie.png").convert()
    background = pg.transform.scale(background,fenetre)
    
    # coller le rectangle par dessus en (0,0)
    ecran.blit(background,(0,0))

def charger_bouton(ecran: pg.Surface, position: tuple[int, int], taille: tuple[int, int], action: Callable[[], None]):
    """Charge un bouton sur l'écran"""
    # charger l'image, convert_alpha permet la transparence
    button = pg.image.load("images/button.png").convert_alpha()
    button = pg.transform.scale(button,taille)
    ecran.blit(button,position)
    elements.append((position, taille, action))

def actionner_boutons(pos: tuple[int, int]):
    """Actionne les boutons en fonction de la position de la souris"""
    for element in elements:
        position, taille, action = element
        if (position[0] <= pos[0] < position[0] + taille[0]) and (position[1] <= pos[1] < position[1] + taille[1]) :
            action()
            break

def nourrir_bouton():
    print("nourrir")
    nourriture.nourrir()


async def game_loop():
    """La boucle de jeu asynchrone"""
    pg.init()
    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)

    charger_arriere_plan(ecran)
    charger_bouton(ecran, (500, 300), (20, 10), nourrir_bouton)
    pg.display.flip()

    jouer = True
    while jouer:
        # 1. Gestion des événements Pygame
        for event in pg.event.get():
            if event.type == QUIT:
                jouer = False
            if event.type == MOUSEBUTTONDOWN:
                actionner_boutons(event.pos)

        # 2. Rendu Pygame
        pg.display.update()

        # 3. C'est ici l'astuce : on rend la main à asyncio 
        # pour que les autres tâches (ex: main()) puissent s'exécuter
        await asyncio.sleep(0.01) 

    pg.quit()

async def run_all():
    """Lance tout en parallèle"""
    # On lance main() et la boucle de jeu en même temps
    await asyncio.gather(
        main(),
        game_loop()
    )

if __name__ == "__main__":
    asyncio.run(run_all())