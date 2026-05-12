# Créé par paulem, le 12/05/2026 en Python 3.7
import pygame as pg
from pygame.locals import *
from typing import Callable

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

pg.init()

fenetre = (800, 600)
ecran = creer_ecran(fenetre)

charger_arriere_plan(ecran)

button_pos = (500,300)
button_taille = (20,10)
charger_bouton(ecran, button_pos, button_taille, lambda: print("cliqué !"))

pg.display.flip() # rafraîchir l’écran

jouer = True
while jouer:
    for event in pg.event.get():
        if event.type == QUIT:
            jouer = False
        if event.type == KEYDOWN:
            print("dd")
        if event.type == MOUSEBUTTONDOWN:
            pos = event.pos
            actionner_boutons(pos)

pg.quit()