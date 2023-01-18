import pygame as pg
import sys
import os


pg.init()
WIDTH, HEIGHT = 900, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
FPS = 2
corn_count = 0
wheat_count = 0
corn_seed_count = 10
wheat_seed_count = 10
egg_count = 0
rabbit_skin_count = 0
duck_egg_count = 0
money_count = 999999
is_chicken_coop = False
is_rabbit_house = False
is_lake = False
is_build_window = False
is_home_window = False
is_chicken_window = False
is_rabbit_window = False
is_duck_window = False
is_wheat_seed_window = False
is_corn_seed_window = False
is_start_display = True
chicken_count = 0
rabbit_count = 0
duck_count = 0


def load_image(name, colorkey=None, scale=False, width=10, height=10, rotate=False, degree=0):
    fullname = os.path.join('data/sprites', name)
    if not os.path.isfile(fullname):
        print(f'Изображение не найдено!!!')
        sys.exit()

    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    if scale:
        image = pg.transform.scale(image, (width, height))
    if rotate:
        image = pg.transform.rotate(image, float(degree))
    return image


tile_images = {
    'grass': load_image('grass.png', None, True, 30, 30),
    'home': load_image('home.png', None, True, 140, 140),
    'wheat': load_image('wheat.png'),
    'corn': load_image('corn.png'),
    'tree': load_image('tree.png', None, True, 40, 60),
    'oak': load_image('oak.png', None, True, 50, 70),
    'car': load_image('car.png', None, True, 30, 60, True, -90),
    'tractor': load_image('tractor.png', None, True, 30, 50, True, -90),
    'garage': load_image('garage.png', None, True, 120, 80, True, 180),
    'barn': load_image('barn.png', None, True, 100, 110), 
    'chicken_coop': load_image('chicken_coop.png', None, True, 120, 95),
    'rabbit_house': load_image('rabbit_house.png', None, True, 120, 120),
    'corn_shop': load_image('corn_shop.png', None, True, 100, 100),
    'wheat_shop': load_image('wheat_shop.png', None, True, 100, 102),
    'auto_shop': load_image('auto_shop.png', None, True, 100, 102, True, -90),
    'chicken_shop': load_image('chicken_shop.png', None, True, 95, 102, True, -90),
    'rabbit_shop': load_image('rabbit_shop.png', None, True, 95, 102, True, -90),
    'duck_shop': load_image('duck_shop.png', None, True, 95, 102, True, -90),
    'lake': load_image('lake.png', None, True, 120, 130, True, 90),
    'snow': load_image('snow.png', None, True, 30, 30),
    'start_display': load_image('start_display.png'),
    'finish_display': load_image('finish_display.png')
}


animal_images = {
    'chicken1': load_image('chicken1.png', None, True, 15, 15),
    'chicken2': load_image('chicken2.png', None, True, 15, 15),
    'chicken3': load_image('chicken3.png', None, True, 15, 15),
    'chicken4': load_image('chicken4.png', None, True, 15, 15),
    'rabbit1': load_image('rabbit1.png', None, True, 15, 15),
    'rabbit2': load_image('rabbit2.png', None, True, 15, 15),
    'rabbit3': load_image('rabbit3.png', None, True, 15, 15),
    'rabbit4': load_image('rabbit4.png', None, True, 15, 15),
    'duck1': load_image('duck1.png', None, True, 25, 25),
    'duck2': load_image('duck2.png', None, True, 25, 25),
    'duck3': load_image('duck3.png', None, True, 25, 25),
    'duck4': load_image('duck4.png', None, True, 25, 25)
}

tile_width = 30
tile_height = 30
tiles_group = pg.sprite.Group()
all_sprites = pg.sprite.Group() 
buildings_group = pg.sprite.Group()
plants_group = pg.sprite.Group()
tree_group = pg.sprite.Group()
car_group = pg.sprite.Group()
animal_group = pg.sprite.Group()
window_group = pg.sprite.Group()
displays_group = pg.sprite.Group()


def load_level(filename):
    filename = 'data/levels/' + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


def terminate():
    pg.quit()
    sys.exit()


class Tile(pg.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y
        )


class Home(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['home']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Garage(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['garage']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Barn(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['barn']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class ChickenCoop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['chicken_coop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class RabbitHouse(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['rabbit_house']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class CornShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['corn_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class WheatShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['wheat_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class AutoShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['auto_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class ChickenShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['chicken_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class RabbitShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['rabbit_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class DuckShop(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['duck_shop']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Lake(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(buildings_group, all_sprites)
        self.image = tile_images['lake']
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Wheat(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(plants_group, all_sprites)
        self.image = tile_images['wheat']
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.WHEAT = pg.USEREVENT + 1
        pg.time.set_timer(self.WHEAT, 1000)


class Tree(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tree_group, all_sprites)
        self.image = tile_images['tree']
        self.rect = self.image.get_rect().move(pos_x, pos_y)  


class Oak(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tree_group, all_sprites)
        self.image = tile_images['oak']
        self.rect = self.image.get_rect().move(pos_x, pos_y)  


class Corn(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(plants_group, all_sprites)
        self.image = tile_images['corn']
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.CORN = pg.USEREVENT + 1
        pg.time.set_timer(self.CORN, 1000)


class Chicken(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(animal_group, all_sprites)
        self.image = animal_images['chicken1']
        self.cur_frame = 1
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.CHICKEN = pg.USEREVENT + 1
        pg.time.set_timer(self.CHICKEN, 1000)
    
    def update(self):
        if self.cur_frame != 4:
            self.cur_frame += 1
        else:
            self.cur_frame = 1
        self.image = animal_images[f'chicken{self.cur_frame}']


class Rabbit(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(animal_group, all_sprites)
        self.image = animal_images['rabbit1']
        self.cur_frame = 1
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.RABBIT = pg.USEREVENT + 1
        pg.time.set_timer(self.RABBIT, 1000)
    
    def update(self):
        if self.cur_frame != 4:
            self.cur_frame += 1
        else:
            self.cur_frame = 1
        self.image = animal_images[f'rabbit{self.cur_frame}']


class Duck(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(animal_group, all_sprites)
        self.image = animal_images['duck1']
        self.cur_frame = 1
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.DUCK = pg.USEREVENT + 1
        pg.time.set_timer(self.DUCK, 1000)
    
    def update(self):
        if self.cur_frame != 4:
            self.cur_frame += 1
        else:
            self.cur_frame = 1
        self.image = animal_images[f'duck{self.cur_frame}']


class Car(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(car_group, all_sprites)
        self.image = tile_images['car']
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def move_to_corn_seeds(self):
        pass


class Tractor(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(car_group, all_sprites)
        self.image = tile_images['tractor']
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.right = True

    def update(self):
        if self.right:              
            if not pg.sprite.spritecollideany(self, buildings_group):
                self.rect.x += 10    
            else:
                self.image = pg.transform.flip(self.image, True, False)   
                self.right = False 
        elif not self.right:
            if not pg.sprite.spritecollideany(self, tree_group):
                self.rect.x -= 10
            else:
                self.image = pg.transform.flip(self.image, True, False)
                self.right = True


class HomeWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((540, 160))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Пшеница - ', True,
                  (180, 0, 0))
        self.image.blit(text1, (10, 10))
        text2 = font.render(str(wheat_count) + ' кг', True,
                  (180, 0, 0))
        self.image.blit(text2, (100, 10))
        text3 = font.render('Кукуруза - ', True,
                  (180, 0, 0))
        self.image.blit(text3, (10, 30))
        text4 = font.render(str(corn_count) + ' кг', True,
                  (180, 0, 0))
        self.image.blit(text4, (95, 30))
        text5 = font.render('Семена пшеницы - ', True,
                  (180, 0, 0))
        self.image.blit(text5, (10, 50))
        text6 = font.render(str(wheat_seed_count), True,
                  (180, 0, 0))
        self.image.blit(text6, (160, 50))
        text7 = font.render('Семена кукурузы - ', True,
                  (180, 0, 0))
        self.image.blit(text7, (10, 70))
        text8 = font.render(str(corn_seed_count), True,
                  (180, 0, 0))
        self.image.blit(text8, (160, 70))
        text9 = font.render('Куриные яйца - ', True,
                  (180, 0, 0))
        self.image.blit(text9, (10, 90))
        text10 = font.render(str(egg_count), True,
                  (180, 0, 0))
        self.image.blit(text10, (135, 90))
        text11 = font.render('Крольчатина - ', True,
                  (180, 0, 0))
        self.image.blit(text11, (10, 110))
        text12 = font.render(str(rabbit_skin_count), True,
                  (180, 0, 0))
        self.image.blit(text12, (125, 110))
        text13 = font.render('Утятина - ', True,
                  (180, 0, 0))
        self.image.blit(text13, (10, 130))
        text14 = font.render(str(duck_egg_count), True,
                  (180, 0, 0))
        self.image.blit(text14, (95, 130))
        text15 = font.render('Всего денег - ', True,
                  (180, 0, 0))
        self.image.blit(text15, (280, 10))
        text16 = font.render(str(money_count) + '₽', True,
                  (180, 0, 0))
        self.image.blit(text16, (390, 10))
        text17 = font.render('F1', True,
                  (180, 0, 0))
        self.image.blit(text17, (220, 10))
        text18 = font.render('F2', True,
                  (180, 0, 0))
        self.image.blit(text18, (220, 30))
        text21 = font.render('F3', True,
                  (180, 0, 0))
        self.image.blit(text21, (220, 90))
        text22 = font.render('F4', True,
                  (180, 0, 0))
        self.image.blit(text22, (220, 110))
        text23 = font.render('F5', True,
                  (180, 0, 0))
        self.image.blit(text23, (220, 130))


class Board:
    def __init__(self, width, height, level_map):
        self.width = width
        self.height = height
        self.board = [[[0, 0]] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30
        self.level_map = load_level(level_map)
        self.pos_b = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        #level = load_level(self.level_map)
        x, y = self.left, self.top
        for n in range(self.height):
            for m in range(self.width):
                Tile('grass', m, n)
                self.board[n][m] = [x, y]
                x += self.cell_size
            y += self.cell_size
            x = self.left

    def get_cell(self, mouse_pos):
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        for row in self.board:
            for cell in row:
                if mouse_x > cell[0] and mouse_x < cell[0] + self.cell_size:
                    if mouse_y > cell[1] and mouse_y < cell[1] + self.cell_size:
                        return self.board.index(row), cell

    def on_click(self, cell_coords):
        pass 

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def move_camera(self):
        with open('data/levels/' + self.level_map, 'r+') as map_file:
            lines = [list(line.strip()) for line in map_file]
            for m in range(len(lines)):
                lines[m][self.pos_b - 1], lines[m][self.pos_b] = lines[m][self.pos_b], lines[m][0]
            self.pos_b -= 1
            if self.pos_b == 0:
                self.pos_b = 30
        with open('data/levels/' + self.level_map, 'w+') as map_file:
            for m in lines:
                map_file.write(''.join(m))
                map_file.write('\n')           


class BuildWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((400, 85))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Построить курятник - 10000₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('Построить крольчатник - 50000₽', True,
                  (180, 0, 0))
        self.image.blit(text2, (30, 30))
        text3 = font.render('Выкопать озеро для уток - 100000₽', True,
                  (180, 0, 0))
        self.image.blit(text3, (30, 50))
        text4 = font.render('U', True,
                  (180, 0, 0))
        self.image.blit(text4, (350, 10))
        text5 = font.render('R', True,
                  (180, 0, 0))
        self.image.blit(text5, (350, 30))
        text6 = font.render('L', True,
                  (180, 0, 0))
        self.image.blit(text6, (350, 50))


class ChickenShopWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((270, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Купить курицу - 500₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('I', True,
                  (180, 0, 0))
        self.image.blit(text2, (220, 10))


class RabbitShopWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((270, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Купить кролика - 1000₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('I', True,
                  (180, 0, 0))
        self.image.blit(text2, (220, 10))


class DuckShopWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((270, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Купить утку - 600₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('I', True,
                  (180, 0, 0))
        self.image.blit(text2, (220, 10))


class WheatSeedWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((400, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Купить смена пшеницы 5шт - 2000₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('I', True,
                  (180, 0, 0))
        self.image.blit(text2, (350, 10))


class CornSeedWindow(pg.sprite.Sprite):
    def __init__(self, x=240, y=210):
        super().__init__(window_group, all_sprites)
        self.image = pg.Surface((400, 50))
        self.rect = self.image.get_rect().move(x, y)
        self.image.fill((156, 209, 10))
        pg.font.init()

    def update(self):
        self.image.fill((156, 209, 10))
        font = pg.font.SysFont('serif', 18)
        text1 = font.render('Купить смена кукурузы 5шт - 3000₽', True,
                  (180, 0, 0))
        self.image.blit(text1, (30, 10))
        text2 = font.render('I', True,
                  (180, 0, 0))
        self.image.blit(text2, (350, 10))


class StartDisplay(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(displays_group, all_sprites)
        self.image = tile_images['start_display']
        self.rect = self.image.get_rect().move(0, 0)


class FinishDisplay(pg.sprite.Sprite):
    def __init__(self):
        super().__init__(displays_group, all_sprites)
        self.image = tile_images['finish_display']
        self.rect = self.image.get_rect().move(0, 0)


def start_game():
    global wheat_count
    global corn_count
    global corn_seed_count
    global wheat_seed_count
    global egg_count
    global rabbit_skin_count
    global duck_egg_count
    global is_chicken_coop
    global is_rabbit_house
    global is_lake
    global is_build_window
    global is_home_window
    global money_count
    global is_chicken_window
    global chicken_count
    global is_duck_window
    global is_rabbit_window
    global is_wheat_seed_window
    global is_corn_seed_window
    global rabbit_count
    global duck_count
    global is_start_display
    if is_start_display:
        StartDisplay()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate() 
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        running = False
                        is_start_display = False
            displays_group.draw(screen)
            pg.display.flip()
            clock.tick(FPS)

    if not is_start_display:
        Home(-15, -25)
        Car(10, 120)
        Garage(150, 10)
        Barn(285, -5)
        wheat1 = Wheat(0, 170)
        wheat2 = Wheat(63, 170)
        corn1 = Corn(0, 310)
        corn2 = Corn(60, 310)
        CornShop(630, -5)
        WheatShop(730, -6)
        AutoShop(805, 115)
        ChickenShop(809, 240)
        RabbitShop(809, 340)
        DuckShop(809, 440)
        Tractor(580, 450)
        build_window = BuildWindow(700, 700)
        home_window = HomeWindow(700, 700)
        chicken_window = ChickenShopWindow(700, 700)
        rabbit_window = RabbitShopWindow(700, 700)
        duck_window = DuckShopWindow(700, 700)
        wheat_seed_window = WheatSeedWindow(700, 700)
        corn_seed_window = CornSeedWindow(700, 700)


        trees = [Tree(300, 444), Tree(325, 444), Tree(350, 444), Tree(375, 444), Tree(400, 444), Tree(425, 444), Tree(450, 444), Tree(475, 444), Tree(500, 444), Tree(525, 444),
                Tree(290, 476), Tree(315, 476), Tree(340, 476), Tree(365, 476), Tree(390, 476), Tree(415, 476), Tree(440, 476), Tree(465, 476), Tree(490, 476), Tree(515, 476), Tree(540, 476),
                Tree(300, 508), Tree(325, 508), Tree(350, 508), Tree(375, 508), Tree(400, 508), Tree(425, 508), Tree(450, 508), Tree(475, 508), Tree(500, 508), Tree(525, 508),
                Tree(290, 540), Tree(315, 540), Tree(340, 540), Tree(365, 540), Tree(390, 540), Tree(415, 540), Tree(440, 540), Tree(465, 540), Tree(490, 540), Tree(515, 540), Tree(540, 540)]
        
        oaks = [Oak(10, 440), Oak(40, 440), Oak(70, 440), Oak(100, 440), Oak(130, 440), Oak(160, 440), Oak(190, 440), Oak(220, 440), Oak(248, 440),
                Oak(10, 470), Oak(40, 470), Oak(70, 470), Oak(100, 470), Oak(130, 470), Oak(160, 470), Oak(190, 470), Oak(220, 470), Oak(248, 470),
                Oak(10, 500), Oak(40, 500), Oak(70, 500), Oak(100, 500), Oak(130, 500), Oak(160, 500), Oak(190, 500), Oak(220, 500), Oak(248, 500),
                Oak(10, 530), Oak(40, 530), Oak(70, 530), Oak(100, 530), Oak(130, 530), Oak(160, 530), Oak(190, 530), Oak(220, 530), Oak(248, 530)]

        chicken_coords = [(390, 90), (405, 90), (390, 105), (405, 105), (420, 90), (435, 90), (420, 105), (435, 105),
                        (450, 90), (465, 90), (450, 105), (465, 105), (480, 90), (495, 90), (480, 105), (495, 105)]

        rabbit_coords = [(510, 90), (525, 90), (510, 105), (525, 105), (540, 90), (555, 90), (540, 105), (555, 105),
                        (570, 90), (585, 90), (570, 105), (585, 105), (600, 90), (615, 90), (600, 105), (615, 105)]

        duck_coords = [(625, 505), (650, 505), (675, 505), (625, 530), (650, 530),
                    (675, 530), (625, 555), (650, 555), (675, 555)]

        chickens = []
        rabbits = []
        ducks = []
        board = Board(30, 20, 'map.txt')
        board.render()
        
        while True:
            if money_count >= 1000000:
                break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    terminate()   
                if event.type == pg.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)   
                    board.render()  
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        board.move_camera() 
                        board.render() 
                    elif event.key == pg.K_b:
                        build_window.rect = build_window.image.get_rect().move(240, 210)
                        is_build_window = True
                    elif event.key == pg.K_h:
                        home_window.rect = home_window.image.get_rect().move(240, 210)
                        is_home_window = True
                    elif event.key == pg.K_c and not is_chicken_window:
                        chicken_window.rect = chicken_window.image.get_rect().move(240, 210)
                        is_chicken_window = True        
                    elif event.key == pg.K_o and not is_rabbit_window:
                        rabbit_window.rect = rabbit_window.image.get_rect().move(240, 210)
                        is_rabbit_window = True    
                    elif event.key == pg.K_p and not is_duck_window:
                        duck_window.rect = duck_window.image.get_rect().move(240, 210)
                        is_duck_window = True      
                    elif event.key == pg.K_w and not is_wheat_seed_window:
                        wheat_seed_window.rect = wheat_seed_window.image.get_rect().move(240, 210)
                        is_wheat_seed_window = True      
                    elif event.key == pg.K_t and not is_wheat_seed_window:
                        corn_seed_window.rect = corn_seed_window.image.get_rect().move(240, 210)
                        is_corn_seed_window = True                               
                    elif event.key == pg.K_q:
                        build_window.rect = build_window.image.get_rect().move(700, 700)
                        home_window.rect = home_window.image.get_rect().move(700, 700)
                        chicken_window.rect = chicken_window.image.get_rect().move(700, 700)
                        rabbit_window.rect = rabbit_window.image.get_rect().move(700, 700)
                        duck_window.rect = duck_window.image.get_rect().move(700, 700)
                        wheat_seed_window.rect = wheat_seed_window.image.get_rect().move(700, 700)
                        corn_seed_window.rect = corn_seed_window.image.get_rect().move(700, 700)
                        is_corn_seed_window = False  
                        is_build_window = False
                        is_home_window = False
                        is_chicken_window = False
                        is_rabbit_window = False
                        is_duck_window = False
                        is_wheat_seed_window = False
                    elif event.key == pg.K_F1 and is_home_window:
                        money_count += wheat_count * 100
                        wheat_count = 0
                    elif event.key == pg.K_F2 and is_home_window:
                        money_count += corn_count * 120
                        corn_count = 0
                    elif event.key == pg.K_F3 and is_home_window:
                        money_count += egg_count * 30
                        egg_count = 0
                    elif event.key == pg.K_F4 and is_home_window:
                        money_count += rabbit_skin_count * 60
                        rabbit_skin_count = 0
                    elif event.key == pg.K_F5 and is_home_window:
                        money_count += duck_egg_count * 40
                        duck_egg_count = 0       
                    elif event.key == pg.K_u:
                        if not is_chicken_coop and is_build_window and money_count >= 10000:
                            is_chicken_coop = True
                            ChickenCoop(390, 0)
                            money_count -= 10000
                    elif event.key == pg.K_r and is_build_window:
                        if not is_rabbit_house and money_count >= 50000:
                            is_rabbit_house = True
                            RabbitHouse(510, -16)
                            money_count -= 50000
                    elif event.key == pg.K_l and is_build_window:
                        if not is_lake and money_count >= 100000:
                            is_lake = True   
                            Lake(600, 490)
                            money_count -= 100000  
                    elif event.key == pg.K_i and is_chicken_window and is_chicken_coop:
                        if chicken_count < 16 and money_count >= 500:
                            chickens.append(Chicken(*chicken_coords[chicken_count]))     
                            chicken_count += 1  
                            money_count -= 500
                    elif event.key == pg.K_i and is_rabbit_window and is_rabbit_house:
                        if rabbit_count < 16 and money_count >= 1000:
                            rabbits.append(Rabbit(*rabbit_coords[rabbit_count]))     
                            rabbit_count += 1  
                            money_count -= 1000
                    elif event.key == pg.K_i and is_duck_window and is_lake:
                        if duck_count < 9 and money_count >= 600:
                            ducks.append(Duck(*duck_coords[duck_count]))     
                            duck_count += 1  
                            money_count -= 600    
                    elif event.key == pg.K_i and is_wheat_seed_window:
                        if money_count >= 2000:
                            wheat_seed_count += 5
                            money_count -= 2000  
                    elif event.key == pg.K_i and is_corn_seed_window:
                        if money_count >= 3000:
                            corn_seed_count += 5
                            money_count -= 3000   
                if event.type == wheat1.WHEAT and wheat_count != 500 and wheat_seed_count > 0:
                    wheat_count += 10
                    wheat_seed_count -= 1
                if event.type == corn1.CORN and corn_count != 300 and corn_seed_count > 0:
                    corn_count += 5
                    corn_seed_count -= 1
                for chicken in chickens:
                    if event.type == chicken.CHICKEN and egg_count != 200:
                        egg_count += 1
                for rabbit in rabbits:
                    if event.type == rabbit.RABBIT and rabbit_skin_count != 200:
                        rabbit_skin_count += 1
                for duck in ducks:
                    if event.type == duck.DUCK and duck_egg_count != 200:
                        duck_egg_count += 1
                        
            tiles_group.draw(screen)
            buildings_group.draw(screen)
            plants_group.draw(screen)
            tree_group.draw(screen)
            car_group.draw(screen)
            car_group.update()
            animal_group.draw(screen)
            animal_group.update()
            window_group.draw(screen)
            window_group.update()
            pg.display.flip()
            clock.tick(FPS)

    FinishDisplay()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate() 
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
                    is_start_display = False
        displays_group.draw(screen)
        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    start_game()