import random
from Base import Base
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
        if hasattr(element, 'life'):
            element.life = newLife
                                       
        
    # Recharge la matrice de la map avec tous ses elements
    # Attention, cette fonction est très couteuse en ressources, il faut donc l'utiliser avec parcimonie
    def reloadMatrice(self):         
        self.matrice = [[self.type for x in range(self.size["x"])] for j in range(self.size["y"])]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    def reloadBullets(self):
        for bullet in self.bullets:
            
            #supprier la bullet si elle sort de la map
            if (bullet.position["x"] < 0 or bullet.position["x"] >= self.size["x"] or bullet.position["y"] < 0 or bullet.position["y"] >= self.size["y"]):
                self.bullets.remove(bullet)
            elif (bullet.distance <= 0):
                self.bullets.remove(bullet)
            
            #supprimer la bullet si elle touche un obstacle
            elif "collide" in  self.matrice[bullet.position["y"]][bullet.position["x"]] :
                if ( "bullet" in self.matrice[bullet.position["y"]][bullet.position["x"]]["collide"] ):
                    if (self.matrice[bullet.position["y"]][bullet.position["x"]]["id"] != bullet.type["id"]):
                        self.bullets.remove(bullet)
                        newCollide = self.matrice[bullet.position["y"]][bullet.position["x"]]["collide"].copy()
                        newCollide.remove("bullet")
                        self.matrice[bullet.position["y"]][bullet.position["x"]]["collide"]= newCollide
                        self.matrice[bullet.position["y"]][bullet.position["x"]]["char"] = "X"
                
            if (bullet in self.bullets):
                bullet.run()
        
    
    # Ajoute un element a la map (bateau, obstacle, etc...)
    def addElement(self,element:Element):
        if (element != None):
            if(not self.collide(element)):
                self.elements.append(element)
                self.reloadMatrice()
                return True
    
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

        for y in range(len(matrice1)):
            for x in range(len(matrice1[0])): 
                collide1 = []
                collide2 = []
                if ("collide" in matrice1[y][x]):
                    collide1 = matrice1[y][x]["collide"].copy()
                    if ("bullet" in collide1):
                        collide1.remove("bullet")
                if ("collide" in matrice2[y][x]):    
                    collide2 = matrice2[y][x]["collide"].copy()
                  
                if (len(collide1) > 0 and len(collide2) > 0):
                    if (not matrice1[y][x]["id"] == matrice2[y][x]["id"]):
                        for char in collide1:
                            if (char in collide2):
                                print("matrice1",matrice1[y][x]["collide"],matrice2[y][x]["collide"])
                                print("collision",matrice1[y][x]["char"],matrice2[y][x]["char"])
                                return True
                   
        return False
        
    #Génération aléatoire de la map
    def randGenerate(self):
        # Création des bases 
        base1 = Base(self,"up",1, (255, 0, 0))
        base2 = Base(self,"up",2,(0,255,0))
        # Ajout des bases à la carte
        self.addElement(base1)
        self.addElement(base2)
        
        # On génère un nombre aléatoire d'obstacle
        number_Obstacle = random.randint(5, 6)
        cpt=0
        while(cpt<number_Obstacle):
            # On ajoute l'obstacle à la map si il n'y a pas de collision
            obstacle = Obstacle(self.copy())
            self.addElement(obstacle) 
            if (self.addElement(obstacle)):
                cpt+=1

        
    #Vérifie si le bateau est bien entièrement dans la base avant l'explosion
    def canExplode(self, Vehicule):
        if(Vehicule.dynamite==True):
            for element in self.elements:
                if element.type["char"] == "Q":
                    if element.type["player"] != Vehicule.type["player"]:
                        Base = element
            if (((Vehicule.Front["x"]>=Base.Front["x"]) and (Vehicule.Front["x"]<=Base.Back["x"]))) and (((Vehicule.Front["y"]>=Base.Front["y"]) and (Vehicule.Front["y"]<=Base.Back["y"]))): 
                if(((Vehicule.Back["x"]>=Base.Front["x"]) and (Vehicule.Back["x"]<=Base.Back["x"]))) and (((Vehicule.Back["y"]>=Base.Front["y"]) and (Vehicule.Front["y"]<=Base.Back["y"]))):
                    return True
            return False 
        
        
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
    