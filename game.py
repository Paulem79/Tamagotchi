# Créé par paulem, le 12/05/2026 en Python 3.7
import pygame as pg
from pygame.locals import *
from typing import Callable
import asyncio
import main
import modules.nourriture as nourriture
import modules.eau as eau
import modules.sante as sante
import modules.sport as sport
import modules.config as config

elements: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []

def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    ecran = pg.display.set_mode(fenetre)
    return ecran

def charger_arriere_plan(ecran: pg.Surface, nom: str) -> None:
    """Charge l'arrière plan de jeu"""
    fenetre = (ecran.get_width(), ecran.get_height())
    
    background = pg.image.load(f"images/{nom}").convert()
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


async def game_loop():
    """La boucle de jeu asynchrone"""
    pg.init()
    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)
    
    charger_bouton(ecran, (20, 30), (70, 50), nourriture.nourrir())
    charger_bouton(ecran, (90, 80), (70, 50), eau.boire())
    charger_bouton(ecran, (160, 130), (70, 50), sante.guerir())
    charger_bouton(ecran, (230, 180), (70, 50), sport.sport())
    
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
        
        # Mettre à jour le rendu pygame
        pg.display.update()

        # Attente pour synchroniser avec la logique principale
        await main.attente_ms()

    pg.quit()

async def run_all():
    """Lance tout en parallèle"""
    # On lance main() et la boucle de jeu en même temps
    await asyncio.gather(
        main.main(),
        game_loop()
    )

if __name__ == "__main__":
    asyncio.run(run_all())