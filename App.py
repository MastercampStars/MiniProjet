import pygame
from pygame.locals import *
from Vehicule import *
from Map import Map
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
            if element.type["char"] != "Q":
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
            element.imagePosition = (int(element.Front["x"]*cells_Size),int(element.Front["y"]*cells_Size))
        elif element.direction == "right":
            element.imagePosition = (int(element.Back["x"]*cells_Size),int((element.Back["y"]-(element.size["x"]-1))*cells_Size))
        elif element.direction == "down":
            element.imagePosition = (int(element.Back["x"]*cells_Size),int(element.Back["y"]*cells_Size))
        elif element.direction == "left":
            element.imagePosition = (int(element.Front["x"]*cells_Size),int((element.Front["y"]-(element.size["x"]-1))*cells_Size))
            
        # Redimensionnez l'image pour s'adapter à la taille du bateau et l'ajouter à la liste des images
        # Chargement de l'image du bateau par défaut
        if(hasattr(element,"imageLoc")):
            elementImage = pygame.image.load("assets/"+element.imageLoc).convert_alpha()
            image = pygame.transform.scale(elementImage, (int((element.size["x"]-0.5) * cells_Size), int((element.size["y"]-0.5)*cells_Size)))
            # Faites pivoter l'image en fonction de l'angle du bateau et ajoutez-la à la liste des images
            element.image = pygame.transform.rotate(image, - element.imageAngle)
    
    return teamsVehicules,players



def Main ():
    # Initialisation de Pygame
    pygame.init()
    


    # Création de la fenêtre plein ecran pour récuperer les bonnes dimentions
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Bataille navale")
    
    #responsive
    largeur_fenetre = screen.get_width()
    hauteur_fenetre = screen.get_height()*0.95
    
    
    print(largeur_fenetre,hauteur_fenetre)
    
    # Définition des paramètres de la fenêtre
    mapSize = 100
    ratio = largeur_fenetre/(hauteur_fenetre*0.98)
    #responsive
    cells_Size = largeur_fenetre/mapSize
    game_font = 'assets/joystix monospace.ttf'
    
    screen = pygame.display.set_mode((int(largeur_fenetre*0.9),int(hauteur_fenetre *0.9)), pygame.RESIZABLE)
        

     # Création de la carte. Elle prend en parametre:(la taille de la carte, le dictionnaire du type de case par défaut)

    map = Map({"x":mapSize+1,"y":int(mapSize//ratio)},{"char":"*"})
    
    
    # Création des bateaux. Ils prennent en parametre:({le dictionnaire du type de case}, la carte, {la position du Front du bateau}, la direction du bateau, {la taille du bateau})
    vehicule1 = Carrier(map,{"x":18,"y":25},"left",1,color = (255,0,0))
    vehicule2 = BigBoat(map,{"x":30,"y":25},"up",1,color = (255,0,0))
    
    vehicule3 = MedicaleBoat(map,{"x":18,"y":40},"right",2)
    vehicule4 = Submarine(map,{"x":40,"y":25},"down",2)


    
    # Création de la liste des bateaux jouables
    NewVehicules = [vehicule1,vehicule2,vehicule3,vehicule4]
    
    
    #load les images fixes
    
    vehiculesMenu = [LittleBoat(map,{"x":18,"y":25},"left",1,color = (255,0,0)),
                     MedicaleBoat(map,{"x":18,"y":40},"left",2),
                     BigBoat(map,{"x":30,"y":25},"left",1,color = (255,0,0)),
                     Carrier(map,{"x":18,"y":25},"left",1,color = (255,0,0)),
                     Submarine(map,{"x":40,"y":25},"left",1),
                     Jet(map,{"x":40,"y":25},"left",1)
                     ]
    
    getImages(vehiculesMenu,cells_Size,[],[])
    images = [vehicule.image for vehicule in vehiculesMenu]
    element_image = pygame.image.load("images/cross2.png").convert_alpha()
    gold = pygame.image.load("images/gold1.png").convert_alpha()

    
    
    
    
    # Ajout des bateaux jouables à la carte
    for vehicule in NewVehicules:
        map.addElement(vehicule)
    # ajout des obstacles
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
    
    # Variable d'affichage
    show_popup = True
    game_over = False
    
    # Initialisation du bateau actif
    
    indexVehicule = 0
    indexTeam = 0
    vehicules = teamsVehicules[indexTeam]
    vehicule = vehicules[indexVehicule]

    nbPlayers = len(players)
    distanceImage = 0
    winner = 0
    
    
    # ---------------------------------------------------------------Boucle principale du jeu--------------------------------------------------------------------
    while not close:
        #responsive
        largeur_fenetre = screen.get_width()
        hauteur_fenetre = screen.get_height()      
        cells_Size = largeur_fenetre/mapSize
        background_image = pygame.image.load("images/water32.jpg")
        background_image = pygame.transform.scale(background_image, (int(largeur_fenetre),int(hauteur_fenetre)))

        police = pygame.font.Font(game_font, int(cells_Size*(20/17)))
        getImages(vehiculesMenu,cells_Size,[],[])
        images = [vehicule.image for vehicule in vehiculesMenu]
        
        
        loadImages = True
        
        

        #chargement de la matrice de la carte
        matrice = map.getMatrice()
        
        # Gestion des événements claviers et souris
        for evenement in pygame.event.get():
            
            # Si l'utilisateur quitte le jeu
            if evenement.type == pygame.QUIT:
                close = True
            
            elif evenement.type == pygame.VIDEORESIZE:
            # Récupération des nouvelles dimensions de la fenêtre
                width, height = evenement.size
            # Calcul du ratio largeur/longueur de la fenêtre redimensionnée
                new_ratio = width / height

                if round(new_ratio, 1) > round(ratio, 1) :
                    print("ratio",round(ratio, 2),"new_ratio",round(new_ratio, 2),"width",width,"height",height)
                    # La fenêtre est plus large, on ajuste la largeur
                    new_width = int(height * ratio)
                    window = pygame.display.set_mode((new_width, height), pygame.RESIZABLE)
                elif round(new_ratio, 1) < round(ratio, 1):
                    print("ratio",round(ratio, 1),"new_ratio",round(new_ratio, 1),"width",width,"height",height)
                    # La fenêtre est plus haute, on ajuste la hauteur
                    new_height = int(width / ratio)
                    window = pygame.display.set_mode((width, new_height), pygame.RESIZABLE)
            
            
            if distanceImage == 0:
                # Capte les touches enfoncées pour définir les actions à effectuer
                
                if evenement.type == pygame.KEYDOWN:
                    if show_popup == False :
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
                        
                        elif evenement.key == pygame.K_x:
                            if (map.canExplode(vehicule)):
                                game_over = True
                                winner = vehicule.type["player"]
                                print ("winner : ",winner)
                        elif evenement.key == pygame.K_m:
                            show_popup = True
                        elif evenement.key == pygame.K_v:
                            game_over = True
                    elif evenement.key == pygame.K_SPACE:
                        show_popup = False
     


#---------------------------------------------------------------Affichage du menu--------------------------------------------------------------------

        def show_popup_menu():
            # Define the colors
            BEIGE = (252,202,116)
            BLACK = (58, 41, 11)
            RED = (255, 152, 62)


            menu2 = pygame.image.load("images/small_scroll3.png").convert_alpha()
            menu2 = pygame.transform.scale(menu2, (int(cells_Size*(1250/17)), int(cells_Size*(850/17))))
            
            decallageX = 80
            decallageY = 50
            screen.blit(menu2, (int(cells_Size*((220)/17)), int(cells_Size*(30/17))))

            # Create a text surface and get its rect
            police_goal = pygame.font.Font(game_font, int(cells_Size*(30/17)))
            text1 = "GOAL"
            text = "Destroy the ennemy's base or sink all their ships"
            text_surface1 = police_goal.render(text1, True, RED)
            text_surface = police.render(text, True, BLACK)
            text_rect1 = text_surface1.get_rect(center=(int(cells_Size*((770 + decallageX)/17)), int(cells_Size*((190 + decallageY)/17))))
            text_rect = text_surface.get_rect(center=(int(cells_Size*((770 + decallageX)/17)), int(cells_Size*((220 + decallageY)/17))))

            frame_color = (58, 41, 11) 
            frame_position = (int(cells_Size*((300 + decallageX)/17)), int(cells_Size*((250 + decallageY)/17)))  # Top-left corner of the frame
            frame_size = (int(cells_Size*((940 )/17)), int(cells_Size*(310/17)))  # Width and height of the frame
            frame_thickness = int(3*cells_Size/14)  # Thickness of the frame border
            if frame_thickness == 0 :
                frame_thickness = 1
            # Draw the frame
            pygame.draw.rect(screen, frame_color, (*frame_position, *frame_size), frame_thickness)


            # Create a button surface and get its rect
            button_width, button_height = int(cells_Size*(120/17)), int(cells_Size*(40/17))
            button_surface = pygame.Surface((button_width, button_height))

            button_rect = button_surface.get_rect(center=(int(cells_Size*((770 + decallageX)/17)), int(cells_Size*((600 + decallageY)/17))))
            
            #Display ships and their characteristics
            police_ship = pygame.font.Font(game_font, int(cells_Size*16.5/17))

            text_ship1 = "Corvette : moves twice as far as other ships"
            text_ship2 = "Medical boat : heals one of your ships"
            text_ship3 = "tank ship : Shoots 6 bullets at a time"
            text_ship4 = "Transporter : launches a plane that avoids collisions"
            text_ship5 = "Submarine : avoids collisions but can't blow itself up"

            text_ship_surface1 = police_ship.render(text_ship1, True,RED )
            text_ship_surface2 = police_ship.render(text_ship2, True, BLACK)
            text_ship_surface3 = police_ship.render(text_ship3, True, RED)
            text_ship_surface4 = police_ship.render(text_ship4 , True, BLACK)
            text_ship_surface5 = police_ship.render(text_ship5 , True, RED)
        
            text_rect_ship_surface1 = text_ship_surface1.get_rect(center=(int(cells_Size*((730 + decallageX)/17)),int(cells_Size*((290 + decallageY)/17))))
            text_rect_ship_surface2 = text_ship_surface2.get_rect(center=(int(cells_Size*((730 + decallageX)/17)),int(cells_Size*((340 + decallageY)/17))))
            text_rect_ship_surface3 = text_ship_surface3.get_rect(center=(int(cells_Size*((810 + decallageX)/17)),int(cells_Size*((395 + decallageY)/17))))
            text_rect_ship_surface4 = text_ship_surface4.get_rect(center=(int(cells_Size*((870 + decallageX)/17)),int(cells_Size*((460 + decallageY)/17))))
            text_rect_ship_surface5 = text_ship_surface5.get_rect(center=(int(cells_Size*((810 + decallageX)/17)),int(cells_Size*((525 + decallageY)/17))))

            # Money explanation

            menu_surface = pygame.Surface((int(cells_Size*(190/17)), int(cells_Size*(100/17))))
            menu_surface.fill(BEIGE)
            menu_rect = menu_surface.get_rect(center=(int(cells_Size*((1140 + decallageX)/17)),int(cells_Size*((305 + decallageY)/17))))
            money_text = "For +100"
            canon_text = "Revive +1"
            money_text_surface = police_ship.render(money_text, True, BLACK )
            canon_text_surface = police_ship.render(canon_text, True, BLACK)
            money_text_rect = money_text_surface.get_rect(center=(int(cells_Size*((1120 + decallageX)/17)),int(cells_Size*((280 + decallageY)/17))))
            canon_text_rect = canon_text_surface.get_rect(center=(int(cells_Size*((1120 + decallageX)/17)),int(cells_Size*((322 + decallageY)/17))))

            # Create a text surface for the button and get its rect
            button_text = "Press  Spacebar to Play"
            button_text_surface = police.render(button_text, True, BLACK)
            button_text_rect = button_text_surface.get_rect(center=button_rect.center)


            # Blit the menu surface, text surface, and button surface onto the screen
            
            screen.blit(text_surface, text_rect)
            screen.blit(text_surface1, text_rect1)
            screen.blit(button_text_surface, button_text_rect)
            space = pygame.image.load("images/space_bar1.png").convert_alpha()
            space = pygame.transform.scale(space, (int(cells_Size*(170/17)), int(cells_Size*(40/17))))
            screen.blit(space, (int(cells_Size*((673 + decallageX)/17)), int(cells_Size*((585 + decallageY)/17))))
            screen.blit(images[0], (int(cells_Size*((310 + decallageX)/17)),int(cells_Size*((270 + decallageY)/17))))
            screen.blit(images[1], (int(cells_Size*((310 + decallageX)/17)),int(cells_Size*((330 + decallageY)/17))))
            screen.blit(images[2], (int(cells_Size*((310 + decallageX)/17)),int(cells_Size*((380 + decallageY)/17))))
            screen.blit(images[3], (int(cells_Size*((310 + decallageX)/17)),int(cells_Size*((440 + decallageY)/17))))
            screen.blit(images[4], (int(cells_Size*((310 + decallageX)/17)),int(cells_Size*((510 + decallageY)/17))))
            screen.blit(images[5], (int(cells_Size*((455 + decallageX)/17)),int(cells_Size*((448 + decallageY)/17))))
            screen.blit(text_ship_surface1, text_rect_ship_surface1)
            screen.blit(text_ship_surface2, text_rect_ship_surface2)
            screen.blit(text_ship_surface3, text_rect_ship_surface3)
            screen.blit(text_ship_surface4, text_rect_ship_surface4)
            screen.blit(text_ship_surface5, text_rect_ship_surface5)
            screen.blit(menu_surface, menu_rect)
            screen.blit(gold, (int(cells_Size*((1190 + decallageX)/17)),int(cells_Size*((270 + decallageY)/17))))
            canon = pygame.image.load("images/canon1.png").convert_alpha()
            canon = pygame.transform.scale(canon, (int(cells_Size*(35/17)), int(cells_Size*(27/17))))
            screen.blit(canon, (int(cells_Size*((1190 + decallageX)/17)),int(cells_Size*((310 + decallageY)/17))))
            screen.blit(money_text_surface, money_text_rect)
            screen.blit(canon_text_surface, canon_text_rect)
            
        #--------------------------------------------------Open popup gameover----------------------------------------------------------------------------
        def show_game_over_menu(winner) :
            RED = (255,0,0)
            transparent_black = (0, 0, 0, 198)  # Semi-transparent black
            police_end = pygame.font.Font(game_font, 50)
            # Game Over text
            game_over_text = police_end.render("GAME OVER", True, RED)

            # Winner text
            winner_text = police.render(f"Player {winner} wins!", True, (255, 255, 255))

            # Get the center position of the screen
            screen_center = screen.get_rect().center

            # Create a transparent surface to cover the screen
            filter_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            filter_surface.fill(transparent_black)


            # Draw the filtered surface
            screen.blit(filter_surface, (0, 0))

            # Draw the game over text in the center of the screen
            game_over_text_rect = game_over_text.get_rect(center=screen_center)
            screen.blit(game_over_text, game_over_text_rect)

            # Draw the winner text below the game over text
            winner_text_rect = winner_text.get_rect(midtop=(screen_center[0], game_over_text_rect.bottom + 20))
            screen.blit(winner_text, winner_text_rect)
            
            #------------------------------------------------------------Fin affichage menu------------------------------------------------------------
            #------------------------------------------------------------Début affichage jeu------------------------------------------------------------


        #chargement des images
        if loadImages:
            teamsVehicules,players = getImages(map.elements,cells_Size,players,teamsVehicules)
            vehicules = teamsVehicules[indexTeam]
            loadImages = False
            

        # Déplacement du vehicule
        if direction is not None:
            # Faites ici le traitement de déplacement du vehicule en fonction de la direction et de la distance
            presAngle = getAngle(vehicule.direction)
            vehicule.move(direction) 
            print("Move ", direction) 
            distanceImage = cells_Size * vehicule.speed
            print(getAngle(vehicule.direction))
            
                
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
                vehicule.imagePosition = (int(vehicule.Front["x"]*cells_Size ) ,int(vehicule.Front["y"]*cells_Size + distanceImage))
                
            elif vehicule.direction == "right":
                vehicule.imagePosition = (int(vehicule.Back["x"]*cells_Size - distanceImage) ,(int(vehicule.Back["y"]-(vehicule.size["x"]-1))*cells_Size ))

            elif vehicule.direction == "down":
                vehicule.imagePosition = (int(vehicule.Back["x"]*cells_Size)  ,int(vehicule.Back["y"]*cells_Size - distanceImage ))

            elif vehicule.direction == "left":
                vehicule.imagePosition = (int(vehicule.Front["x"]*cells_Size  + distanceImage) ,int((vehicule.Front["y"]-(vehicule.size["x"]-1))*cells_Size))
            
            MAJImage = False
        
        if distanceImage > cells_Size*0.5 :
            distanceImage -= 1 *cells_Size*0.5
            MAJImage = True
        elif distanceImage < -cells_Size*0.5 :
            distanceImage += 1 *cells_Size*0.5
            MAJImage = True
        elif distanceImage != 0:
            distanceImage = 0
            MAJImage = True
            

            

        # Effacement de l'écran avec une couleur bleue
        screen.fill((0, 0, 200))
        
        #Affichage fond d'écran
        screen.blit(background_image, (0, 0))
        
        
        #---------------------------------------Affichage des scores de chaque coté de la page : ---------------------------------------
        # font = pygame.font.Font(None, 36)
        score1 = 0
        score2 = 0
        

        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                if "player" in matrice[y][x]:
                    if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==1:
                        score2 = score2 + 1
                    if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==2:
                        score1 = score1 + 1
                    
        score_text_1 = police.render(f"P1: {score1}", True, (255, 255, 255)) #score équipe 1
        score_text_2 = police.render(f"P2: {score2}", True, (255, 255, 255)) #score équipe 2

        gold = pygame.image.load("images/gold.png")
        gold = pygame.transform.scale(gold, (int(cells_Size*(25/17)), int(cells_Size*(25/17))))
        
        
        screen.blit(score_text_1, (int(cells_Size*(10/17)), int(cells_Size*(20/17))))
        screen.blit(gold, (int(cells_Size*(45/17)), int(cells_Size*(20/17))))
        
        text_width = score_text_2.get_width()
        screen.blit(score_text_2, (largeur_fenetre - text_width - int(cells_Size*(20/17)), int(cells_Size*(20/17))))
        screen.blit(gold, (largeur_fenetre - text_width + int(cells_Size*(16/17)), int(cells_Size*(20/17))))

        menu_text = police.render(f"Press M for Menu", True, (255, 255, 255)) #score équipe 2
        text_width_menu = menu_text.get_width()
        screen.blit(menu_text, ((largeur_fenetre  - text_width_menu)// 2, 20))
        #--------------------------------------- Fin Affichage des scores de chaque coté de la page : ---------------------------------------
        
        
        # Mise en mouvement des bullets
        map.reloadBullets()
        
        
        policeMap = pygame.font.Font(None, int(cells_Size))
        # Affichage de la matrice de caractères  de la map dans la fenêtre
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                
                # Affichage du caractère de la case
                caractere = ""
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
                if caractere != "":
                    texte = policeMap.render(caractere, True, color)
                    screen.blit(texte, (int(x * cells_Size), int(y * cells_Size)))

        # Impression des images des bateaux dans la fenêtre
        for element in map.elements:
            # Vérification que le bateau est en vie
            if hasattr(element,'image'):
                # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                screen.blit(element.image, element.imagePosition)
                
        darkened_image = element_image.copy()
             
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):    
                if matrice[y][x]["char"] == "X":
                # Darken the slot by drawing a semi-transparent black rectangle
                    screen.blit(darkened_image, (int((x-0.20) * cells_Size), int((y-0.10) * cells_Size)))
        
                

        # Si tous les bateaux de l'équipe sont morts, on affiche un message
        if game_over == False: 
            for team in teamsVehicules:
                game_over = False
                for thisVehicule in team:
                    game_over = True
                    winner = (thisVehicule.type["player"] +1) %2
                    if thisVehicule.life > 0:
                        game_over = False
                        break
                if game_over == True:
                    break

                
        if show_popup:
            show_popup_menu()       
          
        if game_over:
            show_game_over_menu(winner) 
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()
    
    
    
    

Main()