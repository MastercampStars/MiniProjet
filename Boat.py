class Boat:
    
    # Constructeur qui prend en parametre le ({type de bateau} , la map, la position du bateau (Front et Back), la direction, la taille du bateau)
    # La position du bateau peut etre donnée de deux manières différentes :
    # - Soit sous la forme d'un dictionnaire avec les clés "x" et "y" qui contiennent les coordonnées du Front du bateau, il faut alors préciser la direction et la taille du bateau
    # - Soit sous la forme d'une liste de deux dictionnaires avec les clés "x" et "y" qui contiennent les coordonnées du Front et du Back du bateau
    # Le type du bateau est un dictionnaire qui contient les clés "char" qui corespond au charactère qui le représente et "color" et peut égalment contenir d'autres paramétres si besoin
    
    def __init__(self, type, map ,Position, direction = None, size = None):
        print("Position = ",Position)
        
        # Constructeur si on utilise la position Front et Back
        if isinstance(Position, list):
            print(Position)
            self.Front = Position[0]
            self.Back = Position[1]
            self.direction = self.getDirection()
            self.size = self.getSize()
        
        # Constructeur si on utilise la position Front, la direction et la taille    
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
        
        # On calcule la matrice du bateau à sa création
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
    
    # Calcule Size["x"] (Largeure) et la Size["y"] (Longueure) du bateau a partir de ses coordonnées Front et Back et de son orientation
    def getSize(self):
        if(self.direction == "up" or self.direction == "down"):
            return {"x":abs(self.Front["x"]-self.Back["x"])+1,"y":abs(self.Front["y"]-self.Back["y"])+1}
        elif(self.direction == "right" or self.direction == "left"):
            return {"x":abs(self.Front["y"]-self.Back["y"])+1,"y":abs(self.Front["x"]-self.Back["x"])+1}
    
    # Calcule la matrice du bateau en fonction de sa longueure, largeure 
    def getMatrice(self):
        
        # Creer une matrice de la taille du bateau avet un "T" pour les tourelles du bateau, Pour l'instant je laisse ça ici mais ça va bouger
        # Les trourelles tirent a droite si elles sont à la droite du bateau et inversement
        pos_Tourelle_left = [{"x":0,"y":1},{"x":0,"y":self.size["y"]-2}]
        typeLeft = self.type.copy()
        typeLeft["char"] = "T"
        typeLeft["direction"] = "left"
        
        pos_Tourelle_right = [{"x":self.size["x"]-1,"y":1},{"x":self.size["x"]-1,"y":self.size["y"]-2}]
        typeRight = self.type.copy()
        typeRight["char"] = "T"
        typeRight["direction"] = "right"
        
        # On remplie la matrice avec les tourelles et le type du bateau
        # A noter que puisque le type de la case est un dictionnaire, il se comporte comme un pointeur et donc si on modifie le type d'une case, le type sera modifié a la fois sur la map et sur le bateau (et inversement)
        matrice = [[typeLeft.copy() if ( {"x":x,"y":y} in pos_Tourelle_left) else typeRight.copy() if ( {"x":x,"y":y} in pos_Tourelle_right) else self.type.copy()  for x in range(self.size["x"])] for y in range(self.size["y"])]
        
        # Permet d'avoir une tourelle qui tire de chaque coté si le bateau est de largeure 1
        matrice[self.size["y"]-2][self.size["x"]-1] = typeRight.copy()
        
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
    def move(self,direction,distance):
        self.direction = self.getDirection()
        #le bateau est vers le haut
        newFront = self.Front.copy()
        newDirection = self.direction

        if direction == "up" :
            #le bateau avance vers le haut
            if self.direction != "down":
                newFront["y"] -= distance 
                newDirection = "up"
            else:
                newFront["y"] -= distance//2
        
        elif direction == "down" :
            #le bateau avance vers le bas
            if self.direction != "up":
                newFront["y"] += distance
                newDirection = "down"
            else:
                newFront["y"] += distance//2
        
        elif direction == "right" :
            #le bateau avance vers la droite
            if  self.direction != "left":
                newFront["x"] += distance
                newDirection = "right"
            else:
                newFront["x"] += distance//2
        
        elif direction == "left" :
            #le bateau avance vers la gauche
            if self.direction != "right":
                newFront["x"] -= distance
                newDirection = "left"
            else:
                newFront["x"] -= distance//2
    
        else:
            print("Direction invalide")   
            
        #mise a jour de la position du bateau si il n'y a pas de collision
        newBoat = Boat(self.type,self.map,newFront,newDirection,self.size)
        if (not self.map.collide(newBoat,self)):
            self.Front = newFront
            self.direction = newDirection
            self.reloadBack()
            self.map.reloadMatrice()
        
    
    # Permet d'actionner les tourelles du bateau
    def fire(self):
        for y in range(self.size["y"]):
            for x in range(self.size["x"]):
                if (self.matrice[y][x]["char"]== "T"):
                    print("fire fire")
                    self.matrice[y][x]["char"]= "f"
        self.map.reloadMatrice()
        self.unFire()
    
    # permet aux tourerelles de ne pas rester en mode tir            
    def unFire(self):
        for y in range(self.size["y"]):
            for x in range(self.size["x"]):
                if (self.matrice[y][x]["char"]== "f"):
                    self.matrice[y][x]["char"]= "T"
        self.map.reloadMatrice()
    
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
