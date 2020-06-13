# Objet case

class Frame:
    def __init__(self):
        self._neighbours = [] # Liste contenant les cases voisines à la case
        self.covered = True
        self.mined = False
        self.flagged = False
        self._pos_number = 0
        self._pos_number_cached = False # Si le nombre a déjà été calculé

    def _get_pos_number(self):  # Renvois le nombre de la case
        if not self._pos_number_cached: # Si il n'a pas déjà été calculé
            count = 0
            for neigh in self._neighbours: # On le calcul en comptant le nombre de cases voisines minées
                if neigh.mined:
                    count += 1
            self._pos_number_cached = True
            self._pos_number = count
        return self._pos_number

    def _put_mine(self): # Méthode pour ajouter une mine
        self.mined = True

    def _add_neighbour(self, neighbour): # Méthode pour ajouter un voisin
        self._neighbours.append(neighbour)

    def flag(self): # Méthode pour marquer la case
        if self.covered: # Seulement si elle est couverte
            if self.flagged : # On enlève si le drapeau est dessus, sinon l'inverse
                self.flagged = False
            else :
                self.flagged = True

    def _uncover(self): # On découvre la case si elle n'est pas marquée ou découverte
        if self.covered and not self.flagged:
            self.covered = False

    def update(self): # Méthode de découvertes des cases adjacentes récursive
        if not self.mined: # Si la case n'est pas minée
            self._uncover() # On la découvre
            if self._get_pos_number() == 0: # Si le nombre de la case est égal à 0
                for neigh in self._neighbours:
                    if neigh.covered: # On refait cette méthode sur les cases couvertes adjacentes
                        neigh.update()