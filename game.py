"""
Note: La manière dont l'interface de jeu a été faite n'a pas été conçu pour être optimisée et efficace, au contraire,
en termes de performances, on pourrait avoir eu mieux. Elle a surtout été conçue pour être facilement modifiable par
nous trois, sinon ça aurait été une anarchie de classes dans tous les sens, et ce n'était pas le but.
"""
import asyncio
from typing import Callable
import aiohttp
import random

import pygame as pg
from pygame.constants import QUIT

import config
import main
import modules.DAE as DAE
import modules.eau as eau
import modules.nourriture as nourriture
import modules.sante as sante
import modules.sport as sport
from jeu.aspect_scale import aspect_scale
from jeu.deobfuscateur import deobfusquer
from jeu.musique import jouer_son, jouer_musique, get_volume_musique, set_volume_musique

leaderboard_data: list = []
pseudo_joueur: str = "POYO"

POLICE_MINECRAFT: str = "polices/pixel.otf"

# Contient la liste des boutons, avec leur position, taille et action associée
boutons: list[tuple[tuple[int, int], tuple[int, int], Callable[[], None]]] = []

# Voir dans le début de game_loop
IMAGES: dict[str, pg.Surface | None] = {
    "bouton": None,
    "poyo_idle": None,
    "poyo_sick": None,
    "poyo_dead": None,
    "lejedupandu": None
}

apres_mort_fini: bool = False


def creer_ecran(fenetre: tuple[int, int]) -> pg.Surface:
    """Crée l'écran de jeu"""
    # Dire qu'on veut cette taille de fenêtre
    ecran = pg.display.set_mode(fenetre, pg.RESIZABLE)
    return ecran


def charger_arriere_plan(ecran: pg.Surface, nom: str) -> None:
    """Charge l'arrière plan de jeu"""
    # Obtenir les dimensions de l'écran
    fenetre = (ecran.get_width(), ecran.get_height())
    charger_image(ecran, nom, fenetre, (0, 0))


def charger_image(ecran: pg.Surface, nom: str, taille: tuple[int, int], position: tuple[int, int]) -> None:
    """Charge une image redimensionnée à une position donnée"""
    # Charger l'image
    image = pg.image.load(f"images/{nom}").convert_alpha()
    # Redimensionner l'image
    image = pg.transform.scale(image, taille)
    # Coller l'image sur l'écran à la position donnée
    ecran.blit(image, position)

compteurDepla=0

def charger_personnage(ecran: pg.Surface, mort: bool) -> None:
    """Charge le personnage de jeu"""
    # Si mort, on charge l'image de mort
    personnage = IMAGES["poyo_idle"]
    if config.lejedupandu:
        personnage = IMAGES["lejedupandu"]
    elif mort:
        personnage = IMAGES["poyo_dead"]
    elif config.malade:
        personnage = IMAGES["poyo_sick"]

    if personnage is None:
        return

    taille = (400, 400)
    position=(0, ecran.get_height()//2 - taille[1]//3)

    if not config.mort :
        deplacement = []
        for i in range(0,200,10):
            deplacement.append(i)
        for o in range(0,200,10):
            deplacement.append(200-o)
    
        global compteurDepla
        position = (deplacement[0+compteurDepla], ecran.get_height()//2 - taille[1]//3)
        compteurDepla=compteurDepla+1
        if compteurDepla==len(deplacement) :
            compteurDepla=0
    else :
        position = (100, ecran.get_height()//2 - taille[1]//3)
    # redimensionner l'image du personnage
    personnage = aspect_scale(personnage, taille[0], taille[1])
    # coller le personnage sur l'écran
    ecran.blit(personnage, position)


def charger_bouton(
    ecran: pg.Surface,
    position: tuple[int, int],
    taille: tuple[int, int],
    texte: str,
    action: Callable[[], None],
):
    """Charge un bouton avec du texte centré sur l'écran et gère l'enfoncement"""
    # Récupérer la position x, y et la taille
    x, y = position
    largeur, hauteur = taille

    # Obtenir la position de la souris et l'état des clics
    souris_pos = pg.mouse.get_pos()
    clic_souris = pg.mouse.get_pressed()

    # Vérifier si la souris survole le bouton et que le clic gauche est enfoncé
    enfonce = False
    if (x <= souris_pos[0] < x + largeur) and (y <= souris_pos[1] < y + hauteur):
        if clic_souris[0]:
            enfonce = True

    # Si enfoncé, on décale la position de rendu de 3 pixels
    position_rendu = (x + 3, y + 3) if enfonce else (x, y)

    # Charger et redimensionner bouton
    button = IMAGES["bouton"]
    if button is None:
        return
    button = pg.transform.scale(button, taille)

    # Créer texte Arial 20px
    police = pg.font.Font(POLICE_MINECRAFT, 20)
    # Rendu texte en noir
    texte_surface = police.render(texte, False, (0, 0, 0))

    # Récupérer dimensions texte
    texte_rect = texte_surface.get_rect()
    # Placer centre texte sur centre bouton
    texte_rect.center = (taille[0] // 2, taille[1] // 2)

    # Mettre texte sur bouton
    button.blit(texte_surface, texte_rect)

    # Mettre image + texte sur ecran à la position calculée
    ecran.blit(button, position_rendu)

    # Enregistrer pour détection clics
    boutons.append((position, taille, action))

def barre_etat(
    ecran: pg.Surface,
    offset_x: int,
    valeur: int,
    cbase: tuple[int, int, int],
    cmilieu: tuple[int, int, int],
    cfin: tuple[int, int, int],
):
    # Largeur de la jauge (en x)
    jauge_largeur = 30
    # Hauteur de la jauge (en y)
    jauge_hauteur = 300
    
    # Position x et y de la jauge depuis le tuple
    jauge_x = ecran.get_width() - offset_x
    jauge_y = ecran.get_height() - jauge_hauteur
    
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
    pg.draw.rect(
        ecran,
        couleur_jauge,
        (jauge_x, jauge_y_dynamique, jauge_largeur, hauteur_dynamique),
    )
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


async def apres_mort(ecran: pg.Surface):
    # Bouton rejouer
    charger_bouton(ecran, (20, 30), (100, 50), "Rejouer", config.redemarrer)
    
    # Texte GAME OVER
    police = pg.font.Font(POLICE_MINECRAFT, 50)
    texte_surface = police.render("GAME OVER", False, (255, 0, 0))
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (ecran.get_width() // 2, (ecran.get_height() // 2) - 120)
    ecran.blit(texte_surface, texte_rect)
    
    # Texte raison de mort
    texte_surface = police.render(f"Vous êtes mort de {config.mort_raison}", False, (255, 255, 255))
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (ecran.get_width() // 2, (ecran.get_height() // 2) - 60)
    ecran.blit(texte_surface, texte_rect)

    # Texte score
    texte_surface = police.render(f"Score: {config.score}", False, (255, 255, 255))
    texte_rect = texte_surface.get_rect()
    texte_rect.center = (ecran.get_width() // 2, ecran.get_height() // 2)
    ecran.blit(texte_surface, texte_rect)

    # Affichage du classement
    police_titre = pg.font.Font(POLICE_MINECRAFT, 40)
    titre_lb = police_titre.render("Top classement", False, (255, 255, 255))
    titre_rect = titre_lb.get_rect(center=(ecran.get_width() // 2, ecran.get_height() // 2 + 50))
    ecran.blit(titre_lb, titre_rect)

    police_score = pg.font.Font(POLICE_MINECRAFT, 30)
    y_offset = 100

    # Itérer sur la liste récupérée par l'api
    # TODO: ça trie bien dans l'ordre décroissant des scores ? pas sûr
    for index, entre in enumerate(leaderboard_data):
        texte = f"{index + 1}. {entre['pseudo']} : {entre['score']}"
        texte_surface = police_score.render(texte, False, (255, 255, 255))
        texte_rect = texte_surface.get_rect(center=(ecran.get_width() // 2, (ecran.get_height() // 2) + y_offset))
        ecran.blit(texte_surface, texte_rect)
        y_offset += 40

async def gerer_score_et_leaderboard():
    global leaderboard_data
    url_base = "http://home.paulem.net:3035"

    async with aiohttp.ClientSession() as session:
        # Envoyer le score actuel
        await session.post(f"{url_base}/score", json={
            "pseudo": pseudo_joueur,
            "score": config.score
        })

        # Récupérer les nouveaux meilleurs scores
        async with session.get(f"{url_base}/leaderboard") as response:
            if response.status == 200:
                leaderboard_data = await response.json()

def evenements_communs(event: pg.event.Event):
    """Gérer les événements pygame communs à tout le jeu (menu principal + jeu) (pour éviter de dupliquer du code)"""
    # Envoyé par jouer musique à la fin de la première musique, pour enchaîner les musiques
    if event.type == pg.USEREVENT + 1:
        jouer_musique()

    # Si on ferme la fenêtre, on arrête le jeu
    if event.type == QUIT:
        config.stopper_tout()

    # Si on relâche le clic gauche, on actionne les boutons sous la souris
    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
        actionner_boutons(event.pos)

    konami(event)


# Source - https://stackoverflow.com/a/66967741
# Posted by Alderven
# Retrieved 2026-05-21, License - CC BY-SA 4.0
# Et modifié par Paulem
CODE = [pg.K_UP, pg.K_UP, pg.K_DOWN, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_LEFT,
pg.K_RIGHT, pg.K_b, pg.K_a]
code = []
index = 0
running = True

def konami(event: pg.event.Event):
    """Code Konami pour le fun, à activer en appuyant sur L"""
    global code, index
    # Si la touche appuyée correspond à la prochaine touche du code, on continue, sinon on réinitialise
    if event.type == pg.KEYDOWN:
        if event.key == CODE[index]:
            # Petit print pour indiquer tout ça tout ça
            print(f"Touche correcte pour le code Konami ({index + 1}/{len(CODE)})")
            code.append(event.key)
            index += 1
            # Si on a fini tout le code, on réinitialise tout et on active la fonction secrète
            if code == CODE:
                index = 0
                code = []
                config.lejedupandujaje()
                jouer_son("hehe")
        # Si jamais on se trompe, on réinitialise le code
        else:
            code = []
            index = 0


async def game_loop():
    """boucle de jeu en asynchrone (parallèle)"""
    global apres_mort_fini, pseudo_joueur
    
    # Initialisation de pygame
    pg.init()
    # Obligé pour écrire texte
    pg.font.init()
    # Idem, obligé pour lire musique
    # Si audio, pas sur replit par exemple
    if pg.mixer.get_init() is not None:
        pg.mixer.init()

    fenetre = (800, 600)
    ecran = creer_ecran(fenetre)

    pg.display.flip()
    config.fenetre_ouverte = True

    # Améliore les performances en évitant de charger les images à chaque frame
    IMAGES["bouton"] = pg.image.load("images/button.png").convert_alpha()
    IMAGES["poyo_idle"] = pg.image.load("images/poyo_Idle.png").convert_alpha()
    IMAGES["poyo_dead"] = pg.image.load("images/poyo_dead.png").convert_alpha()
    IMAGES["poyo_sick"] = pg.image.load("images/poyo_Idle_sick.png").convert_alpha()
    IMAGES["lejedupandu"] = pg.image.load(deobfusquer("images/lejedupandu.png")).convert_alpha()

    jouer_musique()

    # Variable pour savoir si le slider de volume est en train d'être bougé, pour éviter que ça bouge tout seul...
    slider_bouge = False
    # Rectangle du slider de volume musique, on le définit une fois pour éviter de le recréer à chaque frame car il est fixe
    slider_bg_rect = pg.Rect(500, 55, 200, 10)

    # Compteur pas très précis car si le pc est lent, ça va être plus lent
    menu_ms = 0

    # Menu principal
    while config.fenetre_ouverte and config.pres_jeu:
        menu_ms += 1
        # Fond d'écran du menu principal
        charger_arriere_plan(ecran, "soleil.png")

        # Titre du jeu
        charger_image(ecran, "titre.png", (666, 375), (ecran.get_width() // 2 - 333, 100))
        # Texte dessus
        police = pg.font.Font(POLICE_MINECRAFT, 80)
        
        cligne = " " if menu_ms % 50 < 25 else "_"
        
        texte_surface = police.render(f"{pseudo_joueur}{cligne} !", False, (255, 0, 0))
        ecran.blit(texte_surface, (ecran.get_width() // 2 - texte_surface.get_width() // 2 + 30, 170))
        # Sous texte
        police = pg.font.Font(POLICE_MINECRAFT, 40)
        texte_surface = police.render("Découvre la souffrance !", False, (255, 0, 0))
        ecran.blit(texte_surface, (ecran.get_width() // 2 - texte_surface.get_width() // 2, 380))

        # Bouton jouer
        charger_bouton(ecran, (20, 30), (100, 50), "Jouer", config.jouer)

        # Bouton mode difficile
        charger_bouton(ecran, (130, 30), (100, 50), "Facile" if config.difficile else "Difficile", config.activer_difficile)

        # Dessiner le slider de volume
        vol = get_volume_musique()
        pg.draw.rect(ecran, (255, 100, 100), slider_bg_rect)
        slider_btn_x = slider_bg_rect.x + int(vol * slider_bg_rect.width)
        slider_btn_rect = pg.Rect(slider_btn_x - 5, slider_bg_rect.y - 10, 10, 30)
        pg.draw.rect(ecran, (255, 200, 200), slider_btn_rect)

        police = pg.font.Font(POLICE_MINECRAFT, 20)
        texte_surface = police.render("Musique", False, (0, 0, 0))
        ecran.blit(texte_surface, (slider_bg_rect.x, slider_bg_rect.y - 30))

        pg.display.update()

        # Evenements
        for event in pg.event.get():
            evenements_communs(event)

            # Gestion du clavier pour le pseudo
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:
                    # Supprimer le dernier caractère
                    pseudo_joueur = pseudo_joueur[:-1]

            elif event.type == pg.TEXTINPUT:
                # Ajoute le caractère tapé (gère les majuscules, etc.)
                # Limite à 12 caractères pour éviter que ça dépasse du titre
                if len(pseudo_joueur) < 12:
                    pseudo_joueur += event.text

            # Gérer le slider
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if slider_btn_rect.collidepoint(event.pos) or slider_bg_rect.collidepoint(event.pos):
                    slider_bouge = True

            if event.type == pg.MOUSEMOTION and slider_bouge:
                rel_x = event.pos[0] - slider_bg_rect.x
                new_vol = max(0.0, min(1.0, rel_x / slider_bg_rect.width))
                set_volume_musique(new_vol)

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                slider_bouge = False

        await config.attente_ms()

    while config.fenetre_ouverte and not config.pres_jeu:
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
            if not config.mort:
                charger_bouton(ecran, (20, 30), (100, 50), "Boire", eau.boire)
                charger_bouton(ecran, (130, 30), (100, 50), "Manger", nourriture.nourrir)
                charger_bouton(ecran, (240, 30), (100, 50), "Sport", sport.sport)
                charger_bouton(ecran, (350, 30), (100, 50), "Soigner", sante.guerir)
            # Si besoin d'afficher le défibrillateur et qu'on est mort, on met le bouton
            if config.demande_defibrillateur and config.mort:
                charger_bouton(
                    ecran, (20, 30), (100, 50), "DAE", DAE.actionner
                )

            # On met les barres d'état
            barre_etat(
                ecran,
                50,
                config.etat_de_sante,
                (0, 255, 0),
                (0, 150, 0),
                (255, 0, 0),
            )
            barre_etat(
                ecran,
                100,
                config.faim,
                (200, 150, 0),
                (255, 255, 0),
                (255, 0, 0),
            )
            barre_etat(
                ecran, 150, config.eau, (0, 0, 255), (0, 255, 255), (255, 10, 60)
            )

        elif not apres_mort_fini:
            jouer_son("mort")
            apres_mort_fini = True

            asyncio.create_task(gerer_score_et_leaderboard())

        if not config.jeu_en_cours:
            await apres_mort(ecran)

        # Mettre à jour rendu
        pg.display.update()

        # Evenements
        for event in pg.event.get():
            evenements_communs(event)

        await config.attente_ms()

    pg.quit()


async def run_all():
    """Lance main (notamment les modules) et pygame en parallèle"""
    await asyncio.gather(main.main(), game_loop())


# Tout exécuter si c'est le fichier principal (python game.py)
if __name__ == "__main__":
    asyncio.run(run_all())