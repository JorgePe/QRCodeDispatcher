# QR Code Dispatcher - The Middleware

## Intro

The device running as a dispatcher must be able to
subscribe to a MQTT topic and send BLE messages accordingly.

### MQTT communication
                                                                      
I am using a public MQTT broker, 'test.mosquitto.org', with the
usual default settings for MQTT clients (i.e. port 1883 and
a keepalive timeof 60 seconds).

All messages will are published in the topic '/QRCodeDispatcher/message'.
Any topic can be used, it's mostly just a method of categorizing
information and preventing 'noise' from other clients.

```
mqtt_broker = "test.mosquitto.org"
mqtt_topic = "/QRCodeDispatcher/message"
mqtt_port = 1883
mqtt_keepalive = 60
```

The payload of the MQTT messages is kept very simple and
just a few messages are expected:

```
list_of_messages = ['ALL', 'ORN', 'OWL', 'PHO', 'DRA', 'ORR']
```

The message is used to address a specific model (like 'OWL')
or all models at once (like 'ALL')


## BLE communication

Since I am using the MINDSTORMS EV3 with ev3dev linux and
there aren't many python BLE libraries and even less libraries
(if any) that can be used with the few resources of the
EV3 I'm using system calls to the linux command 'hcitool'.
Not pretty but it works.

'hcitool' requires the name of the HCI device to be used.

My LEGO MINDSTORMS EV3 has 2 HCI devices:
- hci0
- hci1

One is the internal Bluetooth device and since it is
very old (2.x) it cannot support BLE.

The other is the USB Bluetooth 4.x or 5.x device.
Most of the times, it will be 'hci1' but it's better to
check first (I will soon improve my code to prevent this
requirement)

```
robot@ev3dev:~$ hciconfig -a
hci1:	Type: Primary  Bus: USB
	BD Address: 04:42:1A:5B:03:D0  ACL MTU: 1021:6  SCO MTU: 255:12
	DOWN 
	...

hci0:	Type: Primary  Bus: UART
	BD Address: 00:16:53:52:BB:A0  ACL MTU: 1021:4  SCO MTU: 180:4
	DOWN 
	...
```

The above output of 'hciconfig' shows that 'hci1' uses USB
instead of UART so it is the device to use:

```
hcidev = "hci1"
```


To use 'hcitool' to advertise BLE messages in the
Pybricks format I created 4 functions:
 
- prepare_ble_advertise()
- define_ble_advertise()
- initiate_ble_advertise()            
- stop_ble_advertise()

Three of them do not require arguments, they just execute some
pre-defined HCI commands in order to control the BLE
advertisements.

The fourth function ('initiate_ble_advertise()') expects a
4-char string that will be converted to hexacedimal notation
to be embedded in a pre-defined BLE command.

The string has 2 parts:
- a 3-char identifying the model(s) to be addressed
- a 1-char identifying the action to be excecuted

So for now if the dispatcher receives a valid MQTT message it just
just adds a '1' to it and broadcasts it. If the message is 'OWL' it
broadcasts 'OWL1' and all models that are reacting to 'OWL' will
execute action '1'.

For now just '1' doesn't mean anything but I might one day
decide that a model can execute more actions (like '1' to flap wings
in some sequence and '2' to flap wings in some other sequence...
or duration... or whatever).

## Execution

For now I'm just running the script manually:

```
robot@ev3dev:~$ ./bledispatcher.py 
```

I intend to explain how to configure a daemon that executes
it everytime the EV3 boots up.


## The ev3dev installation

I'm using [ev3dev linux](https://www.ev3dev.org/). It's a linux
distribution made for the LEGO MINDSTORMS EV3 (but a version
for the raspberry Pi is also available).

Besides configuring Wi-Fi and activating Bluetooth I just
add to install the python paho-mqtt library

```
pip installl paho-mqtt
```

If you decide to use a Raspberry Pi or other kind of device
you will need to use a proper linux distro (Raspbian is
good enough) that includes bluetooth support (the
BlueZ stack) and python. Of course, Wi-Fi and Bluetooth
Low Energy are needed (the Raspberry Pi 4 and 5 and the W
versions of the Raspberry Pi Zero should work).

If using Raspberry Pi Pico or ESP-32 there is no operating
system so you will need to write your own dispatcher
using MQTT and BLE libraries.


## The Pybricks broadcast message format

I followed the format [documented](https://github.com/pybricks/technical-info/blob/master/pybricks-ble-broadcast-observe.md)
by the Pybricks project.

To keep it simple, I'm using a single object of type STR and length 4.
So I prepare this hcitool message:

```
hci1 cmd 0x08 0x0008 0B 0A FF 97 03 01 00 A4 XX XX XX XX 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```

and if I want to send 'OWL1' I convert it to a string with its
hexadecimal representation:

```
4F 52 4E 31
```

and insert each of the four pairs text in the above XX positions:

```
hci1 cmd 0x08 0x0008 0B 0A FF 97 03 01 00 A4 4F 52 4E 31 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
```


## The Code

This is the script I'm using with the MINDSTORMS EV3:

[EV3 BLE Dispatcher](bledispatcher.py)
