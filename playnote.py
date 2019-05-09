# coding: utf-8
import ABC2Tab.AGP as AGP

##### READ PARAMETERS FROM FILES #####
with open ("/home/pi/AGP/note.txt") as f:
    note = int(f.readline())
    print("string: " + str(note))#nb of string begin at 1

with open ("/home/pi/AGP/slider.txt") as f:
    pos = int(f.readline())
    print("position: " + str(pos))

##### MOVE & PLAY #####
arm = AGP.Arm()
#Set the string
arm.changeID(note)
#Move to position

import time; time.sleep(2)
arm.moveTo(pos)
#Play the note

time.sleep(1)
#arm.strum(True)
arm.moveTo(0)
