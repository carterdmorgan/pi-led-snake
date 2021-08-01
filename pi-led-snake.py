import pygame
import time
import random
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
 
pygame.init()
 
gui_black = (0, 0, 0)
gui_red = (213, 50, 80)
gui_green = (0, 255, 0)
gui_blue = (50, 153, 213)

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

DIS_HEIGHT = LED_GRID_HEIGHT * SNAKE_BLOCK_DIM
DIS_WIDTH = LED_GRID_WIDTH * SNAKE_BLOCK_DIM
 
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

OFFSET = 3

LED_MID_X = int(LED_GRID_WIDTH / 2)
LED_MID_Y = int(LED_GRID_HEIGHT) / 2
GAME_OVER_SHAPE_COORDINATES = []

def populate_game_over_shape(): 
    global GAME_OVER_SHAPE_COORDINATES
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X, LED_MID_Y))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X - 1, LED_MID_Y + 1))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X + 1, LED_MID_Y + 1))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X - 2, LED_MID_Y + 2))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X + 2, LED_MID_Y + 2))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X - 1, LED_MID_Y - 1))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X + 1, LED_MID_Y - 1))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X - 2, LED_MID_Y - 2))
    GAME_OVER_SHAPE_COORDINATES.append((LED_MID_X + 2, LED_MID_Y - 2))

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
 
# need equivalent led version
def draw_gui_snake(SNAKE_BLOCK_DIM, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, gui_black, [x[0], x[1], SNAKE_BLOCK_DIM, SNAKE_BLOCK_DIM])

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
    strip.show()

    game_over = False
    game_close = False
 
    led_x = int(LED_GRID_WIDTH / 2)
    led_y = int(LED_GRID_HEIGHT / 2)
    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2
 
    gridX_change = 0
    gridY_change = 0
    x1_change = 0
    y1_change = 0
 
    currentDirection = 'init'
    snake_List = []
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
 
    while not game_over:
        while game_close == True:
            # color_wipe(strip, RED, 5)
            color_strips(strip, RED, 10)
            dis.fill(gui_blue)
 
            pygame.display.update()

            global SNAKE_COLOR
            SNAKE_COLOR = SNAKE_COLOR_OPTIONS[0]

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c or event.key == pygame.K_KP9:
                        game_loop()
 
        clear_strip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_KP1) and currentDirection != "right":
                    x1_change = -SNAKE_BLOCK_DIM
                    y1_change = 0
                    gridX_change = -1
                    gridY_change = 0
                    currentDirection = "left"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_KP3) and currentDirection != "left":
                    x1_change = SNAKE_BLOCK_DIM
                    y1_change = 0
                    gridX_change = 1
                    gridY_change = 0
                    currentDirection = "right"
                elif (event.key == pygame.K_UP or event.key == pygame.K_KP5)and currentDirection != "down":
                    y1_change = -SNAKE_BLOCK_DIM
                    x1_change = 0
                    gridX_change = 0
                    gridY_change = 1
                    currentDirection = "up"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_KP2) and currentDirection != "up":
                    y1_change = SNAKE_BLOCK_DIM
                    x1_change = 0
                    gridX_change = 0
                    gridY_change = -1
                    currentDirection = "down"

        x1 += x1_change
        y1 += y1_change
        led_x += gridX_change
        led_y += gridY_change
        dis.fill(gui_blue)

        if led_x > LED_GRID_WIDTH - 1:
            led_x = 0
        elif led_x < 0:
            led_x = LED_GRID_WIDTH - 1
        elif led_y >= LED_GRID_HEIGHT:
            led_y = 0
        elif led_y < 0:
            led_y = LED_GRID_HEIGHT - 1
        
        if x1 >= DIS_WIDTH:
            x1 = 0
        if x1 < 0:
            x1 = DIS_WIDTH
        if y1 >= DIS_HEIGHT:
            y1 = 0
        if y1 < 0:
            y1 = DIS_HEIGHT
        food_pos = get_led_pos(int(led_food_x), int(led_food_y))
        strip.setPixelColor(food_pos, FOOD_COLOR)
        snake_Head = []
        led_snake_head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        led_snake_head.append(led_x)
        led_snake_head.append(led_y)
        snake_List.append(snake_Head)
        led_snake_list.append(led_snake_head)
        if len(snake_List) > length_of_snake:
            del snake_List[0]
            del led_snake_list[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        draw_gui_snake(SNAKE_BLOCK_DIM, snake_List)
        draw_led_snake(led_snake_list)
        
        strip.show() # update strip lights
        pygame.display.update()

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
            index = 0
            if length_of_snake <= 8:
                index = 0
            elif length_of_snake <= 16:
                index = 1
            elif length_of_snake <= 24:
                index = 2
            elif length_of_snake > 24:
                index = 3

            SNAKE_COLOR = SNAKE_COLOR_OPTIONS[index]
 
        clock.tick(SNAKE_SPEED)
 
    pygame.quit()
    quit()

populate_game_over_shape()
game_loop()