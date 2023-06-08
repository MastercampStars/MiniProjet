import pygame
import random

# Dimensions de la fenêtre
WIDTH = 800
HEIGHT = 600

# Dimensions d'une tuile
TILE_SIZE = 50

# Nombre de tuiles en largeur et en hauteur
TILES_X = WIDTH // TILE_SIZE
TILES_Y = HEIGHT // TILE_SIZE

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Génération de la carte aléatoire
map_data = []
for y in range(TILES_Y):
    row = []
    for x in range(TILES_X):
        # Génération d'une valeur aléatoire entre 0 et 1
        tile_type = random.randint(0, 1)
        row.append(tile_type)
    map_data.append(row)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Affichage de la carte
    for y in range(TILES_Y):
        for x in range(TILES_X):
            tile_type = map_data[y][x]
            color = (255, 255, 255) if tile_type == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()
