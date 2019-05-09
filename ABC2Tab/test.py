from AGP import *

s = Supervisor()
a = Arm()

note= ([(1, 1), (2, 2), (3, 3), (4, 4), (1, 5), (3, 6), (2, 7)], [1, 2, 3, 4, 5, 6, 7, 8, 9])
a.setNotes(*note)
def inS():
	s.addArms([a])
	s.runArms()

def q():
	exit()

def freq(f):
	Arm.wait_freq = f
