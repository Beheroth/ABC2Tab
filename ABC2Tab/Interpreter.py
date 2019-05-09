#Use with "python3 -i Interpreter.py" in cmd
#Comment out all unsuported library usages in AGP to test without Raspberry

#Allows you to use a as an Arm object and s as a Supervisor object in terminal
#useful functions: 	s.genRan()
#					s.addArms([Arm])	|
#					s.runArms()			|=> or just use inS()	
#					a.changeID(Int)
#					a.moveTo(Int)
#					a.moveMotor(Boolean, Int)
#					a.synchArms()
#					a.strum()
#					a.testStrum()

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
