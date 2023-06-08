import pygame
from Boat import Boat
from Map import Map


def Main ():
    # Initialisation de Pygame
    pygame.init()

    # Définition des paramètres
    largeur_fenetre = 800
    hauteur_fenetre = 600
    police_size = 20

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
    pygame.display.set_caption("Fenêtre Pygame")

    # Chargement de la police de caractères
    police = pygame.font.Font(None, police_size)

    # Création de la carte
    map = Map({"x":85,"y":49},{"char":"*"})
    boat1 = Boat({"char":"P1","able":True},map,{"x":18,"y":25},"left",{"x":3,"y":7})
    boat2 = Boat({"char":"P2","able":True},map,{"x":50,"y":25},"left",{"x":3,"y":7})
    boats = [boat1,boat2]

    for boat in boats:
        map.addElement(boat)


    # Vitesse de déplacement du bateau
    distance = 3

    # Boucle principale du jeu
    close = False
    direction = "up"
    fire = False
    map.randGenerate()
    boat = boats[0]
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
                    boat = boats[(boats.index(boat)+1)%len(boats)]
        


        # Déplacement du bateau
        if direction is not None:
            # Faites ici le traitement de déplacement du bateau en fonction de la direction et de la distance
            boat.move(direction,distance) 
            print("Move ", direction,distance) 
            # Réinitialisation des variables de déplacement
            direction = None
        if fire:
            boat.fire()
            print("Fire")   
        else : 
            boat.unFire()
        fire = False


        # Effacement de l'écran avec une couleur noire
        fenetre.fill((0, 0, 0))
        map.reloadMatrice()
        
        # Affichage de la matrice de caractères
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                caractere = matrice[y][x]["char"]
                for bullet in map.bullets:
                    if bullet.position["x"] == x and bullet.position["y"] == y:
                        print("bullet",bullet.position["x"],bullet.position["y"])
                        caractere = "o"
                texte = police.render(caractere, True, (255, 255, 255))
                position_x = x * police_size
                position_y = y * police_size
                fenetre.blit(texte, (position_x, position_y))

        # Rafraîchissement de l'affichage
        pygame.display.flip()

    # Fermeture de Pygame
    pygame.quit()
Main()