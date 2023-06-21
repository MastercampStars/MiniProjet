from abc import ABC, abstractmethod
from typing import Dict
from typing import List

class Element(ABC):
    def __init__(self, position: Dict[int, int], direction: str, size:Dict[int,int], type:Dict[str,str], matrice: List[List[Dict[str, str]]] = None):
        self.position = position
        self.direction = direction
        self.size = size
        self.type = type
        self.matrice = matrice
        self.front = {'x': 0, 'y': 0}

    @property
    def matrice(self):
        return self._matrice

    @matrice.setter
    def matrice(self, value):
        self._matrice = value

    @abstractmethod # décorateur pour définir une méthode abstraite
    def getSize(self):
        pass

    @abstractmethod
    def getMatrice(self):
        pass

    @abstractmethod
    def copy(self):
        pass
    
    
    
    
    
