from pybricks.hubs import TechnicHub
from pybricks.tools import wait
from pybricks.pupdevices import Motor, DCMotor
from pybricks.parameters import Port, Stop, Direction, Button, Color

technic_hub = TechnicHub(broadcast_channel=0, observe_channels=[1])

mOrnith = Motor(Port.A)

mPhoenix = DCMotor(Port.B)    # Phoenix can use a weaker motor but at the limit
                              # and only negative direction
                              # better to replace for a better motor
mOrrery = Motor(Port.C)

mHungarian = Motor(Port.D)    # Hungarian Dragon need stronger motor

# Initialize variables.
rcv = 0

while True:
    rcv = technic_hub.ble.observe(1)
    if rcv != None:
        print(rcv)            
        if rcv == 'ORN1':
            for i in range(0,6):
                mOrnith.dc(-30)
                wait(800)
                mOrnith.dc(100)
                wait(1100)
            mOrnith.stop()
        elif rcv == 'PHO1':
            mPhoenix.dc(-100)
            wait(8000)
            mPhoenix.stop()
        elif rcv == 'ORR1':
            mOrrery.dc(-50)
            wait(8000)
            mOrrery.stop()
        elif rcv == 'DRA1':
            mHungarian.dc(65)
            wait(8000)
            mHungarian.stop()            
        elif rcv == 'ALL1':
            # activate PHO, ORR and DRA
            # then oscilate ORN 5x
            # at then stop all
            mPhoenix.dc(-100)
            mOrrery.dc(-50)
            mHungarian.dc(65)

            for i in range(0,6):
                mOrnith.dc(-30)
                wait(800)
                mOrnith.dc(100)
                wait(1100)
            mOrnith.stop()

            mPhoenix.stop()
            mOrrery.stop()
            mHungarian.stop()
        else:
            pass
    else:
        pass
    wait(17)    # 10..30 but not perfect yet

