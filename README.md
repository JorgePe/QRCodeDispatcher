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

And I am also using the new
[Pybricks messaging protocol](https://github.com/pybricks/technical-info/blob/master/pybricks-ble-broadcast-observe.md)
that allows broadcasting short BLE messages to or/and from several
hubs without requiring a session. And since several devices can use
this method, a laptop is not needed (even a Raspberry Pi Pico W or a
ESP-32 can be used).

## Proof of concept

A simple scenario with just one model connected to a Technic Hub:

[![LEGO QR Code Dispatcher and The Flying Machine](http://img.youtube.com/vi/gV378WmPev0/0.jpg)](http://www.youtube.com/watch?v=gV378WmPev0 "LEGO QR Code Dispatcher and The Flying Machine")

In this PoC I'm using just one model with just one motor so not making
any use of the remaining 3 ports of the Technic Hub. With just minor
adaptions in the code running in the Hub it is possible to extend it
to 4 one-motor models or 1 four-motor model or any combination in
between.

A somewhat more complex scenario with 5 models and 2 hubs:
- a City Hub dedicated to the Harry Potter' Hedwig the Owl
- a Technic Hub shared by 4 one-motor models:
  - the Leonardo da Vincy Flying Machine
  - the Harry Potter Fawkes, Dumbledore’s Phoenix
  - the Harry Potter Hungarian HorntailDragon
  - the Technic Orrery

[![LEGO QR Code Dispatcher and 5 motorizes sets](http://img.youtube.com/vi/DmP8MC4a8qc/0.jpg)](http://www.youtube.com/watch?v=DmP8MC4a8qc "LEGO QR Code Dispatcher and 5 motorizes sets")

in this scenario I have a QR Code for each of the models and 
an extra QR Code, a wildcard command. Both hubs react to each
single model command and also to the wildcard command so
it is possible (not exactly desired) to activate all models
at once.

Other codes can be implemented, like a code to activate all
"birds" and a code to activate all "machines".

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

I decided to use a python flask web app. Flask is very easy to use
for quick development on my laptop and there are some sites that offer
hosting services for flask apps so I don't need to install or
mantain my own server.

I'm using PythonAywhere, it's free for small web apps but I needed
to upgrade for a paid license to get MQTT connectivity to a
public mosquitto broker.

The file ['QRCodeDispatcher-WebApp'](QRCodeDispatcher-WebApp.md) has
more details about the web app component.


### The middleware

It's also a simple python script that keeps waiting for the proper
MQTT messages to arrive and generates a short duration BLE
advertisement using Pybricks broadcast messaging format.

It advertises a short string that identifies
the model(s) to be reached and the action to be executed and after
a very short period - just enough to ensure the model(s) noticed it -
it stops advertising.

I am using a LEGO MINDSTORMS EV3 but the script can be used on
a Raspberry Pi board or a computer running linux. No BLE library
is needed aslong as the linux has the BlueZ stack with the 'hcitool'
command.

The EV3 boots from a microSD card with [ev3dev linux](https://www.ev3dev.org/)
installed.

For the EV3 communications I use a small USB 4-port USB hub and 2
USB dongles:
- a Wi-Fi network adapter
- a BT BLE adapter

The BT BLE adapter is an Asus USB-BT500, it support BT 5.0 specs but a
4.0 version should also work, aslong as it supports BLE.

No drivers were needed - ev3dev recognizes both devices.

To keep it 'always on' I'm using a battery conected to a wall charger
as an UPS.

Just a reminder: I'm using a public MQTT broker (test.mosquitto.org)
to simplify my solution but if desired/required a private broker
can be used. The ev3dev image already includes a mosquitto broker and it can
run a light web server so in a closed scenario (with no connection to
the internet) both frontend and middleware could run (very slowly) on the EV3.

The file ['QRCodeDispatcher-EV3'](QRCodeDispatcher-EV3.md) has more
details about the middleware component.


### The edge

It's an even simpler micropython script that waits for a BLE
advertisement to be made, checks if its addressed to this model
and executes a pre-definied action (tipically a very simple action,
like flapping the wings for a couple of seconds)

Any LEGO Powered Up hub that supports [Pybricks](https://pybricks.com/)
should work (technically even non LEGO devices should work, aslong as they
understand the
[Pybricks broadcast messaging format](https://github.com/pybricks/technical-info/blob/master/pybricks-ble-broadcast-observe.md)).

I've used the City Hub and the Technic Hub.

The file ['QRCodeDispatcher-Hub'](QRCodeDispatcher-Hub.md) has more details
about the edge component.
