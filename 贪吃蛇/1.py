import pygame
import time
import random
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound module

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

# Game window
DISPLAY = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Enhanced Snake Game 3A Edition by David Yang')

clock = pygame.time.Clock()

# Fonts
SCORE_FONT = pygame.font.SysFont("comicsansms", 35)
MESSAGE_FONT = pygame.font.SysFont("bahnschrift", 25)

# Load images with absolute path
BASE_PATH = "H:/贪吃蛇/"
SNAKE_HEAD_UP = pygame.image.load(BASE_PATH + "snake.png")
SNAKE_HEAD_DOWN = pygame.image.load(BASE_PATH + "down.png")
SNAKE_HEAD_LEFT = pygame.image.load(BASE_PATH + "left.png")
SNAKE_HEAD_RIGHT = pygame.image.load(BASE_PATH + "right.png")
BODY_IMAGE = pygame.image.load(BASE_PATH + "body.png")
FOOD_IMAGE = pygame.image.load(BASE_PATH + "food.png")
SHIELD_IMAGE = pygame.image.load(BASE_PATH + "shield.png")  # 新增护盾道具图片
SPEED_IMAGE = pygame.image.load(BASE_PATH + "speed.png")   # 新增加速道具图片

# Load sounds (需要你准备音频文件)
EAT_SOUND = pygame.mixer.Sound(BASE_PATH + "eat.wav")
HIT_SOUND = pygame.mixer.Sound(BASE_PATH + "hit.wav")
pygame.mixer.music.load(BASE_PATH + "background.mp3")  # 背景音乐
pygame.mixer.music.play(-1)  # 循环播放

# Difficulty levels (speed, food points)
DIFFICULTIES = {
    "Easy": (15, 1),
    "Medium": (20, 2),
    "Hard": (25, 3)
}

# Prop types
PROPS = {
    "shield": {"image": SHIELD_IMAGE, "effect": "protect", "duration": 5},
    "speed": {"image": SPEED_IMAGE, "effect": "speed_up", "duration": 3}
}

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

def draw_prop(prop_pos, prop_type):
    DISPLAY.blit(PROPS[prop_type]["image"], (prop_pos[0], prop_pos[1]))

def show_message(msg, color, y_offset=0):
    msg_surface = MESSAGE_FONT.render(msg, True, color)
    DISPLAY.blit(msg_surface, [DIS_WIDTH / 6, DIS_HEIGHT / 3 + y_offset])

def show_score(score):
    score_text = SCORE_FONT.render(f"Score: {score}", True, WHITE)
    DISPLAY.blit(score_text, [0, 0])

def main_menu():
    while True:
        DISPLAY.fill(BLUE)
        show_message("Snake Game 3A Edition", WHITE, -50)
        show_message("1. Start Game", WHITE, 0)
        show_message("2. Survival Mode", WHITE, 40)
        show_message("3. Quit", WHITE, 80)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "game"
                elif event.key == pygame.K_2:
                    return "survival"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    quit()

def choose_difficulty():
    while True:
        DISPLAY.fill(BLUE)
        show_message("Choose difficulty:", WHITE)
        for i, (diff_name, _) in enumerate(DIFFICULTIES.items()):
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

def spawn_prop():
    prop_type = random.choice(list(PROPS.keys()))
    return ([random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
             random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)], prop_type, time.time())

def game_loop(mode="game"):
    speed, food_points = choose_difficulty()
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_length = 1
    shield_active = False
    speed_boost = False
    boost_end_time = 0

    food_pos = [random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]
    prop = None  # (pos, type, spawn_time)

    obstacles = []  # 障碍物
    if mode == "survival":
        for _ in range(5):
            obstacles.append([random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                              random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)])

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
                        game_loop(mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_p:  # Pause
                    paused = True
                    while paused:
                        show_message("Paused - Press P to Resume", WHITE)
                        pygame.display.update()
                        for pause_event in pygame.event.get():
                            if pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                                paused = False

        # Apply speed boost
        current_time = time.time()
        if speed_boost and current_time > boost_end_time:
            speed_boost = False
            speed /= 2  # Reset speed

        # Move snake
        x1 += x1_change
        y1 += y1_change

        # Check boundaries
        if x1 >= DIS_WIDTH or x1 < 0 or y1 >= DIS_HEIGHT or y1 < 0:
            if not shield_active:
                HIT_SOUND.play()
                game_close = True
            else:
                x1 = max(0, min(x1, DIS_WIDTH - BLOCK_SIZE))
                y1 = max(0, min(y1, DIS_HEIGHT - BLOCK_SIZE))

        DISPLAY.fill(BLUE)
        draw_food(food_pos)
        if prop:
            draw_prop(prop[0], prop[1])

        # Draw obstacles in survival mode
        if mode == "survival":
            for obs in obstacles:
                pygame.draw.rect(DISPLAY, RED, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Collision with self
        for segment in snake_list[:-1]:
            if segment == snake_head and not shield_active:
                HIT_SOUND.play()
                game_close = True

        # Collision with obstacles
        if mode == "survival" and snake_head in obstacles and not shield_active:
            HIT_SOUND.play()
            game_close = True

        draw_snake(BLOCK_SIZE, snake_list, x1_change, y1_change)
        show_score(snake_length - 1)
        pygame.display.update()

        # Food collision
        if x1 == food_pos[0] and y1 == food_pos[1]:
            EAT_SOUND.play()
            food_pos = [random.randrange(0, DIS_WIDTH - BLOCK_SIZE, BLOCK_SIZE),
                        random.randrange(0, DIS_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]
            snake_length += food_points
            if random.random() < 0.3 and not prop:  # 30% chance to spawn a prop
                prop = spawn_prop()

        # Prop collision
        if prop and x1 == prop[0][0] and y1 == prop[0][1]:
            prop_effect = PROPS[prop[1]]["effect"]
            if prop_effect == "protect":
                shield_active = True
                pygame.time.set_timer(pygame.USEREVENT, int(PROPS["shield"]["duration"] * 1000))
            elif prop_effect == "speed_up":
                speed_boost = True
                boost_end_time = current_time + PROPS["speed"]["duration"]
                speed *= 2
            prop = None

        # Shield timer
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                shield_active = False

        clock.tick(speed)

    pygame.quit()
    quit()

# Start the game
mode = main_menu()
if mode == "game":
    game_loop("game")
elif mode == "survival":
    game_loop("survival")