# Tamagotchi
Un jeu type Tamagotchi réalisé en groupe pour la NSI.

## Ce qu'on a fait
### Paulem
- Implémentation des bases pour le fonctionnement des modules (main.py)
- Création de l'agencement de l'affichage pygame et de son organisation au niveau du code
- Création des fonctions basiques du code pour pygame, notamment pour afficher les boutons, le personnage
- Fenêtre pygame rendue responsive : les éléments s'adaptent aux changements de taille de la fenêtre (dans une certaine mesure)
- Création du menu principal
- Création du bouton pour relancer la partie
- Création du sélecteur du pseudo
- Création du système de son/musique
- Création de l'api distante pour le système de score (disponible dans `api/` en Typescript) (enregistrement avec POST, et obtention du top 5 avec GET)
- Ajout de la police personnalisée
- Création du fichier de config (variables mutualisées)
- Création de l'obfuscateur/déobfuscateur des fichiers
- Importation sur Github, gestion du VCS, et commit à la fin de chaque séance et pour les changements faits hors cours
- Ajout des easters eggs (sauf pour la météo)
- Gestion des dépendances
- Aide sur l'affichage et les modules

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
  - [ ] En dernier : amélioration avec effets
- [x] Système de score
- [x] Musique et sound effect
- [x] Pouvoir relancer la partie
- [x] Choix du pseudo
- [x] Système de difficulté
- [x] Options du jeu
- [x] Top joueurs avec API sur mon serveur
- [x] Ajouter L... ? en personnage jouable grâce au code konami
- [ ] Plusieurs tamagotchi ?
- [ ] Système de sauvegarde
- [ ] Ajouter des batailles de Tamagotchi
- [ ] Publier le jeu sur Steam mdr

