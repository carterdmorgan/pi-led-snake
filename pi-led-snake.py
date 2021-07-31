import pygame
import time
import random
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 143      # Number of LED pixels.
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
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

led_height = 18
led_width = 7
 
dis_width = 70
dis_height = 180
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 4
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

OFFSET = 3

def getLedPos(x, y):
    # print('x', x, 'y', y)
    columnIsOdd = x % 2 != 0

    if columnIsOdd:
        first = (led_height + OFFSET) * x - 1
        position = first + y + 1

        return int(position)
    else:
        first = (led_height + OFFSET) * x
        position = first + (led_height - y) - 1# subtract 1 since grid starts at 0

        return int(position)

def lightCoordinate(x, y):
    pos = getLedPos(x, y)
    print('pos', pos)
    strip.setPixelColor(pos, Color(255, 255, 255))
 
# need equivalent led version
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def draw_led_snake(led_snake_list):
    for x in led_snake_list:
        pos = getLedPos(int(x[0]), int(x[1]))
        # print('light pos', pos)
        # clear strip
        strip.setPixelColor(pos, Color(255, 255, 255))
 
# not used in led version
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def colorWipe(strip, color, wait_ms=2):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
 
def gameLoop():
    # clear strip
    for index in range(LED_COUNT):
        strip.setPixelColor(index, Color(0, 0, 0))

    strip.show()

    game_over = False
    game_close = False
 
    gridX = int(led_width / 2)
    gridY = int(led_height / 2)
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    gridX_change = 0
    gridY_change = 0
    x1_change = 0
    y1_change = 0
 
    currentDirection = 'init'
    snake_List = []
    led_snake_list = []
    Length_of_snake = 1

    # foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    # foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    gridfoodx = 3
    gridfoody = 3
 
    while not game_over:
        for index in range(LED_COUNT):
            strip.setPixelColor(index, Color(0, 0, 0))
 
        while game_close == True:
            colorWipe(strip, Color(255, 0, 0))
            dis.fill(blue)

            message("You Lost! Press C-Play Again or Q-Quit", red)
 
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
                print('keydown')
                if event.key == pygame.K_LEFT and currentDirection != "right":
                    x1_change = -snake_block
                    y1_change = 0
                    gridX_change = -1
                    gridY_change = 0
                    currentDirection = "left"
                elif event.key == pygame.K_RIGHT and currentDirection != "left":
                    x1_change = snake_block
                    y1_change = 0
                    gridX_change = 1
                    gridY_change = 0
                    currentDirection = "right"
                elif event.key == pygame.K_UP and currentDirection != "down":
                    y1_change = -snake_block
                    x1_change = 0
                    gridX_change = 0
                    gridY_change = 1
                    currentDirection = "up"
                elif event.key == pygame.K_DOWN and currentDirection != "up":
                    y1_change = snake_block
                    x1_change = 0
                    gridX_change = 0
                    gridY_change = -1
                    currentDirection = "down"

        x1 += x1_change
        y1 += y1_change
        gridX += gridX_change
        gridY += gridY_change
        dis.fill(blue)

        if gridX > led_width - 1:
            print('mallow 1')
            gridX = 0
        elif gridX < 0:
            print('mallow 2')
            gridX = led_width - 1
        elif gridY >= led_height:
            print('mallow 3')
            print('resetting')
            gridY = 0
        elif gridY < 0:
            print('mallow 4')
            gridY = led_height - 1
        
        if x1 >= dis_width:
            x1 = 0
        if x1 < 0:
            x1 = dis_width
        if y1 >= dis_height:
            y1 = 0
        if y1 < 0:
            y1 = dis_height
        # print('first x', gridX, 'y', gridY)
       

        # pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        # print('light pos', pos)
        # clear strip
        pos = getLedPos(int(gridfoodx), int(gridfoody))
        strip.setPixelColor(pos, Color(0, 255, 0))
        snake_Head = []
        led_snake_head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        print('x', gridX, 'y', gridY)
        led_snake_head.append(gridX)
        led_snake_head.append(gridY)
        snake_List.append(snake_Head)
        led_snake_list.append(led_snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
            del led_snake_list[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        #draw led_snake again
        # pos = getLedPos(gridX, gridY)
        # # print('light pos', pos)
        # # clear strip
        # for index in range(LED_COUNT - 1):
        #     strip.setPixelColor(index, Color(0, 0, 0))
        # strip.setPixelColor(pos, Color(255, 0, 0))

        draw_led_snake(led_snake_list)
        
        strip.show() # update strip lights
        pygame.display.update()
 
        # print('foodx', foodx, 'foody', foody)
        # if x1 == foodx and y1 == foody:
        #     foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        #     foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        #     Length_of_snake += 1
        if gridX == gridfoodx and gridY == gridfoody:
            # foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            # foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            gridfoodx = random.randint(0, led_width - 1)
            gridfoody = random.randint(0, led_height - 1)
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()