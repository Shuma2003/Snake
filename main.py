import pygame
import time
import random

pygame.init()

# Цвета
white = (255, 255, 255)
yellow = (255, 255, 22)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Размеры окна
dis_width = 800
dis_height = 600

# Инициализация окна
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка!!')

# Частота обновления экрана
clock = pygame.time.Clock()

# Параметры змейки
snake_block = 10
snake_speed = 15

# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Функция для отображения счёта
def Your_score(score):
    value = score_font.render("Ваш счёт: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Функция для отрисовки змейки
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

# Функция для отображения сообщений
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

# Функция для отображения здоровья
def display_health(health):
    font = pygame.font.Font(None, 30)
    text = font.render("Здоровье: " + str(health), True, white)
    dis.blit(text, (dis_width - 150, 80))

# Функция для отображения попыток
def display_attempts(attempts):
    font = pygame.font.Font(None, 30)
    text = font.render("Попытки: " + str(attempts), True, white)
    dis.blit(text, (dis_width - 150, 30))

# Начальный экран
def start_screen():
    start = True
    while start:
        dis.fill(blue)
        message("Добро пожаловать в игру!", white)
        pygame.draw.rect(dis, green, [dis_width / 3, dis_height / 2, 100, 50])
        pygame.draw.rect(dis, red, [dis_width / 3 * 2, dis_height / 2, 100, 50])
        
        play_text = font_style.render("Играть", True, black)
        exit_text = font_style.render("Выход", True, black)
        
        dis.blit(play_text, [dis_width / 3 + 10, dis_height / 2 + 10])
        dis.blit(exit_text, [dis_width / 3 * 2 + 10, dis_height / 2 + 10])
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if dis_width / 3 <= mouse_pos[0] <= dis_width / 3 + 100 and dis_height / 2 <= mouse_pos[1] <= dis_height / 2 + 50:
                    start = False
                if dis_width / 3 * 2 <= mouse_pos[0] <= dis_width / 3 * 2 + 100 and dis_height / 2 <= mouse_pos[1] <= dis_height / 2 + 50:
                    pygame.quit()
                    quit()

# Основной игровой цикл
def gameLoop():
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Изменение координат змейки
    x1_change = 0
    y1_change = 0

    # Список сегментов змейки
    snake_List = []
    Length_of_snake = 1

    # Начальные координаты еды
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Здоровье и попытки
    health = 100
    attempts = 3

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message("Вы проиграли! Нажмите Q для выхода или C для повторной игры", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Проверка на столкновение со стенами
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            health -= 25  # Уменьшаем здоровье при столкновении
            if health <= 0:
                attempts -= 1  # Уменьшаем количество попыток
                if attempts == 0:
                    game_close = True  # Игра окончена
                else:
                    health = 100  # Восстанавливаем здоровье
                    x1 = dis_width / 2  # Возвращаем змейку в центр
                    y1 = dis_height / 2
                    time.sleep(1)  # Небольшая пауза перед новой попыткой

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])  # Рисуем еду
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # Проверка на столкновение с самой собой
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)  # Рисуем змейку
        Your_score(Length_of_snake - 1)  # Отображаем счёт
        display_health(health)  # Отображаем здоровье
        display_attempts(attempts)  # Отображаем попытки
        pygame.display.update()

        # Проверка на съедание еды
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

start_screen()
gameLoop()
