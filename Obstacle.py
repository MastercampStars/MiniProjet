from Element import Element 

class Obstacle(Element):
    def __init__(self, Position, matrice):
        super().__init__(Position, matrice)
        self.type = "Obstacle"
        