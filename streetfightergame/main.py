import pygame
import sys
import button
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define the coordinates and size of the "Play" text area
play_text_x = 400
play_text_y = 300
play_text_width = 200
play_text_height = 50
play_text_rect = pygame.Rect(play_text_x, play_text_y, play_text_width, play_text_height)



# Function to check if a point (mouse click) is within a rectangle
def point_is_inside_rect(point, rect):
    x, y = point
    return rect.left <= x <= rect.right and rect.top <= y <= rect.bottom

# Function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game variables
game_paused = False



# Define fonts
font = pygame.font.SysFont("arialblack", 40)

# Define colors
TEXT_COL = (255, 255, 255)

# Load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()

# Create button instances
resume_button = button.Button(405, 125, resume_img, 1)
quit_button = button.Button(440, 250, quit_img, 1)

# Define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wwizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

bonus_img = pygame.image.load("assets/images/icons/cactus.png").convert_alpha()

bonus_aktif = False  # Bonus görselin aktif olup olmadığını belirten bayrak
bonus_baslangic_zamani = 0  # Bonus görselin ne zaman göründüğünü tutan zaman
BONUS_SURESI = 10000  # Süre (5 saniye olarak ayarlandı)
bonus_alani = pygame.Rect(SCREEN_WIDTH // 2 - bonus_img.get_width() // 2, SCREEN_HEIGHT // 2 - bonus_img.get_height() // 2, bonus_img.get_width(), bonus_img.get_height())
# Define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def reduce_health_by_half(fighter):
    fighter.health -= fighter.health // 2 - 30
    if fighter.health < 0:
        fighter.health = 0



# Create instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

player1_can_yenilendi = False
player2_can_yenilendi = False

fighter_1_invisible = False
fighter_2_invisible = False

# Game loop
running = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if point_is_inside_rect(mouse_pos, play_text_rect):
                    running = True
    if running:
        # Game loop
        run = True
        while run:
            guncel_zaman = pygame.time.get_ticks()
            clock.tick(FPS)

            # Draw background
            draw_bg()

            # Check if game is paused
            if game_paused:
                if resume_button.draw(screen):
                    game_paused = False
                if quit_button.draw(screen):
                    run = False
            else:
                # Check and handle bonus image appearance and collision
                if guncel_zaman - bonus_baslangic_zamani > BONUS_SURESI:
                    bonus_aktif = True
                    bonus_baslangic_zamani = guncel_zaman
                    bonus_alani.x = 460
                    bonus_alani.y = 425
                if bonus_aktif:
                    screen.blit(bonus_img, (bonus_alani.x, bonus_alani.y))
                    # Check collision with fighters
                    if fighter_1.rect.colliderect(bonus_alani):
                        reduce_health_by_half(fighter_1)

                        bonus_baslangic_zamani = guncel_zaman
                        bonus_aktif = False

                    elif fighter_2.rect.colliderect(bonus_alani) and bonus_aktif:  # Tekrar kontrol et
                        reduce_health_by_half(fighter_2)
                        bonus_aktif = False
                        bonus_baslangic_zamani = guncel_zaman





                # Show player stats
                draw_health_bar(fighter_1.health, 20, 20)
                draw_health_bar(fighter_2.health, 580, 20)
                draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
                draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

                # Update countdown
                if intro_count <= 0:
                    # Move fighters if the game is not paused
                    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
                    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
                else:
                    # Display count timer
                    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                    # Update count timer
                    if (pygame.time.get_ticks() - last_count_update) >= 1000:
                        intro_count -= 1
                        last_count_update = pygame.time.get_ticks()

                # Update fighters
                fighter_1.update()
                fighter_2.update()

                # Check for player defeat
                if not round_over:
                    if not fighter_1.alive:
                        score[1] += 1
                        round_over = True
                        round_over_time = pygame.time.get_ticks()
                    elif not fighter_2.alive:
                        score[0] += 1
                        round_over = True
                        round_over_time = pygame.time.get_ticks()
                else:
                    # Display victory image
                    screen.blit(victory_img, (360, 150))
                    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                        round_over = False
                        intro_count = 3
                        fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                        fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

            # Event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_paused = True
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and not game_paused:
                    # Player 1's invisibility key (X key)
                    if event.key == pygame.K_x:
                        # Toggle visibility for player 1 if they haven't used invisibility before
                        if not fighter_1_invisible:
                            fighter_1_invisible = True
                            fighter_1.set_invisible(True)
                    # Player 2's invisibility key (Z key)
                    elif event.key == pygame.K_KP_ENTER:
                        # Toggle visibility for player 2 if they haven't used invisibility before
                        if not fighter_2_invisible:
                            fighter_2_invisible = True
                            fighter_2.set_invisible(True)
                    # Player 1's health regeneration key (C key)
                    elif event.key == pygame.K_c:
                        # If player 1 hasn't regenerated health before, regenerate their health
                        if not player1_can_yenilendi:
                            fighter_1.health = 100
                            player1_can_yenilendi = True
                    # Player 2's health regeneration key (M key)
                    elif event.key == pygame.K_m:
                        # If player 2 hasn't regenerated health before, regenerate their health
                        if not player2_can_yenilendi:
                            fighter_2.health = 100
                            player2_can_yenilendi = True

            # Draw fighters
            if not game_paused:
                fighter_1.draw(screen)
                fighter_2.draw(screen)

            # Update display
            pygame.display.update()

        # Exit pygame
        pygame.quit()

        clock.tick(FPS)

        pygame.display.update()
    else:
        # Draw play screen
        screen.fill((0, 0, 0))  # Fill the screen with black
        # Draw "Play" text
        pygame.draw.rect(screen, (0, 0, 0), play_text_rect)  # White rectangle
        draw_text("Play", count_font, WHITE, play_text_x + 30, play_text_y - 20)

        pygame.display.update()