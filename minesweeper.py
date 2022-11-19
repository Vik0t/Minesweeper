import pygame as pg
import sys
from pygame.locals import *
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
drew = -1

k = 30
ScreenSize = 392, 392
cellCount = ScreenSize[0] // k
cells = [[{'IsDrawn': False, 'Number': random.randint(0, 5)} for _ in range(cellCount + 1)] for _ in
         range(cellCount + 1)]

pg.init()
sc = pg.display.set_mode(ScreenSize)
pg.display.set_caption('Minesweeper')


def draw_cell(pos):
    print(cells[pos[0]][pos[1]])
    check = check_cell_neighbors(pos)
    if check == 0 and not cells[pos[0]][pos[1]]['IsDrawn']:
        for x in range(pos[0] - 1, pos[0] + 2):
            for y in range(pos[1] - 1, pos[0] + 2):
                if 0 <= x <= cellCount and 0 <= y <= cellCount:
                    actually_draw_cell(pos, check)
                    cells[pos[0]][pos[1]]['IsDrawn'] = True

    actually_draw_cell(pos, check)
    cells[pos[0]][pos[1]]['IsDrawn'] = True


def actually_draw_cell(pos, check):
    color = RED if cells[pos[0]][pos[1]]['Number'] == 5 else BLUE
    rect1 = pg.Rect((pos[0] * k, pos[1] * k, 30, 30))
    font = pg.font.SysFont('arial', 25)
    text = font.render(str(check), True, WHITE)
    pg.draw.rect(
        sc, GREEN if check == 0 else color, rect1, 20)
    if color != RED and check != 0:
        sc.blit(text, (pos[0] * k + 9, pos[1] * k + 1))


def draw_flag(pos):
    rect1 = pg.Rect((pos[0] * k + 1 + 13, pos[1] * k + 10, 4, 20))
    rect2 = pg.Rect((pos[0] * k + 6, pos[1] * k + 25, 20, 6))
    rect3 = pg.Rect((pos[0] * k + 10, pos[1] * k + 23, 12, 6))
    pg.draw.rect(sc, GRAY, rect1, 20)
    pg.draw.rect(sc, GRAY, rect2, 20)
    pg.draw.rect(sc, GRAY, rect3, 20)
    pg.draw.polygon(sc, RED,
                    ((pos[0] * k, pos[1] * k + 13), (pos[0] * k + 17, pos[1] * k), (pos[0] * k + 17, pos[1] * k + 13)))


def check_cell_neighbors(cell):
    summary = 0
    start_x = cell[0] - 1
    start_y = cell[1] - 1
    end_x = cell[0] + 2
    end_y = cell[1] + 2
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            if 0 <= x < cellCount and cells[x][y]['Number'] == 5 and 0 <= y < cellCount:
                summary += 1
    return summary


while True:  # main game loop
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not cells[event.pos[0] // k][event.pos[1] // k]['IsDrawn']:
                    draw_cell([event.pos[0] // k, event.pos[1] // k])
            elif event.button == 3:
                if not cells[event.pos[0] // k][event.pos[1] // k]['IsDrawn']:
                    draw_flag([event.pos[0] // k, event.pos[1] // k])
            elif event.button == 2:
                sc.fill(BLACK)
    for i in range(cellCount + 1):
        pg.draw.line(sc, WHITE, (0, k * i), (400, k * i), 4)
        pg.draw.line(sc, WHITE, (k * i, 0), (k * i, 400), 4)
    pg.time.delay(20)
    pg.display.update()
