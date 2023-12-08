import pygame
import random
import sqlite3
import time
import pygame_menu
from pygame_menu import themes

# игра
pygame.init()  # Инициализация pygame

# Задаем размеры окна
WIDTH = 800
HEIGHT = 600

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космическая игра")

# Загрузка изображений
spaceship_img = pygame.image.load("spaceship.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
meteor_img = pygame.image.load("meteor.png")
boss_img = pygame.image.load("boss.png")
bullet_enemy = pygame.image.load("bullet_enemy.png")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Зададим размеры объектов
player_widht = 64
player_height = 64
enemy_widht = 64
enemy_height = 64
bullet_widht = 32
bullet_height = 32
boss_widht = 100
boss_height = 100
meteor_widht = 32
meteor_height = 32

scale = [player_widht / spaceship_img.get_size()[0], player_height / spaceship_img.get_size()[1]]
player_img = pygame.transform.scale(spaceship_img,
                                    (spaceship_img.get_size()[0] * scale[0], spaceship_img.get_size()[1] * scale[1]))

scale_enum = [enemy_widht / enemy_img.get_size()[0], enemy_height / enemy_img.get_size()[1]]
enemy_img = pygame.transform.scale(enemy_img, (enemy_img.get_size()[0] * scale[0], enemy_img.get_size()[1] * scale[1]))

scale_bullet = [bullet_widht / bullet_img.get_size()[0], bullet_height / bullet_img.get_size()[1]]
bullet_img = pygame.transform.scale(bullet_img,
                                    (bullet_img.get_size()[0] * scale[0], bullet_img.get_size()[1] * scale[1]))

scale_meteor = [meteor_widht / meteor_img.get_size()[0], meteor_height / meteor_img.get_size()[1]]
meteor_img = pygame.transform.scale(meteor_img,
                                    (meteor_img.get_size()[0] * scale[0], meteor_img.get_size()[1] * scale[1]))

scale_boss = [boss_widht / boss_img.get_size()[0], boss_height / boss_img.get_size()[1]]
boss_img = pygame.transform.scale(boss_img,
                                  (boss_img.get_size()[0] * scale[0], boss_img.get_size()[1] * scale[1]))

scale_bullet_enemy = [bullet_widht / bullet_enemy.get_size()[0], bullet_height / bullet_enemy.get_size()[1]]
bullet_enemy = pygame.transform.scale(bullet_enemy,
                                      (bullet_enemy.get_size()[0] * scale[0], bullet_enemy.get_size()[1] * scale[1]))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - enemy_widht)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - enemy_widht)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        enemy_bullets.add(bullet)
        all_sprites.add(bullet)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 4)

    def update(self):
        self.rect.y += self.speed_y

        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 4)


# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y = -5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_enemy
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y = 3

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed_x = random.randint(-2, 2)
        self.speed_y = random.randint(1, 2)
        self.bullets = pygame.sprite.Group()
        self.shoot_delay = 3000
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x = -self.speed_x

        if self.rect.top > HEIGHT:
            self.rect.y = -self.rect.height
            self.speed_x = random.randint(-3, 3)
            self.speed_y = random.randint(1, 3)

        self.shoot()

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_shot_time > self.shoot_delay:
            bullet1 = Bullet1(self.rect.centerx, self.rect.bottom)
            self.bullets.add(bullet1)
            all_sprites.add(bullet1)
            self.last_shot_time = time_now


# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bulletss = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bosss = pygame.sprite.Group()


def play_music():
    # музыка
    pygame.mixer.init()
    pygame.mixer.music.load('space_music.mp3')
    pygame.mixer.music.play(-1)


def pause_music():
    pygame.mixer.music.pause()


def unpause_music():
    pygame.mixer.music.unpause()


data_base = sqlite3.connect('data_base.db')
cur = data_base.cursor()
cur.execute(
    """CREATE TABLE IF NOT EXISTS Users (user_name TEXT,levels INTEGER, score INTEGER, hp INTEGER);""")
data_base.commit()
cur.close()
data_base.close()


def Game(player_name):
    # Создание игрока
    player = Player(WIDTH // 2 - player_widht // 2, HEIGHT - player_height - 10)
    all_sprites.add(player)

    for _ in range(10):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Уровень игры
    level = 1
    score = 0
    hp = 100
    font = pygame.font.Font(None, 36)

    # Флаги игровых состояний
    game_over = False
    game_win = False

    # Основной игровой цикл
    running = True
    paused = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pause_music()
                elif event.key == pygame.K_w:
                    unpause_music()
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                    if not paused:
                        screen.fill(BLACK)
                    else:
                        draw_text(screen, "ПАУЗА", 64, WIDTH / 2, HEIGHT / 2)
                    pygame.display.flip()
                elif event.key == pygame.K_LEFT:
                    player.speed_x = -5
                elif event.key == pygame.K_RIGHT:
                    player.speed_x = 5
                elif event.key == pygame.K_SPACE:
                    player.shoot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.speed_x = 0
        if paused:
            continue

        all_sprites.update()

        # Проверка столкновений игрока с врагами
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if len(hits) > 0:
            hp -= 20
            if hp <= 0:
                game_over = True

        # Проверка столкновений игрока с метеоритами
        hits = pygame.sprite.spritecollide(player, meteors, True)
        if len(hits) > 0:
            hp -= 10
            if hp <= 0:
                game_over = True

        # Проверка столкновений пуль с врагами
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            score += 10

        # Проверка столкновений пуль врага с кораблем
        hits = pygame.sprite.groupcollide(bulletss, player, True, True)
        for hit in hits:
            bullets1 = Bullet1()
            all_sprites.add(bullets1)
            enemies.add(bullets1)
            hp -= 10

        # Проверка столкновения врaжеского босса с кораблем
        hits = pygame.sprite.spritecollide(player, bosss, True)
        if len(hits) > 0:
            hp -= 20
            if hp <= 0:
                game_over = True

        # Проверка столкновений игрока с вражескими кораблями
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if len(hits) > 0:
            game_over = True

        # Проверка условий для перехода на следующий уровень
        if score >= level * 300:
            level += 1
            if level == 1:
                for _ in range(level + 5):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif level == 2:
                for _ in range(level + 7):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif level == 3:
                for _ in range(level + 7):
                    enemy = Enemy()
                    meteor = Meteor()
                    all_sprites.add(enemy)
                    all_sprites.add(meteor)
                    enemies.add(enemy)
                    meteors.add(meteor)
            if level == 4:
                for _ in range(level + 7):
                    enemy = Enemy()
                    boss = Boss()
                    all_sprites.add(boss)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                    bosss.add(boss)

        # Проверка условий победы игрока
        if level >= 5:
            game_win = True

        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Отображение уровня, счета, здоровья
        level_text = font.render("Level: " + str(level), True, WHITE)
        screen.blit(level_text, (10, 10))
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 40))
        score_hp = font.render("HP: " + str(hp), True, WHITE)
        screen.blit(score_hp, (10, 70))

        # Отображение текста при окончании игры
        if game_over:

            mass_list = []
            mass_list.append(player_name)
            mass_list.append(level)
            mass_list.append(score)
            mass_list.append(hp)

            data_base = sqlite3.connect('data_base.db')
            cur = data_base.cursor()
            cur.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", mass_list)
            data_base.commit()
            cur.close()
            data_base.close()
            mass_list.clear()

            screen.fill(BLACK)
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 75, HEIGHT // 2 - 18))
            pygame.display.flip()
            time.sleep(3)
            main()

        elif game_win:
            mass_list = []
            mass_list.append(player_name)
            mass_list.append(level)
            mass_list.append(score)
            mass_list.append(hp)

            data_base = sqlite3.connect('data_base.db')
            cur = data_base.cursor()
            cur.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", mass_list)
            data_base.commit()
            cur.close()
            data_base.close()
            mass_list.clear()

            screen.fill(BLACK)
            game_win_text = font.render("You Win!", True, RED)
            screen.blit(game_win_text, (WIDTH // 2 - 63, HEIGHT // 2 - 18))
            pygame.display.flip()
            time.sleep(3)
            main()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont(None, size)
    text_obj = font.render(text, True, (255, 255, 255))
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)


class Menu:
    def __init__(self):
        self.data = ''
        self.player_game = ''
        self.mainmenu = pygame_menu.Menu('Главное меню', 800, 600, theme=themes.THEME_SOLARIZED)
        self.mainmenu.add.text_input('Имя: ', default='Имя', onchange=self.save_name)
        self.mainmenu.add.button('Начать игру', self.progress)
        self.mainmenu.add.button("Управление", self.informations)
        self.mainmenu.add.button("Рекорды", self.recording_draw)
        self.mainmenu.add.button('Закрыть игру', pygame_menu.events.EXIT)

        self.loading = pygame_menu.Menu('Загрузка игры...', 800, 600, theme=themes.THEME_DARK)
        self.loading.add.progress_bar("Прогресс", progressbar_id="1", default=0, width=200)

        self.arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

        self.update_loading = pygame.USEREVENT + 0
        self.menu_type = 0

    def save_name(self, name):
        self.player_game = name

    def game_menu_run(self):
        clock = pygame.time.Clock()

        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == self.update_loading:
                    progress = self.loading.get_widget("1")
                    progress.set_value(progress.get_value() + 1)
                    if progress.get_value() == 100:
                        pygame.time.set_timer(self.update_loading, 0)
                if event.type == pygame.QUIT:
                    exit()

            if self.mainmenu.is_enabled():
                if self.menu_type == 0:
                    self.mainmenu.update(events)
                    self.mainmenu.draw(screen)
                    if (self.mainmenu.get_current().get_selected_widget()):
                        self.arrow.draw(screen, self.mainmenu.get_current().get_selected_widget())
                elif self.menu_type == 1:
                    self.information_page_draw(events)
                elif self.menu_type == 2:
                    self.recording(events)

            pygame.display.update()
            clock.tick(60)

    def blit_text(self, surface, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]
                    y += word_height
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    def information_page_draw(self, events):

        file_object = open("information", "r")
        data = file_object.read()
        file_object.close()

        font = pygame.font.SysFont('freesansbold.ttf', 32)
        screen.fill(WHITE)
        button_rect = pygame.Rect(200, 200, 300, 100)
        button_text = "Вернуться назад в меню"

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        self.menu_type = 0

        pygame.draw.rect(screen, BLACK, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 2)

        # Отрисовка текста на кнопке
        font = pygame.font.Font(None, 20)
        text = font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        self.blit_text(screen, data, (40, 40), font)

        pygame.display.flip()

    def recording(self, events):
        screen.fill(WHITE)
        data_base = sqlite3.connect('data_base.db')
        cur = data_base.cursor()

        cur.execute("SELECT * FROM Users ORDER BY score")
        cur.execute("SELECT * FROM Users LIMIT 5")

        button_rect = pygame.Rect(400, 200, 200, 50)
        button_text = "Вернуться назад в меню"

        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        self.menu_type = 0

        pygame.draw.rect(screen, BLACK, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 2)

        font = pygame.font.Font(None, 20)
        text = font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

        data = cur.fetchall()
        row_height = 50
        for i, row in enumerate(data):
            text = f"Имя: {row[0]}, Уровень: {row[1]}, Cчет: {row[2]}"
            font = pygame.font.SysFont(None, 24)
            text_obj = font.render(text, True, (BLACK))
            screen.blit(text_obj, (10, i * row_height + 10))

        cur.close()
        data_base.close()

        pygame.display.flip()

    def recording_draw(self):
        self.menu_type = 2

    def progress(self):
        self.mainmenu._open(self.loading)
        pygame.time.set_timer(self.update_loading, 30)
        self.start_the_game()

    def start_the_game(self):
        Game(self.player_game)

    def informations(self):
        pygame.display.flip()
        self.menu_type = 1


def main():
    # play_music()
    menu = Menu()
    menu.game_menu_run()


if __name__ == "__main__":
    main()
    pygame.quit()
