import paho.mqtt.client as mqtt

# Define constants
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
CLIENT_ID = "ee513/test"
TOPIC = "ee513/test"
LAST_WILL_MSG = "Client disconnected unexpectedly"
USERNAME = "CreggL"
PASSWORD = "1234"

# Define callback functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC)

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code "+str(rc))

def on_message(client, userdata, msg):
    print("Message received: "+msg.payload.decode())

# Create MQTT client instance
client = mqtt.Client(CLIENT_ID)

# Set last will message
client.will_set(TOPIC, LAST_WILL_MSG, qos=1, retain=False)

# Set username and password
client.username_pw_set(USERNAME, password=PASSWORD)

# Assign callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connect to MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start MQTT loop
client.loop_forever()
