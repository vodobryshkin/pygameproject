import pygame
import pygame
import pygame.gfxdraw
from random import choice
import time
import datetime


WIDTH = 1000
HEIGHT = 500
TITLE= "BreakTheBrick"

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


def main():
    # initializes Pygame
    pygame.init()

    # sets the window title
    pygame.display.set_caption(u'Draw a circle')

    # sets the window size
    screen = pygame.display.set_mode((400, 400))

    # draws 3 circles
    pygame.draw.circle(screen, shape_color, (105, 105), 80, 1)
    pygame.draw.circle(screen, shape_color, (290, 105), 80, 4)
    pygame.draw.circle(screen, shape_color, (105, 290), 80, 0)

    # updates the screen
    pygame.display.flip()

    # infinite loop
    while True:
        # returns a single event from the queue
        event = pygame.event.wait()

        # if the 'close' button of the window is pressed
        if event.type == pygame.QUIT:
            # stops the application
            break

    # finalizes Pygame
    pygame.quit()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super(Player, self).__init__()
        self.width = 130
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
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
        self.height = 15
        self.width = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
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
        if self.rect.bottom >= self.p.rect.top and (
                self.rect.x >= self.p.rect.left and self.rect.x <= self.p.rect.right):
            self.y_vel *= -1


class Brick(pygame.sprite.Sprite):
    def __init__(self, ball, player, x, y):
        super(Brick, self).__init__()
        self.image = pygame.Surface((95, 50))
        self.image.fill(BLACK)
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
        while self.playing:
            self.clock.tick(FPS)
            self.win.fill(WHITE)
            self.draw()
            self.events()
            self.update()

    def draw(self):
        self.all_sprites.draw(self.win)

    def events(self):
        if self.ball.hasCollided and self.counter:

            self.gameOver()
            self.counter = False

        if self.player.score >= 20 and self.counter:

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
        
        button = Button(self.win, (255, 0, 0), Text("Play Again",(305, 310), 20, (0, 0, 0)),
                        (300, 300), (110, 50), lambda: self.broadcast_new_game(button))

        button.render(True)

    def draw_text(self, string, coordx, coordy, fontSize, color):
        Text.draw_text(self.win, string, coordx, coordy, fontSize, color)


import pygame
import pygame.gfxdraw

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
    def draw_text(win, string, coordx, coordy, fontSize, color):
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(string, True, color)
        win.blit(text, (coordx, coordy))


class Button:
    def __init__(self, win, color, text, position, size, command):
        self.win = win
        self.color = color
        self.text = text
        self.coordx = position[0]
        self.coordy = position[1]
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

    def draw_rounded_rect(self, surface, rect, color, corner_radius):
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

        # need to use anti aliasing circle drawing routines to smooth the corners
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


    def render(self, bool):
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    pygame.quit()
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if(self.coordx < mouse[0] < self.coordx + self.width) and (self.coordy < mouse[1] < self.coordy + self.height):
                        self.command()
                        self.isClicked = True

            if(self.coordx < mouse[0] < self.coordx + self.width) and (self.coordy < mouse[1] < self.coordy + self.height):
                rect = pygame.rect.Rect(self.coordx, self.coordy, self.width, self.height)
                self.draw_rounded_rect(self.win, rect, self.lightColor, 10)
            else:
                rect = pygame.rect.Rect(self.coordx, self.coordy, self.width, self.height)
                self.draw_rounded_rect(self.win, rect, self.color, 10)

            Text.draw_text(self.win, self.text.string, self.text.coordx, self.text.coordy, self.text.fontSize, self.text.color)
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
