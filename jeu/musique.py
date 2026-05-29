import pygame as pg
import random

from jeu.deobfuscateur import deobfusquer

volume_musique: float = 1.0

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
    ],
    "hehe": "sons/hehe.mp3",
}

musiques = ["sons/fluffing_a_duck.mp3", "sons/monkeys_spinning_monkeys.mp3", "sons/sneaky_snitch.mp3"]


def jouer_son(nom: str):
    if pg.mixer.get_init() is None:
        return

    if nom in sons:
        fichier = sons[nom]

        # Si c'est une liste, on choisit au hasard un son
        if isinstance(fichier, list):
            fichier = random.choice(fichier)

        #pg.mixer.music.load(fichier)
        pg.mixer.Channel(1).play(pg.mixer.Sound(fichier))
    else:
        print("Son inconnu :", nom)

def set_volume_musique(vol: float):
    global volume_musique
    # C'est clamp, donc entre 0 et 1
    volume_musique = max(0.0, min(1.0, vol))
    # Si y'a bien une sortie audio, définir le volume du canal de musique
    if pg.mixer.get_init() is not None:
        pg.mixer.Channel(0).set_volume(volume_musique)

def get_volume_musique() -> float:
    return volume_musique

def jouer_musique():
    if pg.mixer.get_init() is None:
        return

    # Créer le canal de musique
    canal = pg.mixer.Channel(0)
    canal.set_volume(volume_musique)
    canal.set_endevent(pg.USEREVENT + 1)

    # 1% de chance de jouer le son secret
    if random.randint(1, 100) == 1:
        try:
            buffer = deobfusquer("sons/letih.mp3")
            son = pg.mixer.Sound(buffer)
            canal.play(son)
            return
        except FileNotFoundError:
            pass

    # Jouer sur channel 0 pour la musique de fond, pour pas bloquer les autres sons et inversement avec volume 0.5
    # Passer à un autre son quand la musique actuelle est terminée
    fichier = random.choice(musiques)
    son = pg.mixer.Sound(fichier)
    canal.play(son)
