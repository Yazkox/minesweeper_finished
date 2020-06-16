import pygame
import random as rd
from math import *
import time
import grid
import asyncio

#############
# Variables #
#############

# Constantes d'affichage
LARGEUR = 1080
HAUTEUR = int((LARGEUR * 9) / 16)
FPS = 30
frame_size = 20  # Taille des cases
frame_x_offset = 350 # Debut en x du coin haut gauche de la grille
frame_y_offset = 50 # Même chose en y
frame_inter = 2 # Espace entre les cases
# Initialisation de pygame
pygame.init()
game_window = pygame.display.set_mode((LARGEUR, HAUTEUR)) # Création de la fenêtre et tout ce qui va avec
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("arial", 30)  # On fait les 3 polices
subtitle_font = pygame.font.SysFont("arial", 15)
number_font = pygame.font.SysFont("arial",20)

choice = [[100, "Facile", 9, 9, 10], [225, "Moyen", 16, 16, 40], [350, "Difficile", 16, 32, 99]] # Choix des menus Pos, hauteur, largeur de grille, nombre de mine
color = [(13,143,214),(0,200,200),(100,190,70),(220,160,0),(240,100,80),(250,50,40),(255,20,20)]  # Couleur des chiffres 1 à 8 en RGB


#############
# Fonctions #
#############

# Classe pour créer les 3 boutons du menu avec un titre et un sous titre

class Selection:
    def __init__(self, hauteur, title, subtitle):
        self.hauteur = hauteur

        self.title = title_font.render(title, True, (0, 0, 0))
        self.subtitle = subtitle_font.render(subtitle, True, (0, 0, 0))

    def update(self, coord): # Fonction pour update le bouton
        pygame.draw.rect(game_window, (175, 201, 26), (((540 // 2), self.hauteur), (500, 75))) # On fait le rectangle

        if (540 / 2) <= coord[0] <= (540 / 2) + 500 and self.hauteur <= coord[1] <= self.hauteur + 75: # Si la souris est dessus (coord)
            pygame.draw.rect(game_window, (175, 201, 26), (((540 // 2), self.hauteur), (500, 75)), 10) # On met en "surbriance"

        game_window.blit(self.title,
                         (540 // 2 + 250 - self.title.get_width() // 2, self.hauteur + self.title.get_height() // 2)) # On met les deux textes
        game_window.blit(self.subtitle,
                         (540 // 2 + 250 - self.subtitle.get_width() // 2,
                          self.hauteur + self.title.get_height() + self.subtitle.get_height()))

# Affichage de la grille de jeu

def display_grid(grid):
    for y in range(len(grid.frame_array)):
        for x in range(len(grid.frame_array[0])) :
            x_pos = frame_x_offset+x*(frame_size+frame_inter)
            y_pos = frame_y_offset+y*(frame_size+frame_inter)
            if grid.frame_array[y][x].covered: # Si la grille est couverte
                if not grid.frame_array[y][x].flagged: # Si elle est marquée un carré
                    pygame.draw.rect(game_window, (175, 201, 26), ((x_pos, y_pos), (frame_size, frame_size)))
                else : # Sinon un carré d'une autre couleur avec un F dessus
                    pygame.draw.rect(game_window, (255, 50, 55), ((x_pos, y_pos), (frame_size, frame_size)))
                    display_number = number_font.render("F", True, (60,20,20))
                    game_window.blit(display_number, (x_pos + (frame_size - display_number.get_width()) // 2,y_pos + (frame_size - display_number.get_height()) // 2))
            else: # Si la case est découverte
                if grid.frame_array[y][x].mined : # Si elle est minée (pour l'affichage des mines en cas de défaite)
                    pygame.draw.rect(game_window, (230, 20, 20), ((x_pos, y_pos), (frame_size, frame_size)))
                    display_number = number_font.render("M", True, (60,20,20))
                    game_window.blit(display_number, (x_pos + (frame_size - display_number.get_width()) // 2,y_pos + (frame_size - display_number.get_height()) // 2))
                else : # Si elle est pas minée
                    pygame.draw.rect(game_window, (50, 50, 50), ((x_pos,y_pos ),(frame_size, frame_size)))
                    number = grid.frame_array[y][x]._get_pos_number() # On prend le numéro qu'à la case
                    if number >0 : # Si il est non nul
                        display_number = number_font.render(str(number), True, color[number-1]) # On affiche le nombre avec la couleur de la liste couleur
                        game_window.blit(display_number, (x_pos+(frame_size-display_number.get_width())//2,y_pos+(frame_size-display_number.get_height())//2))


# Retourne la position de la case sur laquelle le curseur est

def on_click():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x = floor((mouse_x - frame_x_offset) / (frame_size + frame_inter))
    y = floor((mouse_y - frame_y_offset) / (frame_size + frame_inter))
    return x,y


##################
# Menu Principal #
##################

def menu_principal():
    background = pygame.image.load("image_fond.jpg").convert() # On charge l'image de fond
    menu_choice = []
    # Création des boutons avec les textes à afficher
    for attributes in choice:
        subtitle = "Taille : " + str(attributes[2]) + " x " + str(attributes[3]) + " - Mines : " + str(attributes[4])
        menu_choice.append(Selection(attributes[0], attributes[1], subtitle))
    menu_choice.append(Selection(choice[-1][0] + 125, "Quitter", "")) # Et le dernier bouton quitter
    on_menu = True
    while on_menu: # Tant qu'on est sur le menu
        clock.tick(FPS) # On setup la clock

        game_window.blit(background, (0, 0)) # On met l'image de fond

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Si on ferme la fenêtre ça ferme la fenêtre et le programme
                pygame.quit()
                on_menu = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Si on clique
                for attributes in choice: # For pour chaque bouton de jeu
                    if (540 / 2) <= pygame.mouse.get_pos()[0] <= (540 / 2) + 500 and attributes[0] <= \
                            pygame.mouse.get_pos()[1] <= attributes[0] + 75: # Si le curseur est sur le bouton
                        on_menu = False
                        start_game(attributes[2:])
                if (540 / 2) <= pygame.mouse.get_pos()[0] <= (540 / 2) + 500 and choice[-1][0] + 125 <= \
                        pygame.mouse.get_pos()[1] <= choice[-1][0] + 200: # La même pour le bouton quitter
                    pygame.quit()

        for select in menu_choice:
            select.update(pygame.mouse.get_pos()) # On affiche la case, et la surbillance si la souris est dessus

        pygame.display.flip() # On affiche ce qui a été render (tout les carrés, text, etc.)



#########################
# Démarage d'une partie #
#########################

# Debute une partie avec la liste des attributs (hauteur, largeur, nb mines)
def start_game(attributes):

    #########################
    # Initialisation du jeu #
    #########################

    background = pygame.image.load("image_fond.jpg").convert()
    game_window.blit(background, (0, 0))
    game_grid = grid.Grid(attributes[0],attributes[1],attributes[2]) # On créé la grille (grid.py) avec les attributs de la liste attributes
    display_grid(game_grid) # On l'affiche
    mine_amount_display = title_font.render("Mine restantes : " + str(game_grid.mine_left()), True, (0, 0, 0)) # On affiche le nombre de mine restantes (=nb mine)
    pygame.draw.rect(game_window, (175, 201, 26), ((20, 20), (250, 150)))
    game_window.blit(mine_amount_display, (30, 50))
    pygame.display.flip()
    started = False
    while not started : # On attend que le joueur clique sur la case où il veut commencer (pour pas mettre de mine dessus)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Le quit comme toujours
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x,y = on_click() # Si on clique, on regarde sur quelle case il la fait
                if attributes[1]>x>=0 and attributes[0]>y>=0: # Si la position de la case existe (pour pas avoir d'IndexError)
                    game_grid.generate(x,y) # On génère la grille avec la position de départ
                    started = True
    starting_time = time.time() # On sauvegarde l'heure à laquelle le jeu a commencé
    display_grid(game_grid)
    game_grid.check_won() # On regarde si on a gagné (possible au premier coup avec certains paramètres)

    #################
    # Boucle de jeu #
    #################

    while not game_grid.won and not game_grid.lost : # Tant qu'on a pas perdu ou gagné
        clock.tick(FPS)
        game_window.blit(background, (0, 0))
        timer = trunc(100*(time.time()-starting_time))/100
        mine_amount_display = title_font.render("Mine restantes : " + str(game_grid.mine_left()), True, (0, 0, 0)) # On affiche le nombre de mines restantes
        timer_display = title_font.render("Timer " + str(timer), True, (0, 0, 0))  # On affiche le timer
        pygame.draw.rect(game_window, (175, 201, 26), ((20,20), (250, 150)))
        game_window.blit(mine_amount_display, (30, 50))
        game_window.blit(timer_display, (30, 110))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Si on ferme la fenêtre via le bouton, ça la ferme
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP: # Si on clique
                    if event.button == 1: # Si clique gauche
                        x,y = on_click() # On récupère les coordonnées de la case où on a cliqué
                        if attributes[1]>x>=0 and attributes[0]>y>=0: # Si elles sont valides
                            game_grid.check(x,y) # On découvre la case
                    if event.button == 3 :  # Si clique droit
                        x, y = on_click() # On récupère les coordonnées
                        if attributes[1] > x >= 0 and attributes[0] > y >= 0: # Si elles sont valides
                            game_grid.frame_array[y][x].flag() # On flag la case


        display_grid(game_grid)
        game_grid.check_won()
        pygame.display.flip()

    ###########################
    # Affichage de fin de jeu #
    ###########################

    still_waiting = True
    time_won = time.time()
    timer = floor(100 * (time_won - starting_time)) / 100
    while still_waiting :
        clock.tick(FPS)
        game_window.blit(background, (0, 0))
        if game_grid.lost:  # Si on a perdu
            death_message = title_font.render("RIP, vous avez perdu", True, (0, 0, 0))
            pygame.draw.rect(game_window, (175, 201, 26), ((20, 300), (250, 110)))
            game_window.blit(death_message, (30, 330))
            for line in game_grid.frame_array: # On découvre toute les mines
                for frame in line:
                    if frame.mined:
                        frame._uncover()
            display_grid(game_grid) # On affiche la grille avec les mines
        else: # Si on a gagné
            win_message1 = title_font.render("GG vous avez gagné", True, (0, 0, 0))
            win_message2 = title_font.render("en : " + str(timer) + "s", True, (0, 0, 0)) # On affiche le temps de victoire
            pygame.draw.rect(game_window, (175, 201, 26), ((20, 300), (250, 110)))
            game_window.blit(win_message1, (30, 320))
            game_window.blit(win_message2, (30, 360))
        menu_message = title_font.render("Menu principal", True, (0, 0, 0))  # On créé le bouton retour au menu principal
        button = pygame.draw.rect(game_window, (175, 201, 26), ((20, 450), (250, 110)))
        game_window.blit(menu_message, (30, 470))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Si on ferme la fenêtre
                pygame.quit() # On quitte
                still_waiting = False
            if pygame.mouse.get_pressed()[0] and button.collidepoint(pygame.mouse.get_pos()): # Si clique sur le bouton
                still_waiting = False
                menu_principal() # Retour au menu



# On lance le programme

menu_principal()
