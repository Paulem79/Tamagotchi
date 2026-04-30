import pygame

import modules.nourriture as nourriture

# Initialize Pygame
pygame.init()
pygame.font.init()

# Source - https://stackoverflow.com/a/20842987
# Posted by Bartlomiej Lewandowski, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-30, License - CC BY-SA 4.0
my_font = pygame.font.SysFont('Arial', 150)

# Set up the game window
screen = pygame.display.set_mode((1400, 700))
pygame.display.set_caption("Hello Pygame")

# create a surface object, image is drawn on it.
imp = pygame.image.load("images/personnage.bmp").convert()

# Using blit to copy content from one surface to other
screen.blit(imp, (0, 0))

# paint screen one time
pygame.display.flip()

# Rendu du texte
text_surface = my_font.render("Nourri !", False, (0, 0, 0), (255, 255, 255))

screen.blit(text_surface, (0,0))

# Game loop
running = True
while running:
    text: str = "Appuie sur la flèche gauche !"
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Nourri !")
                nourriture.nourrir(1)
                text = "Nourri !"
                print(f"Faim: {nourriture.faim}")




# Quit Pygame
pygame.quit()
