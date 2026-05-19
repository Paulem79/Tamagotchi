import pygame as pg
import random

sons = {
    "mort": "sons/mort.mp3",
    "dae": "sons/dae.mp3",
    "manger": [
        "sons/manger1.mp3",
        "sons/manger2.mp3",
        "sons/manger3.mp3",
        "sons/manger4.mp3",
        "sons/manger5.mp3",
        "sons/manger6.mp3",
    ],
    "boire": [
        "sons/boire1.mp3",
        "sons/boire2.mp3",
        "sons/boire3.mp3",
    ],
    "sport": [
        "sons/sport1.mp3",
        "sons/sport2.mp3",
        "sons/sport3.mp3",
        "sons/sport4.mp3",
        "sons/sport5.mp3",
        "sons/sport6.mp3",
        "sons/sport7.mp3",
    ]
}

def jouer_son(nom: str):
    if nom in sons:
        fichier = sons[nom]

        # Si c'est une liste, on choisit au hasard un son
        if isinstance(fichier, list):
            fichier = random.choice(fichier)

        pg.mixer.music.load(fichier)
        pg.mixer.music.play()
    else:
        print("Son inconnu :", nom)