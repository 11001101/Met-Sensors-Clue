#Monitor customisable temperature and humidity ranges, with an optional audible alarm tone."""
from adafruit_clue import clue
import math

temp_offset =  -7.1 # in celcius to steady state Clue
humid_offset = 13.5 # in % RH
elevation = 1045 # in meters set your elevation here

# Set desired temperature range in degrees Celsius.
min_temperature = 22
max_temperature = 24

# Set desired humidity range in percent.
min_humidity = 15
max_humidity = 40

# Set to true to enable audible alarm tone.
alarm_enable = False

clue_display = clue.simple_text_display(text_scale=3, colors=(clue.WHITE,))

while True:
    alarm = False

    temperature = clue.temperature + temp_offset
    humidity = clue.humidity + humid_offset
    pressure = clue.pressure
    slp = pressure / math.exp(-1 * elevation / ((temperature + 273.15) * 29.263))
    # https://www.sandhurstweather.org.uk/barometric.pdf
    
    
    clue_display[0].text = " Temp:{:.1f}C".format(temperature)
    clue_display[2].text = " Humi:{:.1f}%".format(humidity)
    #clue_display[3].text = " Pres:{:.1f}kPa".format(pressure/10)
    clue_display[4].text = " Bar:{:.1f}kPa".format(slp/10)
    
    if temperature < min_temperature:
        clue_display[0].color = clue.BLUE
        alarm = True
    elif temperature > max_temperature:
        clue_display[0].color = clue.RED
        alarm = True
    else:
        clue_display[0].color = clue.WHITE

    if humidity < min_humidity:
        clue_display[2].color = clue.BLUE
        alarm = True
    elif humidity > max_humidity:
        clue_display[2].color = clue.RED
        alarm = True
    else:
        clue_display[2].color = clue.WHITE
    
    clue_display.show()

    if alarm and alarm_enable:
        clue.start_tone(2000)
    else:
        clue.stop_tone()
