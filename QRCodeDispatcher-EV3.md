# QR Code Dispatcher - The Middleware

## Intro

The device running as a dispatcher must subscribe
to a MQTT topic and send BLE messages accordingly.

The payload of the MQTT messages is kept very simple,
just a few messages are expected:

```
list_of_messages = ['ALL', 'ORN', 'OWL', 'PHO', 'DRA', 'ORR']
```

The message is used to address a specific model (like 'OWL')
or all models at once (like 'ALL') and I just add an extra
character (for now just '1') in case iI ever decide that
a model can execute more actions (like '1' to flap wings
in some sequence and '2' to flap wings in some other sequence...
or duration... or whatever).

Since I am using the MINDSTORMS EV3 with ev3dv linux and
there aren't many python BLE libraries and even less libraries
(if any) that can be used with the few resources of the
EV3 I'm using system calls to the linux command 'hcitool'.
Not pretty but it works.

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

For now I'm just running the script manually. I intend to later
explain hot to configure a daemon that executes it everyime
the EV3 boots up.

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
