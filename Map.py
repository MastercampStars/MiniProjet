class Map:
    # Constructeur
    def __init__(self,size,type,elements=[]):
        self.type = type
        self.size = size
        self.elements = elements
        self.matrice = [[type for x in range(size["x"])] for j in range(size["y"])]
    

    
    
    
    # Ajoute un element à la liste des elements de la map
    def addElement(self,element):
        self.elements.append(element)
        self.reloadMatrice()
     
    # Supprime un element de la liste des elements de la map  
    def removeElement(self,element):
        self.elements.remove(element)
        self.reloadMatrice()
    
    def getMatrice(self):
        return self.matrice
    # Ajoute un element a la matrice en fonction de sa direction, de sa taille et de sa matrice et de sa position Front
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
        self.matrice[element.Front["y"]][element.Front["x"]] = "f"
        self.matrice[element.Back["y"]][element.Back["x"]] = "b"
        
    # Recharge la matrice de la map avec tous ses elements
    def reloadMatrice(self):    
        self.matrice = [[self.type for x in range(self.size["x"])] for j in range(self.size["y"])]
        for element in self.elements:
            self.addElementToMatrice(element)
    
    # Ajoute un element a la map
    def addElement(self,element):
        self.elements.append(element)
        self.reloadMatrice()
    
    # Supprime un element de la map
    def removeElement(self,element):
        self.elements.remove(element)
        self.reloadMatrice()
        
    # Copie de la map
    def copy(self):
        return Map(self.size,self.type,self.elements.copy())
    
    # Affichage de la map
    def __str__(self) -> str:
        matrice = ""
        for y in range(self.size["y"]):
            for x in range(self.size["x"]):
                matrice += str(self.matrice[y][x]) + " "
            matrice += "\n"
        return f"Map: {self.type} \n\n{matrice}"
    