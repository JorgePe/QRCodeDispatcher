#!/usr/bin/env python3

# bledispatcher
# this script works as a MQTT to BLE gateway/dispatcher for my public LEGO events:
# - subscribes to a MQTT broker
# - waits for messages
# - sends a control message to the LEGO device
#
# All LEGO devices should be running Pybricks firmware and listening on same channel
# Each LEGO device should be activated with a sequence of two messages:
# - an ID of the device (several devices can share the same ID if required)
# - a state like '1' or '0'

import paho.mqtt.client as mqtt
import subprocess
from time import sleep

mqtt_broker = "test.mosquitto.org"                # public mosquitto broker - WARNING: not secure, no SLA's
mqtt_topic = "/QRCodeDispatcher/message"          # topic used for communication between the web app and the dispatcher
mqtt_port = 1883                                  # default port = 1883
mqtt_keepalive = 60                               # default keepalive time between client and broker = 60 seconds

hcidev = "hci1"                                   # hci0 or hci1, needs to be properly checked at initialization

broadcast_duration = 0.20                         # duration in seconds of the broadcasting
                                                  # 0.10 was too short, 0.15 seems to work but sometimes
                                                  # the LEGO hub doesn'r receive it (specially with City Hubs)


# messages accepted
# ALL is a Willcard, should activate all models that acept it
# other messages should address only particular models
list_of_messages = ['ALL', 'ORN', 'OWL', 'PHO', 'DRA', 'ORR']


### Functions for sending messages using Pybricks advertisement protocol ###

# using a linux tool (hcitool, from the BlueZ bluetooth stack)
# because the python BLE libraries I was using no longer work with ev3dev
# and most recent libraries are too demanding, cannot event install

def prepare_ble_advertise():
    # prepares BLE for advertisement (broadcast)   
    subprocess.run(["hcitool", "-i", hcidev, "cmd", "0x08", "0x0006", "A1", "00", "A1", "00", \
        "03", "00", "00", "00", "00", "00", "00", "00", "00", "07", "002"])


def define_ble_advertise(msg):
    # msg: a 4 byte string a 3-char ID and a 1-char digit
    
    # we need to convert each of the 4 characters received
    # in a string containing the 2-byte hexadecimal representation 
    print(msg, \
        format(ord(msg[0]), "x"), \
        format(ord(msg[1]), "x"), \
        format(ord(msg[2]), "x"), \
        format(ord(msg[3]), "x")
        )
    
    # then we insert these 4 hexadecimal values in a pre-defined hcitool command
    subprocess.run(["hcitool", "-i", hcidev, "cmd", "0x08", "0x0008", "0B", "07", "FF", "97", \
        "03", "01", "00", "A4", format(ord(msg[0]), "x"), format(ord(msg[1]), "x"), \
        format(ord(msg[2]), "x"), format(ord(msg[3]), "x"), "00", "00", "00", "00", "00", "00", \
        "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00", "00"])


def initiate_ble_advertise():
    subprocess.run(["hcitool", "-i", hcidev, "cmd", "0x08", "0x000a", "01"])


def stop_ble_advertise():
    subprocess.run(["hcitool", "-i", hcidev, "cmd", "0x08", "0x000a", "00"])


def pybricks_broadcast(msg):
    # the sequence is always:
    # - prepare the hci (BLE) device for advertisements
    # - define the content of the advertisement
    # - initiate advertisement
    # - wait enough time for the hubs to receive it
    # - stop advertisement
    
    prepare_ble_advertise()
    define_ble_advertise(msg)
    initiate_ble_advertise()            
    sleep(broadcast_duration)
    stop_ble_advertise()

### Functions for MQTT ###

# callback for MQTT client connection
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(mqtt_topic)


# callback for MQTT message reception
def on_message(client, userdata, msg):
#    print("MSG")
    if msg.topic == mqtt_topic:      
        payload = msg.payload.decode()
        print(payload)
        if payload in list_of_messages:
            pybricks_broadcast(payload + "1")
        else:
            print("Unknown")

### Initialization ###

#subprocess.run(["hcitool", "-i", hcidev, "cmd", "0x08", "0x000a", "00"])

# create MQTT client and assign callback functions
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect    # subscribe to a particular topic when connected
mqttc.on_message = on_message    # action to execute when a message arrives

# connect to broker and keep waiting for messages to arrive
mqttc.connect(mqtt_broker, mqtt_port, mqtt_keepalive)
mqttc.loop_forever()
