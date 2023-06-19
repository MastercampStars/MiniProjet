import pygame
from pygame.locals import *
import cProfile
from Vehicule import *
from Vehicule import LittleBoat
from Map import Map
from Bullet import Bullet
from Base import Base
from Obstacle import Obstacle
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
        return -90
     
def getImages(elements,cells_Size,players,teamsVehicules): 
    
    for element in elements:
        if ("player" in element.type):
            if element.type["player"] not in players:
                players.append(element.type["player"])
                teamsVehicules.append([])
            if element not in teamsVehicules[players.index(element.type["player"])]:
                teamsVehicules[players.index(element.type["player"])].append(element)
        
        # Récupérez l'angle de l'image en fonction de la direction de l'element et le stockez dans la liste des angles
        element.imageAngle = getAngle(element.direction)  
        # Définir la position de l'image en fonction de la direction du bateau et l'ajouter à la liste des positions
        # La position de l'image correspond toujours à la case la plus en haut à gauche du bateau
        if element.direction == "up":
            element.imagePosition = (element.Front["x"]*cells_Size,element.Front["y"]*cells_Size)
        elif element.direction == "right":
            element.imagePosition = (element.Back["x"]*cells_Size,(element.Back["y"]-(element.size["x"]-1))*cells_Size)
        elif element.direction == "down":
            element.imagePosition = (element.Back["x"]*cells_Size,element.Back["y"]*cells_Size)
        elif element.direction == "left":
            element.imagePosition = (element.Front["x"]*cells_Size,(element.Front["y"]-(element.size["x"]-1))*cells_Size)
            
        # Redimensionnez l'image pour s'adapter à la taille du bateau et l'ajouter à la liste des images
        # Chargement de l'image du bateau par défaut
        if(hasattr(element,"life")):
            elementImage = pygame.image.load("assets/"+element.imageLoc).convert_alpha()
            image = pygame.transform.scale(elementImage, ((element.size["x"]-0.5) * cells_Size, (element.size["y"]-0.5)*cells_Size))
            
        # Faites pivoter l'image en fonction de l'angle du bateau et ajoutez-la à la liste des images
            element.image = pygame.transform.rotate(image, - element.imageAngle)
    return teamsVehicules,players






def Main ():
    # Initialisation de Pygame
    pygame.init()

    # Définition des paramètres de la fenêtre
    ratio = 1920/1080
    hauteur_fenetre  = 400
    largeur_fenetre = int(ratio*hauteur_fenetre )

    cells_Size = 17

    # Création de la fenêtre Resizable
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
    pygame.display.set_caption("Bataille navale")
    

    
    # Chargement de la police de caractères
    police = pygame.font.Font(None, cells_Size)


    # Création de la carte. Elle prend en parametre:(la taille de la carte, le dictionnaire du type de case par défaut)
    mapSize = 70
    map = Map({"x":mapSize,"y":int(50)},{"char":"*"})
    # Création des bateaux. Ils prennent en parametre:({le dictionnaire du type de case}, la carte, {la position du Front du bateau}, la direction du bateau, {la taille du bateau})
    vehicule1 = Carrier(map,{"x":18,"y":25},"left","player1",color = (255,0,0))
    vehicule2 = BigBoat(map,{"x":30,"y":25},"up","player1",color = (255,0,0))
    
    vehicule3 = MedicaleBoat(map,{"x":18,"y":40},"right","player2")
    vehicule4 = Submarine(map,{"x":40,"y":25},"down","player2")
    vehicule5 = Jet(map,{"x":40,"y":40},"down")
    
    # Création des bases 
    base1 = Base(map,"up","player1", (255, 0, 0))

    base2 = Base(map,"up","player2",(0,255,0))
    # Ajout des bases à la carte
    map.addElement(base1)
    map.addElement(base2)
    
    # Création de la liste des bateaux jouables
    NewVehicules = [vehicule1,vehicule2,vehicule3,vehicule4]
    
    # Ajout des bateaux jouables à la carte
    for vehicule in NewVehicules:
        map.addElement(vehicule)
    
    
    map.randGenerate()
    

    players = []
    teamsVehicules = []
    
    #chargement des images
    teamsVehicules,players = getImages(map.elements,cells_Size,players,teamsVehicules)
    

    # Variable de boucle
    direction = None
    close = False
    fire = False
    MAJImage = False
    loadImages = False
    
    # Initialisation du bateau actif
    
    indexVehicule = 0
    indexTeam = 0
    vehicules = teamsVehicules[indexTeam]
    vehicule = vehicules[indexVehicule]

    nbPlayers = len(players)
    distanceImage = 0
    diffRotation = 0
    
    # Boucle principale du jeu
    while not close:

        #chargement de la matrice de la carte
        matrice = map.getMatrice()
        
        # Gestion des événements claviers et souris
        for evenement in pygame.event.get():
            
            # Si l'utilisateur quitte le jeu
            if evenement.type == pygame.QUIT:
                close = True
            if distanceImage == 0:
                # Capte les touches enfoncées pour définir les actions à effectuer
                if evenement.type == pygame.KEYDOWN:
                    if evenement.key == pygame.K_q:
                        direction = "left"
                    elif evenement.key == pygame.K_d:
                        direction = "right"
                    elif evenement.key == pygame.K_z:
                        direction = "up"
                    elif evenement.key == pygame.K_s:
                        direction = "down"
                    elif evenement.key == pygame.K_PLUS or evenement.key == pygame.K_KP_PLUS:
                        vehicule.maxSpeed += 1
                    elif evenement.key == pygame.K_MINUS or evenement.key == pygame.K_KP_MINUS:
                        vehicule.maxSpeed -= 1
                    elif evenement.key == pygame.K_SPACE:
                        fire = True
                    elif evenement.key == pygame.K_KP_ENTER or evenement.key == pygame.K_RETURN:
                        print("special")
                        if hasattr (vehicule,'special') :
                            vehicule.special()
                        loadImages = True
                        
                    elif evenement.key == pygame.K_TAB:
                        indexVehicule = (indexVehicule+1)%len(vehicules)
                        print(len(vehicules))
                        vehicule = vehicules[indexVehicule]
                        
                        # Si le bateau est mort : on passe au bateau suivant
                        if vehicule.life == 0 :
                            indexVehicule = (indexVehicule+1)%len(vehicules)
                            vehicule = vehicules[indexVehicule]
    
                    elif evenement.key == pygame.K_p:
                        indexTeam = (indexTeam+1)%len(teamsVehicules)
                        vehicules = teamsVehicules[indexTeam]
                        indexVehicule = 0
                        vehicule = vehicules[indexVehicule]
                        
                        # Si le bateau est mort : on passe au bateau suivant
                        if vehicule.life == 0 :
                            indexVehicule = (indexVehicule+1)%len(vehicules)
                            vehicule = vehicules[indexVehicule]


        #chargement des images
        if loadImages:
            teamsVehicules,players = getImages(map.elements,cells_Size,players,teamsVehicules)
            vehicules = teamsVehicules[indexTeam]
            loadImages = False
            

        # Déplacement du bateau
        if direction is not None:
            # Faites ici le traitement de déplacement du bateau en fonction de la direction et de la distance
            presAngle = getAngle(vehicule.direction)
            vehicule.move(direction) 
            print("Move ", direction) 
            distanceImage = cells_Size * vehicule.speed
            print(getAngle(vehicule.direction))
            
            diffRotation = (getAngle(vehicule.direction) - presAngle)%360
            
            if diffRotation > 180:
                diffRotation -= 360
             
            #print("diffRotation : ", diffRotation)
            
                
            MAJImage = True
            # Réinitialisation des variables de déplacement
            direction = None
        
        # Tir du bateau
        if fire:
            vehicule.fire()
            print("Fire") 
            print(len(map.bullets))
            fire = False

        
        # Mise à jour de la position et de l'angle de l'image du bateau uniquement si le bateau a bougé    
        if MAJImage:
             # Mise à jour de l'angle de l'image
            vehicule.image = pygame.transform.rotate(vehicule.image, vehicule.imageAngle - getAngle(vehicule.direction))  
            vehicule.imageAngle  = getAngle(vehicule.direction)
            if vehicule.direction == "up":
                vehicule.imagePosition = (vehicule.Front["x"]*cells_Size  ,vehicule.Front["y"]*cells_Size + distanceImage)
                
            elif vehicule.direction == "right":
                vehicule.imagePosition = (vehicule.Back["x"]*cells_Size - distanceImage ,(vehicule.Back["y"]-(vehicule.size["x"]-1))*cells_Size )

            elif vehicule.direction == "down":
                vehicule.imagePosition = (vehicule.Back["x"]*cells_Size  ,vehicule.Back["y"]*cells_Size - distanceImage )

            elif vehicule.direction == "left":
                vehicule.imagePosition = (vehicule.Front["x"]*cells_Size  + distanceImage ,(vehicule.Front["y"]-(vehicule.size["x"]-1))*cells_Size)
            
            MAJImage = False
        
        if distanceImage > 0 :
            distanceImage -= 1 *cells_Size*0.5
            MAJImage = True
        elif distanceImage < 0 :
            distanceImage += 1 *cells_Size*0.5
            MAJImage = True
            
        if diffRotation > 0 :
            diffRotation -= 5
            MAJImage = True
        elif diffRotation < 0 :
            diffRotation += 5
            MAJImage = True
        #print("diffRotation : ", diffRotation)
            


        
        
        #print(positions[indexVehicule])
            

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
                
                
                #caractere =" "
                
                # Affichage des bullets de la map
                for bullet in map.bullets:
                    if bullet.position["x"] == x and bullet.position["y"] == y:
                        caractere = "o"
                        
                # Impression du caractère dans la fenêtre aux coordonnées x et y
                if caractere != "":
                    texte = police.render(caractere, True, color)
                    screen.blit(texte, (x * cells_Size, y * cells_Size))

        # Impression des images des bateaux dans la fenêtre
        for element in map.elements:
            # Vérification que le bateau est en vie
            if hasattr(element,'life') and element.life > 0:
                # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                screen.blit(element.image, element.imagePosition)
            # Si tous les bateaux de l'équipe sont morts, on affiche un message
                
                

          
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()

cProfile.run('Main()')