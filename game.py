import random
import pygame
from CrazyPlane import Crazy_Plane


# gets the bg image
# draw that bg and the grid
def draw_background(background_img):
    screen.blit(background_img, (0, 0))
    for line_loc in range(0, 10):
        pygame.draw.line(screen, BLACK, (line_loc * 150, 0), (line_loc * 150, 1000))
        pygame.draw.line(screen, BLACK, (0, line_loc * 100), (1500, line_loc * 100))


# constants
MAX_PLANES = 20
# time constants
REFRESH_RATE = 3
clock = pygame.time.Clock()

# screen constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000

# color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# create screen
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Crazy Plane")

quit_game = False  # quit game flag
end_game = False  # crash flag
play_end_music = True  # play end music once flag

# bg image load
background = "background.jpg"  # bg 
backgroundImage = pygame.image.load(background)
draw_background(backgroundImage)

old_loc = []  # old planes location
loc_list = []  # current planes location
loc = ()  # plane location
plane_list = pygame.sprite.Group()  # list of every(MAX_PLANES) plane
for i in range(0, MAX_PLANES):
    color = random.randint(0, 4)
    if color == 0:
        plane = Crazy_Plane('red_plane.png', loc_list)  # creates a plane
    elif color == 1:
        plane = Crazy_Plane('blue_plane.png', loc_list)
    elif color == 2:
        plane = Crazy_Plane('green_plane.png', loc_list)
    else:
        plane = Crazy_Plane('purple_plane.png', loc_list)
    plane_list.add(plane)  # add to plane list
    plane_x, plane_y = plane.get_loc()  # get plane loc
    loc = (plane_x, plane_y)
    loc_list.append(loc)  # update plane loc in loc list
    old_loc.append((-1, -1))  # "trash" variable

crash_count = 0  # time the game had to redirect a plane
loop_count = 0  # turns

# play main game music
pygame.mixer.music.load("flight_music.mp3")
pygame.mixer.music.play(2)

# font for endgame text
font = pygame.font.Font("CoFont.otf", 75)

pygame.display.flip()
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if the red X is pressed 
            quit_game = True  # quit game

    if loop_count >= 100 * MAX_PLANES:  # if 1000 turns were played without a crash
        screen.blit(pygame.image.load("airport.jpg"), (0, 0))  # load end img
        screen.blit(pygame.image.load("sing.png"), (0, 0))

        # load text
        text_a_str = "End of the day!"
        text_b_str = " Crash %: "

        if crash_count != 0:
            text_c_str = " " + str((((100 / (loop_count / crash_count)) * 1000 // 1) // 1000)) + '%'
        else:
            text_c_str = ' 0%'
        text_a = font.render(text_a_str, True, BLACK)
        text_b = font.render(text_b_str, True, BLACK)
        text_c = font.render(text_c_str, True, BLACK)
        screen.blit(text_a, (10, 10))
        screen.blit(text_b, (10, 85))
        screen.blit(text_c, (10, 160))

        # play end jingle only once
        if play_end_music:
            pygame.mixer.music.load("win.mp3")
            play_end_music = False
            pygame.mixer.music.play()

    else:
        draw_background(backgroundImage)
        index = 0

        for i in plane_list:
            loc_x, loc_y = i.get_loc()
            old_loc[index] = loc_x, loc_y
            i.move()
            loc_x, loc_y = i.get_loc()
            loc_list[index] = (loc_x, loc_y)
            index += 1
            print(index, ":", i.get_loc())
        index = 0
        checked_tries = 0
        for i in plane_list:
            loc_found_flag = False
            while loc_list.count(loc_list[index]) > 1 and checked_tries < 8 and not loc_found_flag:
                for added_x in range(-1, 2):
                    for added_y in range(-1, 2):
                        if not loc_found_flag:

                            check_loc_x, check_loc_y = old_loc[index][0] + (added_x * 150), old_loc[index][1] + (
                                    added_y * 100)
                            if loc_list.count(
                                    (check_loc_x, check_loc_y)) == 0 and check_loc_x >= 0 and check_loc_y >= 0 and \
                                    check_loc_x < 1500 and check_loc_y < 1000:

                                i.update_loc(check_loc_x / 150, check_loc_y / 100)
                                loc_list[index] = (check_loc_x, check_loc_y)
                                loc_found_flag = True
                            else:
                                checked_tries += 1

            if checked_tries >= 8:
                i.update_loc(old_loc[index][0] / 150, old_loc[index][1] / 100)
                loc_list[index] = old_loc[index][0], old_loc[index][1]
                crash_count += 1
            index += 1
            loc_x, loc_y = i.get_loc()
            screen.blit(i.plane_sprite, (loc_x, loc_y))
        loop_count += 1 * MAX_PLANES
        print("loop: ", loop_count / MAX_PLANES)

    pygame.display.flip()
    clock.tick(REFRESH_RATE)
