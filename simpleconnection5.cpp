#include <iostream>
#include <string>
#include "MQTTClient.h"
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

#define ADXL345_ADDRESS 0x53
#define ADXL345_REG_BYTES 6

#define MQTT_BROKER_ADDRESS "tcp6://localhost"
#define CLIENT_ID "ee513/test"
#define TOPIC "ee513/test"
#define QOS 1

#define USERNAME "CreggL"
#define PASSWORD "1234"

int readAccelerometerData(int file, int16_t *x, int16_t *y, int16_t *z) {
    uint8_t data[ADXL345_REG_BYTES];
    if (::read(file, data, ADXL345_REG_BYTES) != ADXL345_REG_BYTES) {
        return -1; // Error reading accelerometer data
    }
    *x = (data[1] << 8) | data[0];
    *y = (data[3] << 8) | data[2];
    *z = (data[5] << 8) | data[4];
    return 0; // Success
}

int main() {
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;

    MQTTClient_create(&client, MQTT_BROKER_ADDRESS, CLIENT_ID, MQTTCLIENT_PERSISTENCE_NONE, NULL);
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    conn_opts.username = USERNAME;
    conn_opts.password = PASSWORD;

    int rc;
    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) {
        std::cerr << "Failed to connect to MQTT broker, return code " << rc << std::endl;
        return -1;
    }

    int file = ::open("/dev/i2c-1", O_RDWR);
    if (file < 0) {
        std::cerr << "Error opening I2C device" << std::endl;
        MQTTClient_destroy(&client);
        return -1;
    }

    if (ioctl(file, I2C_SLAVE, ADXL345_ADDRESS) < 0) {
        std::cerr << "Error setting I2C address" << std::endl;
        ::close(file);
        MQTTClient_destroy(&client);
        return -1;
    }

    while (true) {
        int16_t x, y, z;
        if (readAccelerometerData(file, &x, &y, &z) == 0) {
            std::string payload = "{\"x\": " + std::to_string(x) + ", \"y\": " + std::to_string(y) + ", \"z\": " + std::to_string(z) + "}";
            pubmsg.payload = (void *)payload.c_str();
            pubmsg.payloadlen = payload.size();
            pubmsg.qos = QOS;
            pubmsg.retained = 0;

            MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
            MQTTClient_waitForCompletion(client, token, 10000L);
        } else {
            std::cerr << "Failed to read accelerometer data" << std::endl;
        }
        usleep(1000000); // Delay for 1 second
    }

    ::close(file);
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);

    return 0;
}
