import math
import random
import cv2
import mediapipe as mp
import pygame
import numpy as np

# Asset Source https://github.com/jaredly/fruit-ninja-assets/tree/master

pygame.init()

win_width, win_height = 640, 480
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Fruit Ninja")

font_size = 25
score_green = (66, 245, 90)
lives_red = (245, 66, 87)

start_menu = 0
game_playing = 1
game_over = 2
instruction_screen = 3
current_state = start_menu

current_score = 0
remaining_lives = 3

apple_image = pygame.image.load("Images/apple_small.png")
banana_image = pygame.image.load("Images/banana_small.png")
coconut_image = pygame.image.load("Images/coconut_small.png")
orange_image = pygame.image.load("Images/orange_small.png")
pineapple_image = pygame.image.load("Images/pineapple_small.png")
watermelon_image = pygame.image.load("Images/watermelon_small.png")
bomb_image = pygame.image.load("Images/bomb_small.png")
explosion = pygame.image.load("Images/explosion_small.png")
red_splash = pygame.image.load("Images/splash_red_small.png")
yellow_splash = pygame.image.load("Images/splash_yellow_small.png")
orange_splash = pygame.image.load("Images/splash_orange_small.png")
sword_image = pygame.image.load("Images/sword.png")
sword_image = pygame.transform.scale(sword_image, (100, 100))

apple_width, apple_height = apple_image.get_size()
banana_width, banana_height = banana_image.get_size()
coconut_width, coconut_height = coconut_image.get_size()
orange_width, orange_height = orange_image.get_size()
pineapple_width, pineapple_height = apple_image.get_size()
watermelon_width, watermelon_height = apple_image.get_size()
bomb_width, bomb_height = apple_image.get_size()
sword_width, sword_height = sword_image.get_size()


sword_x, sword_y = 0, 0

tuple_of_throwables = ([apple_image, apple_width, apple_height, 0, 0],
                       [banana_image, banana_width, banana_height, 0, 0],
                       [bomb_image, bomb_width, bomb_height, 0, 0],
                       [coconut_image, coconut_width, coconut_height, 0, 0],
                       [orange_image, orange_width, orange_height, 0, 0],
                       [pineapple_image, pineapple_width, pineapple_height, 0, 0],
                       [watermelon_image, watermelon_width, watermelon_height, 0, 0])

tuple_of_effects = (explosion, red_splash, yellow_splash, orange_splash)

on_screen_items = []
on_screen_effects = []
# fruit_width, fruit_height = apple_image.get_size()
# fruit_x, fruit_y = 400, 300

time_elapsed_since_last_update = 0
time_elapsed_since_last_spawn = 0

clock = pygame.time.Clock()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


font = pygame.font.Font("Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", font_size)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_state == start_menu:
        win.fill((163, 150, 91))
        title_font = pygame.font.Font("Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 72)
        title_text = title_font.render("Finger Fruit Ninja", True, score_green)
        title_rect = title_text.get_rect(center=(win_width // 2, 30))
        win.blit(title_text, title_rect)

        # Example: Display a start button and check for mouse click event
        start_button_rect = pygame.Rect(win_width // 2 - 75, 250, 150, 50)
        pygame.draw.rect(win, (0, 255, 0), start_button_rect)  # Green button
        start_font = pygame.font.Font(None, 36)
        start_text = start_font.render("Start", True, (0, 0, 0))
        text_rect = start_text.get_rect(center=start_button_rect.center)
        win.blit(start_text, text_rect)

        # Check for mouse click event to start the game
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and start_button_rect.collidepoint(mouse_x, mouse_y):
            current_score = 0
            remaining_lives = 3
            on_screen_items = []
            on_screen_effects = []
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, win_width)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, win_height)

            current_state = game_playing

        # Example: Display an instructions button and check for mouse click event
        instructions_button_rect = pygame.Rect(win_width // 2 - 75, 320, 150, 50)
        pygame.draw.rect(win, (0, 0, 255), instructions_button_rect)  # Blue button
        instructions_font = pygame.font.Font(None, 36)
        instructions_text = instructions_font.render("Instructions", True, (0, 0, 0))
        text_rect = instructions_text.get_rect(center=instructions_button_rect.center)
        win.blit(instructions_text, text_rect)

        # Check for mouse click event to show instructions
        if event.type == pygame.MOUSEBUTTONDOWN and instructions_button_rect.collidepoint(mouse_x, mouse_y):
            current_state = instruction_screen

        # Example: Display a quit button and check for mouse click event
        quit_button_rect = pygame.Rect(win_width // 2 - 75, 390, 150, 50)
        pygame.draw.rect(win, (255, 0, 0), quit_button_rect)  # Red button
        quit_font = pygame.font.Font(None, 36)
        quit_text = quit_font.render("Quit", True, (0, 0, 0))
        text_rect = quit_text.get_rect(center=quit_button_rect.center)
        win.blit(quit_text, text_rect)

        # Check for mouse click event to quit the game
        if event.type == pygame.MOUSEBUTTONDOWN and quit_button_rect.collidepoint(mouse_x, mouse_y):
            pygame.quit()
            quit()

    elif current_state == instruction_screen:
        win.fill((163, 150, 91))
        title_font = pygame.font.Font("Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 18)
        title_text = title_font.render("Your goal is to destroy as many fruits\n as possible,if you destroy a\n"
                                       "fruit you score a point, if you\n"
                                       "destroy a bomb a life is lost \n, if your score becomes negative \n"
                                       "a life is lost, if you miss a fruit\n, you score is reduced by 1\n"
                                       "This game tracks the index finger \nof your hand,"
                                       "only one finger can be used \nat this time. You may have to "
                                       "tweak your ticks \nand window resolution to get best results \n"
                                       "for your computer. ", True, score_green)
        title_rect = title_text.get_rect(center=(win_width // 2, 30))
        win.blit(title_text, title_rect)

        return_button_rect = pygame.Rect(win_width // 2 - 75, 250, 150, 50)
        pygame.draw.rect(win, (0, 255, 0), return_button_rect)  # Green button
        return_font = pygame.font.Font(None, 20)
        return_text = return_font.render("Start Game", True, (0, 0, 0))
        text_rect = return_text.get_rect(center=return_button_rect.center)
        win.blit(return_text, text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and return_button_rect.collidepoint(mouse_x, mouse_y):
            current_state = start_menu
            # ERROR should go to start menu but then automatically starts game


    elif current_state == game_playing:

        ret, frame = cap.read()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_tip = mp_hands.HandLandmark.INDEX_FINGER_TIP
                normalized_point = hand_landmarks.landmark[finger_tip]
                pixel_coordinates = mp.solutions.drawing_utils.\
                    _normalized_to_pixel_coordinates(normalized_point.x, normalized_point.y, frame.shape[1], frame.shape[0])
                # cv2.circle(rgb_frame, pixel_coordinates, 10, (0, 255, 0), -1)
                if pixel_coordinates:
                    sword_x, sword_y = pixel_coordinates
                    sword_x = rgb_frame.shape[1] - pixel_coordinates[0]
        else:
            sword_x, sword_y = -sword_width, -sword_height
            # sword_y -= sword_height // 2
            # print("Pixel Coordinates x :" + str(pixel_coordinates[0]) + "Mirrored_x: " + str(mirrored_x))
            # print("Pixel Coordinates y :" + str(pixel_coordinates[1]) + "Sword_y: " + str(sword_y))

        # cv2.imshow("Hand Track", frame)

        dt = clock.tick()
        time_elapsed_since_last_update += dt
        time_elapsed_since_last_spawn += dt

        if time_elapsed_since_last_update > 5:
            # fruit_x = (fruit_x + 10) % (win_width - fruit_width)
            # fruit_y = (fruit_y + 2) % (win_height - fruit_height)
            index_to_be_remove = []
            for i in range(len(on_screen_items)):
                fruit, fruit_width, fruit_height, fruit_x, fruit_y = on_screen_items[i]

                if fruit in tuple_of_effects:
                    continue

                distance = math.sqrt((fruit_x - sword_x)**2 + (fruit_y - sword_y)**2)

                if(distance < sword_width//2 + fruit_width //2):
                    if fruit == bomb_image:
                        remaining_lives -= 1
                        on_screen_effects.append([explosion, fruit_x, fruit_y])
                    else:
                        current_score += 1
                        if fruit == apple_image or fruit == coconut_image:
                            on_screen_effects.append([red_splash, fruit_x, fruit_y])
                        elif fruit == banana_image or fruit == pineapple_image:
                            on_screen_effects.append([yellow_splash, fruit_x, fruit_y])
                        else:
                            on_screen_effects.append([orange_splash, fruit_x, fruit_y])

                    index_to_be_remove.append(i)
                    # print("collision")

                elif fruit_y > 500:
                    index_to_be_remove.append(i)
                    if fruit != bomb_image:
                        current_score -= 1
                        if current_score < 0:
                            remaining_lives -= 1
                            current_score = 0
                    # print("To be deleted")
                else:
                    on_screen_items[i][4] = (fruit_y + 2)

            for i in index_to_be_remove:
                on_screen_items.pop(i)
                # print("Deleted: " + str(len(on_screen_items)))

            time_elapsed_since_last_update = 0


        if time_elapsed_since_last_spawn > 800:
            new_spawn = random.choice(tuple_of_throwables).copy()
            new_spawn[3] = random.randint(0 + new_spawn[2]//2, win_width - new_spawn[2])
            on_screen_items.append(new_spawn)
            if len(on_screen_effects) > 0:
                on_screen_effects.pop(0)

            time_elapsed_since_last_spawn = 0

        win.fill((255, 255, 255))
        # rgb_frame = cv2.resize(rgb_frame, (win_width, win_height))

        rgb_frame = np.rot90(rgb_frame)
        rgb_frame = pygame.surfarray.make_surface(rgb_frame)
        win.blit(rgb_frame, (0, 0))
        pygame.draw.circle(win, (255, 0, 0), (sword_x, sword_y), sword_width//2, 1)

        for i in range(len(on_screen_items)):
            fruit, fruit_width, fruit_height, fruit_x, fruit_y = on_screen_items[i]
            win.blit(fruit, (fruit_x - fruit_width//2, fruit_y - fruit_height//2))  # Draw the fruit on the screen
            # print(fruit_x, fruit_y)

        for i in range(len(on_screen_effects)):
            effect, effect_x, effect_y = on_screen_effects[i]
            win.blit(effect, (effect_x, effect_y))

        # win.blit(apple_image, (fruit_x, fruit_y))  # Draw the fruit on the screen
        win.blit(sword_image, (sword_x - sword_width//2, sword_y - sword_height//2))
        score_text = font.render("Score: {}".format(current_score), True, score_green)
        win.blit(score_text, (20, 10))

        lives_text = font.render("Lives: {}".format(remaining_lives), True, lives_red)
        win.blit(lives_text, (win_width - 150, 10))
        # print("Swordx"+str(sword_x))
        # print(fruit_x,fruit_y)
        # if cv2.waitKey(1) & 0xff == ord('q'):
            # break
        if remaining_lives <= 0:
            current_state = game_over
            cap.release()


    elif current_state == game_over:
        win.fill((163, 150, 91))
        title_font = pygame.font.Font("Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 72)
        title_text = title_font.render("Game Over", True, lives_red)
        score_text = title_font.render(f'Score: {current_score}', True, score_green)
        win.blit(title_text, (60, 10))
        win.blit(score_text, (60, 60))

        return_button_rect = pygame.Rect(win_width // 2 - 75, 250, 150, 50)
        pygame.draw.rect(win, (0, 255, 0), return_button_rect)  # Green button
        return_font = pygame.font.Font(None, 20)
        return_text = return_font.render("New Game", True, (0, 0, 0))
        text_rect = return_text.get_rect(center=return_button_rect.center)
        win.blit(return_text, text_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and return_button_rect.collidepoint(mouse_x, mouse_y):
            current_state = start_menu
            # ERROR should go to start menu but then automatically starts game


    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 frames per second


cap.release()
pygame.quit()
cv2.destroyAllWindows()
