# coding: utf-8

import ABC2Tab.Converter as ABC
import ABC2Tab.AGP as AGP

##### READ PARAMETERS FROM FILES #####
with open ("/home/pi/AGP/song.txt") as f:
    song = f.readline()

path = "songs/" + song


#Stayin'Alive not functional. Spaces still in file
##COde overwrites the string_note_pos.json and causes errors!
conv = ABC.Converter(path)
conv.convert_song()

sup = AGP.Supervisor()

arms = []
for i in range(1, 7):
    a = AGP.Arm()
    notes = conv.get_left(str(i))
    tics  = conv.get_right(str(i))
    a.setNotes(notes, tics)
    arms += [a]

sup.addArms(arms)
sup.quantum(conv.get_quantum())
sup.runArms()