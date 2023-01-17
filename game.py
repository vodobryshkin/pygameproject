import pygame
import random


def load_image(title):
    image = pygame.image.load(title)
    return image


backsides_fonts = ['космосы/космос1.jpg', 'космосы/космос2.jpeg', 'космосы/космос3.jpg', 'космосы/космос4.jpeg']

backsides_music = ['музыка/All_Of_The_Lights.mp3', 'музыка/Drunk_and_Hot_Girls.mp3', 'музыка/Flashing_Lights.mp3',
                   'музыка/Hell_Of_A_Life.mp3']

backside = load_image(random.choice(backsides_fonts))
backside = pygame.transform.scale(backside, (700, 700))

music = random.choice(backsides_music)

asteroids = pygame.sprite.Group()


class MainGame:  # класс, отвечающий за игру
    def __init__(self, title='Игра на питоне', width=700, height=700):  # в параметрах класса название и размер окна
        self.title = title
        self.size = self.width, self.height = width, height

        self.screen = pygame.display.set_mode(self.size)  # создание окна игры

        self.running = True  # переменная основного игрового цикла
        self.level = 1
        self.create_new_line_of_blocks()
        self.screen.blit(backside, (0, 0))
        asteroids.draw(self.screen)

    def draw_around(self):  # отрисовка всех компонентов игры
        pass
        #  self.screen.blit(backside, (0, 0))  # отрисовка фона

    def run(self):  # запуск игры и основного игрового цикла для одиночного режима игры (против бота)
        pygame.init()
        pygame.display.set_caption(self.title)

        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1, 0.0)

        fps = 50  # количество кадров в секунду
        clock = pygame.time.Clock()
        self.running = True
        while self.running:  # главный игровой цикл
            self.click_button_events()
            self.pressed_buttons_events()
            # обработка остальных событий
            # ...
            self.draw_around()
            pygame.display.flip()  # смена кадра
            # изменение игрового мира
            # ...
            # временная задержка
            clock.tick(fps)

    def pressed_buttons_events(self):
        keys = pygame.key.get_pressed()

    def click_button_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def create_new_line_of_blocks(self):
        line_probability = random.choice([1, 1, 2, 2, 1, 1, 1, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        curr_line = []
        if not line_probability:
            curr_line = random.choice([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                                       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                                       [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                       [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        elif line_probability == 1:
            curr_line = random.choice([[0, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                                       [1, 0, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
                                       [1, 1, 0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                                       [1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
                                       [1, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]])
        elif line_probability == 2:
            curr_line = random.choice([[1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
                                       [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                                       [0, 0, 1, 0, 0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                                       [0, 0, 0, 1, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
                                       [0, 0, 0, 0, 1, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1, 0, 0]])

        elif line_probability == 3:
            curr_line = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in range(10):
            if curr_line[i]:
                hype = random.choice([0, 0, 0, 0, 0, 0, 1])
                health = self.level
                if hype:
                    health *= 2
                asteroid = Asteroid(asteroids, health, i * 70, 0)
                asteroids.add(asteroid)


class Kanye(pygame.sprite.Sprite):
    image = load_image("лицо канье.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Kanye.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self, *args):
        pass


class Asteroid(pygame.sprite.Sprite):
    image = load_image("астероид.png")
    image = pygame.transform.scale(image, (70, 70))

    def __init__(self, group, health, x, y):
        super().__init__(group)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health

    def update(self, *args):
        pass


if __name__ == '__main__':
    game = MainGame('Kanye in the Space')
    game.run()
