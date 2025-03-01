import pygame
import time
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Constants
DIS_WIDTH = 800
DIS_HEIGHT = 600
BLOCK_SIZE = 20

# Difficulty levels (speed, food points)
DIFFICULTIES = {
    "Easy": (15, 1),
    "Medium": (20, 2),
    "Hard": (25, 3)
}

# Game window
DISPLAY = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Enhanced Snake Game with Bounce by David Yang')

clock = pygame.time.Clock()

# Fonts
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
MESSAGE_FONT = pygame.font.SysFont("bahnschrift", 25)

# Load images
BASE_PATH = "H:/贪吃蛇/"
SNAKE_HEAD_UP = pygame.image.load(BASE_PATH + "snake.png")
SNAKE_HEAD_DOWN = pygame.image.load(BASE_PATH + "down.png")
SNAKE_HEAD_LEFT = pygame.image.load(BASE_PATH + "left.png")
SNAKE_HEAD_RIGHT = pygame.image.load(BASE_PATH + "right.png")
BODY_IMAGE = pygame.image.load(BASE_PATH + "body.png")
FOOD_IMAGE = pygame.image.load(BASE_PATH + "food.png")

def get_head_image(x_change, y_change):
    if x_change < 0:
        return SNAKE_HEAD_LEFT
    elif x_change > 0:
        return SNAKE_HEAD_RIGHT
    elif y_change < 0:
        return SNAKE_HEAD_UP
    elif y_change > 0:
        return SNAKE_HEAD_DOWN
    return SNAKE_HEAD_RIGHT

def draw_snake(snake_block, snake_list, x_change, y_change):
    for i, pos in enumerate(snake_list):
        if i == len(snake_list) - 1:
            head_image = get_head_image(x_change, y_change)
            DISPLAY.blit(head_image, (pos[0], pos[1]))
        else:
            DISPLAY.blit(BODY_IMAGE, (pos[0], pos[1]))

def draw_food(food_pos):
    DISPLAY.blit(FOOD_IMAGE, (food_pos[0], food_pos[1]))

def show_message(msg, color, y_offset=0):
    msg_surface = MESSAGE_FONT.render(msg, True, color)
    DISPLAY.blit(msg_surface, [DIS_WIDTH / 6, DIS_HEIGHT / 3 + y_offset])

def show_score(score):
    score_text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    DISPLAY.blit(score_text, [0, 0])

def show_cheat_status(speed, food_points, bounce_mode):
    status_text = SCORE_FONT.render(f"Speed: {speed} Food: {food_points} Bounce: {bounce_mode}", True, YELLOW)
    DISPLAY.blit(status_text, [0, 40])

def choose_difficulty():
    while True:
        DISPLAY.fill(BLUE)
        show_message("Choose difficulty:", WHITE)
        for i, (diff_name, (_, _)) in enumerate(DIFFICULTIES.items()):
            text = SCORE_FONT.render(f"{i+1}. {diff_name}", True, WHITE)
            DISPLAY.blit(text, [DIS_WIDTH / 6, DIS_HEIGHT / 3 + 40 * (i+1)])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return DIFFICULTIES["Easy"]
                elif event.key == pygame.K_2:
                    return DIFFICULTIES["Medium"]
                elif event.key == pygame.K_3:
                    return DIFFICULTIES["Hard"]

def game_loop():
    speed, food_points = choose_difficulty()
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1
    bounce_mode = False  # 反弹模式开关

    food_pos = [random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]

    while not game_over:
        while game_close:
            DISPLAY.fill(BLUE)
            show_message("You Lost! Press Q-Quit or C-Play Again", RED)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # 方向控制
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0
                # 作弊功能
                elif event.key == pygame.K_s:  # 按 S 减慢速度
                    speed = max(5, speed - 5)
                elif event.key == pygame.K_f:  # 按 F 增加食物得分
                    food_points += 1
                elif event.key == pygame.K_l:  # 按 L 增加长度
                    snake_length += 5
                elif event.key == pygame.K_i:  # 按 I 切换反弹模式
                    bounce_mode = not bounce_mode

        # 边界处理（反弹模式）
        if x1 >= DIS_WIDTH:
            if bounce_mode:
                x1 = DIS_WIDTH - BLOCK_SIZE
                x1_change = -x1_change  # 反转方向
            else:
                game_close = True
        elif x1 < 0:
            if bounce_mode:
                x1 = 0
                x1_change = -x1_change
            else:
                game_close = True
        elif y1 >= DIS_HEIGHT:
            if bounce_mode:
                y1 = DIS_HEIGHT - BLOCK_SIZE
                y1_change = -y1_change
            else:
                game_close = True
        elif y1 < 0:
            if bounce_mode:
                y1 = 0
                y1_change = -y1_change
            else:
                game_close = True
        else:
            x1 += x1_change
            y1 += y1_change

        DISPLAY.fill(BLUE)
        draw_food(food_pos)
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # 自撞检测（反弹模式不影响自撞）
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list, x1_change, y1_change)
        show_score(snake_length - 1)
        show_cheat_status(speed, food_points, bounce_mode)  # 显示反弹状态
        pygame.display.update()

        if x1 == food_pos[0] and y1 == food_pos[1]:
            food_pos = [random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                        random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]
            snake_length += food_points

        clock.tick(speed)

    pygame.quit()
    quit()

# Start the game
game_loop()