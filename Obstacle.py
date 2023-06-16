from Element import Element 
from typing import Dict
from typing import List

class Obstacle(Element):
    def __init__(self, position:Dict[int,int], direction:str, size:Dict[int,int], matrice:List[List[Dict[str, str]]] = None):
        super().__init__(position, direction, size, matrice)
        self.type = {"Obstacle"}
        