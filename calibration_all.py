# coding: utf-8

import ABC2Tab.AGP as AGP

##### CALIBRATE #####
arm = AGP.Arm()

for string in range(6):
    #Set the string
    arm.changeID(string)
    #Move to position
    arm.moveTo(1)#replace with arm.calibrate()
