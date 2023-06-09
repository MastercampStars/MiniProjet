import pygame
from pygame.locals import *
import cProfile
from Boat import Boat
from Map import Map
from Bullet import Bullet
clock = pygame.time.Clock()


def getAngle(direction):
    if direction == "up":
        return 0
    if direction == "right":
        return 90
    if direction == "down":
        return 180
    if direction == "left":
        return 270
        

def Main ():
    # Initialisation de Pygame
    pygame.init()

    # Définition des paramètres
    largeur_fenetre = 800
    hauteur_fenetre = 600
    police_size = 20

    # Création de la fenêtre
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
    pygame.display.set_caption("Fenêtre Pygame")
    
    # Chargement de l'image de fond
    boatImage = pygame.image.load("assets/corvette.png").convert_alpha()
    images = []
    positions = []
    angles = []
    # Chargement de la police de caractères
    police = pygame.font.Font(None, police_size)


    # Création de la carte
    map = Map({"x":85,"y":49},{"char":"*"})
    boat1 = Boat({"char":"P","color":(0,255,0),"able":True,"player":1},map,{"x":18,"y":25},"left",{"x":2,"y":7})
    boat2 = Boat({"char":"P","color":(0,255,0),"able":True,"player":1},map,{"x":50,"y":25},"left",{"x":2,"y":7})
    boat3 = Boat({"char":"P","color":(0,0,255),"able":True,"player":2},map,{"x":22,"y":40},"left",{"x":3,"y":7})
    boat4 = Boat({"char":"P","color":(0,0,255),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":1,"y":7})
    boats = [boat1,boat2,boat3,boat4]

    for boat in boats:
        map.addElement(boat)
        # Redimensionnez l'image pour s'adapter à un carré de 200x200 pixels
        images.append(pygame.transform.scale(boatImage, ((boat.size["x"]-0.5)*police_size, (boat.size["y"]-0.5)*police_size)))
        angles.append(0)
        # Définissez l'angle de l'image et sa position
        if boat.direction == "up":
            positions.append((boat.Front["x"]*police_size,boat.Front["y"]*police_size))
            
        elif boat.direction == "right":
            positions.append((boat.Back["x"]*police_size,(boat.Back["y"]-boat.size["x"])*police_size))

        elif boat.direction == "down":
            positions.append((boat.Back["x"]*police_size,boat.Back["y"]*police_size))

        elif boat.direction == "left":
            positions.append((boat.Front["x"]*police_size,(boat.Front["y"]+100)*police_size))


 

    # Vitesse de déplacement du bateau
    distance = 3

    # Boucle principale du jeu
    close = False
    direction = boat.direction
    fire = False
    unfire = False
    map.randGenerate()
    boat = boats[0]
    indexBoat = 0
    MAJImage = True
    while not close:
        # Gestion des événements
        matrice = map.getMatrice()
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                close = True
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
                elif evenement.key == pygame.K_SPACE:
                    fire = True
                elif evenement.key == pygame.K_TAB:
                    indexBoat = (indexBoat+1)%len(boats)
                    boat = boats[indexBoat]
                    MAJImage = True
                
                    
        

        # Déplacement du bateau
        if direction is not None:
            # Faites ici le traitement de déplacement du bateau en fonction de la direction et de la distance
            boat.move(direction,distance) 
            print("Move ", direction,distance) 
            MAJImage = True
            # Réinitialisation des variables de déplacement
            direction = None
        
        if fire:
            boat.fire()
            print("Fire") 
            print(len(map.bullets))
            fire = False
            
        if MAJImage:
             # Mise à jour de l'angle de l'image
            images[boats.index(boat)] = pygame.transform.rotate(images[boats.index(boat)], angles[boats.index(boat)] - getAngle(boat.direction))
            angles[boats.index(boat)]  = getAngle(boat.direction)
            
            if boat.direction == "up":
                positions[indexBoat] = (boat.Front["x"]*police_size,boat.Front["y"]*police_size)
                
            elif boat.direction == "right":
                positions[indexBoat] = (boat.Back["x"]*police_size,(boat.Back["y"]-(boat.size["x"]-1))*police_size)
            
            elif boat.direction == "down":
                positions[indexBoat] = (boat.Back["x"]*police_size,boat.Back["y"]*police_size)

            elif boat.direction == "left":
                positions[indexBoat] = (boat.Front["x"]*police_size,(boat.Front["y"]-(boat.size["x"]-1))*police_size)
                
            MAJImage = False
            


        # Effacement de l'écran avec une couleur noire
        screen.fill((0, 0, 0))
        map.reloadBullets()
        
        # Affichage de la matrice de caractères
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                caractere = matrice[y][x]["char"]
                if "color"  in matrice[y][x]:
                    color = matrice[y][x]["color"]
                else: color = (255,255,255)
                for bullet in map.bullets:
                    if bullet.position["x"] == x and bullet.position["y"] == y:
                        caractere = "o"
                texte = police.render(caractere, True, color)
                position_x = x * police_size
                position_y = y * police_size
                screen.blit(texte, (position_x, position_y))

        # Rafraîchissement de l'affichage
        screen.blit(images[boats.index(boat)], positions[boats.index(boat)])
        pygame.display.flip()
        clock.tick(60) 

    # Fermeture de Pygame
    pygame.quit()
cProfile.run('Main()')