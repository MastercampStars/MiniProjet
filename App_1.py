import pygame
from Boat import Boat
from Map import Map

# Initialisation de Pygame
pygame.init()


# Définition des paramètres
largeur_fenetre = 800
hauteur_fenetre = 600
taille_police = 20
TILE_SIZE = 64

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
pygame.display.set_caption('Bataille Navale')
background_image = pygame.image.load("images/water1.jpg")
# Chargement de la police de caractères
police = pygame.font.Font(None, taille_police)

# Création de la carte
map = Map({"x":100,"y":60}," ")
boat = Boat("P",map,[{"x":6,"y":3},{"x":6,"y":9}])
rock = Boat("M",map,[{"x":12,"y":14},{"x":17,"y":19}])
stones_image = pygame.image.load("images/stones.png")
map.addElement(boat)
map.addElement(rock)
# Vitesse de déplacement du bateau
distance = 1
# Boucle principale du jeu
terminer = False
direction = "up"


while not terminer:
     # Clear the screen
    fenetre.fill((0, 0, 0))

    # Draw the background
   
    fenetre.blit(background_image, (0, 0))


    for Position in rock.Positions:
        x = Position["x"] * TILE_SIZE  # Assuming TILE_SIZE is the size of each tile
        y = Position["y"] * TILE_SIZE
        fenetre.blit(stones_image, (x, y))


    # Gestion des événements
    matrice = map.getMatrice()
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            terminer = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_q:
                direction = "left"
            elif evenement.key == pygame.K_d:
                direction = "right"
            elif evenement.key == pygame.K_z:
                direction = "up"
            elif evenement.key == pygame.K_s:
                direction = "down"
            elif evenement.key == pygame.K_PLUS or evenement.key == pygame.K_KP_PLUS:
                distance += 1
            elif evenement.key == pygame.K_MINUS or evenement.key == pygame.K_KP_MINUS:
                distance -= 1


    # Déplacement du bateau
    if direction is not None:
        # Faites ici le traitement de déplacement du bateau en fonction de la direction et de la distance
        boat.move(direction,distance) 
        print("Move ", direction,distance)  
        map.reloadMatrice()
        #print(map)
        #print("",boat)
        
        # Réinitialisation des variables de déplacement
        direction = None


    # # Effacement de l'écran avec une couleur noire
    # fenetre.fill((0, 0, 0))

    # Affichage de la matrice de caractères
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            caractere = matrice[i][j]
            texte = police.render(caractere, True, (255, 255, 255))
            position_x = j * taille_police
            position_y = i * taille_police
            fenetre.blit(texte, (position_x, position_y))

    # Rafraîchissement de l'affichage
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()