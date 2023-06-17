import random
from Vehicule import Vehicule
from Bullet import Bullet
from Obstacle import Obstacle
from Element import Element
from typing import List
class Map:
    # Constructeur qui prend en parametre la taille {"x":taille_x, "y":taille_y}, le type de case par défaut {"char":" "} et la liste des elements de la map (bateaux, obstacles, etc...)
    def __init__(self, size, type, elements:List[Element] = []):
        self.type = type
        self.size = size
        self.elements = elements
        
        # les bullets sont stockés dans une liste a part pour ne pas les afficher dans la matrice
        self.bullets = []
        
        # Création de la matrice de la map en fonction de sa taille et de son type de case par défaut
        self.matrice = [[type for x in range(size["x"])] for j in range(size["y"])]
    
    
    def getMatrice(self):
        return self.matrice
    
    # Ajoute un element à la matrice en fonction de sa direction, de sa taille et de sa matrice et de sa position Front. 
    # C'est aussi ici que l'on gère les différentes inetractions entre les elements de la map (tire des tourelles, collision, etc...)
    def addElementToMatrice(self,element:Element):
        if hasattr(element, 'life'):
            newLife = 0
        # On parcours la matrice de l'element et on les entre dans la matrice de la map en fonction de la direction de l'element et de sa position Front
        for y in range(element.size["y"]):
            for x in range(element.size["x"]):
                if hasattr(element, 'life'):
                    if (element.matrice[y][x]["char"] != "X"):
                        newLife += 1
                # Calcul de la position de chaques cases de l'élément dans la matrice de la map
                if (element.direction == "up"):
                    posX = element.Front["x"] + x
                    posY = element.Front["y"] + y
                elif (element.direction == "down"):
                    posX = element.Front["x"] - x
                    posY = element.Front["y"] - y
                elif (element.direction == "right"):
                    posX = element.Front["x"] - y
                    posY = element.Front["y"] + x
                elif (element.direction == "left"):
                    posX = element.Front["x"] + y
                    posY = element.Front["y"] - x
                
                # C'est une sécurité pour éviter les erreurs de dépassement de la matrice
                if (posX >= 0 and posX < self.size["x"] and posY >= 0 and posY < self.size["y"]):   
                    self.matrice[posY][posX] = element.matrice[y][x]
                    
                # Si la case est une tourelle, on tire une bullet en fonction de la direction de la tourelle et de la direction du bateau
                bulletDirection = None
                if (element.matrice[y][x]["char"] == "f"):
                    print("addElementToMatrice fire")
                    if (element.direction == "up" and element.matrice[y][x]["direction"] == "up" or element.direction == "down" and element.matrice[y][x]["direction"] == "down" or element.direction == "right" and element.matrice[y][x]["direction"] == "left" or element.direction == "left" and element.matrice[y][x]["direction"] == "right" ):
                        bulletDirection = "up"
                        
                    if (element.direction == "down" and element.matrice[y][x]["direction"] == "up" or element.direction == "up" and element.matrice[y][x]["direction"] == "down" or element.direction == "left" and element.matrice[y][x]["direction"] == "left" or element.direction == "right" and element.matrice[y][x]["direction"] == "right" ):
                        bulletDirection = "down"
                    
                    if (element.direction == "right" and element.matrice[y][x]["direction"] == "up" or element.direction == "left" and element.matrice[y][x]["direction"] == "down" or element.direction == "down" and element.matrice[y][x]["direction"] == "left" or element.direction == "up" and element.matrice[y][x]["direction"] == "right" ):
                        bulletDirection = "right"
                    
                    if (element.direction == "left" and element.matrice[y][x]["direction"] == "up" or element.direction == "right" and element.matrice[y][x]["direction"] == "down" or element.direction == "up" and element.matrice[y][x]["direction"] == "left" or element.direction == "down" and element.matrice[y][x]["direction"] == "right" ):
                        bulletDirection = "left"
                
                # On ajoute la bullet à la liste des bullets de la map
                if (bulletDirection != None):
                    bullet = Bullet({"x":posX,"y":posY},bulletDirection,element.type)
                    self.bullets.append(bullet)
                    bullet.run()
        element.life = newLife
                                       
        
    # Recharge la matrice de la map avec tous ses elements
    # Attention, cette fonction est très couteuse en ressources, il faut donc l'utiliser avec parcimonie
    def reloadMatrice(self):         
        self.matrice = [[self.type for x in range(self.size["x"])] for j in range(self.size["y"])]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    def reloadBullets(self):
        for bullet in self.bullets:
            
            nonCollisions = [self.type["char"],"X","f"]
            
            #supprier la bullet si elle sort de la map
            if (bullet.position["x"] < 0 or bullet.position["x"] >= self.size["x"] or bullet.position["y"] < 0 or bullet.position["y"] >= self.size["y"]):
                self.bullets.remove(bullet)
            elif (bullet.distance <= 0):
                self.bullets.remove(bullet)
            
            #supprimer la bullet si elle touche un obstacle
            
            elif (self.matrice[bullet.position["y"]][bullet.position["x"]]["char"] not in nonCollisions):
                if (self.matrice[bullet.position["y"]][bullet.position["x"]]["id"] != bullet.type["id"]):
                    self.bullets.remove(bullet)
                    self.matrice[bullet.position["y"]][bullet.position["x"]]["char"] = "X"
                
            if (bullet in self.bullets):
                bullet.run()
        
    
    # Ajoute un element a la map (bateau, obstacle, etc...)
    def addElement(self,element:Element):
        if (element != None):
            if(not self.collide(element)):
                self.elements.append(element)
                self.reloadMatrice()
    
    # Supprime un element de la map si il existe (bateau, obstacle, etc...)
    def removeElement(self,element:Element):
        if (element != None):
            if (element in self.elements):
                self.elements.remove(element)
                self.reloadMatrice()
         
    # Detecte si le bateau entre en collision avec un autre bateau
    def collide(self,vehicule,lastVehicule:Vehicule = None):
        # On verrifie si le bateau est dans la map sinon on detecte une collision
        if (vehicule.Front["x"] < 0 or vehicule.Front["x"] >= self.size["x"] or vehicule.Front["y"] < 0 or vehicule.Front["y"] >= self.size["y"]):
            print("out of map")
            return True
        
        if (vehicule.Back["x"] < 0 or vehicule.Back["x"] >= self.size["x"] or vehicule.Back["y"] < 0 or vehicule.Back["y"] >= self.size["y"]):
            print("out of map")
            return True
        
        # On supprime le bateau de la map afin de générer une matrice de la map sans le bateau que l'on nomme matrice1
        self.removeElement(lastVehicule)
        matrice1 = self.matrice.copy()
        
        # On ajoute la nouvelle position du bateau à la map afin de générer une matrice de la map avec le bateau que l'on nomme matrice2
        self.elements.append(vehicule)
        self.reloadMatrice()
        matrice2 = self.matrice.copy()
        
        # On remet la map dans son état initial
        self.removeElement(vehicule)
        self.addElement(lastVehicule)
        self.reloadMatrice()
        
        # On compare les deux matrices pour voir si il y a une supperposition de charactère pour une case de la map (autre que le charactère de la map)
        nonCollision = [self.type["char"],"J","T"]
        for y in range(len(matrice1)):
            for x in range(len(matrice1[0])):
                if (matrice1[y][x]["char"] not in nonCollision and matrice2[y][x]["char"] not in nonCollision and not matrice1[y][x]["id"] == matrice2[y][x]["id"]):
                    print("collision",matrice1[y][x]["char"],matrice2[y][x]["char"])
                    return True
        return False
        
    #Génération aléatoire de la map
    def randGenerate(self):
        
        
        # On génère un nombre aléatoire d'obstacle
        number_Obstacle = random.randint(5, 10)
        for i in range(number_Obstacle):
            
            # On génère aléatoirement la position, la taille et la direction de l'obstacle
            pos_X = random.randint(0, self.size["x"]-1)
            pos_Y = random.randint(0, self.size["y"]-1)
            size_X = random.randint(1, 10)
            size_Y = random.randint(1, 10)
            direction = random.choice(["up","down","right","left"])
            
            # On ajoute l'obstacle à la map si il n'y a pas de collision
            obstacle = Vehicule({"char":"R","able":True,"color":(255,255,255),"player":0},self.copy(),{"x":pos_X,"y":pos_Y},direction,{"x":size_X,"y":size_Y})
            self.addElement(obstacle)       
        
        
    # Copie de la map
    def copy(self):
        return Map(self.size,self.type,self.elements.copy())
    
    # Affichage de la map
    def __str__(self) -> str:
        matrice = ""
        for y in range(self.size["y"]):
            for x in range(self.size["x"]):
                matrice += str(self.matrice[y][x]['char']) + " "
            matrice += "\n"
        return f"Map: {self.type} \n\n{matrice}"
    