class Map:
    # Constructeur d'une Map vide
    def __init__(self,size,type):
        self.type = type
        self.size = size
        self.elements = []
        #creer une matrice de taille size*size
        self.matrice = [[type for i in range(size)] for j in range(size)]
    
    # Constructeur d'une Map avec des elements   
    def __init__(self,size,type,elements):
        self.type = type
        self.size = size
        self.elements = elements
        #creer une matrice de taille size*size
        self.matrice = [[type for i in range(size)] for j in range(size)]
    
    
    # Ajoute un element à la liste des elements de la map
    def addElement(self,element):
        self.elements.append(element)
        self.reloadMatrice()
     
    # Supprime un element de la liste des elements de la map  
    def removeElement(self,element):
        self.elements.remove(element)
        self.reloadMatrice()
    
    # retourne la matrice de la map
    def getMatrice(self):
        return self.matrice
    
    # Ajoute un element à la matrice qui représente la map
    def addElementToMatrice(self,element):
        # Ajoute l'element à la matrice de la Map en fonction de sa direction, de son Front et de sa matrice interne
        # Si l'element est orienté vers le haut
        if (element.direction == "up"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]+y][element.Front["x"]+x] = element.matrice[y][x]
        
        # Si l'element est orienté vers le bas
        elif (element.direction == "down"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]-y][element.Front["x"]-x] = element.matrice[y][x]
        
        # Si l'element est orienté vers la droite
        elif (element.direction == "right"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]+x][element.Front["x"]-y] = element.matrice[y][x]
        
        # Si l'element est orienté vers la gauche
        elif (element.direction == "left"):
            for y in range(element.size["y"]):
                for x in range(element.size["x"]):
                    self.matrice[element.Front["y"]-x][element.Front["x"]+y] = element.matrice[y][x]
        """ self.matrice[element.Front["y"]][element.Front["x"]] = "f"
        self.matrice[element.Back["y"]][element.Back["x"]] = "b" """
    
    # Recharge la matrice de la map en fonction des elements de la liste des elements  
    def reloadMatrice(self):    
        self.matrice = [[self.type for x in range(self.size)] for y in range(self.size)]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    
    # Retourne la matrice de la map sous forme de string    
    def __str__(self) -> str:
        matrice = ""
        for y in range(self.size):
            for x in range(self.size):
                matrice += str(self.matrice[y][x]) + " "
            matrice += "\n"
        return f"Map: {self.type} \n\n{matrice}"
    