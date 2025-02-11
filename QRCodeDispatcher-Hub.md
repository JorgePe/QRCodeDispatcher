# QR Code Dispatcher - The HUB Component

## Intro

Each edge device (LEGO model) used in this project must understand
the Pybricks broadcast messaging format.

So if using a LEGO hub, it needs to be flashed with a recent
Pybricks firmware and run a micropython script that observes
messages comming on the same channel that the dispatcher uses
to broadcast - in my examples channel #1

```
city_hub = CityHub(broadcast_channel=0, observe_channels=[1])
```

then the main script is just a loop that keeps observing on
that channel and when something is received it checks
and decides if needs to do something or not:

```
rcv = 0
while True:
    rcv = city_hub.ble.observe(1)
    if rcv != None:
        if rcv == 'OWL1' or rcv == 'ALL1':
            do_something_interesting()
    wait(some_time)
```

in this case the Owl reacts to two codes:
- OWL1
- ALL1

this allows us to use two different QR Codes,
one to address just this Owl (and any other
models that run the same script) and the
other (a wildcard) that address all models
at once.

## Code

I have two examples, one I've been using with the Harry Potter
Owl (with a dedicated City Hub) and other I've used with
a combination of 4 models sharing the same Technic Hub
(please note that this might demand too much current, depending
on the combination of motors used at the same time).

[The Owl](CityHub_Owl.py)

[Technic Hub with 4 models](TechnicHub_4sets.py)
