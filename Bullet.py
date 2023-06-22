class Bullet:
    # On initialise la bullet avec sa position, sa direction et son type
    def __init__(self, position, direction, type, speed = 1,distance = 30):
        self.position = position
        self.direction = direction
        self.type = type
        self.speed = speed
        self.distance = distance
        self.imageLoc = "bullet2.png"
        self.size = {"x":1.2,"y":1.5}

        
    
    # On fait avancer la bullet dans sa direction
    def run(self):
        if (self.direction == "up"):
            self.position["y"] -= self.speed
        elif (self.direction == "down"):
            self.position["y"] += self.speed
        elif (self.direction == "right"):
            self.position["x"] += self.speed
        elif (self.direction == "left"):
            self.position["x"] -= self.speed
        self.distance -= 1
        self.Front = self.position
    
        
