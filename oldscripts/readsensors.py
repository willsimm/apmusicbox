import serial
sensor_port = '/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo_HIDPC-if00'
baud = 9600
sensors = serial.Serial(sensor_port, baud, timeout = 0)


while True:
    input = sensors.readline()
    input = input.replace('\n', '')
    input = input.replace('\r', '')
    if(input != ""):
            values = input.split("#")
            flex = values[0]
            force = values[1]
            print flex



