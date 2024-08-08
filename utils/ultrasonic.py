from gpiozero import DistanceSensor
import time

class UltrasonicSensor:
    def __init__(self, echo_pin, trigger_pin, threshold_distance=0.5):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, threshold_distance=threshold_distance)
    
    def get_distance_cm(self):
        return self.sensor.distance * 100
    
    def get_distance_m(self):
        return self.sensor.distance
    
    def wait_for_in_range(self):
        self.sensor.wait_for_in_range()
    
    def wait_for_out_of_range(self):
        self.sensor.wait_for_out_of_range()

# Test script
if __name__ == "__main__":
    try:
        # ultrasonic1 = UltrasonicSensor(echo_pin=13, trigger_pin=6, threshold_distance=0.5)
        ultrasonic2 = UltrasonicSensor(echo_pin=26, trigger_pin=19, threshold_distance=0.5)
        ultrasonic3 = UltrasonicSensor(echo_pin=0, trigger_pin=5, threshold_distance=0.5)
        print("Distance measurement in progress. Press Ctrl+C to stop.")
        while True:
            # print("sonic1 " + str(ultrasonic1.get_distance_cm()))
            print("sonic2 " + str(ultrasonic2.get_distance_cm()))
            print("sonic3 " + str(ultrasonic3.get_distance_cm()))
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user")
    finally:
        print("Cleaning up...")