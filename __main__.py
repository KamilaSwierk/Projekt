import pygame
import random

pygame.font.init()
pygame.init()

# STAŁE WIELKOŚCI
WIDTH, HEIGHT = 600, 600
SIZE = 20

WIDTH_JOEY = 40
HEIGHT_JOEY = 40
WIDTH_FOOD = 20
HEIGHT_FOOD = 20
WIDTH_ENEMY = 40
HEIGHT_ENEMY = 40

# KOLORY
BLACK = (0, 0, 0)


#GRAFIKA
START_IMAGE = pygame.image.load("start.png")
START_IMAGE = pygame.transform.scale(START_IMAGE, (WIDTH, HEIGHT))
BACKGROUND = pygame.image.load("background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
CHANDLER = "chandler.png"
MONICA = "monica.png"
JANICE = "janice.png"

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#GRACZ
class Joey(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = WIDTH_JOEY
        self.height = HEIGHT_JOEY
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT // 2 - self.height // 2
        self.store = 0
        self.image = pygame.image.load("joey.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    #PORUSZANIE SIĘ GRACZA
    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 8
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += 8
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= 8
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += 8

        self.rect.x = self.x
        self.rect.y = self.y

    #RYSOWANIE POSTACI
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def eat(self, points):
        self.store += points

#WROGOWIE
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image_path, speed_x, speed_y, points):
        pygame.sprite.Sprite.__init__(self)
        self.image_path = image_path  # Przechowuj nazwę pliku obrazka
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (WIDTH_ENEMY, HEIGHT_ENEMY))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.points = points

#RYSOWANIE WROGÓW
    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self, joey):
        if pygame.sprite.spritecollide(self, [joey], False):
            joey.eat(self.points)
            self.points = 0

            #ODEJMOWANIE PUNKTÓW PRZEZ WROGÓW I ZMIENIANIE ICH MIEJSCA PO KOLIZJI Z GRACZEM
            if self.image_path == JANICE:
                game_over(loser=True)
                return
            elif self.image_path == CHANDLER:
                joey.eat(-1)
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            elif self.image_path == MONICA:
                joey.eat(-5)
                self.rect.x = random.randint(0, WIDTH - self.rect.width)
                self.rect.y = random.randint(0, HEIGHT - self.rect.height)

        #RUCH WROGÓW
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed_y *= -1



#JEDZENIE GRACZA/ PUNKTY ZDOBYWANE PRZEZ GRACZA
class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = WIDTH_FOOD
        self.height = HEIGHT_FOOD
        self.image = pygame.image.load("pizza.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    #RYSOWANIE JEDZENIA
    def draw(self, win):
        win.blit(self.image, self.rect)

    def update(self, joey):
        # KOLIZJA Z GRACZEM
        if pygame.sprite.collide_rect(self, joey):
            joey.eat(1)
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)

#FUNKCJA NA ZAKOŃCZENIE GRY
def game_over(loser=False):
    if loser:
        ending_image = pygame.image.load("ending_loser.png")    #W PRZYPADKU PRZEGRANEJ
    else:
        ending_image = pygame.image.load("ending_win.png")      #W PRZYPADKU WYGRANEJ

    ending_image = pygame.transform.scale(ending_image, (WIDTH, HEIGHT))

    #DZIAŁANIE WEDŁUG INSTRUKCJI Z OBRAZÓW KOŃCZĄCYCH GRĘ
    show_image = True
    while show_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_image = False
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return

        WIN.blit(ending_image, (0, 0))
        pygame.display.update()

    main()

#RYSOWANIE TŁA
def draw_board(win):
    win.blit(BACKGROUND, (0, 0))

#WROGOWIE NIE BĘDĄ POJAWIAĆ SIĘ W TYM SAMYM MIEJSCU
def check_enemy_collisions(enemies):
    for enemy1 in enemies:
        for enemy2 in enemies:
            if enemy1 != enemy2:
                if pygame.sprite.collide_rect(enemy1, enemy2):
                    enemy1.rect.x = random.randint(0, WIDTH - enemy1.rect.width)
                    enemy1.rect.y = random.randint(0, HEIGHT - enemy1.rect.height)

def main():
    pygame.display.set_caption('JOEY DOESNT SHARE FOOD')

    joey = Joey()
    food = Food()
    enemy1 = Enemy(CHANDLER, 7, 7, 0)
    enemy2 = Enemy(MONICA, 3, 3, 0)
    enemy3 = Enemy(JANICE, 1, 1, 0)

    enemies = [enemy1, enemy2, enemy3]

    #OBRAZ POWITALNY
    show_image = True
    while show_image:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    show_image = False
                elif event.key == pygame.K_RETURN:
                    pygame.quit()
                    return

        WIN.blit(START_IMAGE, (0, 0))
        pygame.display.update()

    #PĘTLA GŁÓWNA PROGRAMU
    run = True
    while run:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        joey.move()

        for enemy in enemies:
            enemy.update(joey)



        draw_board(WIN)

        # WYŚWIETLANIE PUNKTACJI
        font = pygame.font.SysFont(None, 24)
        score_text = font.render("Score: " + str(joey.store), True, BLACK)
        WIN.blit(score_text, (10, 10))

        joey.draw(WIN)
        food.draw(WIN)
        food.update(joey)

        for enemy in enemies:
            enemy.draw(WIN)

        check_enemy_collisions(enemies)

        pygame.display.update()

        # WYGRANA
        if joey.store >= 10:
            game_over(loser=False)

    game_over(loser=True)


if __name__ == '__main__':
    main()
