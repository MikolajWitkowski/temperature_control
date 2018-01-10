import os
import glob
import re
import RPi.GPIO as GPIO
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
path_temp = glob.glob('/sys/bus/w1/devices/28*/w1_slave')[0]
path_temp_cpu = '/sys/class/thermal/thermal_zone0/temp'

lcd_rs = 26
lcd_e = 19
lcd_db4 = 13
lcd_db5 = 6
lcd_db6 = 5
lcd_db7 = 11
lcd_delay = 0.005
info_refresh = 10

def main():
    lcd()
    while True:
        lcd_reset()        
        read_temp_cpu()
        read_temp()
        lcd_info("temp: "+read_temp()+chr(176)+"C"+
                " \nCPU: "+read_temp_cpu()+chr(176)+"C")
        time.sleep(info_refresh)
        

def read_temp_cpu():
    f = open(path_temp_cpu, 'r')
    line = f.readlines()
    f.close()
    temp_cpu = line[0][:2]
    return str(temp_cpu)


def read_temp_raw():
    f = open(path_temp, 'r')
    lines = str(f.readlines())
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    if re.match(r'(.*) YES(.*)', lines):
        temp = re.search(r'(.*) t=(.*)', lines).group(2)[:-4]
        temp_c = round((float(temp) / 1000), 1)
    return str(temp_c)


def lcd():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lcd_rs, GPIO.OUT)
    GPIO.setup(lcd_e, GPIO.OUT)
    GPIO.setup(lcd_db4, GPIO.OUT)
    GPIO.setup(lcd_db5, GPIO.OUT)
    GPIO.setup(lcd_db6, GPIO.OUT)
    GPIO.setup(lcd_db7, GPIO.OUT)

    lcd_reset()


def lcd_reset():
    lcd_byte(0x33)
    lcd_byte(0x32)
    lcd_byte(0x28)
    lcd_byte(0x06)
    lcd_byte(0x01)
    lcd_byte(0x0C)
    time.sleep(lcd_delay)


def lcd_byte(bits, mode=False):
    GPIO.output(lcd_rs, mode)
    GPIO.output(lcd_db4, False)
    GPIO.output(lcd_db5, False)
    GPIO.output(lcd_db6, False)
    GPIO.output(lcd_db7, False)

    if bits & 0x10 == 0x10:
        GPIO.output(lcd_db4, True)

    if bits & 0x20 == 0x20:
        GPIO.output(lcd_db5, True)

    if bits & 0x40 == 0x40:
        GPIO.output(lcd_db6, True)

    if bits & 0x80 == 0x80:
        GPIO.output(lcd_db7, True)

    lcd_refresh()
            
    GPIO.output(lcd_db4, False)
    GPIO.output(lcd_db5, False)
    GPIO.output(lcd_db6, False)
    GPIO.output(lcd_db7, False)

    if bits & 0x01 == 0x01:
        GPIO.output(lcd_db4, True)

    if bits & 0x02 == 0x02:
        GPIO.output(lcd_db5, True)

    if bits & 0x04 == 0x04:
        GPIO.output(lcd_db6, True)

    if bits & 0x08 == 0x08:
        GPIO.output(lcd_db7, True)
    
    lcd_refresh()
   
def lcd_refresh():
    time.sleep(lcd_delay)
    GPIO.output(lcd_e, True)
    time.sleep(lcd_delay)
    GPIO.output(lcd_e, False)
    time.sleep(lcd_delay)
    

def lcd_info(text):
    for char in text:
        if char == '\n':
            lcd_byte(0xc0)
        else:
            lcd_byte(ord(char), True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        lcd_reset()
        GPIO.cleanup()

