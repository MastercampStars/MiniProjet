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
    largeur_fenetre = 1520
    hauteur_fenetre = 780
    cells_Size = 15
    game_font = 'assets/joystix monospace.ttf'

    # Création de la fenêtre Resizable
    screen = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.RESIZABLE)
    pygame.display.set_caption("Bataille navale")
    background_image = pygame.image.load("images/water32.jpg")
    
    #initialisation des listes nécessaires pour l'affichage des images
    allImag = []
    allPos = []
    allAngles = []

    
    # Chargement de la police de caractères
    police = pygame.font.Font(game_font, 20)


    # Création de la carte. Elle prend en parametre:(la taille de la carte, le dictionnaire du type de case par défaut)
    map = Map({"x":85,"y":49},{"char":" "})
    # Création des bateaux. Ils prennent en parametre:({le dictionnaire du type de case}, la carte, {la position du Front du bateau}, la direction du bateau, {la taille du bateau})
    #Team 1
    boat1 = Boat({"char":"P","color":(0,255,0),"able":True,"player":1},map,{"x":18,"y":25},"left",{"x":3,"y":5}) #bateau de base
    boat2 = Boat({"char":"N","color":(0,255,0),"able":True,"player":1},map,{"x":50,"y":25},"left",{"x":2,"y":7}) #bateau médical
    boat3 = Boat({"char":"M","color":(0,255,0),"able":True,"player":1},map,{"x":10,"y":25},"left",{"x":3,"y":13}) #gros bateau
    boat4 = Boat({"char":"L","color":(0,255,0),"able":True,"player":1},map,{"x":30,"y":25},"left",{"x":4,"y":9}) #porte-avion
    boat5 = Boat({"char":"C","color":(0,255,0),"able":True,"player":1},map,{"x":60,"y":25},"left",{"x":3,"y":7}) #sous-marin
    plane1 = Boat({"char":"R","color":(0,255,0),"able":True,"player":1},map,{"x":70,"y":25},"left",{"x":3,"y":3}) #avion
    stone1 = Boat({"char":"S","color":(0,255,0),"able":True,"player":1},map,{"x":80,"y":45},"left",{"x":2,"y":2}) #avion
    stone2 = Boat({"char":"B","color":(0,255,0),"able":True,"player":1},map,{"x":80,"y":65},"left",{"x":7,"y":3}) #avion
    # Team 2
    boat12 = Boat({"char":"P","color":(255,0,0),"able":True,"player":2},map,{"x":22,"y":40},"left",{"x":3,"y":5})
    boat22 = Boat({"char":"N","color":(255,0,0),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":2,"y":7})
    boat32 = Boat({"char":"M","color":(255,0,0),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":3,"y":13})
    boat42 = Boat({"char":"L","color":(255,0,0),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":4,"y":9})
    boat52 = Boat({"char":"C","color":(255,0,0),"able":True,"player":2},map,{"x":50,"y":40},"left",{"x":3,"y":7})
    plane2 = Boat({"char":"R","color":(255,0,0),"able":True,"player":2},map,{"x":70,"y":25},"left",{"x":3,"y":3})
    stone12 = Boat({"char":"Q","color":(0,255,0),"able":True,"player":1},map,{"x":80,"y":44},"left",{"x":8,"y":4}) #avion
    stone22= Boat({"char":"B","color":(0,255,0),"able":True,"player":1},map,{"x":83,"y":47},"left",{"x":9,"y":4}) #avion

    
    # Création d'une liste par team
    team1 = [boat1, boat2, boat3, boat4, boat5, plane1, stone1, stone2]
    team2 = [boat12, boat22, boat32, boat42, boat52, plane2, stone12, stone22]
    
    # Création d'une liste de toutes les teams
    teamsBoats = [team1,team2]
    
    # Chargement de l'image du bateau par défaut (on pourra changer l'image en fonction du type de bateau plus tard si besoin)
    boatImageP = pygame.image.load("assets/corvette.png").convert_alpha()
    boatImageN = pygame.image.load("assets/bateauMedical2.png").convert_alpha()
    boatImageM = pygame.image.load("assets/bigBoat.png").convert_alpha()
    boatImageL = pygame.image.load("assets/porteAvion.png").convert_alpha()
    boatImageC = pygame.image.load("assets/sousMarin.png").convert_alpha()
    boatImageR = pygame.image.load("assets/avionMilitaire.png").convert_alpha()
    stoneImage1 = pygame.image.load("images/little-stone1.png").convert_alpha()
    stoneImage2 = pygame.image.load("images/big-stone.png").convert_alpha()
    stoneImage3 = pygame.image.load("images/medium-stone.png").convert_alpha()
    element_image = pygame.image.load("images/cross2.png").convert_alpha()
    gold = pygame.image.load("images/gold1.png").convert_alpha()
    # menu = pygame.image.load("images/small_scroll.png").convert_alpha()
    # menu1 = pygame.image.load("images/Big_scroll1.png").convert_alpha()
    menu2 = pygame.image.load("images/small_scroll3.png").convert_alpha()
    space = pygame.image.load("images/space_bar1.png").convert_alpha()
    canon = pygame.image.load("images/canon1.png").convert_alpha()
    castleP1 = pygame.image.load("images/Castle_grey22.png").convert_alpha()
    redFlag = pygame.image.load("images/red_flag1.png").convert_alpha()
    yellowFlag = pygame.image.load("images/yellow_flag1.png").convert_alpha()


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
            if(boat.type["char"]=="P"):
                image = pygame.transform.scale(boatImageP, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="N"):
                image = pygame.transform.scale(boatImageN, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="M"):
                image = pygame.transform.scale(boatImageM, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="L"):
                image = pygame.transform.scale(boatImageL, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="C"):
                image = pygame.transform.scale(boatImageC, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="R"):
                image = pygame.transform.scale(boatImageR, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="S"):
                image = pygame.transform.scale(stoneImage1, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="B"):
                image = pygame.transform.scale(stoneImage2, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
            if(boat.type["char"]=="Q"):
                image = pygame.transform.scale(stoneImage3, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))


            # Faites pivoter l'image en fonction de l'angle du bateau et ajoutez-la à la liste des images
            images.append(pygame.transform.rotate(image, - angles[-1]))
        
        # Ajout des listes de charactéristiques à la liste des listes de charactéristiques
        allImag.append(images)
        allPos.append(positions)
        allAngles.append(angles)
    


    # Génération d'obstacles aléatoires de la carte après avoir ajouté les bateaux pour éviter les collisions au chargement
    map.randGenerate()
    
    # if(map.element[-1]=="R"):
    #             image = pygame.transform.scale(stoneImageP, ((boat.size["x"]-0.5) * cells_Size, (boat.size["y"]-0.5)*cells_Size))
    
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
    show_popup = True
    game_over = False

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
                    
                    
                    elif evenement.key == pygame.K_m:
                        show_popup = True
                    elif evenement.key == pygame.K_v:
                        game_over = True
                elif evenement.key == pygame.K_SPACE:
                    show_popup = False

                    
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
            # text_ship1 = "The corvette can move twice as far as the other ships"
            # text_ship2 = "The medical boat can heal one of your other ships"
            # text_ship3 = "The tank ship can shoot up to 6 bullets at a time"
            # text_ship4 = "The transporter can launch a plane that avoids collisions"
            # text_ship5 = "The submarine avoids collisions but can't blow itself up"


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
        
            # text_rect_ship_surface1 = text_ship_surface1.get_rect(center=(630,290))
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
    





        def show_game_over_menu(winner) :
            RED = (255,0,0)
            transparent_black = (0, 0, 0, 200)
            transparent_white = (255, 255, 255, 1)  # Semi-transparent black
            police_end = pygame.font.Font(game_font, 50)
            police_last = pygame.font.Font(game_font, 15)
            # Game Over text
            game_over_text = police_end.render("GAME OVER", True, RED)

            # Winner text
            winner_text = police.render(f"Player {winner} wins!", True, (255, 255, 255))

            retry_text = police_last.render(f"press x to exit", True, transparent_white)

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

            retry_text_rect = retry_text.get_rect(midtop=(screen_center[0], winner_text_rect.bottom + 250))
            screen.blit(retry_text, retry_text_rect)

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
        
         
        # # Effacement de l'écran avec une couleur bleue
        # screen.fill((0, 0, 200))
        
         # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the background
   
        screen.blit(background_image, (0, 0))

        
        #Affichage des scores de chaque coté de la page : 
        # font = pygame.font.Font(None, 36)
        score1 = 0
        score2 = 0

        for y in range(len(matrice)):
            for x in range(len(matrice[y])):
                if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==1:
                    score2 = score2 + 1
                if matrice[y][x]["char"] == "X" and matrice[y][x]["player"]==2:
                    score1 = score1 + 1
                    
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
                # screen.blit(texte, (x * cells_Size, y * cells_Size))
                

        # Impression des images des bateaux dans la fenêtre
        for i in range (len(teamsBoats)):
            inlife_boats = 0
            for j in range (len(boats)):
                
                # Vérification que le bateau est en vie
                if teamsBoats[i][j].life > 0:
                    
                    # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                    screen.blit(allImag[i][j], allPos[i][j])
                    # element_image = allImag[i][j]
                    darkened_image = element_image.copy()
                    # mask_surface = pygame.Surface(element_image.get_size(), pygame.SRCALPHA)
                    # mask_surface.fill((0, 0, 0, 28)) 
                    # darkened_image.blit(darkened_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                    for y in range(len(matrice)):
                        for x in range(len(matrice[y])):    
                            if matrice[y][x]["char"] == "X":
                # Darken the slot by drawing a semi-transparent black rectangle
                                
                                
                                screen.blit(darkened_image, (x * cells_Size, y * cells_Size))
                                
                                # darken_surface = pygame.Surface((15  , 15), pygame.SRCALPHA)
                                # darken_surface.fill((0, 0, 0, 28))  # Semi-transparent black color
                                # screen.blit(darken_surface, (x * cells_Size, y * cells_Size))
                    inlife_boats += 1

            screen.blit(castleP1, (1410, hauteur_fenetre// 2))
            screen.blit(castleP1, (0, hauteur_fenetre// 2))
            screen.blit(redFlag, (1410, (hauteur_fenetre// 2)-45))
            screen.blit(yellowFlag, (5, (hauteur_fenetre// 2)-35))

            # Si tous les bateaux de l'équipe sont morts, on affiche un message
            if inlife_boats == 0:
                game_over=True
                print("Team ", i+1, " is dead")
                close = True
                break
                
        if show_popup:
            show_popup_menu()       
          
        if game_over:
            show_game_over_menu(1)     
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()
Main()