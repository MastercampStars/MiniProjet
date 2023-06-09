import random
import pygame
from Boat import Boat
from Bullet import Bullet
class Map:
    # Constructeur
    def __init__(self, size, type, elements = []):
        self.type = type
        self.size = size
        self.elements = elements
        self.bullets = []
        self.matrice = [[type for x in range(size["x"])] for j in range(size["y"])]
    
    def getMatrice(self):
        return self.matrice
    # Ajoute un element a la matrice en fonction de sa direction, de sa taille et de sa matrice et de sa position Front
    def addElementToMatrice(self,element):
        for y in range(element.size["y"]):
            for x in range(element.size["x"]):
                # Affichage des elements de la map
                if (element.direction == "up"):
                    posX = element.Front["x"]+x
                    posY = element.Front["y"]+y
                elif (element.direction == "down"):
                    posX = element.Front["x"]-x
                    posY = element.Front["y"]-y
                elif (element.direction == "right"):
                    posX = element.Front["x"]-y
                    posY = element.Front["y"]+x
                elif (element.direction == "left"):
                    posX = element.Front["x"]+y
                    posY = element.Front["y"]-x
                
                if (posX >= 0 and posX < self.size["x"] and posY >= 0 and posY < self.size["y"]):   
                    self.matrice[posY][posX] = element.matrice[y][x]
                    
                # gestion du tire des tourelles
                bulletDirection = None
                if (element.direction == "up" and element.matrice[y][x]["char"] == "fu" or element.direction == "down" and element.matrice[y][x]["char"] == "fd" or element.direction == "right" and element.matrice[y][x]["char"] == "fl" or element.direction == "left" and element.matrice[y][x]["char"] == "fr" ):
                    bulletDirection = "up"
                    
                if (element.direction == "down" and element.matrice[y][x]["char"] == "fu" or element.direction == "up" and element.matrice[y][x]["char"] == "fd" or element.direction == "left" and element.matrice[y][x]["char"] == "fl" or element.direction == "right" and element.matrice[y][x]["char"] == "fr" ):
                    bulletDirection = "down"
                
                if (element.direction == "right" and element.matrice[y][x]["char"] == "fu" or element.direction == "left" and element.matrice[y][x]["char"] == "fd" or element.direction == "down" and element.matrice[y][x]["char"] == "fl" or element.direction == "up" and element.matrice[y][x]["char"] == "fr" ):
                    bulletDirection = "right"
                
                if (element.direction == "left" and element.matrice[y][x]["char"] == "fu" or element.direction == "right" and element.matrice[y][x]["char"] == "fd" or element.direction == "up" and element.matrice[y][x]["char"] == "fl" or element.direction == "down" and element.matrice[y][x]["char"] == "fr" ):
                    bulletDirection = "left"
                
                if (bulletDirection != None):
                    bullet = Bullet({"x":posX,"y":posY},bulletDirection,element.type)
                    self.bullets.append(bullet)
                    bullet.run()
                                       
        
    # Recharge la matrice de la map avec tous ses elements
    def reloadMatrice(self):         
        self.matrice = [[self.type for x in range(self.size["x"])] for j in range(self.size["y"])]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    def reloadBullets(self):
        for bullet in self.bullets:
            
            #supprier la bullet si elle sort de la map
            if (bullet.position["x"] < 0 or bullet.position["x"] >= self.size["x"] or bullet.position["y"] < 0 or bullet.position["y"] >= self.size["y"]):
                self.bullets.remove(bullet)
            
            #supprier la bullet si elle touche un obstacle
            elif (self.matrice[bullet.position["y"]][bullet.position["x"]]["char"] != "*" and self.matrice[bullet.position["y"]][bullet.position["x"]]["able"] == True):
                if (self.matrice[bullet.position["y"]][bullet.position["x"]]["player"] != bullet.type["player"]):
                    self.bullets.remove(bullet)
                    self.matrice[bullet.position["y"]][bullet.position["x"]]["char"] = "X"
                    self.matrice[bullet.position["y"]][bullet.position["x"]]["able"] = False
                
            if (bullet in self.bullets):
                bullet.run()
        
    
    # Ajoute un element a la map
    def addElement(self,element):
        if (element != None):
            if(not self.collide(element)):
                self.elements.append(element)
                self.reloadMatrice()
    
    # Supprime un element de la map
    def removeElement(self,element):
        if (element != None):
            if (element in self.elements):
                self.elements.remove(element)
                self.reloadMatrice()
        
        
         
    # Detecte si le bateau entre en collision avec un autre bateau
    def collide(self,boat,lastBoat = None):
        # On verrifie si le bateau est dans la map
        if (boat.Front["x"] < 0 or boat.Front["x"] >= self.size["x"] or boat.Front["y"] < 0 or boat.Front["y"] >= self.size["y"]):
            print("out of map")
            return True
        
        if (boat.Back["x"] < 0 or boat.Back["x"] >= self.size["x"] or boat.Back["y"] < 0 or boat.Back["y"] >= self.size["y"]):
            print("out of map")
            return True
        
        # On copie la map et on enleve le bateau affin de générer une matrice de la map sans le bateau
        
        self.removeElement(lastBoat)
        matrice1 = self.matrice.copy()
        
        # On ajoute le bateau à la map affin de générer une matrice de la map avec le bateau
        self.elements.append(boat)
        self.reloadMatrice()
        matrice2 = self.matrice.copy()
        
        self.removeElement(boat)
        self.addElement(lastBoat)
        self.reloadMatrice()
        
        # On compare les deux matrices pour voir si il y a une une supperposition de deux charactéres autres que "*"
        for y in range(len(matrice1)):
            for x in range(len(matrice1[0])):
                if (matrice1[y][x]["char"] != "*" and not matrice1[y][x]== matrice2[y][x]):
                    print("collide")
                    return True
        return False
        
    #Génération aléatoire de la map
    def randGenerate(self):
        number_Obstacle = random.randint(5, 10)
        for i in range(number_Obstacle):
            pos_X = random.randint(0, self.size["x"]-1)
            pos_Y = random.randint(0, self.size["y"]-1)
            size_X = random.randint(1, 10)
            size_Y = random.randint(1, 10)
            direction = random.choice(["up","down","right","left"])
            obstacle = Boat({"char":"R","able":True,"color":(255,255,255),"player":0},self.copy(),{"x":pos_X,"y":pos_Y},direction,{"x":size_X,"y":size_Y})
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
    