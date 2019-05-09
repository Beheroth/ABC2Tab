# coding: utf-8

import ABC2Tab.AGP as AGP

##### READ PARAMETERS FROM FILES #####
with open ("/home/pi/AGP/note.txt") as f:
    note = int(f.readline())
    print("string: " + str(note + 1))#nb of string begin at 1

##### CALIBRATE #####
arm = AGP.Arm()
#Set the string
arm.changeID(note)
#Move to position
arm.moveTo(1)#replace with arm.calibrate()
