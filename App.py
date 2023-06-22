import pygame
from pygame.locals import *
from Vehicule import *
from Map import Map
clock = pygame.time.Clock()

#permet de récuperer l'angle en fonction de la direction, utile pour la rotation des images des bateaux




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
    #team1 
    littleBoat1 = LittleBoat(map,{"x":18,"y":25},"right",1,color = (255,0,0))
    medicaleBoat = MedicaleBoat(map,{"x":18,"y":40},"right",1,color = (255,0,0))
    bigBoat1 = BigBoat(map,{"x":30,"y":25},"right",1,color = (255,0,0))
    carrier1 = Carrier(map,{"x":18,"y":25},"right",1,color = (255,0,0))
    submarine1 = Submarine(map,{"x":40,"y":25},"right",1,color = (255,0,0))
    
    #team2
    littleBoat2 = LittleBoat(map,{"x":18,"y":25},"left",2,color = (0,0,255))
    medicaleBoat2 = MedicaleBoat(map,{"x":18,"y":40},"left",2,color = (0,0,255))
    bigBoat2 = BigBoat(map,{"x":30,"y":25},"left",2,color = (0,0,255))
    carrier2 = Carrier(map,{"x":18,"y":25},"left",2,color = (0,0,255))
    submarine2 = Submarine(map,{"x":40,"y":25},"left",2,color = (0,0,255))
    
    # Création de la liste des bateaux jouables
    NewVehicules = [submarine1,submarine2,carrier1,carrier2,bigBoat1,bigBoat2,medicaleBoat,medicaleBoat2,littleBoat1,littleBoat2]
    
    
    #load les images fixes
    
    vehiculesMenu = [LittleBoat(map,{"x":18,"y":25},"left",1),
                     MedicaleBoat(map,{"x":18,"y":40},"left",1),
                     BigBoat(map,{"x":30,"y":25},"left",1),
                     Carrier(map,{"x":18,"y":25},"left",1),
                     Submarine(map,{"x":40,"y":25},"left",1),
                     Jet(map,{"x":40,"y":25},"left",1)
                     ]
    
    getImages(vehiculesMenu,cells_Size,[],[])
    images = [vehicule.image for vehicule in vehiculesMenu]
    element_image = pygame.image.load("images/cross2.png").convert_alpha()
    gold = pygame.image.load("images/gold1.png").convert_alpha()
    
    # ajout des obstacles
    map.randGenerate()
    
    #chargement des images
    teamsVehicules,players = getImages(NewVehicules,cells_Size)
    

    # Variable de boucle
    direction = None
    close = False
    fire = False
    MAJImage = True
    loadImages = False
    Image_player = True
    
    # Variable d'affichage
    show_popup = True
    game_over = False
    
    # Initialisation du bateau actif
    
    indexVehicule = 0
    indexTeam = 0
    vehicules = teamsVehicules[indexTeam]
    vehicule = vehicules[indexVehicule]

    distanceImage = 0
    winner = 0
    one_is_placed = False
    two_is_placed = False
    place_1 = True
    place_2 = True
    direction_placement = "right"
    vehiculeFixed = []
    fixVehicule = False
    
    nb_dep_max=5
    nb_tir_max=3
    nb_speciale_max=1
    nb_dep=0
    nb_tir=0
    nb_speciale=0


    
    
    # ---------------------------------------------------------------Boucle principale du jeu--------------------------------------------------------------------
    while not close:
        #responsive
        mouse_x, mouse_y = pygame.mouse.get_pos()
        largeur_fenetre = screen.get_width()
        hauteur_fenetre = screen.get_height()      
        cells_Size = largeur_fenetre/mapSize
        background_image = pygame.image.load("images/water32.jpg")
        background_image = pygame.transform.scale(background_image, (int(largeur_fenetre),int(hauteur_fenetre)))
        police = pygame.font.Font(game_font, int(cells_Size*(20/17)))
        getImages(vehiculesMenu,cells_Size,[],[])
        images = [vehicule.image for vehicule in vehiculesMenu]
        bullets = pygame.image.load("images/bullet2.png").convert_alpha()
        obstacle_boom = pygame.image.load("images/cross2_obstacle.png").convert_alpha()
        
        loadImages = True
        
        

        #chargement de la matrice de la carte
        matrice = map.getMatrice()
        
        #Définition des tours
        dep=False
        tir = False  
        speciale=False 
        if (nb_dep!=nb_dep_max):
            dep=True
        if (nb_tir!=nb_tir_max):
            tir = True
        if(nb_speciale!=nb_speciale_max):
            speciale=True
        
        # Gestion des événements claviers et souris
        for evenement in pygame.event.get():
            
            # Si l'utilisateur quitte le jeu
            if evenement.type == pygame.QUIT:
                close = True
            
            # Si on change la taile de la fentre
            elif evenement.type == pygame.VIDEORESIZE:
                width, height = evenement.size
                new_ratio = width / height
                if round(new_ratio, 1) > round(ratio, 1) :
                    new_width = int(height * ratio)
                    window = pygame.display.set_mode((new_width, height), pygame.RESIZABLE)
                elif round(new_ratio, 1) < round(ratio, 1):
                    new_height = int(width / ratio)
                    window = pygame.display.set_mode((width, new_height), pygame.RESIZABLE)
                loadImages = True
                Image_player = True
            
            
            if distanceImage == 0:
                # Capte les touches enfoncées pour définir les actions à effectuer
                if evenement.type == pygame.MOUSEBUTTONDOWN :
                    if one_is_placed == False or two_is_placed == False:
                        print ("clic")
                        if vehicule in vehiculeFixed:
                            vehiculeFixed.remove(vehicule)
                        else:
                            fixVehicule = True
                        

                if evenement.type == pygame.KEYDOWN:
                    if show_popup == True :
                        if evenement.key == pygame.K_SPACE:
                            show_popup = False
                    else :
                        if one_is_placed == False or two_is_placed == False:
                            if evenement.key == pygame.K_q:
                                direction_placement = "left"
                            elif evenement.key == pygame.K_d:
                                direction_placement = "right"
                            elif evenement.key == pygame.K_z:
                                direction_placement = "up"
                            elif evenement.key == pygame.K_s:
                                direction_placement = "down"
                            # detecte si l y a un click de souris

                            elif evenement.key == pygame.K_p: 
                                if one_is_placed == False:
                                    one_is_placed = True
                                elif two_is_placed == False:
                                    two_is_placed = True
                                
                                indexTeam = (indexTeam+1)%len(teamsVehicules)
                                vehicules = teamsVehicules[indexTeam]
                                indexVehicule = 0
                                vehicule = vehicules[indexVehicule]
                                Image_player = True     
                                
                            elif evenement.key == pygame.K_TAB:
                                indexVehicule = (indexVehicule+1)%len(vehicules)
                                vehicule = vehicules[indexVehicule]
                                Image_player = True
                
                                
                                
                                
                                
                            


                            # Vérification si le clic de souris est à l'intérieur du rectangle
                            # if rectangle.collidepoint(mouse_x, mouse_y):
                            #     print("Clic sur le rectangle détecté")
                        
                        # if one_is_placed == False:
                            
                            
                            
                        # elif two_is_placed == False:
                            
                        #     two_is_placed = True
                            
                        else:
                        
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
                            elif evenement.key == pygame.K_SPACE and tir==True:
                                fire = True
                                nb_tir+=1
                        
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
                                    
                            elif (evenement.key == pygame.K_KP_ENTER or evenement.key == pygame.K_RETURN) :
                                print("special")
                                if hasattr (vehicule,'special') and speciale==True:
                                    vehicule.special()
                                    nb_speciale+=1
                                loadImages = True
                                Image_player = True
                                
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
                                    
                                
                                nb_dep=0
                                nb_tir=0
                                nb_speciale=0
                            
                            elif evenement.key == pygame.K_x:
                                if (map.canExplode(vehicule)):
                                    game_over = True
                                    winner = vehicule.type["player"]
                                    print ("winner : ",winner)
                            elif evenement.key == pygame.K_m:
                                show_popup = True
                            elif evenement.key == pygame.K_v:
                                game_over = True
                                
                                
 

     



        
        
            #------------------------------------------------------------Début affichage jeu------------------------------------------------------------


        #chargement des images
        if loadImages:
            if Image_player :
                teamsVehicules,players = getImages(map.elements,cells_Size,players,teamsVehicules)
                getImages(map.elements,cells_Size)
                vehicule_image = vehicule.image.copy()
                mask_surface = pygame.Surface(vehicule_image.get_size(), pygame.SRCALPHA)
                mask_surface.fill((255, 255, 255, 128)) 
                vehicule_image.blit(vehicule_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                vehicule.image = pygame.transform.rotate(vehicule_image, vehicule.imageAngle - getAngle(vehicule.direction))
                Image_player = False
            vehicules = teamsVehicules[indexTeam]
            loadImages = False
            

        # Déplacement du vehicule
        if direction is not None:
            if dep:
                if vehicule.move(direction) :
                    nb_dep += 1
                    print("Move ", direction) 
                    distanceImage = cells_Size * vehicule.speed
            MAJImage = True
            # Réinitialisation des variables de déplacement
            direction = None
        
        # Tir du bateau
        if fire :
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
                vehicule.imagePosition = (int((vehicule.Front["x"]-vehicule.size["y"]+1)*cells_Size - distanceImage) ,(int(vehicule.Front["y"])*cells_Size ))
            elif vehicule.direction == "down":
                vehicule.imagePosition = (int((vehicule.Front["x"]-vehicule.size["x"]+1)*cells_Size)  ,int((vehicule.Front["y"]-vehicule.size["y"]+1)*cells_Size - distanceImage ))
            elif vehicule.direction == "left":
                vehicule.imagePosition = (int(vehicule.Front["x"]*cells_Size  + distanceImage) ,int((vehicule.Front["y"]-vehicule.size["x"] +1)*cells_Size))
            
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
                if caractere == "o":
                    screen.blit(bullets,(x * cells_Size, y * cells_Size))
                        
                # Impression du caractère dans la fenêtre aux coordonnées x et y
                if caractere != "":
                    texte = policeMap.render(caractere, True, color)
                    screen.blit(texte, (x * cells_Size, y * cells_Size))
                    
                    
                    

        # Impression des images des bateaux dans la fenêtre
        for element in map.elements:
            # if isinstance(element, Vehicule):
            #     print (element)
            # Vérification que le bateau est en vie
            if hasattr(element,'image'):
                # Affichage de l'image du bateau, i correspond à l'index de l'équipe et j à l'index du bateau
                screen.blit(element.image, element.imagePosition)
                
        darkened_image = element_image.copy()
        obstacle = obstacle_boom.copy()
             
        for y in range(len(matrice)):
            for x in range(len(matrice[y])):    
                if matrice[y][x]["char"] == "X":
                # Darken the slot by drawing a semi-transparent black rectangle
                    screen.blit(darkened_image, (int((x-0.20) * cells_Size), int((y-0.10) * cells_Size)))
                    if "obstacle" in matrice[y][x]:
                        screen.blit(obstacle, (int((x-0.20) * cells_Size), int((y-0.10) * cells_Size)))

        
                

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

             
        if one_is_placed:
            place_1 = False
        if two_is_placed:
            place_2 = False
                
        if show_popup:
            show_popup_menu(screen,cells_Size,game_font,police,images)      
        

        elif place_1 or place_2:
            player = vehicule.type["player"]
                
            if vehicule in map.elements:
                if not vehicule in vehiculeFixed:
                    map.elements.remove(vehicule)
            
            if not vehicule in vehiculeFixed:
                if player == 1:
                    if mouse_x > 50 * cells_Size :
                        vehicule.Front["x"] = int(mouse_x//cells_Size)
                        vehicule.Front["y"] = int(mouse_y//cells_Size)
                        
 
                if player == 2:
                    if mouse_x < 50 * cells_Size :
                        vehicule.Front["x"] = int(mouse_x//cells_Size)
                        vehicule.Front["y"] = int(mouse_y//cells_Size)
            
                vehicule.direction = direction_placement
                getImages(NewVehicules,cells_Size)
                Image_player = True
                vehicule.reloadBack()  
                fixe = map.addElement(vehicule)
                print (fixe)
                if (fixe and fixVehicule):
                    vehiculeFixed.append(vehicule)
                    fixVehicule = False
                    if teamsVehicules[(indexTeam+1)%len(teamsVehicules)] not in vehiculeFixed:
                        indexVehicule = (indexVehicule+1)%len(vehicules)
                        vehicule = vehicules[indexVehicule]
            place_ships_P(player,police,vehicules,largeur_fenetre,hauteur_fenetre,screen) 
            
            MAJImage = True
            

                
        elif game_over:
            show_game_over_menu(winner) 
        # Mise à jour de la fenêtre  
        pygame.display.flip()
        print()
        
        # Limitation des fps pour économiser les ressources de l'ordinateur
        clock.tick(40) 

    # Fermeture de Pygame
    pygame.quit()
#--------------------------------------- Fin de boucle de jeu : ---------------------------------------
    
    
def getAngle(direction):
    
    if direction == "up":
        return 0
    if direction == "right":
        return 90
    if direction == "down":
        return 180
    if direction == "left":
        return -90
     
def getImages(elements,cells_Size,players =[],teamsVehicules=[]): 
    
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
            element.imagePosition = (int((element.Front["x"]-element.size["y"] + 1)*cells_Size),int((element.Front["y"])*cells_Size))
        elif element.direction == "down":
            element.imagePosition = (int((element.Front["x"]-element.size["x"] + 1)*cells_Size),int((element.Front["y"]-element.size["y"] + 1)*cells_Size))
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



#---------------------------------------------------------------Affichage du menu--------------------------------------------------------------------

def show_popup_menu(screen,cells_Size,game_font,police,images):
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
    screen.blit(images[5], (int(cells_Size*((460 + decallageX)/17)),int(cells_Size*((448 + decallageY)/17))))
    screen.blit(text_ship_surface1, text_rect_ship_surface1)
    screen.blit(text_ship_surface2, text_rect_ship_surface2)
    screen.blit(text_ship_surface3, text_rect_ship_surface3)
    screen.blit(text_ship_surface4, text_rect_ship_surface4)
    screen.blit(text_ship_surface5, text_rect_ship_surface5)
    screen.blit(menu_surface, menu_rect)
    gold = pygame.image.load("images/gold.png")
    gold = pygame.transform.scale(gold, (int(cells_Size*(25/17)), int(cells_Size*(25/17))))
    screen.blit(gold, (int(cells_Size*((1190 + decallageX)/17)),int(cells_Size*((270 + decallageY)/17))))
    canon = pygame.image.load("images/canon1.png").convert_alpha()
    canon = pygame.transform.scale(canon, (int(cells_Size*(35/17)), int(cells_Size*(27/17))))
    screen.blit(canon, (int(cells_Size*((1190 + decallageX)/17)),int(cells_Size*((310 + decallageY)/17))))
    screen.blit(money_text_surface, money_text_rect)
    screen.blit(canon_text_surface, canon_text_rect)
    
    
#--------------------------------------------------Open popup Place ships p1----------------------------------------------------------------------------
def place_ships_P(player,police,vehicules,largeur_fenetre,hauteur_fenetre,screen) :

    transparent_black = (0, 0, 0, 228)  # Semi-transparent black
    images={}
    for vehicule in vehicules:
        if isinstance(vehicule,LittleBoat):
            images["littleBoat"] = vehicule.image
        if isinstance(vehicule,MedicaleBoat):
            images["medicalBoat"] = vehicule.image
        if isinstance(vehicule,BigBoat):
            images["bigBoat"] = vehicule.image
        if isinstance(vehicule,Carrier):
            images["carrier"] = vehicule.image
        if isinstance(vehicule,Submarine):
            images["submarine"] = vehicule.image
            

    text = police.render("Pick a ship and place it", True, (255, 255, 255))
    text1 = police.render("Press P to validate", True, (255, 255, 255))

        # Calculate the left half of the screen
    left_half_rect = pygame.Rect(0, 0, largeur_fenetre // 2, hauteur_fenetre)
    right_half_rect = pygame.Rect(largeur_fenetre // 2, 0, largeur_fenetre // 2, hauteur_fenetre)

    # Create a transparent surface to cover the left half of the screen
    if player == 1:
        filter_surface = pygame.Surface(left_half_rect.size, pygame.SRCALPHA)
    if player  == 2: 
        filter_surface = pygame.Surface(right_half_rect.size, pygame.SRCALPHA)
    
    filter_surface.fill(transparent_black)

    if player == 1:
        screen.blit(filter_surface, left_half_rect.topleft)
        text_rect = text.get_rect(midtop=(left_half_rect.centerx, 100))
        posX = [320 for i in range(5)]
        
    if player == 2:
        screen.blit(filter_surface, right_half_rect.topleft)
        text_rect = text.get_rect(midtop=(right_half_rect.centerx, 100))
        posX=[1120,1110,1080,1100,1120]
    # Draw the text at the middle top of the darkened surface
    screen.blit(text, text_rect)
    if "littleBoat" in images:
        screen.blit(images["littleBoat"], (posX[0],210))
    if "medicalBoat" in images:
        screen.blit(images["medicalBoat"], (posX[1],300))
    if "bigBoat" in images:
        screen.blit(images["bigBoat"], (posX[2],380))
    if "carrier" in images:
        screen.blit(images["carrier"], (posX[3],460))
    if "submarine" in images:
        screen.blit(images["submarine"], (posX[4],550))
        
    if player == 1:
        text_rect1 = text1.get_rect(midtop=(left_half_rect.centerx, 670))
    elif player == 2:
        text_rect1 = text1.get_rect(midtop=(right_half_rect.centerx, 670))  
    screen.blit(text1, text_rect1)

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
    

Main()