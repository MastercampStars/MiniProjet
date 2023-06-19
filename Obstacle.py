import random
from Element import Element 
from typing import Dict, List

class Obstacle(Element):
    
    instance=0
    def __init__(self, map_instance ,matrice :List[List[Dict[str, str]]]= None):
        self.type = {"char":"O"} # or self.type={"Obstacle"}    
        self.direction = random.choice(["up", "down", "right", "left"])
        # On génère aléatoirement la position, la taille et la direction de l'obstacle
        self.size = {"x":random.randint(1, 10),"y":random.randint(1, 10)}
        self.position={"x":random.randint(0, map_instance.size["x"]-self.size["x"]),"y":random.randint(0, map_instance.size["y"]-self.size["y"])}
        self.Front = self.position 
        self.Back = {}
        self.reloadBack()  
        Obstacle.instance += 1
        self.type["id"] = "O" + str(Obstacle.instance)
        self.matrice = matrice or [[self.type.copy() for i in range(self.size["x"])] for j in range(self.size["y"])]   
        super().__init__(self.position,self.direction,self.size,self.type,self.matrice) 
    
    def __str__(self) -> str:
        matrice = ""
        for i in range(len(self.matrice)):
            for j in range(len(self.matrice[0])):
                matrice += str(self.matrice[i][j]) + " "
            matrice += "\n"
        return f"Obstacle: {self.type} \nForme: \n{matrice}Direction: {self.direction}\nSize: {self.size}"
    
         
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
                
    def getSize(self):
        return self.size

    def getMatrice(self):
        # Implement the logic to generate the matrice for the Base
        pass

    def copy(self):
        # Implement the logic to create a copy of the Base
        pass

