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
     
def getImages(elements,cells_Size,players= [] ,teamsVehicules = []): 
    
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
    


    # Création de la fenêtre plein ecran pour récuperer les bonnes dimentions
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Bataille navale")
    
    #responsive
    #largeur_fenetre = screen.get_width()
    #hauteur_fenetre = screen.get_height()*0.95
    
    
    largeur_fenetre = 1540
    hauteur_fenetre = 880
    cells_Size = 15
    print(largeur_fenetre,hauteur_fenetre)
    
    # Définition des paramètres de la fenêtre
    mapSize = 100
    ratio = largeur_fenetre/hauteur_fenetre
    #responsive
    #cells_Size = largeur_fenetre//mapSize
    game_font = 'assets/joystix monospace.ttf'
    
    screen = pygame.display.set_mode((int(largeur_fenetre*0.9),int(hauteur_fenetre *0.9)), pygame.RESIZABLE)
    
    
    background_image = pygame.image.load("images/water32.jpg")
    

    #responsive
    # Chargement de la police de caractères
    # police = pygame.font.Font(None, cells_Size)
        # Chargement de la police de caractères
    police = pygame.font.Font(game_font, 20)

     # Création de la carte. Elle prend en parametre:(la taille de la carte, le dictionnaire du type de case par défaut)

    map = Map({"x":mapSize+1,"y":int(mapSize//ratio)},{"char":"*"})
    
    
    # Création des bateaux. Ils prennent en parametre:({le dictionnaire du type de case}, la carte, {la position du Front du bateau}, la direction du bateau, {la taille du bateau})
    vehicule1 = Carrier(map,{"x":18,"y":25},"left",1,color = (255,0,0))
    vehicule2 = BigBoat(map,{"x":30,"y":25},"up",1,color = (255,0,0))
    
    vehicule3 = MedicaleBoat(map,{"x":18,"y":40},"right",1)
    vehicule4 = Submarine(map,{"x":40,"y":25},"down",1)

    vehicule5 = Jet(map,{"x":25,"y":25},"left",1)
    vehicule6 = LittleBoat(map,{"x":35,"y":35},"left",1)

    vehicule11 = Carrier(map,{"x":58,"y":25},"left",2,color = (255,0,0))
    vehicule21 = BigBoat(map,{"x":90,"y":25},"up",2,color = (255,0,0))
    
    vehicule31 = MedicaleBoat(map,{"x":58,"y":40},"right",2)
    vehicule41 = Submarine(map,{"x":80,"y":25},"down",2)

    vehicule51 = Jet(map,{"x":75,"y":25},"left",2)
    vehicule61 = LittleBoat(map,{"x":85,"y":35},"left",2)



    
    # Création de la liste des bateaux jouables
    NewVehicules = [vehicule1,vehicule2,vehicule3,vehicule4,vehicule5,vehicule6,vehicule11,vehicule21,vehicule31,vehicule41,vehicule51,vehicule61]
    
    
    
    
    
    #load les images fixes
    
    vehiculesMenu = [LittleBoat(map,{"x":18,"y":25},"left",1,color = (255,0,0)),
                     MedicaleBoat(map,{"x":18,"y":40},"left",1),
                     BigBoat(map,{"x":30,"y":25},"left",1,color = (255,0,0)),
                     Carrier(map,{"x":18,"y":25},"left",1,color = (255,0,0)),
                     Submarine(map,{"x":40,"y":25},"left",1),
                     Jet(map,{"x":40,"y":25},"left",1)
                     ]
    
    getImages(vehiculesMenu,cells_Size,[],[])
    images = [vehicule.image for vehicule in vehiculesMenu]
    stoneImage1 = pygame.image.load("images/little-stone1.png").convert_alpha()
    stoneImage2 = pygame.image.load("images/big-stone.png").convert_alpha()
    stoneImage3 = pygame.image.load("images/medium-stone.png").convert_alpha()
    element_image = pygame.image.load("images/cross2.png").convert_alpha()
    obstacle_boom = pygame.image.load("images/cross2_obstacle.png").convert_alpha()
    gold = pygame.image.load("images/gold1.png").convert_alpha()
    menu2 = pygame.image.load("images/small_scroll3.png").convert_alpha()
    space = pygame.image.load("images/space_bar1.png").convert_alpha()
    canon = pygame.image.load("images/canon1.png").convert_alpha()
    castleP1 = pygame.image.load("images/Castle_grey22.png").convert_alpha()
    redFlag = pygame.image.load("images/red_flag1.png").convert_alpha()
    yellowFlag = pygame.image.load("images/yellow_flag1.png").convert_alpha()
    bullets = pygame.image.load("images/bullet2.png").convert_alpha()
    
    
    
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
    MAJImage = True
    Image_player = True
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
    place_1 = False
    place_2 = False
    
    # ---------------------------------------------------------------Boucle principale du jeu--------------------------------------------------------------------
    while not close:
        #responsive
        #largeur_fenetre = screen.get_width()
        #hauteur_fenetre = screen.get_height()*0.95        
        #cells_Size = largeur_fenetre//mapSize
        #police = pygame.font.Font(None, cells_Size)
        loadImages = True
        
        

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
                        elif evenement.key == pygame.K_k:
                            if place_1 :
                                place_1 = False
                            else :
                                place_1 = True
                        elif evenement.key == pygame.K_j:
                            if place_2 :
                                place_2 = False
                            else :
                                place_2 = True
                        elif evenement.key == pygame.K_KP_ENTER or evenement.key == pygame.K_RETURN:
                            print("special")
                            if hasattr (vehicule,'special') :
                                vehicule.special()
                            loadImages = True
                            
                        elif evenement.key == pygame.K_TAB:
                            indexVehicule = (indexVehicule+1)%len(vehicules)
                            print(len(vehicules))
                            vehicule = vehicules[indexVehicule]
                            Image_player = True
                            # Si le bateau est mort : on passe au bateau suivant
                            if vehicule.life == 0 :
                                indexVehicule = (indexVehicule+1)%len(vehicules)
                                vehicule = vehicules[indexVehicule]
                                
        
                        elif evenement.key == pygame.K_p:
                            indexTeam = (indexTeam+1)%len(teamsVehicules)
                            vehicules = teamsVehicules[indexTeam]
                            indexVehicule = 0
                            vehicule = vehicules[indexVehicule]
                            Image_player = True
                            
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
            BROWN = (128, 85, 11)
            BEIGE = (252,202,116)
            BEIGE1 = (255,190,77)
            WHITE = (255, 255, 255)
            BLACK = (58, 41, 11)
            RED = (255, 152, 62)

            # Create a surface for the menu rectangle
            # menu_surface = pygame.Surface((400, 200))
            # menu_surface.fill(BROWN)
            # menu_rect = menu_surface.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2))
            # screen.blit(menu, (largeur_fenetre // 2, hauteur_fenetre // 2))
            # screen.blit(menu, (100, 60))
            # screen.blit(menu1, (100, 60))
            screen.blit(menu2, (140, 20))

            # Create a font object for the text and button
            font = pygame.font.Font(None, 24)

            # Create a text surface and get its rect
            police_goal = pygame.font.Font(game_font, 30)
            text1 = "GOAL"
            text = "Destroy the ennemy's base or sink all their ships"
            text_surface1 = police_goal.render(text1, True, RED)
            text_surface = police.render(text, True, BLACK)
            text_rect1 = text_surface1.get_rect(center=(largeur_fenetre // 2, 190))
            text_rect = text_surface.get_rect(center=(largeur_fenetre // 2, 220))

            frame_color = (58, 41, 11) 
            frame_position = (300, 250)  # Top-left corner of the frame
            frame_size = (940, 310)  # Width and height of the frame
            frame_thickness = 3  # Thickness of the frame border

            # Draw the frame
            pygame.draw.rect(screen, frame_color, (*frame_position, *frame_size), frame_thickness)


            # Create a button surface and get its rect
            button_width, button_height = 120, 40
            button_surface = pygame.Surface((button_width, button_height))
            # button_surface.fill(WHITE)
            button_rect = button_surface.get_rect(center=(largeur_fenetre // 2, hauteur_fenetre // 2 + 210))
            
            #Display ships and their characteristics
            police_ship = pygame.font.Font(game_font, 16)

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
        
            text_rect_ship_surface1 = text_ship_surface1.get_rect(center=(730,290))
            text_rect_ship_surface2 = text_ship_surface2.get_rect(center=(730,340))
            text_rect_ship_surface3 = text_ship_surface3.get_rect(center=(810,395))
            text_rect_ship_surface4 = text_ship_surface4.get_rect(center=(870,460))
            text_rect_ship_surface5 = text_ship_surface5.get_rect(center=(810,525))

            # Money explanation

            menu_surface = pygame.Surface((190, 100))
            menu_surface.fill(BEIGE)
            menu_rect = menu_surface.get_rect(center=(1140,305))
            money_text = "For +100"
            canon_text = "Revive +1"
            money_text_surface = police_ship.render(money_text, True, BLACK )
            canon_text_surface = police_ship.render(canon_text, True, BLACK)
            money_text_rect = money_text_surface.get_rect(center=(1120,280))
            canon_text_rect = canon_text_surface.get_rect(center=(1120,322))

            # Create a text surface for the button and get its rect
            button_text = "Press  Spacebar to Play"
            button_text_surface = police.render(button_text, True, BLACK)
            button_text_rect = button_text_surface.get_rect(center=button_rect.center)


            # Blit the menu surface, text surface, and button surface onto the screen
            
            screen.blit(text_surface, text_rect)
            screen.blit(text_surface1, text_rect1)
            # screen.blit(button_surface, button_rect)
            screen.blit(button_text_surface, button_text_rect)
            screen.blit(space, ((largeur_fenetre // 2)-90, hauteur_fenetre // 2 + 190))
            screen.blit(images[0], (320,270))
            screen.blit(images[1], (320,330))
            screen.blit(images[2], (320,380))
            screen.blit(images[3], (320,440))
            screen.blit(images[4], (320,510))
            screen.blit(images[5], (460,448))
            screen.blit(text_ship_surface1, text_rect_ship_surface1)
            screen.blit(text_ship_surface2, text_rect_ship_surface2)
            screen.blit(text_ship_surface3, text_rect_ship_surface3)
            screen.blit(text_ship_surface4, text_rect_ship_surface4)
            screen.blit(text_ship_surface5, text_rect_ship_surface5)
            screen.blit(menu_surface, menu_rect)
            screen.blit(gold, (1190,270))
            screen.blit(canon, (1190,310))
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
            
            #--------------------------------------------------Open popup Place ships p1----------------------------------------------------------------------------
        def place_ships_P1() :

            transparent_black = (0, 0, 0, 228)  # Semi-transparent black

            text = police.render("Pick a ship and place it", True, (255, 255, 255))
            text1 = police.render("Press g to validate", True, (255, 255, 255))

              # Calculate the left half of the screen
            left_half_rect = pygame.Rect(0, 0, largeur_fenetre // 2, hauteur_fenetre)

            # Create a transparent surface to cover the left half of the screen
            filter_surface = pygame.Surface(left_half_rect.size, pygame.SRCALPHA)
            filter_surface.fill(transparent_black)

             # Draw the filtered surface on the left half of the screen
            screen.blit(filter_surface, left_half_rect.topleft)

            # Draw the text at the middle top of the darkened surface
            text_rect = text.get_rect(midtop=(left_half_rect.centerx, 100))
            screen.blit(text, text_rect)
            screen.blit(images[0], (320,210))
            screen.blit(images[1], (320,300))
            screen.blit(images[2], (320,380))
            screen.blit(images[3], (320,460))
            screen.blit(images[4], (320,550))
            text_rect1 = text1.get_rect(midtop=(left_half_rect.centerx, 670))
            screen.blit(text1, text_rect1)




        def place_ships_P2() :

            transparent_black = (0, 0, 0, 228)  # Semi-transparent black

            text = police.render("Pick a ship and place it", True, (255, 255, 255))
            text1 = police.render("Press g to validate", True, (255, 255, 255))

              # Calculate the left half of the screen
            right_half_rect = pygame.Rect(largeur_fenetre // 2, 0, largeur_fenetre // 2, hauteur_fenetre)

            # Create a transparent surface to cover the left half of the screen
            filter_surface = pygame.Surface(right_half_rect.size, pygame.SRCALPHA)
            filter_surface.fill(transparent_black)

             # Draw the filtered surface on the left half of the screen
            screen.blit(filter_surface, right_half_rect.topleft)

            # Draw the text at the middle top of the darkened surface
            text_rect = text.get_rect(midtop=(right_half_rect.centerx, 100))
            screen.blit(text, text_rect)
            screen.blit(images[0], (1120,210))
            screen.blit(images[1], (1110,300))
            screen.blit(images[2], (1080,380))
            screen.blit(images[3], (1100,460))
            screen.blit(images[4], (1120,550))
            text_rect1 = text.get_rect(midtop=(right_half_rect.centerx+60, 670))
            screen.blit(text1, text_rect1)



            #------------------------------------------------------------Fin affichage menu------------------------------------------------------------
            #------------------------------------------------------------Début affichage jeu------------------------------------------------------------


        #chargement des images
        if loadImages:
            
            #teamsVehicules,players = getImages(map.elements,cells_Size,players,teamsVehicules)
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
            vehicule_image = vehicule.image.copy()
            # mask_surface = pygame.Surface(vehicule_image.get_size(), pygame.SRCALPHA)
            # mask_surface.fill((255, 255, 255, 128)) 
            # vehicule_image.blit(vehicule_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            vehicule.image = pygame.transform.rotate(vehicule_image, vehicule.imageAngle - getAngle(vehicule.direction))  
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
            

            

        # Effacement de l'écran avec une couleur bleue
        screen.fill((0, 0, 200))
        
        #Affichage fond d'écran
        screen.blit(background_image, (0, 0))
        
        
        #---------------------------------------Affichage des scores de chaque coté de la page : ---------------------------------------
        # font = pygame.font.Font(None, 36)
        score1 = 0
        score2 = 0
        dead = 0

        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                if "player" in matrice[y][x]:
                    if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==1:
                        score2 = score2 + 10
                        if "self" in matrice[y][x] and hasattr(matrice[y][x]["self"],'life') and matrice[y][x]["self"].life == 0:
                            dead = 2
                            # score2 = score2 + 100
                            # print("score2:", score2)
                            # break

                    if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==2:
                        score1 = score1 + 10
                        if "self" in matrice[y][x] and hasattr(matrice[y][x]["self"],'life') and matrice[y][x]["self"].life == 0:
                            dead = 1
                        #     break
                        # break
        
        if dead == 1:
            # print("score1 before:", score1)
            score1 = score1 + 100
            # print("score1:", score1)
        

        if dead == 2:
            # print("score2 before:", score1)
            score2 = score2 + 100
            # print("score2:", score2)

        if score1>=100:
            for vehicule in vehicules:
                vehicule.revive_tourelle()
            score1 = score1 - 100
            
            # print("score1-100:", score1)

        if score2>=100:
            for vehicule in vehicules:
                vehicule.revive_tourelle()
            score2 = score2 - 100
            
            # print("score2-100:", score2)
                    
        score_text_1 = police.render(f"P1: {score1}", True, (255, 255, 255)) #score équipe 1
        score_text_2 = police.render(f"P2: {score2}", True, (255, 255, 255)) #score équipe 2

        # text_width1 = score_text_1.get_width()
        screen.blit(score_text_1, (10, 20))
        screen.blit(gold, (50, 20))
        text_width = score_text_2.get_width()
        screen.blit(score_text_2, (largeur_fenetre - text_width - 20, 20))
        screen.blit(gold, (largeur_fenetre - text_width+18, 20))

        menu_text = police.render(f"Press M for Menu", True, (255, 255, 255)) #score équipe 2
        text_width_menu = menu_text.get_width()
        screen.blit(menu_text, ((largeur_fenetre  - text_width_menu)// 2, 20))
        #--------------------------------------- Fin Affichage des scores de chaque coté de la page : ---------------------------------------
        
        
        
        
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
                
                if caractere == "o":
                    screen.blit(bullets,(x * cells_Size, y * cells_Size))
                        
                # Impression du caractère dans la fenêtre aux coordonnées x et y
                if caractere != "":
                    texte = police.render(caractere, True, color)
                    screen.blit(texte, (x * cells_Size, y * cells_Size))

        # Mise a jour filtre bateau selectionné 

        if Image_player :
            getImages(map.elements,cells_Size)
            vehicule_image = vehicule.image.copy()
            mask_surface = pygame.Surface(vehicule_image.get_size(), pygame.SRCALPHA)
            mask_surface.fill((255, 255, 255, 228)) 
            vehicule_image.blit(vehicule_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            vehicule.image = pygame.transform.rotate(vehicule_image, vehicule.imageAngle - getAngle(vehicule.direction))
            Image_player = False  

        # Impression des images des bateaux dans la fenêtre
        for element in map.elements:
            # Vérification que le bateau est en vie
            if hasattr(element,'life') and element.life > 0:
                # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                screen.blit(element.image, element.imagePosition)
                
        darkened_image = element_image.copy()
        # obstacle = obstacle_boom.copy()
             
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):    
                if matrice[y][x]["char"] == "X":
            # Darken the slot by drawing a semi-transparent black rectangle
                    screen.blit(darkened_image, ((x-0.25) * cells_Size, (y-0.25) * cells_Size))
                # if matrice[y][x]["char"] == "O":
                #     screen.blit(obstacle, ((x-0.25) * cells_Size, (y-0.25) * cells_Size))
        
            screen.blit(castleP1, (largeur_fenetre-120, hauteur_fenetre// 2))
            screen.blit(castleP1, (0, hauteur_fenetre// 2))
            screen.blit(redFlag, (largeur_fenetre-120, (hauteur_fenetre// 2)-45))
            screen.blit(yellowFlag, (5, (hauteur_fenetre// 2)-35))
        
                            

                

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
          
        if place_1:
            place_ships_P1() 

        if place_2:
            place_ships_P2()       

        if game_over:
            show_game_over_menu(winner) 
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()
    
    
    
    

Main()