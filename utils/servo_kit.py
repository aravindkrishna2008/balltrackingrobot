# Import libraries
import RPi.GPIO as GPIO
import time

class ServoKit():
    def __init__(self, horizontal_pin, verticle_pin):
        self.horizontal_pin = horizontal_pin
        self.verticle_pin = verticle_pin
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(horizontal_pin,GPIO.OUT)
        self.verticleServo = GPIO.PWM(horizontal_pin, 50)
        
        GPIO.setup(verticle_pin, GPIO.OUT)
        self.horizontalServo = GPIO.PWM(verticle_pin, 50)
        
        self.verticleServo.start(0)
        self.horizontalServo.start(0)
    
    def setVerticle(self, angle):
        self.verticleServo.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        self.verticleServo.ChangeDutyCycle(0)
    
    def setHorizontal(self, angle):
        angle = angle+90
        self.horizontalServo.ChangeDutyCycle(2+(angle/18))
        time.sleep(0.5)
        self.horizontalServo.ChangeDutyCycle(0)
        
    def moveHorizontal(self):
        self.horizontalServo.ChangeDutyCycle(12)
    
    def estop(self):
        self.verticleServo.stop()
        self.horizontalServo.stop()
        GPIO.cleanup()
        
        

        
if __name__ == "__main__":
    servokit = ServoKit(2, 3)
    servokit.setHorizontal(90)
    servokit.setVerticle(90)
    time.sleep(2)
    servokit.estop()

