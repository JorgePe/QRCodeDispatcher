# QRCodeDispatcher
A python based solution to control LEGO models through QR Codes

## Intro

I needed a way to allow visitors to our LEGO User Group event to
self control some of my LEGO models in a easy way.

Some years ago I made a motorized version of the LEGO Hedwig owl and
managed to control it by sending an e-mail but it required a python
script to be running on my laptop near and sending an e-mail is not
so easy for a visitor

So now I am using QR Codes: each model has a QR Code near it,
if the visitor wants to see it move just needs to point its
smartphone or tablet to the QR Code.

## Implementation

My solution has 3 components:
- a frontend python web app running on a public web server
- a middleware python script running on a MINDSTORMS EV3 (or a Raspbberry Pi)
- a edge micropython script running on each of my LEGO models

The frontend web app just serves the links used by the QR Codes and
each time a link is reached it sends a MQTT message.

The middleware script keeps waiting for the proper MQTT messages to
arrive and generates a Bluetooth Low Energy advertisement using
Pybricks broadcast messaging format with a simple 4-char payload:

+ the first 3 chars specify which model(s) should be
addressed
+ the last char specifies the action to execute

The edge micropython script is just a Pybricks script that
waits for a broadcast message to arrive, checks if it has the
proper payload and executes a pre-definied action (usually a 
very simple action, like flapping the wings for a couple of
seconds)

## Proof of concept

1 model connected to a Technic Hub:

[![LEGO QR Code Dispatcher and The Flying Machine](http://img.youtube.com/vi/gV378WmPev0/0.jpg)](http://www.youtube.com/watch?v=gV378WmPev0 "LEGO QR Code Dispatcher and The Flying Machine")

In this example I'm using just one model with just one motor so it is possible the 3 available connectors for 3
other one-moter models (all reacting to the same payload or each one reacting to a different payload).

## Detailed explanation

### The Frontend

I decided to use a python flask web app. Flask is very easy to use for quick deploy on my laptop
and there are some sites that offer hosting services for flask apps so I don't need to install or
mantain my own server.
I'm using PythonAywhere, it's free for small web apps but I needed to register for a paid license
to get MQTT connectivity to the mosquitto broker.

### The Middleare

I am using a LEGO MINDSTORMS EV3 with a USB 4-port USB hub to connect a Wi-Fi dongle and a Bluetooth
5.0 dongle (a 4.0 version should also work, aslong as it supports BLE).

It has a microSD card with ev3dev installed. Will detail it latter.

To keep it 'always on' I'm using a battery conected to a wall charger as an UPS.

### The Edge

Any LEGO Powered Up hub that supports Pybricks should work.
I've used the City Hub and the Technic Hub.
