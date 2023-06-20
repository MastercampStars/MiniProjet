from Element import Element
from typing import Dict, List

class Base(Element):
    size = {"x": int(13), "y": int(13)}
        
    def __init__(self, map_instance, direction :str, player :str,color :tuple = None, matrice :List[List[Dict[str, str]]]= None):
        self.type = {"char":"Q","id":"B"}
        self.type["player"] = player
        self.type["color"] = color or (255,255,255)
        self.type["collide"] = ["base"]
        self.direction=direction
        if (player==1):
            self.position={"x":0,"y":int(map_instance.size["y"]*0.5)-self.size["y"]//2}
            self.imageLoc = "Base_Jaune.png"
        else:
            self.position={"x":map_instance.size["x"]-self.size["x"],"y":int(map_instance.size["y"]*0.5)-self.size["y"]//2}
            self.imageLoc = "Base_Rouge.png"
        self.matrice = matrice or [[self.type.copy() for i in range(self.size["x"])] for j in range(self.size["y"])]       
        self.Front = self.position 
        self.Back = {}
        self.reloadBack()  
        print(self.Front,self.Back)
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
