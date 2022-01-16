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
current_temperature = 0
current_humidity = 0
current_phase = ""
humidifier = False
heatmat = False
target_temperature = 0
target_humidity = 0


def setup(target_temp,target_hum):
    print('Setting up display')
    global target_humidity
    global target_temperature
    target_temperature = target_temp
    target_humidity = target_hum


def destructor():
    print('Shutting down display')
    clear()


def clear():
    # Clear display.
    oled.fill(0)
    oled.show()


def set_phase(phase):
    global current_phase
    current_phase = phase
    write_to_display()


def set_output_heatmat(on):
    global heatmat
    heatmat = on
    write_to_display()


def set_output_humidifier(on):
    global humidifier
    humidifier = on
    write_to_display()


def set_sensors(temp, hum):
    global current_humidity
    global current_temperature
    current_humidity = hum
    current_temperature = temp
    write_to_display()


def write_to_display():
    outputs = "Hum: "
    if humidifier:
        outputs += "on"
    else:
        outputs += "off"
    outputs += " | Heat: "
    if heatmat:
        outputs += "on"
    else:
        outputs += "off"
    sensor_temp = "Temp: {} / {}".format(current_temperature, target_temperature)
    sensor_humidity = "Hum: {} / {}".format(current_humidity, target_humidity)
    phase = current_phase
    write_text(outputs, sensor_temp, sensor_humidity, phase)


def write_text(outputs, sensor_temp, sensor_hum, phase):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Load default font.
    font = ImageFont.load_default()

    top = -2
    x = 0

    draw.text((x, top + 0), outputs, font=font, fill=255)
    draw.text((x, top + 8), sensor_temp, font=font, fill=255)
    draw.text((x, top + 16), sensor_hum, font=font, fill=255)
    draw.text((x, top + 25), phase, font=font, fill=255)

    # Display image
    oled.image(image)
    oled.show()
