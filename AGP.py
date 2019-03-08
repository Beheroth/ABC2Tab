from time import sleep
from random import randint
from threading import Thread
from colorama import init, Fore, Style
from rprint import print
import RPi.GPIO as GPIO
import smbus

#40Hz - 1kHz
class Arm(Thread):
    id = 0
    colors = [Fore.RED, Fore.GREEN, Fore.BLUE,
              Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
    wait_freq = 0.005 #~800Hz
    slider_coeff = 6 #distance for one rotation [cm / rot]
    stepmotor_coeff = 200 #impulses for one rotation [imp / rot]
    stepmotor_pins  = [11, 13, 15, 19, 21, 23]
    distances = {0: 1.75, 1: 5.35, 2: 8.7, 3: 11.85, 4: 14.8, 5: 17.6,
                 6: 20.25, 7: 22.75, 8: 25.15, 9: 27.4, 10: 29.5, 11: 31.5} #distance [cm]

    pins = [[1, 1], [1, 1], [1, 1],
            [1, 1], [1, 1], [1, 1]]

    impulses = {}
    for key in distances:
        impulses[key] = (distances[key] / slider_coeff) * stepmotor_coeff
    def __init__(self):
        self.id = Arm.getId()
        super().__init__(name = self.id)
        self.color = Arm.colors[self.id - 1] 
        self.pos = 0
        self.ready = False
        self.tic = 0
        self.IMPULSES_PER_DISTANCE = 1
        self.bus = smbus.SMBus(1)
        self.address = 0x12
        self.pprint('Initialized arm {}')

        #Raspberry parameters
        GPIO.setmode(GPIO.BCM)
        self.dir_pin = pins[self.id - 1][0]
        self.motor_pin = pins[self.id - 1][1]
        self.sensor_pin = 1

        GPIO.setup(self.dirPin, GPIO.OUT)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    #Utility, for testing use!------------------------------#
    def getId():
        Arm.id+=1
        return Arm.id

    def pprint(self, string):
        print(self.color + string.format(self.id) + '\r',
              flush=True)
        #print(string.format(self.id))
    #-------------------------------------------------------#

    #Physical based functions-------------------------------#
    def nextTic(self):
        self.strum()
        self.increaseTic()

    def strum(self):
        #PWM to motor, pins in stepmotor_pins
        self.pprint("strum string {}")
        if self.tic in self.ticlist:
            print("Nothing")
            self.bus.write_byte(self.address, self.id)

    def increaseTic(self):
        self.tic += 1

    def moveMotor(self, forward, impulses):
        if forward:
            GPIO.output(self.dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)

        imp = 0
        while imp < impulses:
            GPIO.output(self.motor_pin, GPIO.HIGH)
            sleep(Arm.wait_freq) 
            GPIO.output(self.motor_pin, GPIO.LOW)
            sleep(Arm.wait_freq)
            imp+=1

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
        self.pprint('Running arm {}')
        self.initMovement()
    
    def initMovement(self):
        if self.ready:
            self.pprint(str(self.notes))
            for note in self.notes:
                self.pprint("from " + str(self.pos) + " to " + str(note[0]) + " until " + str(note[1]))
                self.moveTo(note[0])
                while note[1] >= self.tic:
                    sleep(0.1)
        else:
            self.pprint("No notes available to play!")

    def moveTo(self, destination):
        delta = self.pos - destination
        impulses = abs(delta * self.IMPULSES_PER_DISTANCE)
        self.pprint('Arm {}: '+'{} impulses'.format(impulses))
        self.moveMotor(delta > 0, impulses)
        self.pos = destination
    #-------------------------------------------------------#

class Supervisor:
    def __init__(self):
        self.arms = []
        self.tic_time = 1

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
            tuples += [(randint(-1, 3), tupl)]

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
    init()
    supervisor = Supervisor()

    arms = []
    for num in range(2):
        current_arm = Arm()
        current_arm.setNotes(*supervisor.genRan())
        arms += [current_arm]

    supervisor.addArms(arms)
    supervisor.runArms()
