class Bullet:
    def __init__(self,position,direction,type):
        self.position = position
        self.direction = direction
        self.type = type
    
    def run(self):
        if (self.direction == "up"):
            self.position["y"] -= 1
        elif (self.direction == "down"):
            self.position["y"] += 1
        elif (self.direction == "right"):
            self.position["x"] += 1
        elif (self.direction == "left"):
            self.position["x"] -= 1
    
        
