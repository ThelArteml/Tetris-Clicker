import os
import sys
import pygame
from random import *
import datetime as dt


# Класс выхода и сохранения основных переменных
def terminate(prim):
    f = open('data/SAVE.txt', 'w+')
    for i in prim:
        print(i, file=f)
    f.close()
    pygame.quit()
    sys.exit()


# Класс для отслеживания покупок
class ShopSold:

    def __init__(self, start, end, price, coeff):
        self.start = start
        self.end = end
        self.price = price
        self.coeff = coeff

    # Функция покупки
    def buying(self):
        if self.start != self.end:
            self.price *= self.coeff
            self.start += 1
            return True
        else:
            return False

    def varies(self):
        return [self.start, self.end, self.price, self.coeff]


# Класс загрузки картинок
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


stop = True
# Открытие файла с сохраннёными переменными
with open('data/SAVE.txt', 'r') as File:
    vars = [line.strip() for line in File]
nums = '1234567890.'
n = ''
times = []
points = 0
# Расспаковка списков
if vars[0] != '[]':
    for i in range(len(vars[0])):
        if vars[0][i] in nums:
            n += vars[0][i]
        if vars[0][i] in nums and vars[0][i + 1] not in nums:
            times.append(int(n))
            n = ''
    datetime = dt.datetime(int(str(times[0])), times[1], times[2], times[3], times[4], times[5])
    pointPerSecond = 350 // int(vars[5])
    if datetime < dt.datetime.now():
        a = dt.datetime.now() - datetime
        points = (a.total_seconds() // pointPerSecond) * 4 * float(vars[3])
# Основные, сохраняемые переменные
FPS = 1
backgroundSound = vars[6]  # Музыка на заднем фоне
points += float(vars[1])  # Заработанные игроком баллы
coef = int(vars[3])  # Коэффициент умножения балов игрока
FPS_perClick = int(vars[4])  # Увеличение скорости падения блоков за клик
gravity = int(vars[5])  # Скорость падения блоков
music_c = int(vars[7])  # Включение - отключения музыки
sound_c = int(vars[8])  # Включение - отключения звуков
# Расспаковка списков
num = []
for i in range(len(vars[9])):
    if vars[9][i] in nums:
        n += vars[9][i]
    if vars[9][i] in nums and vars[9][i + 1] not in nums:
        num.append(float(n))
        n = ''
costMouse = ShopSold(num[0], num[1], num[2], num[3])
costGravi = ShopSold(num[4], num[5], num[6], num[7])
costBlock = ShopSold(num[8], num[9], num[10], num[11])
costX = ShopSold(num[12], num[13], num[14], num[15])
costStickmin = ShopSold(num[16], num[17], num[18], num[19])
costWIN = ShopSold(num[20], num[21], num[22], num[23])
goods = [costMouse, costGravi, costBlock, costX, costStickmin, costWIN]
n = ''
num = []
# Расспаковка списков
for i in range(len(vars[2])):
    if vars[2][i] in nums:
        n += vars[2][i]
    if vars[2][i] in nums and vars[2][i + 1] not in nums:
        num.append(int(n))
        n = ''
tile_images = num  # Рисунки блока в зависимости от улучшения
# Группы Sprite
Amount_clicks = int(vars[10])
Amount_blocks = int(vars[11])
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

# Размеры блоков
tile_width = tile_height = 32
# Рисунки для магазина
shop_images = ['ClickUpgrade.png', 'GravyUpgrade.png', 'BlockUpgrade.png', str(coef + 1) + 'xUpgrade.png', \
               'HenryStickminUpgrade.png', 'WINUpgrade.png']
shop_images_OFF = ['ClickUpgradeOFF.png', 'GravyUpgradeOFF.png', 'BlockUpgradeOFF.png', \
                   str(coef + 1) + 'xUpgradeOFF.png', 'HenryStickminUpgradeOFF.png', 'WINUpgradeOFF.png']
shop_images_out = ['OutOfSold.png', 'OutOfSold.png', 'OutOfSold.png', 'OutOfSold.png', 'OutOfSold.png',\
                   'OutOfSold.png',]


class Tile(pygame.sprite.Sprite):

    def __init__(self, tile_type, pos_x, pos_y, tiles_image_random):
        super().__init__(tiles_group, all_sprites)
        table_x, table_y = game.get_information()
        self.pos_x = (tile_width * pos_x) + table_x + 1
        self.pos_y = (tile_height * pos_y) + table_y + 1
        self.stop = True
        self.image = load_image('Stage' + str(tiles_image_random[tile_type]) + '.png')
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)

    def update(self, y):
        if pygame.sprite.spritecollideany(self, horizontal_borders) and self.stop:
            self.stop = False
            return True
        else:
            self.rect = self.rect.move(0, y)
            return False


def generate_block(level, out_c):
    c = 0
    block = []
    tiles_image_random = sorted(tile_images, key=lambda A: random())
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                if out_c == 0 and y == 0:
                    x -= 3
                block.append(Tile(c, x, y, tiles_image_random))
                c += 1
    return block


# Функция проверки нажатия
def is_click(locate, mouse_pos):
    a = False
    if locate[0] <= mouse_pos[0] <= locate[0] + 50 and locate[1] <= mouse_pos[1] <= locate[1] + 50:
        a = True
    return a


# Функция смены музыки
def music_change(music_c, sound_c):
    if music_c % 2 == 0:
        music_btn = pygame.transform.scale(load_image('MusicON.png'), (50, 50))
        screen.blit(music_btn, (10, 70))
        pygame.mixer.music.play(-1)
    else:
        music_btn = pygame.transform.scale(load_image('MusicOff.png'), (50, 50))
        screen.blit(music_btn, (10, 70))
        pygame.mixer.music.stop()
    if sound_c % 2 == 0:
        sound_btn = pygame.transform.scale(load_image('SoundON.png'), (50, 50))
        screen.blit(sound_btn, (10, 130))
        sound = True
    else:
        sound_btn = pygame.transform.scale(load_image('SoundOFF.png'), (50, 50))
        screen.blit(sound_btn, (10, 130))
        sound = False
    return sound


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.line_width = 1

    # настройка внешнего вида
    def set_view(self, left, top, cell_size, line_width):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.line_width = line_width

    # Отрисовка полей
    def render(self, color):
        left = self.left
        top = self.top
        for h in range(self.height):
            for w in range(self.width):
                pygame.draw.rect(screen, color, (left, top, self.cell_size, self.cell_size), self.line_width)
                left += self.cell_size
            top += self.cell_size
            left = self.left

    # Проверка нажатия на клетку
    def get_cell(self, mouse_pos):
        left = self.left
        top = self.top
        m = self.cell_size
        a = -1
        for h in range(self.height):
            for w in range(self.width):
                if left <= mouse_pos[0] <= left + m and top <= mouse_pos[1] <= top + m:
                    a = w
                left += self.cell_size
            top += self.cell_size
            left = self.left
        return a

    # Вывод начальных координат таблицы
    def get_information(self):
        return self.left, self.top

    # Функция для отрисовки частей в нутри таблицы
    def load(self, images, imagesOFF, goods):
        for i in range(len(images)):
            if points >= goods[i].varies()[2]:
                image = pygame.transform.scale(load_image(images[i]), (self.cell_size - 2, self.cell_size - 3))
                screen.blit(image, (self.left + (i * self.cell_size) + 2, self.top + 2))
            else:
                image = pygame.transform.scale(load_image(imagesOFF[i]), (self.cell_size - 2, self.cell_size - 3))
                screen.blit(image, (self.left + (i * self.cell_size) + 2, self.top + 2))


# Функция для замены переменных в списке
def replace_prim(prim, old_num, new):
    new_prim = []
    for i in range(len(prim)):
        if i == old_num:
            new_prim.append(new)
        else:
            new_prim.append(prim[i])
    return new_prim


# Класс для отрисовки линий остановки блоков
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# Функция для написания текста
def write(font_size, intro_text, located):
    font = pygame.font.Font(None, font_size)
    string_rendered = font.render(intro_text, 1, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = located[1]
    intro_rect.x = located[0]
    screen.blit(string_rendered, intro_rect)


# Начальный экран
def start_screen():
    intro_text = ['Tap to play']
    fon = pygame.transform.scale(load_image('Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    global stop
    while stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                stop = False
        pygame.display.flip()
        clock.tick(1)


def settings_screen():
    intro_text = ['Всего кликов: ' + str(Amount_clicks),
                  'Всего блоков упало: ' + str(Amount_clicks),
                  '1 Mouse Upgarde: ' + str(costMouse.varies()[0]) + '/' + str(costMouse.varies()[1]) + ', '\
                                         + str(costMouse.varies()[2]),
                  '2 Gravi Upgrade: ' + str(costGravi.varies()[0]) + '/' + str(costGravi.varies()[1]) + ', ' \
                                         + str(costGravi.varies()[2]),
                  '3 Block Upgarde: ' + str(costBlock.varies()[0]) + '/' + str(costBlock.varies()[1]) + ', ' \
                                         + str(costBlock.varies()[2]),
                  '4 X Upgarde: ' + str(costX.varies()[0]) + '/' + str(costX.varies()[1]) + ', ' \
                                         + str(costX.varies()[2]),
                  '5 Stickmin Upgarde: ' + str(costStickmin.varies()[0]) + '/' + str(costStickmin.varies()[1]) + ', ' \
                                         + str(costStickmin.varies()[2]),
                  '6 WIN Upgarde: ' + '???'
                  ]
    fon = pygame.transform.scale(load_image('Background.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    global start
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                start = False
        pygame.display.flip()
        clock.tick(1)

# Отрисовка всех элемнтов экрана
def start_game():
    pygame.display.set_icon(pygame.image.load("data/Icon.bmp"))  # Иконка
    pygame.draw.rect(screen, 'black', (0, 0, WIDTH, HEIGHT), 1)  # Границы экрана
    background = pygame.transform.scale(load_image('Background.png'), (WIDTH - 2, HEIGHT - 2))  # Задняя часть экрана
    screen.blit(background, (1, 1))
    background_tetris = pygame.transform.scale(load_image('Background Tetris.png'), (317, 413))  # Задняя часть таблицы
    screen.blit(background_tetris, (92, 77))
    settings_btn = pygame.transform.scale(load_image('Setup.png'), (50, 50))  # Кнопка настроек
    screen.blit(settings_btn, (10, 10))
    music_btn = pygame.transform.scale(load_image('MusicON.png'), (50, 50))  # Кнопка включения/выключения музыки
    screen.blit(music_btn, (10, 70))
    sound_btn = pygame.transform.scale(load_image('SoundON.png'), (50, 50))  # Кнопка включения/выключения звуков
    screen.blit(sound_btn, (10, 130))
    pygame.draw.rect(screen, 'black', (90, 10, 400, 50), 2)  # Грани поля очков
    pygame.draw.rect(screen, 'white', (92, 12, 397, 47), 0)  # Поле очков
    # Создания и настройка таблицы-магазина
    shop = Board(6, 1)
    shop.set_view(10, 510, 80, 2)
    shop.render('black')
    # Создания и настрока таблицы-Tetris
    game = Board(10, 13)
    game.set_view(90, 75, 32, 1)
    game.render((205, 205, 205))
    pygame.draw.rect(screen, (84, 226, 204), (90, 75, 320, 416), 3)  # Создания граний таблицы-Tetris
    Border(90, 489, 410, 489)
    return game, shop, background_tetris


# Генератор случайности для меньшей вероятности "Бага"
def Mychoice():
    a = choice(list_plates)
    if a == 'BAG':
        a = choice(list_plates)
    return a


# Функция зашрузки шаблонов
def load_block(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        map = [line.strip() for line in mapFile]
    block = []
    blocks = []
    for i in map:
        if i != '':
            block.append(i)
        else:
            blocks.append(block)
            block = []
    return blocks


if __name__ == '__main__':
    # Включение Pygame и его модулей
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()

    # Установка главного окна
    size = WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode(size)
    screen.fill('black')
    pygame.display.set_caption('Tetris Clicker')

    # Запуск экрана
    game, shop, background = start_game()

    # Установка музыки
    pygame.mixer.music.load(backgroundSound)
    pygame.mixer.music.play(-1)
    MouseDown = pygame.mixer.Sound('data/Sounds/MouseDown Sound.ogg')
    Buy = pygame.mixer.Sound('data/Sounds/Buying Sound.ogg')
    Cancel = pygame.mixer.Sound('data/Sounds/Cancel.ogg')
    sound = music_change(music_c, sound_c)

    # Создание переменных
    running = True
    write(90, str(points), (92, 8))
    c = 0
    list_plates = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'BAG']
    now_plate = load_block('Plates/Plate' + str(Mychoice()) + '.txt')
    block = generate_block(now_plate[c], c)
    last_time = dt.datetime.now()
    # Цикл игры
    while running:
        while stop:
            start_screen()
            if not stop:
                start_game()
        shop.load(shop_images, shop_images_OFF, goods)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = dt.datetime.now()
                time = [a.strftime('%Y'), a.strftime('%m'), a.strftime('%d'), a.strftime('%H'), a.strftime('%M'), \
                        a.strftime('%S')]  # Сохранение времени
                shop_goods = [goods[0].varies(), goods[1].varies(), goods[2].varies(), goods[3].varies(), \
                              goods[4].varies(), goods[5].varies()]  # Сохранение товаров магазина
                terminate([time, points, tile_images, coef, FPS_perClick, gravity, backgroundSound, \
                           music_c, sound_c, shop_goods, Amount_clicks, Amount_blocks])
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Нажатие на таблицу-Tetris
                if game.get_cell(event.pos) != -1:
                    Amount_clicks += 1
                    if sound:  # Издование звука, если он включён
                        MouseDown.play(0)
                    FPS += FPS_perClick
                    last_time = dt.datetime.now()
                # Нажатия на таблицу-магазин
                shop_x = shop.get_cell(event.pos) + 1
                if shop_x:
                    if goods[shop_x - 1].varies()[2] <= points:
                        if sound:  # Издование звука, если он включён
                            Buy.play(0)
                        if shop_x == 1 and costMouse.buying():
                            FPS_perClick += 1
                            points -= costMouse.varies()[2]
                            if not costMouse.buying():
                                shop_images = replace_prim(shop_images, shop_x - 1, 'OutOfSold.png')
                                shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, 'OutOfSold.png')
                                shop.load(shop_images, shop_images_OFF, goods)
                        if shop_x == 2 and costGravi.buying():
                            gravity += 1
                            points -= costGravi.varies()[2]
                            if not costGravi.buying():
                                shop_images = replace_prim(shop_images, shop_x - 1, 'OutOfSold.png')
                                shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, 'OutOfSold.png')
                                shop.load(shop_images, shop_images_OFF, goods)
                        if shop_x == 3 and costBlock.buying():
                            x1, x2, x3, x4 = tile_images
                            if x1 == x2:
                                x1 += 1
                            elif x2 == x3:
                                x2 += 1
                            elif x3 == x4:
                                x3 += 1
                            else:
                                x4 += 1
                            tile_images = [x1, x2, x3, x4]
                            points -= costBlock.varies()[2]
                            if not costBlock.buying():
                                shop_images = replace_prim(shop_images, shop_x - 1, 'OutOfSold.png')
                                shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, 'OutOfSold.png')
                                shop.load(shop_images, shop_images_OFF, goods)
                        if shop_x == 4 and costX.buying():
                            coef += 1
                            shop_images = replace_prim(shop_images, shop_x - 1, '3xUpgrade.png')
                            shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, '3xUpgradeOFF.png')
                            points -= costX.varies()[2]
                            if not costX.buying():
                                shop_images = replace_prim(shop_images, shop_x - 1, 'OutOfSold.png')
                                shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, 'OutOfSold.png')
                                shop.load(shop_images, shop_images_OFF, goods)
                        if shop_x == 5 and costStickmin.buying():
                            backgroundSound = 'data/Sounds/Henry StickMan Upgrade.ogg'
                            pygame.mixer.music.load(backgroundSound)
                            points -= costStickmin.varies()[2]
                            if not costStickmin.buying():
                                shop_images = replace_prim(shop_images, shop_x - 1, 'OutOfSold.png')
                                shop_images_OFF = replace_prim(shop_images_OFF, shop_x - 1, 'OutOfSold.png')
                                shop.load(shop_images, shop_images_OFF, goods)
                        if shop_x == 6 and costStickmin.buying():
                            terminate(['[]', 0, [1, 1, 1, 1], 1, 1, 1, 'data/Sound/Henry StickMan Upgrade.ogg',\
                                       0, 0, [[0, 40, 100, 1.25], [0, 100, 20, 1.5], [0, 40, 100, 1.5],\
                                              [0, 2, 2000, 15], [0, 1, 1000, 0], [0, 1, 1000000000, 0]], 0, 0])
                    else:
                        if sound:  # Издование звука, если он включён
                            Cancel.play(0)
                if is_click((10, 70), event.pos):
                    # Включение/выключение музыки
                    music_c += 1
                    if music_c % 2 == 0:
                        music_btn = pygame.transform.scale(load_image('MusicON.png'), (50, 50))
                        screen.blit(music_btn, (10, 70))
                        pygame.mixer.music.play(-1)
                    else:
                        music_btn = pygame.transform.scale(load_image('MusicOff.png'), (50, 50))
                        screen.blit(music_btn, (10, 70))
                        pygame.mixer.music.stop()
                if is_click((10, 130), event.pos):
                    # Включение/выключение звука
                    sound_c += 1
                    if sound_c % 2 == 0:
                        sound_btn = pygame.transform.scale(load_image('SoundON.png'), (50, 50))
                        screen.blit(sound_btn, (10, 130))
                        sound = True
                    else:
                        sound_btn = pygame.transform.scale(load_image('SoundOFF.png'), (50, 50))
                        screen.blit(sound_btn, (10, 130))
                        sound = False
                if is_click((10, 10), event.pos):
                    start = True
                    while start:
                        settings_screen()
                        if not start:
                            start_game()
        for i in all_sprites:  # Проверка столкновения блоков с нижней границей
            if i.update(gravity):
                c += 1
                if c != len(now_plate):
                    for j in block:
                        j.kill()
                    points += sum(tile_images) * coef
                    pygame.draw.rect(screen, 'white', (92, 12, 397, 47), 0)
                    write(90, str(points), (92, 8))
                    block = generate_block(now_plate[c], c)
                    Amount_blocks += 1
                    break
                else:
                    now_plate = load_block('Plates/Plate' + str(choice(list_plates)) + '.txt')
                    c = 0
                    break
        if (dt.datetime.now() - last_time).total_seconds() >= 3.0 and FPS != 1:
            FPS -= 1
        screen.blit(background, (92, 77))
        game.render((205, 205, 205))
        pygame.draw.rect(screen, (84, 226, 204), (90, 75, 320, 416), 3)
        tiles_group.draw(screen)
        pygame.draw.rect(screen, 'white', (92, 12, 397, 47), 0)
        write(90, str(points), (92, 8))
        clock.tick(FPS)
        pygame.display.flip()
        pygame.time.delay(20)