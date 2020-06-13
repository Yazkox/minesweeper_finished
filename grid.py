import random
import frame
# Liste des positions relatives autour d'une case
around_frame = [(1, 1), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1), (1, -1)]

# Objet grille

class Grid:
    def __init__(self, height, width, mine_amount):
        self.height = height
        self.width = width
        self.mine_amount = mine_amount
        self.lost = False
        self.won = False
        self.frame_array = []
        for y in range(height): # On créé le tableau contenant les objets cases
            L = []
            for x in range(width):
                L.append(frame.Frame())
            self.frame_array.append(L)
        for y in range(height): # On affecte aux cases leurs voisins
            for x in range(width):
                for adjacent in around_frame:
                    if y + adjacent[0] >= 0 and x + adjacent[1] >= 0: # Pour éviter d'avoir une grille en forme de tor ( pour éviter d'avoir les bords collés entre eux)
                        try:
                            self.frame_array[y][x]._neighbours.append(self.frame_array[y + adjacent[0]][x + adjacent[1]])
                        except IndexError:
                            pass

    def generate(self, start_x, start_y): # Génération de la grille en donnant la position de la case de départ
        mine_placed = 0
        while mine_placed < self.mine_amount: # Tant qu'il n'y a pas assez de mines placées
            y = random.randint(0, self.height - 1) # On choisit une position aléatoire
            x = random.randint(0, self.width - 1)
            if not self.frame_array[y][x].mined and not (
                    start_x - 1 <= x <= start_x + 1 and start_y - 1 <= y <= start_y + 1): # Si elle est pas déjà minée où à côté de la case de départ
                self.frame_array[y][x]._put_mine() # On met la mine
                mine_placed += 1
        self.frame_array[start_y][start_x].update() # On découvre et update la case de départ

    def check(self, x, y):  # Correspond à un click sur la case
        if not self.frame_array[y][x].flagged: # Si la case est pas minée
            self.frame_array[y][x].update() # On update la case
            if self.frame_array[y][x].mined: # Si elle est minée : on perd
                self.lost = True

    def check_won(self): # Check la victoire
        discovered_frame = 0
        for line in self.frame_array: # Compte le nombre de mine découverte
            for frame in line:
                if not frame.covered:
                    discovered_frame += 1
        if discovered_frame + self.mine_amount >= self.height * self.width: # Si toutes les cases non minées sont découvertes
            self.won = True
    def mine_left(self): # Renvois le nombre de mine restantes
        flagged_frame = 0
        for line in self.frame_array: # Compte les drapeaux
            for frame in line:
                if frame.flagged:
                    flagged_frame += 1
        return self.mine_amount- flagged_frame