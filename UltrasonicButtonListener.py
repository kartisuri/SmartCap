import RPi.GPIO as GPIO
import time
import pickle

prev_inp = 1
GPIO_switch = 25
run = False

def listener():
    global run, prev_inp, p
    while True :
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(GPIO_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        inp = GPIO.input(GPIO_switch)
        if (not prev_inp) and  inp:
            print "Button pressed"
            run = not run
            with open('run_value.pickle', 'wb') as handle:
                pickle.dump(run, handle)
            print run
        prev_inp = inp
        time.sleep(0.05)

if __name__ == '__main__':
    try:
        listener()
    except KeyboardInterrupt:
        print "  Quit"
        GPIO.cleanup()
