from Element import Element
from Map import Map
from typing import Dict, List

class Base(Element):
    size = {"x": int(5), "y": int(15)}
        
    def __init__(self, map_instance: Map , direction :str, player :str,color :tuple = None, matrice :List[List[Dict[str, str]]]= None):
        self.type = {"char":"Q"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.direction=direction
        if (player=="player1"):
            self.position={"x":0,"y":int(map_instance.size["y"]*0.5)-self.size["y"]//2}
        else:
            self.position={"x":map_instance.size["x"]-self.size["x"],"y":int(map_instance.size["y"]*0.5)-self.size["y"]//2}
        self.matrice = matrice or [[self.type.copy() for i in range(self.size["x"])] for j in range(self.size["y"])]       
        self.Front = self.position 
        self.Back = {}
        self.reloadBack()  
        super().__init__(self.position,self.direction,self.size, self.type,self.matrice) 
        
        
        
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
