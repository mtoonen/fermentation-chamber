import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Change these
# to the right size for your display!
WIDTH = 128
HEIGHT = 64  # Change to 64 if needed
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)


def setup():
    print('Setting up display')


def destructor():
    print('Shutting down display')
    clear()

def clear():
    # Clear display.
    oled.fill(0)
    oled.show()


def writeText(text):

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
   # draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle draw.rectangle(        (BORDER, BORDER, oled.width - BORDER - 1, oled.height -
    # BORDER - 1),        outline=0,        fill=0,    )

    # Load default font.
    font = ImageFont.load_default()

    # Draw Some Text
    #  text = "Hello World!"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()

def writeText2(text1, text2):

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a white background
   # draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

    # Draw a smaller inner rectangle draw.rectangle(        (BORDER, BORDER, oled.width - BORDER - 1, oled.height -
    # BORDER - 1),        outline=0,        fill=0,    )

    # Load default font.
    font = ImageFont.load_default()

    # Draw Some Text
    #  text = "Hello World!"
    #(font_width, font_height) = font.getsize(text)
    #draw.text(
    #    (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
    #    text,
    #    font=font,
    #    fill=255,

    #)
    x = 0
    top = -2
    IP = 'ipee'
    CPU = "cepeeuu"

    MemUsage = 'memen'
    Disk = 'disque'
    draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
    draw.text((x, top + 8), "CPU load: " + CPU, font=font, fill=255)
    draw.text((x, top + 16), MemUsage, font=font, fill=255)
    draw.text((x, top + 25), Disk, font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
