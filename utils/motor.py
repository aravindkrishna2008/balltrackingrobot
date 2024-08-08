import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self, a1a_pin, a1b_pin, b1a_pin, b1b_pin):
        self.motor1_pins = (a1a_pin, a1b_pin)
        self.motor2_pins = (b1a_pin, b1b_pin)
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor1_pins, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.motor2_pins, GPIO.OUT, initial=GPIO.LOW)

    def set_motor_speed(self, motor, speed):
        if motor == 0:
            self._set_motor_speed(self.motor1_pins, speed)
            self._set_motor_speed(self.motor2_pins, speed)
        elif motor == 1:
            self._set_motor_speed(self.motor1_pins, speed)
        elif motor == 2:
            self._set_motor_speed(self.motor2_pins, speed)
        else:
            raise ValueError("Motor number should be 1 or 2")

    def _set_motor_speed(self, pins, speed):
        pin1, pin2 = pins
        if speed > 0:
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.output(pin2, GPIO.LOW)
        elif speed < 0:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.HIGH)
        else:
            GPIO.output(pin1, GPIO.LOW)
            GPIO.output(pin2, GPIO.LOW)

    def stop_motor(self, motor):
        if motor == 0:
            self._stop_motor(self.motor1_pins)
            self._stop_motor(self.motor2_pins)            
        elif motor == 1:
            self._stop_motor(self.motor1_pins)
        elif motor == 2:
            self._stop_motor(self.motor2_pins)
        else:
            raise ValueError("Motor number should be 1 or 2")

    def _stop_motor(self, pins):
        pin1, pin2 = pins
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()

    def turn_left(self, degrees):
        self.set_motor_speed(1, -50)
        self.set_motor_speed(2, 50)
        
        turn_duration = degrees * 0.01
        
        time.sleep(turn_duration)
        self.stop_motor(0)

    def turn_right(self, degrees):
        self.set_motor_speed(1, 50)
        self.set_motor_speed(2, -50)
        
        turn_duration = degrees * 0.008
        
        time.sleep(turn_duration)
        self.stop_motor(0)

if __name__ == "__main__":
    motor_driver = DCMotor(a1b_pin=24, a1a_pin=23, b1b_pin=22, b1a_pin=27)
    try:
        # motor_driver.set_motor_speed(0,100)
        motor_driver.turn_right(90)
        # time.sleep(10)

    finally:
        motor_driver.cleanup()