# import pygame
import time
import random
import keyboard
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 144      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
 
# pygame.init()

WHITE = Color(255, 255, 255)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
BLACK = Color(0, 0, 0)
YELLOW = Color(255, 255, 0)
BLUE = Color(0, 0, 255)
ORANGE = Color(255, 50, 0)
PINK = Color(255,105,255)
INDIGO = Color(75, 0, 130)

SNAKE_COLOR_OPTIONS = [
    GREEN,
    YELLOW,
    ORANGE,
    INDIGO,
]

FOOD_COLOR = BLUE
SNAKE_COLOR = SNAKE_COLOR_OPTIONS[0]

SNAKE_BLOCK_DIM = 10
SNAKE_SPEED = 12

LED_GRID_HEIGHT = 18
LED_GRID_WIDTH = 7
OFFSET = 3

DIS_HEIGHT = LED_GRID_HEIGHT * SNAKE_BLOCK_DIM
DIS_WIDTH = LED_GRID_WIDTH * SNAKE_BLOCK_DIM
 
# dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
 
# clock = pygame.time.Clock()


LED_MID_X = int(LED_GRID_WIDTH / 2)
LED_MID_Y = int(LED_GRID_HEIGHT) / 2
GAME_OVER_ANIM_DELAY = 7
ORIENTATION = 0

GAME_OVER_SHAPE_COORDINATES = [
    (LED_MID_X, LED_MID_Y),
    (LED_MID_X - 1, LED_MID_Y + 1),
    (LED_MID_X + 1, LED_MID_Y + 1),
    (LED_MID_X - 2, LED_MID_Y + 2),
    (LED_MID_X + 2, LED_MID_Y + 2),
    (LED_MID_X - 1, LED_MID_Y - 1),
    (LED_MID_X + 1, LED_MID_Y - 1),
    (LED_MID_X - 2, LED_MID_Y - 2),
    (LED_MID_X + 2, LED_MID_Y - 2)
]

ZERO_ARROW_COORDINATES = [
    (LED_MID_X, LED_MID_Y), # top line
    (LED_MID_X, LED_MID_Y - 1), # mid line
    (LED_MID_X, LED_MID_Y - 2), # bottom line
    (LED_MID_X, LED_MID_Y + 2), # top  arrow
    (LED_MID_X - 1, LED_MID_Y + 1), # middle left arrow
    (LED_MID_X + 1, LED_MID_Y + 1), # middle right arrow
    (LED_MID_X + 2, LED_MID_Y), # bottom right arrow
    (LED_MID_X - 2, LED_MID_Y), # bottom left arrow
]

ONE_EIGHTY_ARROW_COORDINATES = [
    (LED_MID_X, LED_MID_Y), # top line
    (LED_MID_X, LED_MID_Y + 1), # mid line
    (LED_MID_X, LED_MID_Y + 2), # bottom line
    (LED_MID_X, LED_MID_Y - 2), # top  arrow
    (LED_MID_X - 1, LED_MID_Y - 1), # middle left arrow
    (LED_MID_X + 1, LED_MID_Y - 1), # middle right arrow
    (LED_MID_X + 2, LED_MID_Y), # bottom right arrow
    (LED_MID_X - 2, LED_MID_Y), # bottom left arrow
]

NINETY_ARROW_COORDINATES = [
    (LED_MID_X, LED_MID_Y), # top line
    (LED_MID_X - 1, LED_MID_Y), # mid line
    (LED_MID_X - 2, LED_MID_Y), # bottom line
    (LED_MID_X + 2, LED_MID_Y), # top  arrow
    (LED_MID_X + 1, LED_MID_Y + 1), # middle left arrow
    (LED_MID_X + 1, LED_MID_Y - 1), # middle right arrow
    (LED_MID_X, LED_MID_Y - 2), # bottom right arrow
    (LED_MID_X, LED_MID_Y + 2), # bottom left arrow
]

TWO_SEVENTY_ARROW_COORDINATES = [
    (LED_MID_X, LED_MID_Y), # top line
    (LED_MID_X + 1, LED_MID_Y), # mid line
    (LED_MID_X + 2, LED_MID_Y), # bottom line
    (LED_MID_X - 2, LED_MID_Y), # top  arrow
    (LED_MID_X - 1, LED_MID_Y + 1), # middle left arrow
    (LED_MID_X - 1, LED_MID_Y - 1), # middle right arrow
    (LED_MID_X, LED_MID_Y - 2), # bottom right arrow
    (LED_MID_X, LED_MID_Y + 2), # bottom left arrow
]

ARROW_COORDINATES_DICT = {
    0: ZERO_ARROW_COORDINATES,
    90: NINETY_ARROW_COORDINATES,
    180: ONE_EIGHTY_ARROW_COORDINATES,
    270: TWO_SEVENTY_ARROW_COORDINATES
}

ZERO_UP_CHANGE = (0,1)
ZERO_RIGHT_CHANGE = (1,0)
ZERO_DOWN_CHANGE = (0,-1)
ZERO_LEFT_CHANGE = (-1,0)

NINETY_UP_CHANGE = (1,0)
NINETY_RIGHT_CHANGE = (0,-1)
NINETY_DOWN_CHANGE = (-1,0)
NINETY_LEFT_CHANGE = (0,1)

ONE_EIGHTY_UP_CHANGE = (0,-1)
ONE_EIGHTY_RIGHT_CHANGE = (-1,0)
ONE_EIGHTY_DOWN_CHANGE = (0,1)
ONE_EIGHTY_LEFT_CHANGE = (1,0)

TWO_SEVENTY_UP_CHANGE = (-1,0)
TWO_SEVENTY_RIGHT_CHANGE = (0,1)
TWO_SEVENTY_DOWN_CHANGE = (1,0)
TWO_SEVENTY_LEFT_CHANGE = (0,-1)

UP_CHANGE = ZERO_UP_CHANGE
RIGHT_CHANGE = ZERO_RIGHT_CHANGE
DOWN_CHANGE = ZERO_DOWN_CHANGE
LEFT_CHANGE = ZERO_LEFT_CHANGE

gridX_change = 0
gridY_change = 0

currentDirection = 'init'
orientation_selected = False

in_menu = True
game_close = False
new_game = False

def main_menu():
    print('selecting orientaion')
    clear_strip()
    
    orientation_arrow_coordinates = ZERO_ARROW_COORDINATES

    # global ORIENTATION

    # nav_keys = {
    #     pygame.K_LEFT, 
    #     pygame.K_RIGHT, 
    #     pygame.K_UP, 
    #     pygame.K_DOWN,
    #     pygame.K_KP1,
    #     pygame.K_KP3,
    #     pygame.K_KP5,
    #     pygame.K_KP2,
    # }

    while not orientation_selected:
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key in nav_keys:
        #             ORIENTATION += 90
        #             if ORIENTATION > 270:
        #                 ORIENTATION = 0
        #             orientation_arrow_coordinates = ARROW_COORDINATES_DICT[ORIENTATION]
        #         elif event.key == pygame.K_c or event.key == pygame.K_KP9:
        #             orientation_selected = True
        #         elif event.key in {pygame.K_q, pygame.K_KP7}:
        #             print('will quit here')

        orientation_arrow_coordinates = ARROW_COORDINATES_DICT[ORIENTATION]
        clear_strip()

        for coordinate in orientation_arrow_coordinates:
            pos = get_led_pos(coordinate[0], coordinate[1])
            strip.setPixelColor(pos, WHITE)

        strip.show()

    global UP_CHANGE
    global RIGHT_CHANGE
    global DOWN_CHANGE
    global LEFT_CHANGE
    
    print('confirming orientation', ORIENTATION)
    if ORIENTATION == 0:
        UP_CHANGE = ZERO_UP_CHANGE
        RIGHT_CHANGE = ZERO_RIGHT_CHANGE
        DOWN_CHANGE = ZERO_DOWN_CHANGE
        LEFT_CHANGE = ZERO_LEFT_CHANGE
    elif ORIENTATION == 90:
        UP_CHANGE = NINETY_UP_CHANGE
        RIGHT_CHANGE = NINETY_RIGHT_CHANGE
        DOWN_CHANGE = NINETY_DOWN_CHANGE
        LEFT_CHANGE = NINETY_LEFT_CHANGE
    elif ORIENTATION == 180:
        UP_CHANGE = ONE_EIGHTY_UP_CHANGE
        RIGHT_CHANGE = ONE_EIGHTY_RIGHT_CHANGE
        DOWN_CHANGE = ONE_EIGHTY_DOWN_CHANGE
        LEFT_CHANGE = ONE_EIGHTY_LEFT_CHANGE
    elif ORIENTATION == 270:
        UP_CHANGE = TWO_SEVENTY_UP_CHANGE
        RIGHT_CHANGE = TWO_SEVENTY_RIGHT_CHANGE
        DOWN_CHANGE = TWO_SEVENTY_DOWN_CHANGE
        LEFT_CHANGE = TWO_SEVENTY_LEFT_CHANGE

    global in_menu
    in_menu = False
    game_loop()

def get_led_pos(x, y):
    columnIsOdd = x % 2 != 0

    if columnIsOdd:
        first = (LED_GRID_HEIGHT + OFFSET) * x - 1
        position = first + y + 1

        return int(position)
    else:
        first = (LED_GRID_HEIGHT + OFFSET) * x
        position = first + (LED_GRID_HEIGHT - y) - 1# subtract 1 since grid starts at 0

        return int(position)

def clear_strip():
    for index in range(LED_COUNT):
        strip.setPixelColor(index, BLACK)

def light_coordinate(x, y, color):
    pos = get_led_pos(int(x), int(y))
    strip.setPixelColor(pos, color)

def draw_led_snake(led_snake_list):
    for x in led_snake_list:
        light_coordinate(x[0], x[1], SNAKE_COLOR)

def color_strips(strip, color, wait_ms=100):
    coordinates = []
    for y in range(LED_GRID_HEIGHT):
        for x in range(LED_GRID_WIDTH, -1, -1):
            coordinates.append((x,y))
    coordinates.reverse()

    for coordinate in coordinates:
        pos = get_led_pos(coordinate[0], coordinate[1])
        if (coordinate in GAME_OVER_SHAPE_COORDINATES):
            strip.setPixelColor(pos, WHITE)
        else:
            strip.setPixelColor(pos, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def color_wipe(strip, color, wait_ms=100):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def gen_random_coordinate():
    x = random.randint(0, LED_GRID_WIDTH - 1)
    y = random.randint(0, LED_GRID_HEIGHT - 1)
    return (x, y)
 
def game_loop():
    print('in game loop')
    strip.show()

    global game_close
    game_over = False
 
    led_x = int(LED_GRID_WIDTH / 2)
    led_y = int(LED_GRID_HEIGHT / 2)
 
    led_snake_list = []
    length_of_snake = 1

    food_added = False

    while not food_added:
        led_food_coordinate = gen_random_coordinate()
        led_food_x = led_food_coordinate[0]
        led_food_y = led_food_coordinate[1]

        food_added = True

        for snake_part in led_snake_list:
            if snake_part[0] == led_food_x and snake_part[1] == led_food_y:
                food_added = False
    
    food_added = False
 
    while game_close == True:
        # color_wipe(strip, RED, 5)
        color_strips(strip, RED, GAME_OVER_ANIM_DELAY)

        global SNAKE_COLOR
        SNAKE_COLOR = SNAKE_COLOR_OPTIONS[0]

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_q:
        #             clear_strip()
        #             game_over = True
        #             game_close = False
        #         if event.key == pygame.K_c or event.key == pygame.K_KP9:
        #             game_loop()
    global new_game
    if new_game:
        led_x = int(LED_GRID_WIDTH / 2)
        led_y = int(LED_GRID_HEIGHT / 2)
    
        led_snake_list = []
        length_of_snake = 1

        food_added = False

        while not food_added:
            led_food_coordinate = gen_random_coordinate()
            led_food_x = led_food_coordinate[0]
            led_food_y = led_food_coordinate[1]

            food_added = True

            for snake_part in led_snake_list:
                if snake_part[0] == led_food_x and snake_part[1] == led_food_y:
                    food_added = False
        
        new_game = False


    clear_strip()

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         game_over = True
        # if event.type == pygame.KEYDOWN:
        #     if (event.key == pygame.K_LEFT or event.key == pygame.K_KP1) and currentDirection != "right":
        #         gridX_change = LEFT_CHANGE[0]
        #         gridY_change = LEFT_CHANGE[1]
        #         currentDirection = "left"
        #     elif (event.key == pygame.K_RIGHT or event.key == pygame.K_KP3) and currentDirection != "left":
        #         gridX_change = RIGHT_CHANGE[0]
        #         gridY_change = RIGHT_CHANGE[1]
        #         currentDirection = "right"
        #     elif (event.key == pygame.K_UP or event.key == pygame.K_KP5)and currentDirection != "down":
        #         gridX_change = UP_CHANGE[0]
        #         gridY_change = UP_CHANGE[1]
        #         currentDirection = "up"
        #     elif (event.key == pygame.K_DOWN or event.key == pygame.K_KP2) and currentDirection != "up":
        #         gridX_change = DOWN_CHANGE[0]
        #         gridY_change = DOWN_CHANGE[1]
        #         currentDirection = "down"
        #     elif event.key == pygame.K_c or event.key == pygame.K_KP9:
        #         main_menu()
    led_x += gridX_change
    led_y += gridY_change

    if led_x > LED_GRID_WIDTH - 1:
        led_x = 0
    elif led_x < 0:
        led_x = LED_GRID_WIDTH - 1
    elif led_y >= LED_GRID_HEIGHT:
        led_y = 0
    elif led_y < 0:
        led_y = LED_GRID_HEIGHT - 1

    food_pos = get_led_pos(int(led_food_x), int(led_food_y))
    strip.setPixelColor(food_pos, FOOD_COLOR)
    led_snake_head = []

    led_snake_head.append(led_x)
    led_snake_head.append(led_y)

    led_snake_list.append(led_snake_head)
    if len(led_snake_list) > length_of_snake:
        del led_snake_list[0]

    for x in led_snake_list[:-1]:
        print ('x', x)
        if x == led_snake_head:
            print('setting game close to true')
            game_close = True

    draw_led_snake(led_snake_list)
    
    strip.show() # update strip lights
    # pygame.display.update()

    if led_x == led_food_x and led_y == led_food_y:
        # foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK_DIM) / 10.0) * 10.0
        # foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK_DIM) / 10.0) * 10.0
        while not food_added:
            led_food_coordinate = gen_random_coordinate()
            led_food_x = led_food_coordinate[0]
            led_food_y = led_food_coordinate[1]

            food_added = True

            for snake_part in led_snake_list:
                if snake_part[0] == led_food_x and snake_part[1] == led_food_y:
                    food_added = False

        food_added = False

        length_of_snake += 1
        index = int(length_of_snake / ((LED_GRID_HEIGHT * LED_GRID_WIDTH) / 10))
        if length_of_snake <= 8:
            index = 0
        elif length_of_snake <= 16:
            index = 1
        elif length_of_snake <= 24:
            index = 2
        elif length_of_snake > 24:
            index = 3

        SNAKE_COLOR = SNAKE_COLOR_OPTIONS[index]

    time.sleep(1/SNAKE_SPEED)

def callback(key):
    print(key.name)
    global gridX_change
    global gridY_change
    global currentDirection
    global game_close
    global new_game

    nav_keys = [
        'left',
        'right',
        'up',
        'down',
        '1',
        '2',
        '3',
        '5'
    ]

    if in_menu:
        print('here 1')
        if key.name in nav_keys:
            global ORIENTATION
            ORIENTATION += 90
            if ORIENTATION > 270:
                ORIENTATION = 0
        elif key.name in {'9', 'c'}:
            global orientation_selected
            orientation_selected = True
    else:
        print('here 2')
        if not game_close:
            if key.name in {'1', 'left'} and currentDirection != "right":
                gridX_change = LEFT_CHANGE[0]
                gridY_change = LEFT_CHANGE[1]
                currentDirection = "left"
            elif key.name in {'3', 'right'} and currentDirection != "left":
                gridX_change = RIGHT_CHANGE[0]
                gridY_change = RIGHT_CHANGE[1]
                currentDirection = "right"
            elif key.name in {'5', 'up'} and currentDirection != "down":
                gridX_change = UP_CHANGE[0]
                gridY_change = UP_CHANGE[1]
                currentDirection = "up"
            elif key.name in {'2', 'down'} and currentDirection != "up":
                gridX_change = DOWN_CHANGE[0]
                gridY_change = DOWN_CHANGE[1]
                currentDirection = "down"
            elif key.name in {'9', 'c'}:
                main_menu()
        else:
            print('here 3')
            if (key.name) in {'9', 'c'}:
                print('starting game loop')
                gridX_change = 0
                gridY_change = 0
                game_close = False
                currentDirection = 'init'
                new_game = True
    
keyboard.on_press(callback=callback)

main_menu()