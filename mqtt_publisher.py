import time
import smbus
import paho.mqtt.client as mqtt

# Define MQTT broker address and topic

broker_address = "localhost"
topic = "ee513/test"
username = "CreggL"
password = "1234"

#Initialize the I2C bus

bus = smbus.SMBus(1) 

#ADXL345 address

DEVICE_ADDRESS = 0x53

DATA_FORMAT = 0x31
POWER_CTL = 0x20
DATAX0 = 0x32
DATAX1 = 0x33
DATAY0 = 0x34
DATAY1 = 0x35
DATAZ0 = 0x36
DATAZ1 = 0x37

#Enable measurements

bus.write_byte_data(DEVICE_ADDRESS, POWER_CTL, 	0X08)

#Set data format
bus.write_byte_data(DEVICE_ADDRESS, DATA_FORMAT, 0x08)

# MQTT on connect callback
def on_connect(client, userdata, flags, rc):
	print("Connected with result code"+str(rc))

# MQTT on publish callback
def on_publish(client, userdata, mid):
	print("Published message with MID: "+str(mid))

#Creating the MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

#Connect to MQTT broker
client.connect(broker_address, 1883, 60)


#Looping to read and publish sensor data 

while True:
	x0 = bus.read_byte_data(DEVICE_ADDRESS, DATAX0)
	x1 = bus.read_byte_data(DEVICE_ADDRESS, DATAX1)
	y0 = bus.read_byte_data(DEVICE_ADDRESS, DATAY0)
	y1 = bus.read_byte_data(DEVICE_ADDRESS, DATAY1)
	z0 = bus.read_byte_data(DEVICE_ADDRESS, DATAZ0)
	z1 = bus.read_byte_data(DEVICE_ADDRESS, DATAZ1)

	#Combining MSV and LSB
	x = x1 << 8 | x0
	y = y1 << 8 | y0
	z = z1 << 8 | z0

	#Publish sensor data
	sensor_data = f"X:{x}, Y:{y}, Z:{z}"
	client.publish(topic, sensor_data)

	time.sleep(1)


