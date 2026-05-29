# Tamagotchi
Un jeu type Tamagotchi réalisé en groupe pour la NSI.

Dépôt Github : https://github.com/Paulem79/Tamagotchi

## Lancer le programme
Installer les prérequis pour le projet :
```bash
pip install -r requirements.txt
# Ou sinon, direct les paquets
pip install pygame aioconsole psutil aiohttp
```
Lancer le projet :
```bash
python game.py
```
Si besoin, il faudra créer un venv python, mais je vais pas tout détailler ici, normalement ça fonctionnera déjà

## Remarquable
- Gestion des différents systèmes du Tamagotchi avec des modules
- Easter eggs
- Musique et sons
- API pour gestion du score (avec classement !)
- Menu principal
- DA graphique cohérente
- Mode de difficulté sélectionnable
- Jouable en graphique et en quasiment entièrement en lignes de commande ! (voir modules/commande.py)
- Et bien d'autre

## Léo
### Fait :
- Création de jauge de vie, de nourriture et d'eau
- Création du module de nourriture, de dépression, d'eau, de mort, de besoins, de météo avec pression atmosphérique, et de sport
- Aide sur le module de DAE, et de santé
- Aide sur l'affichage pygame

### Difficultés rencontrées :
- à compléter

## Quentin
### Fait :
- Création des graphismes principaux : personnage, fonds par météo, boutons
- Création du module de DAE, de santé, et de score
- Aide et changements sur différents modules
- Aide sur l'affichage pygame

### Difficultés rencontrées :
- à compléter

## Paulem
### Fait :
- Implémentation de tout le fonctionnement des modules et son système (main.py)
- Création de l'agencement de l'affichage pygame et de son organisation au niveau du code
- Création des fonctions basiques du code pour pygame, notamment pour afficher les boutons, le personnage
- Fenêtre pygame rendue responsive : les éléments s'adaptent aux changements de taille de la fenêtre (dans une certaine mesure)
- Création du menu principal
- Création de l'affichage de titre du jeu
- Création du bouton pour relancer la partie et du bouton de difficulté, ainsi que du bouton joué
- Création du sélecteur du pseudo
- Création du système de son/musique
- Création de l'api distante pour le système de score (disponible dans `api/` en Typescript) (enregistrement avec POST, et obtention du top 5 avec GET)
- Ajout de la police personnalisée
- Création du fichier de config (variables mutualisées)
- Création de l'obfuscateur/déobfuscateur de fichiers
- Importation sur Github, gestion du VCS, et commit à la fin de chaque séance et pour les changements faits hors cours
- Ajout des easters eggs (sauf pour la météo)
- Gestion des dépendances
- Aide sur l'affichage et les modules (refactorisation des modules et adaptation pour leur fonctionnement avec pygame)
- Gestion du fonctionnement parallèle, asynchrone, du main et de pygame

### Difficultés rencontrées :
- Je n'avais pas touché depuis 5 ans à pygame
- Les fonctions asynchrones (avec asyncio) et la synchronisation entre pygame et le main.py étaient un peu complexes à mettre en place, mais une fois ajoutées, plus trop besoin de changer les logiques sur lesquelles elles reposent
- Le relancement du jeu aurait impliqué la réinitialisation de trop d'états/variables ainsi que de devoir réexécuter le main et pygame en parallèle pour bien les redémarrer, ce qui aurait demandé trop de code supplémentaire, la solution, qu'on peut juger de facile, est de relancer le programme complètement. Cependant, cela remplit la fonction de relancer le jeu !

## Notes
- Oui, les barres débordent, mais c'est fait exprès, j'ai mis la solution en commentaire dans le code dans game.py !
- Relancer le jeu peut ne pas fonctionner sur Thonny, je ne sais pas pourquoi, mais ça le fait que avec Thonny j'ai l'impression, mystère...
  

## Tamagotchi – Cahier des charges

- [x] Système de modules
- [x] Module : nourriture
- [x] Module : soif
- [x] Module : santé – maladie
- [x] Module : besoins
- [x] Module : sport
- [x] Module : émotions (triste = plus de sport et tombe malade) arrière plan change de couleur et d’environnement (triste = pluie)
- [x] Module : météo
- [x] Module : défibrillateur après AVC
- [x] Affichage graphique
  - [x] Base PyGame
  - [x] Boutons pour tous les états
  - [x] Affichage personnage
  - [x] Menu principal
- [x] Système de score
- [x] Pouvoir relancer la partie
<p>Bonus :</p>

- [x] Musique et sound effect
- [x] Système de difficulté + Options du jeu
- [x] Choix du pseudo
- [x] Top joueurs avec API sur mon serveur
- [x] Ajouter L... ? en personnage jouable grâce au code konami
- [ ] Affichage graphique : amélioration avec effets
- [ ] Plusieurs tamagotchi ?
- [ ] Système de sauvegarde
- [ ] Ajouter des batailles de Tamagotchi
- [ ] Publier le jeu sur Steam mdr

