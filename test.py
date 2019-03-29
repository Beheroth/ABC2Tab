from AGP import *

s = Supervisor()
a = Arm()

def inS():
	s.addArms([a])

def q():
	exit()

def freq(f):
	Arm.wait_freq = f
