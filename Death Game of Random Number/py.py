import pygame
import random
import os
import math
from datetime import datetime, timedelta
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)  # Remove window decorations
pygame.display.set_caption("The Devil's Game")
clock = pygame.time.Clock()

# Configure paths
SOUNDS_DIR = os.path.join("Death Game of Random Number", "sounds")
BG_MUSIC = os.path.join(SOUNDS_DIR, "background.mp3")
HORROR_SOUND = os.path.join(SOUNDS_DIR, "horror_scream.mp3")
LAUGH_SOUND = os.path.join(SOUNDS_DIR, "evil_laugh.mp3")
SAD_SOUND = os.path.join(SOUNDS_DIR, "sad.mp3")
HEAVENLY_BGM = os.path.join(SOUNDS_DIR, "so good.mp3")  # Heavenly background music
SNAKE_MUSIC = os.path.join(SOUNDS_DIR, "snake.mp3")      # Music for Bloody Demon Mode
WARNING_MUSIC = os.path.join(SOUNDS_DIR, "warning.mp3")    # Warning screen music

# Colors
BLACK       = (0, 0, 0)
RED         = (255, 0, 0)
BLOOD_RED   = (102, 0, 0)
HELL_ORANGE = (255, 69, 0)
GREEN       = (0, 255, 0)
SKY_BLUE    = (135, 206, 235)
WHITE       = (255, 255, 255)
YELLOW      = (255, 255, 0)

# Fonts
font = pygame.font.SysFont('arial', 40)
creepy_font = pygame.font.Font(None, 60)
glitch_font = pygame.font.Font(None, 100)

# Load sounds (except warning, which is loaded in warning_screen)
try:
    pygame.mixer.music.load(BG_MUSIC)
    horror_sound = pygame.mixer.Sound(HORROR_SOUND)
    laugh_sound = pygame.mixer.Sound(LAUGH_SOUND)
    sad_sound = pygame.mixer.Sound(SAD_SOUND)
except Exception as e:
    print(f"Sound error: {str(e)}")
    sys.exit()

# -------------------------
# Utility: Draw Heaven Background
# -------------------------
def draw_heaven_background():
    screen.fill(SKY_BLUE)
    pygame.draw.ellipse(screen, WHITE, (50, 50, 200, 100))
    pygame.draw.ellipse(screen, WHITE, (300, 30, 250, 120))
    pygame.draw.ellipse(screen, WHITE, (600, 80, 150, 80))
    pygame.draw.ellipse(screen, WHITE, (100, 150, 220, 110))

# -------------------------
# Dragon Drawing and Animation
# -------------------------
def draw_dragon(x, y):
    pygame.draw.rect(screen, YELLOW, (x, y, 120, 60))
    pygame.draw.rect(screen, YELLOW, (x + 20, y - 40, 60, 40))
    pygame.draw.rect(screen, YELLOW, (x - 40, y + 20, 40, 20))
    pygame.draw.rect(screen, BLACK, (x + 90, y + 10, 10, 10))
    pygame.draw.rect(screen, YELLOW, (x + 40, y - 10, 10, 10))
    pygame.draw.rect(screen, YELLOW, (x + 60, y - 20, 10, 10))

def dragon_animation():
    start_x = -100
    end_x = 850
    y_position = random.randint(50, 200)
    x = start_x
    while x < end_x:
        screen.fill(BLACK)
        draw_dragon(x, y_position)
        pygame.display.flip()
        clock.tick(60)
        x += 8
    escape_sequence()

# -------------------------
# Lose Dialogue (for Bloody Demon Mode)
# -------------------------
def lose_dialogue():
    """
    Displays a unique, evil, Undertale‑like lose dialogue when you lose in Bloody Demon Mode.
    The music is stopped immediately before showing the dialogue.
    After you press any key, the game-over sequence is triggered.
    """
    # Stop any playing music immediately.
    pygame.mixer.music.stop()
    
    dialogue_font = pygame.font.SysFont('arial', 30)  # Smaller font for better fit
    dialogue_lines = [
        "Oh, you foolish mortal!",
        "Your feeble attempt has crumbled before the abyss.",
        "The darkness mocks your weakness...",
        "You lost the game... and now, you die!"
    ]
    screen.fill(BLACK)
    # Blit each line with vertical spacing.
    for i, line in enumerate(dialogue_lines):
        text_surface = dialogue_font.render(line, True, RED)
        screen.blit(text_surface, (50, 100 + i * 50))
    prompt = dialogue_font.render("Press any key to embrace your fate...", True, WHITE)
    screen.blit(prompt, (50, 400))
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(15)
    game_over_sequence()

# -------------------------
# Bloody Demon Mode (Snake Game)
# -------------------------
def bloody_demon_mode():
    pygame.mixer.music.load(SNAKE_MUSIC)
    pygame.mixer.music.play(-1)
    
    lives = 3
    block_size = 20
    snake_speed = 15
    snake_list = []
    snake_length = 1
    score = 0
    target_score = 1500

    x = 400
    y = 300
    x_change = 0
    y_change = 0
    food_x = round(random.randrange(0, 800 - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, 600 - block_size) / block_size) * block_size

    # Increase the number of enemies
    enemies = []
    num_enemies = 6  # More dark demon enemies appear now.
    enemy_size = block_size
    for i in range(num_enemies):
        enemy = {
            'x': random.randrange(0, 800 - enemy_size),
            'y': random.randrange(0, 600 - enemy_size),
            'vx': random.choice([-4, -3, 3, 4]),
            'vy': random.choice([-4, -3, 3, 4])
        }
        enemies.append(enemy)

    game_over_mode = False
    while not game_over_mode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        x += x_change
        y += y_change

        # Check collision with boundaries.
        if x >= 800 or x < 0 or y >= 600 or y < 0:
            lives -= 1
            if lives <= 0:
                game_over_mode = True
                lose_dialogue()
                return
            else:
                x, y = 400, 300
                x_change, y_change = 0, 0
                snake_list = []
                snake_length = 1
                # Reset enemies.
                enemies = []
                for i in range(num_enemies):
                    enemy = {
                        'x': random.randrange(0, 800 - enemy_size),
                        'y': random.randrange(0, 600 - enemy_size),
                        'vx': random.choice([-4, -3, 3, 4]),
                        'vy': random.choice([-4, -3, 3, 4])
                    }
                    enemies.append(enemy)

        screen.fill(BLOOD_RED)
        pygame.draw.rect(screen, WHITE, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self-collision.
        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives <= 0:
                    game_over_mode = True
                    lose_dialogue()
                    return
                else:
                    x, y = 400, 300
                    x_change, y_change = 0, 0
                    snake_list = []
                    snake_length = 1

        for segment in snake_list:
            pygame.draw.rect(screen, YELLOW, [segment[0], segment[1], block_size, block_size])

        # Update and draw dark demon enemies.
        for enemy in enemies:
            enemy['x'] += enemy['vx']
            enemy['y'] += enemy['vy']
            if enemy['x'] <= 0 or enemy['x'] >= 800 - enemy_size:
                enemy['vx'] = -enemy['vx']
            if enemy['y'] <= 0 or enemy['y'] >= 600 - enemy_size:
                enemy['vy'] = -enemy['vy']
            pygame.draw.rect(screen, RED, [enemy['x'], enemy['y'], enemy_size, enemy_size])
            pygame.draw.rect(screen, BLACK, [enemy['x'] + 5, enemy['y'] + 5, 5, 5])
            # Check collision with snake head.
            if (x < enemy['x'] + enemy_size and
                x + block_size > enemy['x'] and
                y < enemy['y'] + enemy_size and
                y + block_size > enemy['y']):
                lives -= 1
                if lives <= 0:
                    game_over_mode = True
                    lose_dialogue()
                    return
                else:
                    x, y = 400, 300
                    x_change, y_change = 0, 0
                    snake_list = []
                    snake_length = 1

        # Check if snake eats the food.
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, 800 - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, 600 - block_size) / block_size) * block_size
            snake_length += 1
            score += 100

        score_text = font.render("Score: " + str(score), True, WHITE)
        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.update()

        if score >= target_score:
            hell_ending()
            return

        clock.tick(snake_speed)

# -------------------------
# Warning Screen Function (with warning.mp3)
# -------------------------
def warning_screen():
    warning_music = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "warning.mp3"))
    warning_music.play(-1)
    
    yes_button_scale = 1.0
    no_clicked = False

    base_yes_size = (150, 80)
    base_no_size  = (150, 80)
    yes_button_center = (300, 450)
    no_button_center  = (500, 450)
    
    running_warning = True
    while running_warning:
        screen.fill(BLACK)
        
        if not no_clicked:
            warn_title = creepy_font.render("WARNING!", True, RED)
            warn_line1 = font.render("This game is not for the faint of heart.", True, RED)
            warn_line2 = font.render("Do you dare to proceed?", True, RED)
        else:
            warn_title = creepy_font.render("YOUR SOUL IS DAMNED!", True, RED)
            warn_line1 = font.render("You have rejected fate...", True, RED)
            warn_line2 = font.render("Now, eternal torment awaits you!", True, RED)
        
        screen.blit(warn_title, warn_title.get_rect(center=(400, 100)))
        screen.blit(warn_line1, warn_line1.get_rect(center=(400, 200)))
        screen.blit(warn_line2, warn_line2.get_rect(center=(400, 260)))
        
        yes_width  = int(base_yes_size[0] * yes_button_scale)
        yes_height = int(base_yes_size[1] * yes_button_scale)
        yes_rect = pygame.Rect(0, 0, yes_width, yes_height)
        yes_rect.center = yes_button_center
        pygame.draw.rect(screen, RED, yes_rect)
        yes_text = font.render("YES", True, BLACK)
        screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
        
        no_rect = pygame.Rect(0, 0, base_no_size[0], base_no_size[1])
        no_rect.center = no_button_center
        pygame.draw.rect(screen, RED, no_rect)
        no_text = font.render("NO", True, BLACK)
        screen.blit(no_text, no_text.get_rect(center=no_rect.center))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if yes_rect.collidepoint(mouse_pos):
                    warning_music.stop()
                    running_warning = False
                elif no_rect.collidepoint(mouse_pos):
                    no_clicked = True
                    yes_button_scale = 2.0
        
        clock.tick(30)

# -------------------------
# Other Game Functions
# -------------------------
def calculate_death_date():
    death_date = datetime.now() + timedelta(days=random.randint(1, 666))
    return death_date.strftime("%d %B %Y, %H:%M:%S")

def show_hint():
    global hint_active, hint_start_time, last_hint_time
    current_time = pygame.time.get_ticks()
    if current_time - last_hint_time > hint_cooldown:
        hint_active = True
        hint_start_time = current_time
        last_hint_time = current_time

def draw_glitch_hint():
    text = glitch_font.render(str(target_number), True, RED)
    x = random.randint(100, 500)
    y = random.randint(100, 400)
    for _ in range(3):
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        screen.blit(text, (x + offset_x, y + offset_y))

def draw_blood_effect():
    blood = pygame.Surface((800, 600))
    blood.set_alpha(150)
    blood.fill(BLOOD_RED)
    screen.blit(blood, (0, 0))

def draw_hell_scene():
    hell = pygame.Surface((800, 600))
    hell.set_alpha(200)
    hell.fill(HELL_ORANGE)
    screen.blit(hell, (0, 0))

def game_over_sequence():
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    draw_blood_effect()
    
    death_date = calculate_death_date()
    line1 = creepy_font.render("YOUR DEATH DATE:", True, RED)
    line2 = creepy_font.render(death_date, True, RED)
    
    screen.blit(line1, (50, 250))
    screen.blit(line2, (50, 300))
    
    pygame.display.flip()
    horror_sound.play()
    laugh_sound.play()
    pygame.time.wait(5000)
    pygame.quit()
    sys.exit()

# -------------------------
# Heaven Ending (Escape Sequence)
# -------------------------
def escape_sequence():
    pygame.mixer.music.stop()
    try:
        pygame.mixer.music.load(HEAVENLY_BGM)
    except Exception as e:
        print(f"Error loading heavenly bgm: {str(e)}")
    pygame.mixer.music.play(-1)
    
    start_time = pygame.time.get_ticks()
    duration = 120000  # 2 minutes

    sparkles = []
    for i in range(10):
        x = random.randint(0, 800)
        y = random.randint(600, 1200)
        radius = random.randint(20, 50)
        speed = random.uniform(0.2, 1.0)
        sparkles.append([x, y, radius, speed])
    
    exit_button_rect = pygame.Rect(750, 10, 40, 40)
    
    while pygame.time.get_ticks() - start_time < duration:
        draw_heaven_background()
        
        for s in sparkles:
            s[1] -= s[3]
            pygame.draw.circle(screen, WHITE, (int(s[0]), int(s[1])), s[2])
            if s[1] + s[2] < 0:
                s[1] = 600 + s[2]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                else:
                    mx, my = event.pos
                    radius = random.randint(10, 30)
                    speed = random.uniform(0.5, 2.0)
                    sparkles.append([mx, my, radius, speed])
        
        time_elapsed = (pygame.time.get_ticks() - start_time) / 1000.0
        scale = 1 + 0.1 * (1 + math.sin(time_elapsed * 2 * math.pi))
        dynamic_font = pygame.font.SysFont('arial', int(40 * scale))
        congrats_text = dynamic_font.render("CONGRATS, YOU ESCAPED HELL!", True, BLACK)
        screen.blit(congrats_text, congrats_text.get_rect(center=(400, 300)))
        
        credits_font = pygame.font.SysFont('arial', 30)
        credits_text = credits_font.render("Credits: by OmakoZ", True, BLACK)
        screen.blit(credits_text, credits_text.get_rect(center=(400, 550)))
        
        pygame.draw.rect(screen, RED, exit_button_rect)
        x_font = pygame.font.SysFont('arial', 30)
        x_text = x_font.render("X", True, WHITE)
        screen.blit(x_text, x_text.get_rect(center=exit_button_rect.center))
        
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

# -------------------------
# Hell Ending Function
# -------------------------
def hell_ending():
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    draw_hell_scene()
    
    text1 = creepy_font.render("THERE IS NO ESCAPE", True, RED)
    text2 = creepy_font.render("YOU BELONG TO HELL", True, RED)
    screen.blit(text1, (200, 250))
    screen.blit(text2, (200, 300))
    
    sad_sound.play(-1)
    pygame.display.flip()
    
    start_time = pygame.time.get_ticks()
    escape_button_active = False
    escape_button_rect = pygame.Rect(600, 500, 150, 80)
    escape_button_start_time = 0
    
    while pygame.time.get_ticks() - start_time < 600000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if escape_button_active and escape_button_rect.collidepoint(event.pos):
                    sad_sound.stop()
                    escape_sequence()
                    return
        
        current_time = pygame.time.get_ticks()
        if not escape_button_active and random.random() < 0.005:
            escape_button_active = True
            escape_button_start_time = current_time
        
        if escape_button_active and current_time - escape_button_start_time > 2000:
            escape_button_active = False
        
        screen.fill(BLACK)
        draw_hell_scene()
        screen.blit(text1, (200, 250))
        screen.blit(text2, (200, 300))
        
        if escape_button_active:
            pygame.draw.rect(screen, GREEN, escape_button_rect)
            escape_text = font.render("ESCAPE!", True, BLACK)
            screen.blit(escape_text, escape_text.get_rect(center=escape_button_rect.center))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

# -------------------------
# Game Variables
# -------------------------
target_number = random.randint(1, 666)
attempts = 0
max_attempts = 10
user_input = ""
game_over = False
hint_active = False
hint_start_time = 0
HINT_DURATION = 1000  # 1 second
hint_cooldown = 10000
last_hint_time = 0
dragon_triggered = False

# -------------------------
# Main Game Loop
# -------------------------
warning_screen()
pygame.mixer.music.play(-1)

running = True
while running:
    current_time = pygame.time.get_ticks()
    
    if random.random() < 0.0001 and not hint_active:
        show_hint()
    
    if hint_active and current_time - hint_start_time > HINT_DURATION:
        hint_active = False

    if not dragon_triggered and random.random() < 0.0001:
        dragon_triggered = True
        dragon_animation()
        running = False
        break

    screen.fill(BLACK)
    
    instr_text = font.render(f"Guess the number (1-666). Attempts left: {max_attempts - attempts}", True, RED)
    screen.blit(instr_text, (50, 50))
    
    input_text = font.render(f"Your guess: {user_input}", True, RED)
    screen.blit(input_text, (50, 150))
    
    history_text = font.render(f"Failed attempts: {attempts}/10", True, RED)
    screen.blit(history_text, (50, 500))
    
    if hint_active:
        draw_glitch_hint()
    
    hard_time_rect = pygame.Rect(650, 500, 140, 60)
    pygame.draw.rect(screen, RED, hard_time_rect)
    hard_time_text = font.render("Hard Time", True, BLACK)
    screen.blit(hard_time_text, hard_time_text.get_rect(center=hard_time_rect.center))
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hard_time_rect.collidepoint(event.pos):
                bloody_demon_mode()
                running = False
                break
        elif event.type == pygame.KEYDOWN:
            if game_over:
                continue
            if event.key == pygame.K_RETURN:
                try:
                    guess = int(user_input)
                    if guess == target_number:
                        hell_ending()
                        running = False
                    else:
                        laugh_sound.play()
                        attempts += 1
                        if attempts >= max_attempts:
                            game_over = True
                            game_over_sequence()
                            running = False
                        else:
                            user_input = ""
                except:
                    user_input = ""
            elif event.key == pygame.K_BACKSPACE:
                user_input = user_input[:-1]
            else:
                user_input += event.unicode

    clock.tick(30)

pygame.quit()
sys.exit()
