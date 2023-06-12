from abc import ABC, abstractmethod

class Element(ABC): # hérite de ABC(Abstract base class)
       
    def __init__(self, Position, matrice):
        self._Position = Position
        self._matrice = matrice

    @property
    def Position(self):
        return self._Position

    @Position.setter
    def Position(self, value):
        self._Position = value

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
    
    
    
    
    
