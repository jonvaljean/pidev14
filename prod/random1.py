#!/usr/bin/python
# first time using pycharm see if git works here is a change again
# set column wait to 2 secs to see if it fails less frequently. 1 sec before
# first command in line execution, 1 sec after line command,
# 300 ms before start of check status while loop

from __future__ import print_function
import sys
import time
import smbus  # use smbus for i2c
from time import sleep
import random
import defs
from lw14_class import *
from mapbuild import *

# modify this model according to requirements of setting
NR_ARGS = 4

# run the programm
if __name__ == "__main__":

    DaliBus_Bar1 = lw14()  # commented for testing

    # if some arguments given, use this as data.
    # parm is cycle file name

    if len(sys.argv) == NR_ARGS + 1:
        filename = sys.argv[1]
        onval = int(sys.argv[2])
        offval = int(sys.argv[3])
        sleeptime = float(sys.argv[4])

    # If no arguments ar set or to much send this to dali
    else:
        print("Wrong number of parameters")
        sys.exit(0)
    # build list of addresses from dictionaries to then select from randomly

    boxes = []
    for i in range(2,len(box_dict)): #first two rows are x, y not used
        boxes[i][0]=box_dict.keys()[i]
        boxes[i][1]=box_dict.values()[i]
    print("boxes is   ",boxes)
    # print("net_dict is ",net_dict)
    # print("I2C_values is ",I2C_values)
    # print("grp_dict is  ",grp_dict)


    # print("cmd_list is  ", cmd_list)
    while True:
        sleep(sleeptime)  # instead of this, loop until fade bit is 0

                box_id_key = random.randint(0,len(box_dict))
                cmd_element1 = boxes[box_id_key][0]
                cmd_element2 = 'on'
                # print("cmd_element1, cmd_element2 are:  ", cmd_element1, cmd_element2)
                # print("net_dict value is  ",net_dict[cmd_element1])
                dali_bus = I2C_values[net_dict[cmd_element1]]
                print("dali_bus is  ", dali_bus)
                DaliBus_Bar1.SetI2cBus(dali_bus)
                dali_device = box_dict[cmd_element1 + "1"]  # test status of box 1 of the group
                # print("dali_device before QueryStatus - should be 1st box of group is ",dali_device)
                DaliBus_Bar1.SetDaliAddress(dali_device, defs.LW14_ADR_SINGLE,
                                            defs.LW14_MODE_CMD)  # Set the dali address for command, try query from cmd

                while (1):
                    sleep(0.3)  # lets slow it down a liitle bit
                    res = DaliBus_Bar1.QueryStatus()
                    # debug output
                    print("Status res is ", res)
                    # if fade-in-progress bit is 0 than finished
                    # if res = -1 error on bus, but "ignore and go on"
                    if res == -2:
                        print("res is -2, no data")
                        break
                    if (res & 0x10) == 0x00:
                        print("fading ready")
                        break

                dali_device = box_dict[cmd_element1]
                print("dali_device after while - should be group id is ", dali_device)
                if cmd_element2 == "on": dali_value = onval
                if cmd_element2 == "off": dali_value = offval
                print("dali_bus after while is  ", dali_bus)
                print("dali_value after while is  ", dali_value)
                DaliBus_Bar1.SetI2cBus(dali_bus)
                DaliBus_Bar1.SetDaliAddress(dali_device, defs.LW14_ADR_SINGLE,
                                            defs.LW14_MODE_DACP)  # Set the dali address for send data, in this case single device and DACP bit
                DaliBus_Bar1.SendData(dali_value)  # Send data into the dali bus
                DaliBus_Bar1.WaitForReady()  # Wait until DALI is ready. DON'T FORGET IT!!!!!
                sleep(sleeptime)
                cmd_element2 = 'off'

                if cmd_element2 == "on": dali_value = onval
                if cmd_element2 == "off": dali_value = offval
                print("dali_bus after while is  ", dali_bus)
                print("dali_value after while is  ", dali_value)
                DaliBus_Bar1.SetI2cBus(dali_bus)
                DaliBus_Bar1.SetDaliAddress(dali_device, defs.LW14_ADR_SINGLE,
                    defs.LW14_MODE_DACP)  # Set the dali address for send data, in this case single device and DACP bit
                DaliBus_Bar1.SendData(dali_value)  # Send data into the dali bus
                DaliBus_Bar1.WaitForReady()  # Wait until DALI is ready. DON'T FORGET IT!!!!!
                sleep(sleeptime)