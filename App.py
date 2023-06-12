import pygame
from pygame.locals import *
import cProfile
from Boat import Boat
from Map import Map
from Bullet import Bullet
clock = pygame.time.Clock()

#permet de récuperer l'angle en fonction de la direction, utile pour la rotation des images des bateaux
def getAngle(direction):
    
    if direction == "up":
        return 0
    if direction == "right":
        return 90
    if direction == "down":
        return 180
    if direction == "left":
        return 270
        

def Main (): # -------------------------------------------Initialisation du Main ------------------------------------------ 
    # Initialisation de Pygame
    pygame.init()

    # Définition des paramètres de la fenêtre
    largeur_fenetre = 800
    hauteur_fenetre = 600
    cells_Size = 20

    # Création de la fenêtre Resizable
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
    pygame.display.set_caption("Bataille navale")
    
    #initialisation des listes nécessaires pour l'affichage des images
    allImag = []
    allPos = []
    allAngles = []

    
    # Chargement de la police de caractères
    police = pygame.font.Font(None, cells_Size)


    # Création de la carte. Elle prend en parametre:(la taille de la carte, le dictionnaire du type de case par défaut)
    map = Map({"x":85,"y":49},{"char":" "})
    # Création des bateaux. Ils prennent en parametre:({le dictionnaire du type de case}, la carte, {la position du Front du bateau}, la direction du bateau, {la taille du bateau})
    #Team 1
    boat1 = Boat({"char":"P","color":(0,255,0),"able":True,"player":1},map,{"x":18,"y":25},"left",{"x":2,"y":7})
    boat2 = Boat({"char":"P","color":(0,255,0),"able":True,"player":1},map,{"x":50,"y":25},"left",{"x":2,"y":7})
    # Team 2
    boat3 = Boat({"char":"P","color":(255,0,0),"able":True,"player":2},map,{"x":22,"y":40},"left",{"x":3,"y":7})
    boat4 = Boat({"char":"P","color":(255,0,0),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":1,"y":7})
    
    # Création d'une liste par team
    team1 = [boat1,boat2]
    team2 = [boat3,boat4]
    
    # Création d'une liste de toutes les teams
    teamsBoats = [team1,team2]
    
    # Chargement de l'image du bateau par défaut (on pourra changer l'image en fonction du type de bateau plus tard si besoin)
    boatImage = pygame.image.load("assets/corvette.png").convert_alpha()
    
    
    # Remplissage des listes pour l'affichage des images et ajout des bateaux jouables à la carte
    for boats in teamsBoats:
        # Création des listes de charactéristiques par team
        images = []
        positions = []
        angles = []    
        for boat in boats:
            
            # Ajoutez le bateau à la carte
            map.addElement(boat)
            
            # Récupérez l'angle de l'image en fonction de la direction du bateau et le stockez dans la liste des angles
            angles.append(getAngle(boat.direction))
            
            # Définir la position de l'image en fonction de la direction du bateau et l'ajouter à la liste des positions
            # La position de l'image correspond toujours à la case la plus en haut à gauche du bateau
            if boat.direction == "up":
                positions.append((boat.Front["x"]*cells_Size,boat.Front["y"]*cells_Size))
            elif boat.direction == "right":
                positions.append((boat.Back["x"]*cells_Size,(boat.Back["y"]-(boat.size["x"]-1))*cells_Size))
            elif boat.direction == "down":
                positions.append((boat.Back["x"]*cells_Size,boat.Back["y"]*cells_Size))
            elif boat.direction == "left":
                positions.append((boat.Front["x"]*cells_Size,(boat.Front["y"]-(boat.size["x"]-1))*cells_Size))
            
            
            # Redimensionnez l'image pour s'adapter à la taille du bateau et l'ajouter à la liste des images
            image = pygame.transform.scale(boatImage, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            
            # Faites pivoter l'image en fonction de l'angle du bateau et ajoutez-la à la liste des images
            images.append(pygame.transform.rotate(image, - angles[-1]))
        
        # Ajout des listes de charactéristiques à la liste des listes de charactéristiques
        allImag.append(images)
        allPos.append(positions)
        allAngles.append(angles)
    
    # Génération d'obstacles aléatoires de la carte après avoir ajouté les bateaux pour éviter les collisions au chargement
    map.randGenerate()
    

    # Vitesse de déplacement du bateau
    distance = 3

    # Variable de boucle
    direction = None
    close = False
    fire = False
    MAJImage = False
    
    # Initialisation du bateau actif
    
    indexBoat = 0
    indexTeam = 0
    boats = teamsBoats[indexTeam]
    boat = boats[indexBoat]
    images = allImag[indexTeam]
    positions = allPos[indexTeam]
    angles = allAngles[indexTeam]
    nbPlayers = len(teamsBoats)
    
    # ---------------------------------------------------Boucle principale du jeu---------------------------------------------------
    while not close:
        #chargement de la matrice de la carte
        matrice = map.getMatrice()
        
        # Gestion des événements claviers et souris
        for evenement in pygame.event.get():
            
            # Si l'utilisateur quitte le jeu
            if evenement.type == pygame.QUIT:
                close = True
            
            # Capte les touches enfoncées pour définir les actions à effectuer
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
                    
                    # On passe au bateau suivant
                    indexBoat = (indexBoat+1)%len(boats)
                    boat = boats[indexBoat]
                    
                    # Si le bateau est mort : on passe au bateau suivant
                    if boat.life == 0 :
                        indexBoat = (indexBoat+1)%len(boats)
                        boat = boats[indexBoat]
  
                elif evenement.key == pygame.K_p:
                    # On passe au joueur (team) suivant
                    indexTeam = (indexTeam+1)%nbPlayers
                    boats = teamsBoats[indexTeam]
                    images = allImag[indexTeam]
                    angles = allAngles[indexTeam]
                    positions = allPos[indexTeam]
                    indexBoat = 0
                    boat = boats[indexBoat]
                    
                    # Si le bateau est mort : on passe au bateau suivant
                    if boat.life == 0 :
                        indexBoat = (indexBoat+1)%len(boats)
                        boat = boats[indexBoat]

                    
                    

                

        # Déplacement du bateau
        if direction is not None:
            # Faites ici le traitement de déplacement du bateau en fonction de la direction et de la distance
            boat.move(direction,distance) 
            print("Move ", direction,distance) 
            MAJImage = True
            # Réinitialisation des variables de déplacement
            direction = None
        
        # Tir du bateau
        if fire:
            boat.fire()
            print("Fire") 
            print(len(map.bullets))
            fire = False
            
        
        # Mise à jour de la position et de l'angle de l'image du bateau uniquement si le bateau a bougé    
        if MAJImage:
             # Mise à jour de l'angle de l'image
            images[indexBoat] = pygame.transform.rotate(images[indexBoat], angles[indexBoat] - getAngle(boat.direction))
            angles[indexBoat]  = getAngle(boat.direction)
            if boat.direction == "up":
                positions[indexBoat] = (boat.Front["x"]*cells_Size,boat.Front["y"]*cells_Size)
                
            elif boat.direction == "right":
                positions[indexBoat] = (boat.Back["x"]*cells_Size,(boat.Back["y"]-(boat.size["x"]-1))*cells_Size)
            
            elif boat.direction == "down":
                positions[indexBoat] = (boat.Back["x"]*cells_Size,boat.Back["y"]*cells_Size)

            elif boat.direction == "left":
                positions[indexBoat] = (boat.Front["x"]*cells_Size,(boat.Front["y"]-(boat.size["x"]-1))*cells_Size)
            
            MAJImage = False
            
        # --------------------------------------Début de l'impression sur la fenêtre---------------------------------------
        
         
        # Effacement de l'écran avec une couleur bleue
        screen.fill((0, 0, 200))
        
        # Mise en mouvement des bullets
        map.reloadBullets()
        
        # Affichage de la matrice de caractères  de la map dans la fenêtre
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                
                # Affichage du caractère de la case
                caractere = matrice[y][x]["char"]
                
                # Affichage de la couleur de la case
                if "color"  in matrice[y][x]:
                    color = matrice[y][x]["color"]
                else: color = (255,255,255)
                
                # Affichage des bullets de la map
                for bullet in map.bullets:
                    if bullet.position["x"] == x and bullet.position["y"] == y:
                        caractere = "o"
                        
                # Impression du caractère dans la fenêtre aux coordonnées x et y
                texte = police.render(caractere, True, color)
                screen.blit(texte, (x * cells_Size, y * cells_Size))

        # Impression des images des bateaux dans la fenêtre
        for i in range (len(teamsBoats)):
            inlife_boats = 0
            for j in range (len(boats)):
                
                # Vérification que le bateau est en vie
                if teamsBoats[i][j].life > 0:
                    
                    # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                    screen.blit(allImag[i][j], allPos[i][j])
                    inlife_boats += 1
            
            # Si tous les bateaux de l'équipe sont morts, on affiche un message
            if inlife_boats == 0:
                print("Team ", i+1, " is dead")
                close = True
                break
                
                
          
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()
Main()