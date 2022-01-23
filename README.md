# fermentation-chamber
For my birthday I got this cool book about fermentation [1]. This talked about fermenting all kinds of cool stuff. However, this required a fermentation chamber. Being the nerd I am, I build one and went all out doing it. This documents my project.


## Why
* Koji fermentation
* Tempeh
* Dough proofing

# How to build

## Components

* Raspberry Pi (I used 2b)
* Temperature and humidity sensor (AM2301, but DHT11/DHT22 should work as well) [2]
* Solid State Relay [3]
* Humidifier [4]
* Raspberry pi prototyping hat [5]
* Display [6]
* Heatmat [7]
* WiFi module [8]
* Styrofoam box [9]

## Connections
 add connections layout

| Component                   | Pin/color        | RPi pin     |
|-----------------------------|:-----------------|:------------|
| Temperature/humidity sensor | Yellow           | #5          |
|                             | Black            | ground      |
|                             | Red              | 3.3v        |
| Display                     | Power/yellow     | 3.3v        |
|                             | Ground/green     | ground      |
|                             | SCL/orange       | SCL         |
|                             | SDA/red          | SDA         |
| Humidifier                  | - / red          | - SSR (CH2) |
|                             | + / blue         | + SSR (CH2) |
| Heatmat                     | Brown (from mat) | + SSR(CH1)  |
|                             | Brown (to plug)  | - SSR (CH1) |
| SSR                         | +                | 3.3v        |
|                             | -                | ground      |
|                             | CH1              | #17         |
|                             | CH2              | #18         |
## Software
To run this, I used my raspberry pi as the controller for the box. On a different server, I installed postgresql and grafana. Postgresql is used to store the metrics (values from sensors, events like switching on/off the heatmat/humidifier etc). Grafana is an awesome open source tool to visualize data in real time.

### Raspberry Pi OS Lite
I loaded Raspberry Pi OS (formerly known as raspbian) unto a SD card and updated everything. I enabled I2C by using the raspi-blynka.py utility from adafruit.

### Postgres
 add databasemodel
add empty config.py
### Grafana/ grafana cloud

 add json model for dashboard
### Python environment
 add pip packages used

raspberry pi
display
dht


# Expansions
waterlevel meter
PID
# References

[1] https://www.goodreads.com/book/show/37590384-foundations-of-flavor
[2] https://www.otronic.nl/a-61823552/sensors/am2301-temperatuursensor-en-luchtvochtigheidssensor/
[3] https://www.otronic.nl/a-61519535/relais/solid-state-relais-module-5v-2-kanaals-omron-g3mb-202p/
[4] https://www.otronic.nl/a-64876163/verwarmen-koelen/ultrasone-mist-maker-damper-luchtbevochtiger/
[5] https://www.reichelt.nl/nl/nl/raspberry-pi-shield-prototype-rasp-shd-proto-p163031.html?
[6] https://www.otronic.nl/a-59864177/displays/mini-oled-display-wit-0-96-inch-128x64-i2c/
[7] https://www.bol.com/nl/nl/p/kweekmat-verwarmingsmat-planten-zaden-stekjes-kiemen-ook-geschikt-voor-onder-terrariums/9300000062538277/?s2a=
[8] https://www.reichelt.nl/nl/nl/wifi-adapter-usb-150-mbit-s-asus-usb-n10b1-p270874.html?&trstct=pos_8&nbc=1
[9] https://www.bol.com/nl/nl/p/thermobox-60-liter-tempex-doos-grote-isolatiedoos-eps-koelbox/9300000036790032/?s2a=