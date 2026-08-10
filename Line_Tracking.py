import RPi.GPIO as GPIO
import time
from Motor import *
from Servo import *

class Line_Tracking:
    def __init__(self):
        self.IR01 = 16
        self.IR02 = 20
        self.IR03 = 21
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                Motor.setMotorModel(1200,1200)
            elif self.LMR==4:
                Motor.setMotorModel(-1500,2500)
            elif self.LMR==6:
                Motor.setMotorModel(-2000,4000)
            elif self.LMR==1:
                Motor.setMotorModel(2500,-1500)
            elif self.LMR==3:
                Motor.setMotorModel(4000,-2000)
            elif self.LMR==7:
                pass
                #Motor.setMotorModel(0,0,0,0)
            
line_Tracking=Line_Tracking()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    servo=Servo()
    servo.setServoPwm('0',90)
    servo.setServoPwm('1',140)    
    try:
        line_Tracking.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        Motor.setMotorModel(0,0)
        servo.setServoPwm('0',90)
        servo.setServoPwm('1',140)
        print ("\nEnd of program")