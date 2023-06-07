class Map:
    def __init__(self,size,type):
        self.type = type
        self.size = size
        self.elements = []
        #creer une matrice de taille size*size
        self.matrice = [[type for i in range(size)] for j in range(size)]
    
    def getMatrice(self):
        return self.matrice
    
    def addElementToMatrice(self,element):
        if (element.direction == "up"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]+y][element.Front["x"]+x] = element.matrice[y][x]
        elif (element.direction == "down"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]-y][element.Front["x"]-x] = element.matrice[y][x]
        elif (element.direction == "right"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]+x][element.Front["x"]-y] = element.matrice[y][x]
        elif (element.direction == "left"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]-x][element.Front["x"]+y] = element.matrice[y][x]
        self.matrice[element.Front["y"]][element.Front["x"]] = "f"
        self.matrice[element.Back["y"]][element.Back["x"]] = "b"
        
    
    def reloadMatrice(self):    
        self.matrice = [[self.type for x in range(self.size)] for y in range(self.size)]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    
    def addElement(self,element):
        self.elements.append(element)
        self.reloadMatrice()
        
    def removeElement(self,element):
        self.elements.remove(element)
        self.reloadMatrice()
        
    
        
    def __str__(self) -> str:
        matrice = ""
        for y in range(self.size):
            for x in range(self.size):
                matrice += str(self.matrice[y][x]) + " "
            matrice += "\n"
        return f"Map: {self.type} \n\n{matrice}"
    