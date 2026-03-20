import pygame as pg
pg.init()

LIGHT_BLUE = (200,255,255)
RED = (255,0,0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

window = pg.display.set_mode((500,500))
window.fill(LIGHT_BLUE)
clock = pg.time.Clock()

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=LIGHT_BLUE):
        self.rect = pg.Rect(x, y, width, height)
        self.fill_color = color
        
    def set_color(self, fcolor):
        self.fill_color = fcolor

    def fill(self):
        pg.draw.rect(window, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, color=LIGHT_BLUE):
        Area.__init__(self, x=x, y=y, width=width,height=height, color=color)
        self.image = pg.image.load(filename)
        
    def draw(self):
        self.fill()
        window.blit(self.image, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, fsize=14, color=BLACK):
        font = pg.font.SysFont('verdana', fsize)
        bold_text = font.set_bold(True)
        self.image = font.render(text, True, color)

    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
           
ball = Picture('ball.png', 240, 450, 50, 50)
platform = Picture('platform.png', 215, 500, 100, 24)

move_left = False
move_right = False
row = 8
y = 0
x = 15
enemy_list = []
d_y = 2 
d_x = 2
game_over = False

for level in range(3):
    for i in range(row):
        enemy = Picture('enemy.png', x, y, 50, 45)
        enemy_list.append(enemy)
        x += 60
    row -= 1
    y += 50
    x = 15 + 0.6 * y

while not game_over:
    window.fill(LIGHT_BLUE)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_over = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                move_right = True
            if event.key == pg.K_a:
                move_left = True
        if event.type == pg.KEYUP:
            if event.key == pg.K_d:
                move_right = False
            if event.key == pg.K_a:
                move_left = False
    
    if move_right:
        platform.rect.x += 2
    if move_left:
        platform.rect.x -= 2

    if platform.rect.x <= 0:
        platform.rect.x += 2
    if platform.rect.x >= 404:
        platform.rect.x -= 2

    ball.rect.x += d_x
    ball.rect.y -= d_y

    if ball.rect.y < 0:
        d_y *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        d_x *= -1
    if ball.rect.colliderect(platform.rect):
        d_y *= -1

    ball.draw()
    platform.draw()
    
    for enemy in enemy_list:
        enemy.draw()
        if enemy.rect.colliderect(ball.rect):
            enemy_list.remove(enemy) 
            enemy.fill()
            d_y *= -1    
 
    if len(enemy_list) == 0:
        win = Label(0, 0, 500, 820, GREEN)
        win.set_text('Ты выиграл!!!', 50, WHITE)
        win.draw(150, 300)
        game_over = True

    if ball.rect.y > platform.rect.y+20:
        win = Label(0, 0, 500, 820, RED)
        win.set_text('ТЫ АБУБАКАР! ТЫ ПРОИГРАЛ!', 40, WHITE)
        win.draw(25, 300)
        game_over = True    
 
    clock.tick(140)
    pg.display.update()
    