import pygame
import sys
from pygame.math import Vector2
import random

class SNAKE:
    def __init__(self):
        self.body = [Vector2(15,15),Vector2(14,15),Vector2(13,15)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.cruch_sound = pygame.mixer.Sound('Sounds/crunch.wav')

    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)

            snake_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if index == 0:
                color = (26, 118, 189)
            else:
                color = (26, 154, 189)
            pygame.draw.rect(screen,color,snake_rect)

    def move(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.cruch_sound.play()
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(15,15),Vector2(14,15),Vector2(13,15)]
        self.direction = Vector2(0,0)

class FRUIT:
    def __init__(self):
        self.randomize()
    
    def randomize(self):
        self.x = random.randint(0,cell_numb - 1)
        self.y = random.randint(0,cell_numb - 1)

        self.position = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen,(255, 0, 0),fruit_rect)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def draw_everything(self):
        self.draw_floor()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def update(self):
        self.snake.move()
        self.check_if_eaten()
        self.check_fail()

    def check_if_eaten(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for block in self.snake.body[1:]:
            if block == self.fruit.position:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_numb or not 0 <= self.snake.body[0].y < cell_numb:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        

    def draw_floor(self):
        color = (69,69,69)
        for row in range(cell_numb):
            if row % 2 == 0:
                for col in range(cell_numb):
                    if col % 2 == 0:
                        floor_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, floor_rect)
            else:
                for col in range(cell_numb):
                    if col % 2 != 0:
                        floor_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, color, floor_rect)

    def draw_score(self):
        score_text = "Score: {}".format(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(207, 207, 207))
        score_x = int(cell_size * 2)
        score_y = int(cell_size)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

cell_size = 30
cell_numb = 30

pygame.display.set_caption('Snake Game')
screen = pygame.display.set_mode((cell_size * cell_numb, cell_size * cell_numb))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Font/Outfit-ExtraBold.ttf', 25)

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
timer = pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1,0)
        
        screen.fill((79, 79, 79))
        main.draw_everything()
        pygame.display.update()
        clock.tick(60)