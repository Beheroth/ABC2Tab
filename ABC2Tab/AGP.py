from time import sleep
from random import randint
from threading import Thread
import RPi.GPIO as GPIO
import smbus

#Arm that will manipulate one of six strings, commands a Servo and a StepMotor
class Arm(Thread):
    id = 0
    wait_freq = 0.0008 #~800Hz
    slider_coeff = 6 #distance for one rotation [cm / rot]
    stepmotor_coeff = 200 #impulses for one rotation [imp / rot]
    distances = {0: 1.75, 1: 5.35, 2: 8.7, 3: 11.85, 4: 14.8, 5: 17.6,
                 6: 20.25, 7: 22.75, 8: 25.15, 9: 27.4, 10: 29.5, 11: 31.5} #distance on guitar[cm]
    
    pins = [[27, 4, 17, 8], [9, 22, 10, 7], [6, 11, 5, 12],
            [26, 13, 19, 20], [15, 14, 18, 16], [25, 23, 24, 21]]

    def __init__(self):
        self.id = Arm.getId()
        super().__init__(name = self.id)
        self.pos = 0
        self.ready = False
        self.tic = 0
        self.ticlist = []
        self.bus = smbus.SMBus(1)
        self.address = 0x12 #Arduino slave address
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.initGPIO()

    def initGPIO(self):
        #Raspberry parameters
        self.dir_pin   = self.pins[self.id - 1][0]
        self.motor_pin = self.pins[self.id - 1][1]
        self.sleep_pin = self.pins[self.id - 1][2]
        self.sensor_pin = self.pins[self.id -1][3]

        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.motor_pin, GPIO.OUT)
        GPIO.setup(self.sleep_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN)

    #Utility, for testing use!------------------------------#
    #Attributes an different ID for every new arm created
    def getId():
        Arm.id+=1
        return Arm.id

    #Allows user to change ID of an Arm. Allows for debugging and
    #moving/strumming different arms
    def changeID(self, ident):
        self.id = ident
        self.name = "test"
        Arm.id = 0
        self.pos= 0
        self.initGPIO()
    #-------------------------------------------------------#

    #Physical based functions-------------------------------#
    def nextTic(self):
        self.strum()
        self.increaseTic()

    #Commands Arduino to activate ServoMotor
    def strum(self, manual = False):
        #PWM to motor, pins in stepmotor_pins
        if self.tic in self.ticlist or manual:
            self.bus.write_byte(self.address, self.id)
    
    #Infinite loop to test Servos
    def testStrum(self):
        while True:
            self.bus.write_byte(self.address, self.id)
            sleep(Arm.wait_freq)

    #Increase tics to keep track of the time and position on the music sheet
    def increaseTic(self):
        self.tic += 1

    #Used to move the stepmotor, example: self.moveMotor(True, 200), great for testing
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

    #Use the sensor pin to recalibrate all arms
    def synchArm(self):
        self.moveTo(3)
        while not GPIO.input(self.sensor_pin):
            GPIO.output(self.motor_pin, GPIO.HIGH)
            sleep(Arm.wait_freq)
            GPIO.output(self.motor_pin, GPIO.LOW)
            sleep(Arm.wait_freq)

    #-------------------------------------------------------#

    #Run sequence, in order of execution--------------------#
    #Give the arm all the notes it will play before it's ready to run
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

    #Move the arm to a set position on the guitar, calculated number of impulses may be inaccurate
    def moveTo(self, destination):
        print("moving from {} to {}".format(self.pos, destination))
        delta = Arm.distances[destination] - Arm.distances[self.pos]
        print("Distance: ", delta)
        impulses = int( (abs(delta) / Arm.slider_coeff) * Arm.stepmotor_coeff )
        print("Impulses: ", impulses)
        self.moveMotor(delta > 0, impulses)
        self.pos = destination
    #-------------------------------------------------------#

#Will command all 6 Arms and will be in charge of time synchronisation through tics
class Supervisor:
    def __init__(self):
        self.arms = []
        self.tic_time = 2 

    def addArms(self, arms):
        self.arms += arms

    def runArms(self):
        for arm in self.arms:
            arm.start()
        self.tic()

    #In charge of keeping track of tics for all arms
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

    #Synchs all arms
    def synch(self):
        for arm in self.arms:
            arm.synchArm()
            arm.moveTo(1)

    #Generate a random array of notes/tics and tics, see usage below
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
    for num in range(3):
        current_arm = Arm()
        #note= ([(1, 1), (2, 2), (3, 3), (4, 4), (1, 5), (3, 6), (2, 7)], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        note = supervisor.genRan()
        current_arm.setNotes(*note)
        arms += [current_arm]

    supervisor.addArms(arms)
    supervisor.runArms()
