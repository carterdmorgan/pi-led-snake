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

HEIGHT = 18
WIDTH = 7
OFFSET = 3

def getCoordinates(x, y):
    columnIsOdd = x % 2 != 0

    if columnIsOdd:
        first = (HEIGHT + OFFSET) * x
        position = first + y

        return position
    else:
        first = (HEIGHT + OFFSET) * x
        position = first + (HEIGHT - y) - 1 # subtract 1 since grid starts at 0

        return position

x = 6
y = 2

position = getCoordinates(x,y)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

# clear strip
for index in range(LED_COUNT - 1):
    strip.setPixelColor(index, Color(0, 0, 0))

strip.setPixelColor(position, Color(255, 0, 0))
strip.show()
print(position)