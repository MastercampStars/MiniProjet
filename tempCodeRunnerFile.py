def getMatrice(self):
        
        # Creer une matrice de la taille du bateau avet un "T" pour les tourelles du bateau, Pour l'instant je laisse ça ici mais ça va bouger
        # Les trourelles tirent a droite si elles sont à la droite du bateau et inversement

        
        # On remplie la matrice avec les tourelles et le type du bateau
        # A noter que puisque le type de la case est un dictionnaire, il se comporte comme un pointeur et donc si on modifie le type d'une case, le type sera modifié a la fois sur la map et sur le bateau (et inversement)
        matrice = [[self.type.copy() for i in range(self.size["x"])] for j in range(self.size["y"])]
        for tourelle in self.tourelles:
            matrice[tourelle["y"]][tourelle["x"]]["char"] = "T"
            matrice[tourelle["y"]][tourelle["x"]]["direction"] = tourelle["direction"]
        
        
        return matrice