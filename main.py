import pygame
import pygame.gfxdraw
from random import choice
import time
import datetime
import random


backsides_music = ['музыка/All_Of_The_Lights.mp3', 'музыка/Drunk_and_Hot_Girls.mp3', 'музыка/Flashing_Lights.mp3',
                   'музыка/Hell_Of_A_Life.mp3']

music = random.choice(backsides_music)


def load_image(title):
    image = pygame.image.load(title)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("white_brick.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen):
            self.kill()

class Particle21e(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("white_brick.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = 1

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(self.screen):
            self.kill()

class Background(pygame.sprite.Sprite):
    image = load_image("background.jpg")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, *args):
        pass


all_sprites = pygame.sprite.Group()

all_sprites.add(Background(all_sprites))


WIDTH = 1000
HEIGHT = 500
TITLE = "Сломай кирпич 1"

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
DARK_GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
DULL_BLUE = (0, 128, 128)
NAVY = (0, 0, 128)


pygame.init()
pygame.font.init()

pygame.init()
pygame.font.init()


shape_color = (40, 210, 250)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super(Player, self).__init__()
        self.width = 105
        self.height = 26
        self.image = load_image('block.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2 - self.width / 2
        self.rect.y = HEIGHT - (self.height + 10)

        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
        if keys[pygame.K_LEFT]:
            self.rect.x -= 10

        self.bounds()

    def bounds(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, player):
        super(Ball, self).__init__()
        self.height = 40
        self.width = 40
        self.image = load_image('ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.x_vel = 8
        self.y_vel = -7
        self.p = player
        self.hasCollided = False

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.bounds()
        self.collisions()

    def bounds(self):
        if self.rect.top <= 0:
            if self.rect.bottom >= HEIGHT:
                pass
            else:
                self.y_vel *= -1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            if self.rect.bottom >= HEIGHT:
                pass
            else:
                self.x_vel *= -1

        if self.rect.bottom >= HEIGHT:
            self.hasCollided = True

    def collisions(self):
        if self.rect.bottom >= self.p.rect.top and self.rect.x >= self.p.rect.left and self.rect.x <= self.p.rect.right:
            self.y_vel *= -1


class Brick(pygame.sprite.Sprite):
    def __init__(self, ball, player, x, y):
        super(Brick, self).__init__()
        self.image = load_image('white_brick.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.ball = ball
        self.player = player

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        if self.rect.colliderect(self.ball.rect):
            self.ball.y_vel *= -1
            self.player.score += 1
            self.kill()


class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.running = True
        self.playing = True
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()

        self.player = None
        self.ball = None

        self.brick = None
        self.counter = True

    def new(self):
        self.win.fill(WHITE)
        self.init()
        self.draw()
        self.events()
        self.update()
        self.run()

    def init(self):
        self.player = Player()
        self.ball = Ball(self.player)
        if choice([1, 0, 1, 1, 1, 1, 1]):
            for a in range(10):
                self.brick = Brick(self.ball, self.player, a*100, 10)
                self.all_sprites.add(self.brick)
            for a in range(10):
                self.brick = Brick(self.ball, self.player,  a*100, 80)
                self.all_sprites.add(self.brick)

            if choice([1, 0]):
                for a in range(10):
                    self.brick = Brick(self.ball, self.player, a * 100, 150)
                    self.all_sprites.add(self.brick)
        else:
            for a in range(0, 10, 2):
                self.brick = Brick(self.ball, self.player, a*100, 10)
                self.all_sprites.add(self.brick)
            for a in range(0, 10, 2):
                self.brick = Brick(self.ball, self.player,  a*100, 80)
                self.all_sprites.add(self.brick)

        self.all_sprites.add(self.player, self.ball)
        self.counter = True

    def run(self):
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1, 0.0)
        while self.playing:
            self.clock.tick(FPS)
            all_sprites.draw(self.win)
            self.draw()
            self.events()
            self.update()

    def draw(self):
        self.all_sprites.draw(self.win)

    def events(self):
        if self.ball.hasCollided and self.counter:

            self.gameOver()
            self.counter = False

        for event in pygame.event.get():

            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:

                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        pygame.display.flip()

    def start_screen(self):
        waiting = True
        while waiting:

            for event in pygame.event.get():

                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    waiting = False

                    if self.playing:
                        self.playing = False

                    self.running = False

                if keys[pygame.K_q]:
                    waiting = False

                    if self.playing:
                        self.playing = False

                    self.running = False

                if keys[pygame.K_p]:
                    waiting = False

            self.clock.tick(15)

            self.draw_text("Нажми З для начала игры", 100, 100, 28, GREEN)
            self.draw_text("Нажми Й для выхода из игры ", 100, 130, 28, GREEN)

            pygame.display.flip()

    def game_over_screen(self):
        pass

    def broadcast_new_game(self, button):
        self.ball.hasCollided = False
        self.new()

    def gameOver(self):
        self.win.fill(BLACK)
        self.all_sprites.empty()
        self.draw_text("КОНЕЦ ИГРЫ!!", 100, 100, 60, (255, 0, 0))
        self.draw_text("ТВОЙ СЧЁТ: " + str(self.player.score), 200, 200, 20, (0, 255, 0))

        file = open('results.txt', mode='a')
        now = str(datetime.datetime.now())
        file.write(now + '---' + str(self.player.score))
        file.close()
        
        button = Button(self.win, (255, 0, 0), Text("Play Again", (305, 310), 20, (0, 0, 0)), (300, 300), (110, 50),
                        lambda: self.broadcast_new_game(button))

        button.drawning()

    def draw_text(self, string, coordx, coordy, fontSize, color):
        Text.draw_text(self.win, string, coordx, coordy, fontSize, color)

pygame.init()
pygame.font.init()


class Text:
    def __init__(self, string, coords, fontSize, color):
        self.string = string
        self.coordx = coords[0]
        self.coordy = coords[1]
        self.fontSize = fontSize
        self.color = color

    @staticmethod
    def draw_text(screen, string, coordx, coordy, fontSize, color):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(string, True, color)
        screen.blit(text, (coordx, coordy))


class Button:
    def __init__(self, screen, color, text, position, size, command):
        self.screen = screen
        self.color = color
        self.text = text
        self.cx = position[0]
        self.cy = position[1]
        self.width = size[0]
        self.height = size[1]
        self.command = command
        r = 0
        g = 0
        b = 0
        if color[0] >= 15:
            r = color[0] - 15
        if color[1] >= 15:
            g = color[1] - 15
        if color[2] >= 15:
            b = color[2] - 15

        self.lightColor = (r, g, b)

        self.isClicked = False

    def krugliy_krug(self, surface, rect, color, corner_radius):
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(f"Код дристня")

        pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
        pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

        rect_tmp = pygame.Rect(rect)

        rect_tmp.width -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

        rect_tmp.width = rect.width
        rect_tmp.height -= 2 * corner_radius
        rect_tmp.center = rect.center
        pygame.draw.rect(surface, color, rect_tmp)

    def drawning(self):
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.cx < mouse[0] < self.cx + self.width and self.cy < mouse[1] < self.cy + \
                            self.height:
                        self.command()
                        self.isClicked = True

            if(self.cx < mouse[0] < self.cx + self.width) and (self.cy < mouse[1] < self.cy +
                                                               self.height):
                rect = pygame.rect.Rect(self.cx, self.cy, self.width, self.height)
                self.krugliy_krug(self.screen, rect, self.lightColor, 10)
            else:
                rect = pygame.rect.Rect(self.cx, self.cy, self.width, self.height)
                self.krugliy_krug(self.screen, rect, self.color, 10)

            Text.draw_text(self.screen, self.text.string, self.text.cx, self.text.cy, self.text.fontSize,
                           self.text.color)
            pygame.display.update()

            if self.isClicked:
                break


if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    g = Game()
    g.start_screen()
    while g.running:
        g.new()
        g.game_over_screen()
