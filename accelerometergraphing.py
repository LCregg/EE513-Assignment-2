import time
import board
import busio
import adafruit_adxl34x
import matplotlib.pyplot as plt

# Initialize I2C bus and ADXL345 accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# Create figure and axis objects for the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Acceleration (m/s^2)')
ax.set_title('Real-time Accelerometer Data')

# Set up empty lists to store data
timestamps = []
x_values = []
y_values = []
z_values = []

# Turn on interactive mode
plt.ion()

# Main loop to continuously update the plot with accelerometer data
while True:
    # Read accelerometer data
    x, y, z = accelerometer.acceleration
    timestamp = time.time()  # Get current timestamp

    # Append data to lists
    timestamps.append(timestamp)
    x_values.append(x)
    y_values.append(y)
    z_values.append(z)

    # Update the plot with new data
    ax.clear()  # Clear the previous plot
    ax.plot(timestamps, x_values, label='X-axis')
    ax.plot(timestamps, y_values, label='Y-axis')
    ax.plot(timestamps, z_values, label='Z-axis')
    ax.legend()  # Add legend to the plot
    ax.grid(True)  # Add grid to the plot

    # Pause for a short time to allow for smooth animation
    plt.pause(0.1)
