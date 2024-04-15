
import time 
import busio 
import adafruit_adxl34x
import board


i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)

while True:
	print("%f %f %f " %accelerometer.acceleration)
	print("Tapped: %s"%accelerometer.events['tap'])
	time.sleep(1)


