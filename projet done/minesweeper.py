import pygame
import random as rd
from math import *
import time
import grid
import asyncio
# initialisation des constantes
LARGEUR = 1080
HAUTEUR, FPS = int((LARGEUR * 9) / 16), 30
frame_size = 20
frame_x_offset = 350
frame_y_offset = 50
frame_inter = 2
# initialisation de pygame
pygame.init()
game_window = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()

# initialisation du "jeu"

title_font = pygame.font.SysFont("arial", 30)
subtitle_font = pygame.font.SysFont("arial", 15)
number_font = pygame.font.SysFont("arial",20)
# Liste des choix  #Pos #Hauteur #Largeur #Mines
choice = [[100, "Facile", 9, 9, 10], [225, "Moyen", 16, 16, 40], [350, "Difficile", 16, 32, 99]]
color = [(20,20,255),(150,150,255),(150,255,150),(255,255,100),(255,100,10),(80,80,80),(40,40,40),(20,20,20)]

class Selection:
    def __init__(self, hauteur, title, subtitle):
        self.hauteur = hauteur

        self.title = title_font.render(title, True, (0, 0, 0))
        self.subtitle = subtitle_font.render(subtitle, True, (0, 0, 0))

    def update(self, coord):
        pygame.draw.rect(game_window, (0, 255, 255), (((540 / 2), self.hauteur), (500, 75)))

        if (540 / 2) <= coord[0] <= (540 / 2) + 500 and self.hauteur <= coord[1] <= self.hauteur + 75:
            pygame.draw.rect(game_window, (255, 255, 0), (((540 / 2), self.hauteur), (500, 75)), 10)

        game_window.blit(self.title,
                         (540 / 2 + 250 - self.title.get_width() // 2, self.hauteur + self.title.get_height() // 2))
        game_window.blit(self.subtitle,
                         (540 / 2 + 250 - self.subtitle.get_width() // 2,
                          self.hauteur + self.title.get_height() + self.subtitle.get_height()))


# boucle de "jeu"


def menu_principal():
    background = pygame.image.load("image_fond.jpg").convert()
    menu_choice = []
    for attributes in choice:
        subtitle = "Taille : " + str(attributes[2]) + " x " + str(attributes[3]) + " - Mines : " + str(attributes[4])
        menu_choice.append(Selection(attributes[0], attributes[1], subtitle))
    menu_choice.append(Selection(choice[-1][0] + 125, "Quitter", ""))
    while True:
        clock.tick(FPS)

        game_window.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                for attributes in choice:
                    if (540 / 2) <= pygame.mouse.get_pos()[0] <= (540 / 2) + 500 and attributes[0] <= \
                            pygame.mouse.get_pos()[1] <= attributes[0] + 75:
                        start_game(attributes[2:])
                if (540 / 2) <= pygame.mouse.get_pos()[0] <= (540 / 2) + 500 and choice[-1][0] + 125 <= \
                        pygame.mouse.get_pos()[1] <= choice[-1][0] + 200:
                    pygame.quit()

        for select in menu_choice:
            select.update(pygame.mouse.get_pos())

        pygame.display.flip()

def display_grid(grid):
    for y in range(len(grid.display)):
        for x in range(len(grid.display[0])) :
            x_pos = frame_x_offset+x*(frame_size+frame_inter)
            y_pos = frame_y_offset+y*(frame_size+frame_inter)
            if grid.display[y][x].covered:
                pygame.draw.rect(game_window, (0, 220, 220), ((x_pos,y_pos),(frame_size, frame_size)))
                if grid.display[y][x].flagged:
                    display_number = number_font.render("F", True, (255,150,0))
                    game_window.blit(display_number, (x_pos + (frame_size - display_number.get_width()) // 2,
                                                      y_pos + (frame_size - display_number.get_height()) // 2))
            else:
                pygame.draw.rect(game_window, (220, 220, 220), ((x_pos,y_pos ),(frame_size, frame_size)))
                number = grid.display[y][x]._get_pos_number()
                display_number = number_font.render(str(number), True, color[number])
                game_window.blit(display_number, (x_pos+(frame_size-display_number.get_width())//2,y_pos+(frame_size-display_number.get_height())//2))
def on_click():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x = floor((mouse_x - frame_x_offset) / (frame_size + frame_inter))
    y = floor((mouse_y - frame_y_offset) / (frame_size + frame_inter))
    return x,y
def start_game(attributes):
    background = pygame.image.load("image_fond.jpg").convert()
    game_window.blit(background, (0, 0))
    game_grid = grid.Grid(attributes[0],attributes[1],attributes[2])
    display_grid(game_grid)
    pygame.display.flip()
    started = False
    while not started :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                x,y = on_click()
                if attributes[1]>x>=0 and attributes[0]>y>=0:
                    game_grid.generate(x,y)
                    started = True
    starting_time = time.time()
    display_grid(game_grid)
    game_grid.check_won()


    while not game_grid.won and not game_grid.lost :
        clock.tick(FPS)
        game_window.blit(background, (0, 0))
        timer = trunc(100*(time.time()-starting_time))/100
        mine_amount_display = title_font.render("Mine restantes : " + str(game_grid.mine_left()), True, (0, 0, 0))
        timer_display = title_font.render("Timer " + str(timer), True, (0, 0, 0))
        pygame.draw.rect(game_window, (0, 255, 255), ((20,20), (250, 150)))
        game_window.blit(mine_amount_display, (30, 50))
        game_window.blit(timer_display, (30, 110))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        x,y = on_click()
                        if attributes[1]>x>=0 and attributes[0]>y>=0:
                            game_grid.check(x,y)
                    if event.button == 3 :
                        x, y = on_click()
                        if attributes[1] > x >= 0 and attributes[0] > y >= 0:
                            game_grid.display[y][x].flag()


        display_grid(game_grid)
        game_grid.checkwon()
        pygame.display.flip()
    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
menu_principal()
