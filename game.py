import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1400, 700))
pygame.display.set_caption("Hello Pygame")

# create a surface object, image is drawn on it.
imp = pygame.image.load("images/personnage.bmp").convert()

# Using blit to copy content from one surface to other
screen.blit(imp, (0, 0))

# paint screen one time
pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()