import math
import pygame
 
#DEFINIRANJE BOJA
black = (0, 0, 0)
white = (255, 255, 255)
blue = (51, 148, 245)
red = (219, 39, 26)
green = (45, 235, 102)
orange = (235, 155, 45)
yellow = (235, 225, 45)
violet = (45, 235, 102)
 
#VELICINA BLOKOVA
block_width = 51
block_height = 20
 
 
class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load('brick.png') #Ucitavanje slike bloka
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block_blue(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load('brick_blue.png') #Ucitavanje slike bloka
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block_red(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load('brick_red.png') #Ucitavanje slike bloka
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block_green(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.image.load('brick_green.png') #Ucitavanje slike bloka
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
class Ball(pygame.sprite.Sprite):
    
    speed = 8.0  #Brzina lopte u pikselima
    x = 0.0         #Pocetna pozicija X
    y = 180.0       #Pocetna pozicija Y
    direction = 200     #Pocetni smjer lopte
    width = 10
    height = 10
 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('ball.png')
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        direction_radians = math.radians(self.direction)    #Konvertiranje sinusa i kosinusa
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        self.rect.x = self.x
        self.rect.y = self.y
        # Odbijanje od gornji rub prozora
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        #Odbijanje od lijevi rub prozora
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        #Odbijanje od desni rub prozora
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
 
        #Odbijanje od donji rub prozora
        if self.y > 600:
            return True
        else:
            return False
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 75
        self.height = 20
        #self.image = pygame.Surface([self.width, self.height])
        self.image = pygame.image.load('paddle.png') #Ucitavanje slike bloka
        
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
    def update(self):
        pos = pygame.mouse.get_pos()    #Pozicija misa
        self.rect.x = pos[0]

        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

class DonjaCrta(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.width = 899
        self.height = 2
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((black))
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
#Ucitavanje pygame
pygame.init()
 
#Kreiranje prozora u dimenzijama
screen = pygame.display.set_mode([900, 650])
 
#Naslov prozora
pygame.display.set_caption('FERIT Breaker')

#Kreiranje fonrova
font = pygame.font.Font(None, 36)
srednjifont = pygame.font.Font(None, 80)
vecifont = pygame.font.Font(None, 120)

#Ucitavanje slika levela
level_1 = pygame.image.load("lev_1.png")
level_2 = pygame.image.load("lev_2.png")
level_3 = pygame.image.load("lev_3.png")
level_4 = pygame.image.load("lev_4.png")
level_5 = pygame.image.load("lev_5.png")


background = pygame.Surface(screen.get_size())
 
#Kreiranje spriteova
blocks = pygame.sprite.Group() #Blokovi levela 1
blocks2 = pygame.sprite.Group() #Blokovi levela 2
blocks3 = pygame.sprite.Group() #Blokovi levela 3
blocks4 = pygame.sprite.Group() #Blokovi levela 4
blocks5 = pygame.sprite.Group() #Blokovi levela 5
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
crte = pygame.sprite.Group()
 
#Kreiranje paddla
player = Player()
allsprites.add(player)

#Kreiranje donjeg ruba koji detektira jel game over
donjacrta = DonjaCrta()
allsprites.add(donjacrta)
crte.add(donjacrta)

# Kreiranje lopte
ball = Ball()
allsprites.add(ball)
balls.add(ball)

state = "menu" # "play" "game_over" "level_predjen" cemo jos imati
level = 1
score = 0
 
#Gornji rub blokova
top = 80
top2 = 80
top3 = 80
top4 = 80
top5 = 50
 
 
# --- Kreiranje blokova LEVELA 111111111111111111111111
for row in range(1):
    for column in range(0, 15):
        #Kreiranje blokova (color,x,y)
        block = Block(blue, 50 + column * (block_width + 2) + 1, top)
        blocks.add(block)
        #Pomicanje u novi red
    top += block_height + 2
for row in range(1):
    for column in range(0, 15):
        block = Block_blue(blue, 50 + column * (block_width + 2) + 1, top)
        blocks.add(block)
    top += block_height + 2
for row in range(1):
    for column in range(0, 15):
        block = Block_green(blue, 50 + column * (block_width + 2) + 1, top)
        blocks.add(block)
    top += block_height + 2
for row in range(1):
    for column in range(0, 15):
        block = Block_red(blue, 50 + column * (block_width + 2) + 1, top)
        blocks.add(block)
    top += block_height + 2
#-------------------------------------------------#


# --- Kreiranje blokova LEVELA 22222222222222222222
for row in range(1):
    for column in range(0, 3):
        block_2 = Block_red(blue, 368 + column * (block_width + 2) + 1, top2)
        blocks2.add(block_2)
    top2 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_2 = Block_green(blue, 262 + column * (block_width + 2) + 1, top2)
        blocks2.add(block_2)
    top2 += block_height + 2
for row in range(1):
    for column in range(0, 11):
        block_2 = Block(blue, 156 + column * (block_width + 2) + 1, top2)
        blocks2.add(block_2)
    top2 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_2 = Block_green(blue, 262 + column * (block_width + 2) + 1, top2)
        blocks2.add(block_2)
    top2 += block_height + 2
for row in range(1):
    for column in range(0, 3):
        block_2 = Block_red(blue, 368 + column * (block_width + 2) + 1, top2)
        blocks2.add(block_2)
    top2 += block_height + 2
#-------------------------------------------------#

# --- Kreiranje blokova LEVELA 3333333333333333
for row in range(1):
    for column in range(0, 15):
        block_3 = Block(blue, 50 + column * (block_width + 2) + 1, top3)
        blocks3.add(block_3)
    top3 += block_height + 2
for row in range(1):
    for column in range(0, 13):
        block_3 = Block_blue(blue, 103 + column * (block_width + 2) + 1, top3)
        blocks3.add(block_3)
    top3 += block_height + 2
for row in range(1):
    for column in range(0, 11):
        block_3 = Block_green(blue, 156 + column * (block_width + 2) + 1, top3)
        blocks3.add(block_3)
    top3 += block_height + 2
for row in range(1):
    for column in range(0, 9):
        block_3 = Block_blue(blue, 209 + column * (block_width + 2) + 1, top3)
        blocks3.add(block_3)
    top3 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_3 = Block(blue, 262 + column * (block_width + 2) + 1, top3)
        blocks3.add(block_3)
    top3 += block_height + 2
#-------------------------------------------------#

# --- Kreiranje blokova LEVELA 44444444444444444444444
for row in range(1):
    for column in range(0, 8):
        block_4 = Block(blue, 50 + column * (block_width + 55) + 1, top4)
        blocks4.add(block_4)
    top4 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_4 = Block_red(blue, 50 + column * (block_width + 55) + 1, top4)
        blocks4.add(block_4)
    top4 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_4 = Block(blue, 50 + column * (block_width + 55) + 1, top4)
        blocks4.add(block_4)
    top4 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_4 = Block_red(blue, 50 + column * (block_width + 55) + 1, top4)
        blocks4.add(block_4)
    top4 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_4 = Block(blue, 50 + column * (block_width + 55) + 1, top4)
        blocks4.add(block_4)
    top4 += block_height + 2
#-------------------------------------------------#

# --- Create blocks LEVELA 55555555555555555555555555
for row in range(1):
    for column in range(0, 8):
        block_5 = Block(blue, 50 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_5 = Block_blue(blue, 103 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_5 = Block(blue, 50 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_5 = Block_blue(blue, 103 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_5 = Block(blue, 50 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 7):
        block_5 = Block_blue(blue, 103 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
for row in range(1):
    for column in range(0, 8):
        block_5 = Block(blue, 50 + column * (block_width + 55) + 1, top5)
        blocks5.add(block_5)
    top5 += block_height + 2
#-------------------------------------------------#


clock = pygame.time.Clock()
game_over = False
exit_program = False
score = 0


while not exit_program:
    # Limit na 60 fpsa
    clock.tick(60)
    screen.fill(black)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "menu":
                if level1.collidepoint(event.pos):
                    level = 1
                    print(level)
                elif level2.collidepoint(event.pos):
                    level = 2
                    print(level)
                elif level3.collidepoint(event.pos):
                    level = 3
                    print(level)
                elif level4.collidepoint(event.pos):
                    level = 4
                    print(level)
                elif level5.collidepoint(event.pos):
                    level = 5
                    print(level)
                elif play_game.collidepoint(event.pos):
                    state = "play"
            elif state == "level_predjen":
                if exit_text.collidepoint(event.pos):
                    pygame.display.quit()
                    pygame.quit()
                    quit()
            elif state == "game_over":
                if exit_text.collidepoint(event.pos):
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                    
 
    
    #STANJA igre
    if state == "menu":
        screen.fill(black)
        pygame.mouse.set_visible(1) #Mis kursor vidljiv u prozoru
        play_game = vecifont.render("IGRAJ!", True, green)
        play_gamepos = play_game.get_rect(centerx=background.get_width()/2)
        play_gamepos.top = 550
        play_game =screen.blit(play_game, play_gamepos)
        level1 = screen.blit(level_1, (33,100))
        level2 = screen.blit(level_2, (317,100))
        level3 = screen.blit(level_3, (616,100))
        level4 = screen.blit(level_4, (175,300))
        level5 = screen.blit(level_5, (475,300))
        odaberi_level = srednjifont.render("MOLIMO ODABERITE LEVEL:", True, yellow)
        odaberi_levelpos = odaberi_level.get_rect(centerx=background.get_width()/2)
        odaberi_levelpos.top = 15
        screen.blit(odaberi_level, odaberi_levelpos)
        odabrani_level = font.render("Odabrani level: %d"%level, True, orange)
        odabrani_levelpos = odabrani_level.get_rect(centerx=background.get_width()/2)
        odabrani_levelpos.top = 465
        screen.blit(odabrani_level, odabrani_levelpos)
        
    elif state == "play":
        screen.fill(black)
        score_text = font.render("Score: %d"%score, True, white)
        score_textpos = score_text.get_rect(centerx=background.get_width()/2)
        score_textpos.top = 5
        screen.blit(score_text, score_textpos)
        pygame.mouse.set_visible(0) #Mis kursor nevidljiv u prozoru
        
        if not state == "game_over":
            player.update()
            ball.update()
            
        # ako lopta pogadja paddle
        if pygame.sprite.spritecollide(player, balls, False):
            diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
            ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
            ball.bounce(diff)

        if pygame.sprite.spritecollide(ball, blocks, True) and level == 1:
            score += 1
            ball.bounce(0)
            if len(blocks) == 0:
                state = "level_predjen"
        elif pygame.sprite.spritecollide(ball, blocks2, True) and level == 2:
            score += 1
            ball.bounce(0)
            if len(blocks2) == 0:
                state = "level_predjen"
        elif pygame.sprite.spritecollide(ball, blocks3, True) and level == 3:
            score += 1
            ball.bounce(0)
            if len(blocks3) == 0:
                state = "level_predjen"
        elif pygame.sprite.spritecollide(ball, blocks4, True) and level == 4:
            score += 1
            ball.bounce(0)
            if len(blocks4) == 0:
                state = "level_predjen"
        elif pygame.sprite.spritecollide(ball, blocks5, True) and level == 5:
            score += 1
            ball.bounce(0)
            if len(blocks5) == 0:
                state = "level_predjen"

        elif pygame.sprite.spritecollide(ball, crte, True):
            state = "game_over"

        # Nacrtaj sve
        allsprites.draw(screen)
        if  level == 1:
            blocks.draw(screen)
        elif  level == 2:
            blocks2.draw(screen)
        elif  level == 3:
            blocks3.draw(screen)
        elif  level == 4:
            blocks4.draw(screen)
        elif  level == 5:
            blocks5.draw(screen)
        
    elif state == "level_predjen":
        score = 0
        screen.fill(black)
        pygame.mouse.set_visible(1) #Mis kursor vidljiv u prozoru
        proso_level = vecifont.render("PRESLI STE LEVEL!", True, green)
        proso_levelpos = proso_level.get_rect(centerx=background.get_width()/2)
        proso_levelpos.top = 100
        screen.blit(proso_level, proso_levelpos)
        exit_text = srednjifont.render("EXIT", True, red)
        exit_textpos = exit_text.get_rect(centerx=background.get_width()/2)
        exit_textpos.top = 350
        exit_text = screen.blit(exit_text, exit_textpos)

    elif state == "game_over":
        score = 0
        screen.fill(black)
        pygame.mouse.set_visible(1) #Mis kursor vidljiv u prozoru
        tekst1 = vecifont.render("GAME OVER!", True, red)
        tekst1pos = tekst1.get_rect(centerx=background.get_width()/2)
        tekst1pos.top = 100
        screen.blit(tekst1, tekst1pos)
        exit_text = srednjifont.render("EXIT", True, red)
        exit_textpos = exit_text.get_rect(centerx=background.get_width()/2)
        exit_textpos.top = 350
        exit_text = screen.blit(exit_text, exit_textpos)
    
    pygame.display.flip()
 
pygame.quit()
