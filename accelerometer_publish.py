import time 
import busio 
import adafruit_adxl34x
import board
import adafruit_mqtt_publish as mqtt_publish

#Define broker
BROKER = "localhost"
PORT = 1883
TOPIC = "ee513/test"


#Initalize the ADXL345 sensor
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

#Initialize the MQTT broker
mqtt_client= mqtt_publish.MQTTClient(BROKER, PORT)

mqtt_client.connect()

while True:

	x,y,z = accelerometer.acceleration

	data = f"X:{x}, Y:{y}, Z:{z}"

	mqtt_client.publish(TOPIC,data)

	print(data)

	time.sleep(1)

