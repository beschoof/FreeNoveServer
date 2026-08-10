import RPi.GPIO as GPIO
import time
from Motor import *
from Servo import *
from Ultrasonic import *
from Action import *
from Line_Tracking import *

class Remove_Obstacles:
    def __init__(self):
        self.IR01 = 16
        self.IR02 = 20
        self.IR03 = 21
        self.servo=Servo()
        self.Motor=Motor()
        self.distance=Ultrasonic()
        self.infrared=Line_Tracking()
        self.servoMode=ServoMode()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
    def run_Move(self):
        self.servoMode.ServoMode('1')
        self.Motor.setMotorModel(-1500,1500)        #Left 
        time.sleep(1.5)
        self.Motor.setMotorModel(0,0)               #Stop
        self.servoMode.ServoMode('2')
        self.Motor.setMotorModel(1500,-1500)        #Right
        time.sleep(1.4)

    def run_Line(self):
        self.LMR=0x00
        if GPIO.input(self.IR01)==True:
            self.LMR=(self.LMR | 4)
        if GPIO.input(self.IR02)==True:
            self.LMR=(self.LMR | 2)
        if GPIO.input(self.IR03)==True:
            self.LMR=(self.LMR | 1)
        if self.LMR==2:
            self.Motor.setMotorModel(1200,1200)    #Forward
        elif self.LMR==4:
            self.Motor.setMotorModel(-1500,2500)   #Left 
        elif self.LMR==6:
            self.Motor.setMotorModel(-2000,4000)   #Left 
        elif self.LMR==1:
            self.Motor.setMotorModel(2500,-1500)   #Right
        elif self.LMR==3:
            self.Motor.setMotorModel(4000,-2000)   #Right
        elif self.LMR==7:
            pass
        
    def run_Action(self):
        distance=self.distance.get_distance()
        #print ("Obstacle distance is "+str(distance)+"CM")
        self.run_Line()
        if(distance > 5.0 and distance <= 12.0):
            self.Motor.setMotorModel(0,0)          #Stop
            time.sleep(0.01)
            self.run_Move()
        elif(distance > 0.0 and distance <= 5.0):
            self.Motor.setMotorModel(-1200,-1200)  #Back
            
    def run(self):
        time.sleep(1.5)
        while True:
            self.run_Action()            
            
remove_Obstacles=Remove_Obstacles()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        remove_Obstacles.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        remove_Obstacles.Motor.setMotorModel(0,0) #Stop
        remove_Obstacles.servo.setServoPwm('0',90)
        remove_Obstacles.servo.setServoPwm('1',140)
        print ("\nEnd of program")