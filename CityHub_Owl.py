from pybricks.hubs import CityHub
from pybricks.parameters import Button, Direction, Port
from pybricks.pupdevices import DCMotor
from pybricks.tools import wait

city_hub = CityHub(broadcast_channel=0, observe_channels=[1])
mOwl = DCMotor(Port.A, Direction.COUNTERCLOCKWISE)

rcv = 0

while True:
    rcv = city_hub.ble.observe(1)
    if rcv != None:
        print(rcv)
        if rcv == 'OWL1' or rcv == 'ALL1':
            mOwl.dc(75)
            wait(7000)
            mOwl.stop()

    wait(25)    # 10 not enough
