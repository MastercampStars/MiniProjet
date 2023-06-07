class Boat:
    
    def __init__(self,Position,type):
        self.Front = Position[0]
        self.Back = Position[1]
        self.type = type
        self.direction = self.getDirection()
        self.size = self.getSize()
        self.matrice = self.getMatrice()


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
        matrice[0][0] = "F"
        matrice[-1][-1] = "B"
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
        if self.direction == "up":
            #le bateau avance vers le haut
            if direction == "up":
                self.Front["y"] -= vitesse
            #le bateau tourne vers la gauche
            elif direction == "left":
                self.Front["x"] -= vitesse
                self.direction = "left"
            #le bateau tourne vers la droite
            elif direction == "right":
                self.Front["x"] += vitesse
                self.direction = "right"
            #le bateau recule vers le bas
            elif direction == "down":
                self.Front["y"] += vitesse//2
        #le bateau est vers le bas      
        elif self.direction == "down":
            #le bateau avance vers le bas
            if direction == "down":
                self.Front["y"] -= vitesse
            #le bateau tourne vers la gauche
            elif direction == "left":
                self.Front["x"] -= vitesse
                self.direction = "left"
            #le bateau tourne vers la droite
            elif direction == "right":
                self.Front["x"] += vitesse
                self.direction = "right"
            #le bateau recule vers le haut
            elif direction == "up":
                self.Front["y"] += vitesse//2
        #le bateau est vers la droite
        elif self.direction == "right":
            #le bateau avance vers la droite
            if direction == "right":
                self.Front["x"] += vitesse
            #le bateau tourne vers le haut
            elif direction == "up":
                self.Front["y"] -= vitesse
                self.direction = "up"
            #le bateau tourne vers le bas
            elif direction == "down":
                self.Front["y"] += vitesse
                self.direction = "down"
            #le bateau recule vers la gauche
            elif direction == "left":
                self.Front["x"] -= vitesse//2
        #le bateau est vers la gauche
        elif self.direction == "left":
            #le bateau avance vers la gauche
            if direction == "left":
                self.Front["x"] -= vitesse
            #le bateau tourne vers le haut
            elif direction == "up":
                self.Front["y"] -= vitesse
                self.direction = "up"
            #le bateau tourne vers le bas
            elif direction == "down":
                self.Front["y"] += vitesse
                self.direction = "down"
            #le bateau recule vers la droite
            elif direction == "right":
                self.Front["x"] += vitesse//2
        else:
            print("Direction invalide")    
        self.reloadBack()
        
    #Affichage du bateau
    def __str__(self) -> str:
        matrice = ""
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[0])):
                matrice += str(self.matrice[i][j]) + " "
            matrice += "\n"
        return f"Boat: {self.type} \nForme: \n{matrice}Direction: {self.direction}\nSize: {self.size}"
