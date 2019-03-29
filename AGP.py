from time import sleep
from random import randint
from threading import Thread
import RPi.GPIO as GPIO
import smbus

#40Hz - 1kHz
class Arm(Thread):
    id = 0
    wait_freq = 0.0008 #~800Hz
    slider_coeff = 6 #distance for one rotation [cm / rot]
    stepmotor_coeff = 200 #impulses for one rotation [imp / rot]
    distances = {0: 1.75, 1: 5.35, 2: 8.7, 3: 11.85, 4: 14.8, 5: 17.6,
                 6: 20.25, 7: 22.75, 8: 25.15, 9: 27.4, 10: 29.5, 11: 31.5} #distance [cm]

    pins = [[27, 4, 17, 8], [9, 22, 10, 7], [6, 11, 5, 12],
            [26, 13, 19, 20], [15, 14, 18, 16], [25, 23, 24, 21]]

    def __init__(self):
        self.id = Arm.getId()
        super().__init__(name = self.id)
        self.pos = 0
        self.ready = False
        self.tic = 0
        self.bus = smbus.SMBus(1)
        self.address = 0x12

        #Raspberry parameters
        GPIO.setmode(GPIO.BCM)
        self.dir_pin = self.pins[self.id - 1][0]
        self.motor_pin = self.pins[self.id - 1][1]
        self.sleep_pin = self.pins[self.id - 1][2]
        self.sensor_pin = self.pins[self.id -1][3]

        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.sleep_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    #Utility, for testing use!------------------------------#
    def getId():
        Arm.id+=1
        return Arm.id
    #-------------------------------------------------------#

    #Physical based functions-------------------------------#
    def nextTic(self):
        self.strum()
        self.increaseTic()

    def strum(self):
        #PWM to motor, pins in stepmotor_pins
        if self.tic in self.ticlist:
            print("Nothing")
            self.bus.write_byte(self.address, self.id)

    def testStrum(self):
        while True:
            self.bus.write_byte(self.address, self.id)
            sleep(Arm.wait_freq)

    def increaseTic(self):
        self.tic += 1

    def moveMotor(self, forward, impulses):
        #import pdb; pdb.set_trace()
        if forward:
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)

        imp = 0
        GPIO.output(self.sleep_pin, GPIO.HIGH)
        while imp < impulses:
            GPIO.output(self.motor_pin, GPIO.HIGH)
            sleep(Arm.wait_freq) 
            GPIO.output(self.motor_pin, GPIO.LOW)
            sleep(Arm.wait_freq)
            imp+=1
        GPIO.output(self.sleep_pin, GPIO.LOW)

    def synchArm(self):
        self.moveTo(3)
        while not GPIO.input(self.sensor_pin):
            GPIO.output(self.motor_pin, GPIO.HIGH)
            sleep(Arm.wait_freq)
            GPIO.output(self.motor_pin, GPIO.LOW)
            sleep(Arm.wait_freq)

    #-------------------------------------------------------#

    #Run sequence, in order of execution--------------------#
    def setNotes(self, notes, tics):
        self.notes = notes
        self.ticlist = tics
        self.ready = True

    def run(self):
        self.initMovement()
   
    def initMovement(self):
        if self.ready:
            for note in self.notes:
                self.moveTo(note[0])
                while note[1] >= self.tic:
                    sleep(0.1)
        else:
            print("No notes available to play!")

    def moveTo(self, destination):
        print("moving from {} to {}".format(self.pos, destination))
        delta = Arm.distances[destination] - Arm.distances[self.pos]
        impulses = int( (abs(delta) / Arm.slider_coeff) * Arm.stepmotor_coeff )
        self.moveMotor(delta > 0, impulses)
        self.pos = destination
    #-------------------------------------------------------#

class Supervisor:
    def __init__(self):
        self.arms = []
        self.tic_time = 0.3 

    def addArms(self, arms):
        self.arms += arms

    def runArms(self):
        for arm in self.arms:
            arm.start()
        self.tic()

    def tic(self):
        tic = 0
        print("tic " + str(tic))
        sleep(1)
        while tic < 13:
            for arm in self.arms:
                arm.nextTic()
            print("tic " + str(tic))
            tic += 1
            sleep(self.tic_time)

    def synch(self):
        for arm in self.arms:
            arm.synchArm()
            arm.moveTo(1)

    def genRan(self):
        tuples = []
        for tupl in range(12):
            tuples += [(randint(0, 11), tupl)]

        better_tuple = []
        sorting = True
        while sorting:
            if len(tuples) == 1:
                t1, t2 = tuples[0], ['X']
            else:
                t1, t2 = tuples[0], tuples[1]
                
            if t1[0] == t2[0]:
                tuples = tuples[1:]
            else:
                better_tuple += [tuples[0]]
                tuples = tuples[1:]

            if len(tuples) == 0:
                sorting = False

        better_list = []
        for num in range(1, 12):
            if randint(1, 10) <= 7:
                better_list += [num]

        return (better_tuple, better_list)

if __name__ == "__main__":
    supervisor = Supervisor()

    arms = []
    for num in range(1):
        current_arm = Arm()
        current_arm.setNotes(*supervisor.genRan())
        arms += [current_arm]

    supervisor.addArms(arms)
    supervisor.runArms()
