class Boat:
    
    def __init__(self, type, map ,Position, direction = None, size = None):
        print("Position = ",Position)
        if isinstance(Position, list):
            print(Position)
            self.Front = Position[0]
            self.Back = Position[1]
            self.direction = self.getDirection()
            self.size = self.getSize()
            
        elif isinstance(Position, dict) :
            if direction is None or size is None :
                raise Exception("Missing parameters")
            else:
                self.Front = Position
                self.direction = direction
                self.size = size
                self.Back = {}
                self.reloadBack()
        else:
            print("Error with Position type")
            
        self.type = type
        self.matrice = self.getMatrice()
        self.map = map


    # Calcule la direction du bateau a partir de ses coordonnées Front et Back
    def getDirection(self):
        if self.Front["x"] <= self.Back["x"] and self.Front["y"] < self.Back["y"]:
            return  "up"
        elif self.Front["x"] >= self.Back["x"] and self.Front["y"] > self.Back["y"]:
            return "down"
        elif self.Front["x"] > self.Back["x"] and self.Front["y"] <= self.Back["y"]:
            return "right"
        elif self.Front["x"] < self.Back["x"] and self.Front["y"] >= self.Back["y"]:
            return "left"
    
    #Calcule Size["x"] (Largeure) et la Size["y"] (Longueure) du bateau a partir de ses coordonnées Front et Back et de son orientation
    def getSize(self):
        if(self.direction == "up" or self.direction == "down"):
            return {"x":abs(self.Front["x"]-self.Back["x"])+1,"y":abs(self.Front["y"]-self.Back["y"])+1}
        elif(self.direction == "right" or self.direction == "left"):
            return {"x":abs(self.Front["y"]-self.Back["y"])+1,"y":abs(self.Front["x"]-self.Back["x"])+1}
    
    # Calcule la matrice du bateau en fonction de sa longueure, largeure et de sa direction
    def getMatrice(self):
        matrice = [[self.type for x in range(self.size["x"])] for y in range(self.size["y"])]
        matrice[0] = ["F" for x in range(self.size["x"])]
        matrice[-1] = ["B" for x in range(self.size["x"])]
        return matrice
    
    # Recalcul la position arrière du bateau à partir de sa direction, de sa position Front et de sa taille
    def reloadBack(self):
        if (self.direction == "up"):
            self.Back["x"] = self.Front["x"] + (self.size["x"] - 1)
            self.Back["y"] = self.Front["y"] + (self.size["y"] - 1)
        elif (self.direction == "down"):
            self.Back["x"] = self.Front["x"] - (self.size["x"] - 1)
            self.Back["y"] = self.Front["y"] - (self.size["y"] - 1)
        elif (self.direction == "right"):
            self.Back["x"] = self.Front["x"] - (self.size["y"] - 1)
            self.Back["y"] = self.Front["y"] + (self.size["x"] - 1)
        elif (self.direction == "left"):
            self.Back["x"] = self.Front["x"] + (self.size["y"] - 1)
            self.Back["y"] = self.Front["y"] - (self.size["x"] - 1)
            

    #Deplacement du bateau
    #Calcul la nouvelle position du bateau en fonction de sa direction et de la direction demandée
    def move(self,direction,vitesse):
        self.direction = self.getDirection()
        #le bateau est vers le haut
        newFront = self.Front.copy()
        newDirection = self.direction
        if self.direction == "up":
            #le bateau avance vers le haut
            if direction == "up":
                newFront["y"] -= vitesse
            #le bateau tourne vers la gauche
            elif direction == "left":
                newFront["x"] -= vitesse
                newDirection = "left"
            #le bateau tourne vers la droite
            elif direction == "right":
                newFront["x"] += vitesse
                newDirection = "right"
            #le bateau recule vers le bas
            elif direction == "down":
                newFront["y"] += vitesse//2
        #le bateau est vers le bas      
        elif newDirection == "down":
            #le bateau avance vers le bas
            if direction == "down":
                newFront["y"] += vitesse
            #le bateau tourne vers la gauche
            elif direction == "left":
                newFront["x"] -= vitesse
                newDirection = "left"
            #le bateau tourne vers la droite
            elif direction == "right":
                newFront["x"] += vitesse
                newDirection = "right"
            #le bateau recule vers le haut
            elif direction == "up":
                newFront["y"] -= vitesse//2
        #le bateau est vers la droite
        elif newDirection == "right":
            #le bateau avance vers la droite
            if direction == "right":
                newFront["x"] += vitesse
            #le bateau tourne vers le haut
            elif direction == "up":
                newFront["y"] -= vitesse
                newDirection = "up"
            #le bateau tourne vers le bas
            elif direction == "down":
                newFront["y"] += vitesse
                newDirection = "down"
            #le bateau recule vers la gauche
            elif direction == "left":
                newFront["x"] -= vitesse//2
        #le bateau est vers la gauche
        elif newDirection == "left":
            #le bateau avance vers la gauche
            if direction == "left":
                newFront["x"] -= vitesse
            #le bateau tourne vers le haut
            elif direction == "up":
                newFront["y"] -= vitesse
                newDirection = "up"
            #le bateau tourne vers le bas
            elif direction == "down":
                newFront["y"] += vitesse
                newDirection = "down"
            #le bateau recule vers la droite
            elif direction == "right":
                newFront["x"] += vitesse//2
        else:
            print("Direction invalide")   
            
        #mise a jour de la position du bateau
        if (not self.collide(newFront,newDirection)):
            self.Front = newFront
            self.direction = newDirection
            self.reloadBack()
        else:
            print("Collision")
        
    # Detecte si le bateau entre en collision avec un autre bateau
    def collide(self,newFront,newDirection):
        # On verrifie si le bateau est dans la map
        if (newFront["x"] < 0 or newFront["x"] >= self.map.size["x"] or newFront["y"] < 0 or newFront["y"] >= self.map.size["y"]):
            return True
        # On copie le bateau et on le place à la nouvelle position 
        boat = self.copy()
        boat.Front = newFront
        boat.direction = newDirection
        boat.reloadBack()
        if (boat.Back["x"] < 0 or boat.Back["x"] >= self.map.size["x"] or boat.Back["y"] < 0 or boat.Back["y"] >= self.map.size["y"]):
            return True
        # On copie la map et on enleve le bateau affin de générer une matrice de la map sans le bateau
        map = self.map.copy()
        map.removeElement(self)
        map.reloadMatrice()
        matrice1 = map.matrice.copy()
        # On ajoute le bateau à la map affin de générer une matrice de la map avec le bateau
        map.addElement(boat)
        map.reloadMatrice()
        matrice2 = map.matrice.copy()
        # On compare les deux matrices pour voir si il y a une une supperposition de deux charactéres autres que "*"
        for y in range(len(matrice1)):
            for x in range(len(matrice1[0])):
                if (matrice1[y][x] != "*" and matrice1[y][x] != matrice2[y][x] ):
                    return True
        return False
    
    # Copie du bateau
    def copy(self):
        return Boat(self.type,self.map.copy(),self.Front.copy(),self.direction,self.size)
        
    #Affichage du bateau
    def __str__(self) -> str:
        matrice = ""
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[0])):
                matrice += str(self.matrice[i][j]) + " "
            matrice += "\n"
        return f"Boat: {self.type} \nForme: \n{matrice}Direction: {self.direction}\nSize: {self.size}"
