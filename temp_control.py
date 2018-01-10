import os
import glob
import re
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
path_temp = glob.glob('/sys/bus/w1/devices/28*/w1_slave')[0]
path_temp_cpu = '/sys/class/thermal/thermal_zone0/temp'


def read_temp_cpu():
	f = open(path_temp_cpu, 'r')
	line = f.readlines()
	f.close()
	temp_cpu = line[0][:2]
	print(temp_cpu)

def read_temp_raw():
	f = open(path_temp, 'r')
	lines = str(f.readlines())
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	if re.match( r'(.*) YES(.*)', lines):	
		temp = re.search( r'(.*) t=(.*)', lines).group(2)[:-4]
		temp_c = round((float(temp) / 1000), 1)
	print(temp_c)



if __name__ == "__main__":
	read_temp()
	read_temp_cpu()
