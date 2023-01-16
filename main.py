import pygame, random, time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Snake")

grey = (119,136,153)
black = (0, 0, 0)
white = (255, 255, 255)
violet = (138,43,226)
red = (220,20,60)
reward = [-1, -1]
extend = 0
W = 800
H = 600
w = 20
h = 20

def draw_grid():
    global screen, grey, W, H, w, h
    for i in range(W//w):
        pygame.draw.line(screen, grey, (i*w, 0), (i*w, H))
    for i in range(H//h):
        pygame.draw.line(screen, grey, (0, i*h), (W, i*h))

#snake = [[random.randint(0, W//w-1), random.randint(0, H//h-1)]]
snake = [[W//w/2, H//h/2]]
dx = 1
dy = 0
gameover = 0

def move_snake():
    global snake, dx, dy, w, h, W, H, gameover, extend
    head = [snake[0][0], snake[0][1]]
    head[0] += dx
    head[1] += dy
    if(not(0 <= head[0] and head[0] < W//w and 0 <= head[1] and head[1] < H//h)):
        gameover = 1
        return
    if(extend == 0):
        snake = snake[:-1]
    snake = snake[::-1]
    if(head in snake):
        gameover = 1
        return
    snake.append(head)
    snake = snake[::-1]
    if(extend > 0):
        extend-=1

def loc(x, y):
    global H, W, h, w
    return ((w*x, h*y, w, h))

def draw_snake():
    global H, W, h, w, snake, violet    
    col = list(violet)
    for (x, y) in snake:
        pygame.draw.rect(screen, col, loc(x, y))
        col[1] += 5

def proccess_reward():
    global reward, extend, screen, red
    if(snake[0][0] == reward[0] and snake[0][1] == reward[1]):
        reward = [-1, -1]
        extend += 1
    if(reward == [-1, -1]):
        reward = [random.randint(0, W//w-1), random.randint(0, H//h-1)]
        while(reward in snake):
            reward = [random.randint(0, W//w-1), random.randint(0, H//h-1)]
    pygame.draw.rect(screen, red, loc(reward[0], reward[1]))
die = 0

def draw_game_over():
    global red, die
    col = list(red)
    for (x, y) in snake:
        pygame.draw.rect(screen, col, loc(x, y))
        col[0] -= 5
    draw_grid()
    pygame.display.update()
    time.sleep(0.5)
    font = pygame.font.Font(None, 144)
    screen.fill(white)
    txt_surface = font.render("Game over", True, black)
    screen.blit(txt_surface, (130, 250))
    pygame.display.update()
    time.sleep(3)
    die = 1
while True:
    screen.fill(white)
    clock.tick(15)
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            die = 1
            break
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_LEFT and dx != 1):
                dx = -1
                dy = 0
            if(event.key == pygame.K_RIGHT and dx != -1):
                dx = 1
                dy = 0
            if(event.key == pygame.K_UP and dy != 1):
                dx = 0
                dy = -1
            if(event.key == pygame.K_DOWN and dy != -1):
                dx = 0
                dy = 1
    if(die):
        break
    move_snake()
    proccess_reward()
    draw_snake()
    draw_grid()
    if(gameover):
        draw_game_over()

    pygame.display.update()
