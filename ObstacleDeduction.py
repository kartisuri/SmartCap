import RPi.GPIO as GPIO
import time
from subprocess import call
import pickle

TRIG = 23
ECHO = 24

class ObstacleDeduction():
    def __init__(self):
        self.pulse_start = 0
        self.pulse_end = 0
        self.pulse_duration = 0
        self.prev_msg = None
        self.message = "Please proceed"
        
    @staticmethod
    def setupPickle():
        with open('run_value.pickle', 'wb') as handle:
            pickle.dump(False, handle)

    @staticmethod
    def setupSensor():
        print "Obstacle deduction In Progress..."
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, False)
        print "Waiting For Sensor To Settle"
        time.sleep(2)

    def calculateDistance(self):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            self.pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            self.pulse_end = time.time()
        self.pulse_duration = self.pulse_end - self.pulse_start
        distance = self.pulse_duration * 17150
        distance = round(distance, 2)
        print "Distance: ", distance, "cm"
        return distance

    def processDistance(self, distance):
        if distance <= 80:
            self.message = "Stop! Obstacle in front of you"
        elif distance <= 150:
            self.message = "Please go slow! Obstacle at close range"
        else:
            self.message = "Please proceed"
        if self.message != self.prev_msg:
            sound(self.message)
        self.prev_msg = self.message

def sound(spk):
    print spk
    cmd_beg=" espeak -ven+m7 -s180 -k20 --stdout '"
    cmd_end="' | aplay"
    call ([cmd_beg+spk+cmd_end], shell=True)

def main():
    time.sleep(4)
    sound("Press Right Button to Start and Stop the obstacle deduction")
    ObstacleDeduction.setupPickle()
    od = ObstacleDeduction()
    while True:
        try:
            with open('run_value.pickle', 'rb') as handle:
                run = pickle.load(handle)
        except EOFError:
            continue
        if run:
            print 'start'
            GPIO.setmode(GPIO.BCM)
            ObstacleDeduction.setupSensor()
            distance = od.calculateDistance()
            od.processDistance(distance)
            GPIO.cleanup()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "Program Terminated"
        GPIO.cleanup()
