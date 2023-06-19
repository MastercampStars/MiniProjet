from Element import Element
from typing import Dict, List

class Vehicule(Element):
    
    # Constructeur qui prend en parametre le ({type de bateau} , la map, la position du bateau (Front et Back), la direction, la taille du bateau)
    # La position du bateau peut etre donnée de deux manières différentes :
    # - Soit sous la forme d'un dictionnaire avec les clés "x" et "y" qui contiennent les coordonnées du Front du bateau, il faut alors préciser la direction et la taille du bateau
    # - Soit sous la forme d'une liste de deux dictionnaires avec les clés "x" et "y" qui contiennent les coordonnées du Front et du Back du bateau
    # Le type du bateau est un dictionnaire qui contient les clés "char" qui corespond au charactère qui le représente et "color" et peut égalment contenir d'autres paramétres si besoin
    
    def __init__(self, type :Dict[str,str], map ,position :Dict[int,int], direction :str, size :Dict[int,int],maxSpeed:int = None, tourelles :List[dict] = None):
        # Initialize the properties inherited from Element
        super().__init__(position, direction, size, type )  # matrice will be set later
        print("position = ",position) 
        self.type["able"] = True
        self.map = map 
        self.maxSpeed = maxSpeed or 1 
        self.speed = maxSpeed
        self.tourelles = tourelles or []
        self.Front = position
        self.Back = {}
        self.reloadBack()  
        self.life = size["x"]*size["y"]
        
        # On calcule la matrice du bateau à sa création
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

        
        # On remplie la matrice avec les tourelles et le type du bateau
        # A noter que puisque le type de la case est un dictionnaire, il se comporte comme un pointeur et donc si on modifie le type d'une case, le type sera modifié a la fois sur la map et sur le bateau (et inversement)
        matrice = [[self.type.copy() for i in range(self.size["x"])] for j in range(self.size["y"])]
        for tourelle in self.tourelles:
            matrice[tourelle["y"]][tourelle["x"]]["char"] = "T"
            matrice[tourelle["y"]][tourelle["x"]]["direction"] = tourelle["direction"]
        
        
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
    def move(self,direction :str):
        self.direction = self.getDirection()
        #le bateau est vers le haut
        newFront = self.Front.copy()
        newDirection = self.direction
        if isinstance(self, Jet):
            backSpeed = 0
        else: backSpeed = -self.maxSpeed // 2

        if direction == "up" :
            #le bateau avance vers le haut
            if self.direction != "down":
                self.speed = self.maxSpeed 
                newFront["y"] -= self.speed 
                newDirection = "up"
            else:
                self.speed = backSpeed
                newFront["y"] += self.speed
        
        elif direction == "down" :
            #le bateau avance vers le bas
            if self.direction != "up":
                self.speed = self.maxSpeed 
                newFront["y"] += self.speed
                newDirection = "down"
            else:
                self.speed = backSpeed
                newFront["y"] -= self.speed
        
        elif direction == "right" :
            #le bateau avance vers la droite
            if  self.direction != "left":
                self.speed = self.maxSpeed 
                newFront["x"] += self.speed
                newDirection = "right"
            else:
                self.speed = backSpeed
                newFront["x"] -= self.speed
        
        elif direction == "left" :
            #le bateau avance vers la gauche
            if self.direction != "right":
                self.speed = self.maxSpeed 
                newFront["x"] -= self.speed
                newDirection = "left"
            else:
                self.speed = backSpeed
                newFront["x"] += self.speed
    
        else:
            print("Direction invalide")   
            
        #mise a jour de la position du bateau si il n'y a pas de collision
        newVehicule = Vehicule(self.type,self.map,newFront,newDirection,self.size)
        if (not self.map.collide(newVehicule,self)):
            self.Front = newFront
            self.direction = newDirection
            self.reloadBack()
            self.map.reloadMatrice()
        
    
    # Permet d'actionner les tourelles du bateau
    def fire(self):
        for y in range(self.size["y"]):
            for x in range(self.size["x"]):
                if (self.matrice[y][x]["char"]== "T"):
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
        return Vehicule(self.type,self.map.copy(),self.Front.copy(),self.direction,self.size)
        
    #Affichage du bateau
    def __str__(self) -> str:
        matrice = ""
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[0])):
                matrice += str(self.matrice[i][j]) + " "
            matrice += "\n"
        return f"Vehicule: {self.type} \nForme: \n{matrice}Direction: {self.direction}\nSize: {self.size}"
    
    
 #---------------------------------------------------------------differents véhicules--------------------------------------------------------------------------   
    
class LittleBoat(Vehicule):
    size = {"x": 3, "y": 5}
    collide =  ["bullet","element"]
    speed = 6
    imageLoc = "littleBoat.png"
    instance = 0
    tourelles = [{"x":0,"y":0,"direction":"up"},{"x":2,"y":1,"direction":"up"}]
    dynamite = True

    def __init__(self, map, position: Dict[int, int], direction: str, player: str, color: tuple = None):
        self.type = {"char": "L"}
        self.type["player"] = player
        self.type["color"] = color or (255, 255, 255)
        self.type["collide"] = self.collide
        self.type["id"] = self.type["char"] + str(self.instance)
        LittleBoat.instance += 1
        super().__init__(self.type, map, position, direction, self.size, self.speed, self.tourelles)


        
    
 
class MedicaleBoat (Vehicule):
    size = {"x":2,"y":7}
    collide =  ["bullet","element"]
    speed = 3
    instance = 0
    imageLoc = "medicaleBoat.png"
    dynamite = True
    def __init__(self, map ,position :Dict[int,int], direction :str,player :str,color :tuple = None):
        self.type = {"char":"M"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = self.collide
        self.type["id"] = self.type["char"] + str(self.instance)
        MedicaleBoat.instance += 1
        super().__init__(self.type,map,position,direction,self.size,self.speed)
 
        
class BigBoat (Vehicule):
    size = {"x":3,"y":13}
    speed = 3
    collide =  ["bullet","element"]
    instance = 0
    imageLoc = "bigBoat.png"
    tourelles = [{"x":0,"y":1,"direction":"left"},{"x":0,"y":5,"direction":"left"},{"x":0,"y":10,"direction":"left"},{"x":2,"y":0,"direction":"right"},{"x":2,"y":5,"direction":"right"},{"x":2,"y":10,"direction":"right"}]
    dynamite = True
    
    def __init__(self, map ,position :Dict[int,int], direction :str,player :str,color :tuple = None):
        self.type = {"char":"B"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = self.collide
        self.type["id"] = self.type["char"] + str(self.instance)
        BigBoat.instance += 1
        super().__init__(self.type,map,position,direction,self.size,self.speed,self.tourelles)
        
class Carrier (Vehicule):
    size = {"x":4,"y":9}
    speed = 3
    collide =  ["bullet","element"]
    instance = 0
    imageLoc = "carrier.png"
    #tourelles = [{"x":1,"y":0,"direction":"up"},{"x":1,"y":1,"direction":"up"},{"x":1,"y":2,"direction":"up"}]
    dynamite = True
    def __init__(self, map ,position :Dict[int,int], direction :str,player :str,color :tuple = None):
        self.type = {"char":"C"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = self.collide
        self.type["id"] = self.type["char"] + str(self.instance)
        Carrier.instance += 1
        super().__init__(self.type,map,position,direction,self.size,self.speed,self.tourelles)
    
    def special(self):
        self.map.addElement(Jet(self.map,{"x":self.Front["x"],"y":self.Front["y"]},self.direction,self.type["player"],self.type["color"]))
        

class Submarine (Vehicule):
    size = {"x":3,"y":7}
    speed = 3
    collide1 =  ["bullet","element","obstacle"]
    collide2 = ["obstacle"]
    instance = 0
    imageLoc = "submarine.png"
    tourelles = [{"x":0,"y":0,"direction":"up"},{"x":1,"y":0,"direction":"up"},{"x":2,"y":0,"direction":"up"}]
    dynamite = False
    def __init__(self, map ,position :Dict[int,int], direction :str,player :str,color :tuple = None):
        self.type = {"char":"S"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = self.collide1.copy()
        self.type["id"] = self.type["char"] + str(self.instance)
        Submarine.instance += 1
        super().__init__(self.type,map,position,direction,self.size,self.speed,self.tourelles)
        self.type["id"] = "S" + str(Submarine.instance)
    
    def special(self):
        if(self.type["collide"] == Submarine.collide1):
            self.type["collide"] = Submarine.collide2
            for y in range(self.size["y"]):
                for x in range(self.size["x"]):
                    self.matrice[y][x]["collide"] = self.type["collide"].copy()
                    if self.matrice[y][x]["char"] != "X":
                        self.matrice[y][x]["char"] = "W"
        
        elif(self.type["collide"] == Submarine.collide2):
            self.type["collide"] = Submarine.collide1
            for y in range(self.size["y"]):
                for x in range(self.size["x"]):
                    self.matrice[y][x]["collide"] = self.type["collide"].copy()
                    if self.matrice[y][x]["char"] != "X":
                        self.matrice[y][x]["char"] = "S"
            for tourelle in self.tourelles:
                if self.matrice[tourelle["y"]][tourelle["x"]] != "X":
                    self.matrice[tourelle["y"]][tourelle["x"]]["char"] = "T"
                    self.matrice[tourelle["y"]][tourelle["x"]]["direction"] = tourelle["direction"]
        
                
    


class Jet( Vehicule):
    size = {"x":3,"y":3}
    speed = 6
    collide =  ["bullet"]
    instance = 0
    imageLoc = "jet.png"
    tourelles = [{"x":1,"y":0,"direction":"up"}]
    dynamite = False
    
    def __init__(self, map ,position :Dict[int,int], direction :str,player :str = None,color :tuple = None):
        self.type = {"char":"J"}
        self.type["player"] = player or None
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = self.collide
        self.type["id"] = self.type["char"] + str(self.instance)
        Jet.instance += 1
        super().__init__(self.type,map,position,direction,self.size,self.speed,self.tourelles)
        
    
        
        
