import random
from Element import Element 
from Base import Base
from typing import Dict, List

class Obstacle(Element):
    
    instance=0
    def __init__(self, map_instance,  side :str, size:Dict[int,int]=None,matrice :List[List[Dict[str, str]]]= None,):
        self.type = {"char":"O"}  
        # On génère aléatoirement la position et la direction de l'obstacle  
        self.direction = random.choice(["up", "down", "right", "left"])
        # self.size = random.choice([{"x":4,"y":4},{"x":8,"y":4},{"x":10,"y":5}])
        self.size=size
        if self.size["x"]==4 and self.size["y"]==4:
            self.imageLoc = "little-stone1.png"
        if self.size["x"]==8 and self.size["y"]==4:
            self.imageLoc = "medium-stone.png"
        if self.size["x"]==10 and self.size["y"]==5:
            self.imageLoc = "big-stone.png"
        
        
        self.type["collide"] = ["bullet","element","base","obstacle"]
        self.type["obstacle"] = True
        self.type["side"] = side
        if self.type["side"]==1:
            self.position={"x":random.randint(0, int((map_instance.size["x"]*0.5))),"y":random.randint(0, int((map_instance.size["y"]*0.5)))}
        if self.type["side"]==2:
            self.position={"x":random.randint(int((map_instance.size["x"]*0.5)),int((map_instance.size["x"]))),"y":random.randint(0,int((map_instance.size["y"])))}
        
        self.Front = self.position 
        self.Back = {}
        self.reloadBack(self.size)  
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
    
         
    def reloadBack(self,size):
        if (self.direction == "up"):
            self.Back["x"] = self.Front["x"] + (size["x"] - 1)
            self.Back["y"] = self.Front["y"] + (size["y"] - 1)
        elif (self.direction == "down"):
            self.Back["x"] = self.Front["x"] - (size["x"] - 1)
            self.Back["y"] = self.Front["y"] - (size["y"] - 1)
        elif (self.direction == "right"):
            self.Back["x"] = self.Front["x"] - (size["y"] - 1)
            self.Back["y"] = self.Front["y"] + (size["x"] - 1)
        elif (self.direction == "left"):
            self.Back["x"] = self.Front["x"] + (size["y"] - 1)
            self.Back["y"] = self.Front["y"] - (size["x"] - 1)
                
    def getSize(self):
        return self.size

    def getMatrice(self):
        # Implement the logic to generate the matrice for the Base
        pass

    def copy(self):
        # Implement the logic to create a copy of the Base
        pass