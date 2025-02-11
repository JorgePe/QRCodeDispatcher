# QRCodeDispatcher
A python based solution to control my LEGO models through QR Codes

## Intro

I needed a way to allow visitors to our LEGO User Group event to
self control some of my LEGO models in a easy way.

Some years ago I made a motorized version of the LEGO Hedwig owl and
managed to control it by sending an e-mail but it required a python
script to be running on my laptop nearby and sending an e-mail is not
so easy for a visitor.

By then it also required a permanent BLE connection between my laptop
and the model which was not pratical and didn't scale up well if
I wanted to control more models.

So now I am using QR Codes: each model has a QR Code near it,
if the visitor wants to see it move just needs to point its
smartphone or tablet to the QR Code.

And I am also using the new Pybricks messaging protocol that allows
broadcasting short BLE messages to or/and from several hubs without
requiring a session. And since several devices can use this method,
a laptop is not needed (even a Raspberry Pi Pico W or a ESP-32 can
be used).

## Implementation

My solution has 3 major components:
- a frontend python web app running on a public web server
- a middleware python script running on a MINDSTORMS EV3 (or a Raspbberry Pi)
- a edge micropython script running on each of my LEGO models

### The frontend

It's just a small web app that serves the links used by the QR Codes
and each time a link is reached it publishes (sends) a MQTT message.

I call it a frontend because it just makes it easy to use MQTT -
any MQTT client can be used to publish a message and surpass the
frontend. Also several clients can be used "simultaneously".

### The middleware

It's also a simple python script that keeps waiting for the proper
MQTT messages to arrive and generates a short duration BLE
advertisement using Pybricks broadcast messaging format.

It advertises a short string that identifies
the model(s) to be reached and the action to be executed and after
a very short period - just enough to ensure the model(s) noticed it -
it stops advertising.

### The edge

It's an even simpler micropython script that waits for a BLE
advertisement to be made, checks if its addressed to this model
and executes a pre-definied action (tipically a very simple action,
like flapping the wings for a couple of seconds)

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

The file ['QRCodeDispatcher-WebApp'](QRCodeDispatcher-WebApp.md) has more details about the web app component.

### The Middleware

I am using a LEGO MINDSTORMS EV3 with a USB 4-port USB hub to connect a Wi-Fi dongle and a Bluetooth
5.0 dongle (a 4.0 version should also work, aslong as it supports BLE).

It has a microSD card with ev3dev installed. Will detail it latter.

To keep it 'always on' I'm using a battery conected to a wall charger as an UPS.

The file ['QRCodeDispatcher-EV3'](QRCodeDispatcher-EV3.md) has more details about the middleware component.

### The Edge

Any LEGO Powered Up hub that supports Pybricks should work.
I've used the City Hub and the Technic Hub.

The file ['QRCodeDispatcher-Hub'](QRCodeDispatcher-Hub.md) has more details about the edge component.

