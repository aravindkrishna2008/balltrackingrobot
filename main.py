import sys
sys.path.insert(0, '/home/aravind/balltrackingrobot/utils')


from picamera2 import Picamera2, Preview
import cv2
from flask import Flask, Response, request
from flask_cors import CORS
import threading
import time
from process import process
from motor import DCMotor
from ultrasonic import UltrasonicSensor
import math
from servo_kit import ServoKit

from led import LEDMatrix

app = Flask(__name__)
CORS(app)

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (1920, 1080), "format": "RGB888"},
    lores={"size": (640, 480), "format": "YUV420"},
    display="lores"
)
picam2.configure(camera_config)
picam2.start()

motor = DCMotor(a1b_pin=24, a1a_pin=23, b1b_pin=22, b1a_pin=27)
# ultrasonic1 = UltrasonicSensor(echo_pin=0, trigger_pin=5, threshold_distance=0.5)
ultrasonic2 = UltrasonicSensor(echo_pin=26, trigger_pin=19, threshold_distance=0.5)
ultrasonic3 = UltrasonicSensor(echo_pin=0, trigger_pin=5, threshold_distance=0.5)
servokit = ServoKit(2, 3)
matrix = LEDMatrix()

auto_detect = False
# 1 is right -1 is left
past_ball_loc = 1

# matrix.show_welcome("Hello World! Ball Tracking Robot")

def motorThread(x, y, r, ww, hh, past_ball_loc=1):
    print("motor thread")
    posx = x-ww/2
    posy = y
    theta = 0;
    if (posy != 0):
        theta = math.atan(posx/posy)*180/math.pi
    print("theta" + str(theta))
    if (r < 10):
        if (past_ball_loc == 1):
            motor.turn_right(20)
            time.sleep(0.5)
        else:
            motor.turn_left(20)
            time.skeep(0.5)
    elif (theta > 45):
        print("motor clockwise")
        motor.turn_right(10)
        past_ball_loc = 1
    elif (theta < -45):
        print("motor anticlockwise")
        motor.turn_left(10)
        past_ball_loc = -1
    else:
        print("motor forward")
        motor.set_motor_speed(0, 100)
        time.sleep(2)
        
def ultrasonicThread():
    return ultrasonic2.get_distance_cm(), ultrasonic3.get_distance_cm()

def generate_frames():
    global auto_detect
    frame_count = 0
    start_time = time.time()
    while True:
        frame = picam2.capture_array()
        x, y, r, ww, hh, result = process(frame)
        u2, u3 = ultrasonicThread()
        # matrix.show_verticle_message(f"U1 {u2}cm U2 {u3}cm")
        if (auto_detect == True):
            motorThread(x,y,r,ww,hh, past_ball_loc)
            print(u2, u3)
            if ((u2 < 15 or u3 < 15) and r > 15):
                print("reached")
                motor.stop_motor(0)
                time.sleep(5)
                
        _, buffer = cv2.imencode('.jpg', result)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        frame_count += 1
        if frame_count == 30:  # Calculate FPS every 30 frames
            end_time = time.time()
            fps = frame_count / (end_time - start_time)
            print(f"FPS: {fps:.2f}")
            frame_count = 0
            start_time = time.time()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/angle/<verticle>/<horizontal>')
def angle(verticle, horizontal):
    print(verticle, horizontal)
    servokit.setVerticle(int(verticle))
    time.sleep(0.5)
    servokit.setHorizontal(int(horizontal))

@app.route('/move/<direction>')
def move(direction):
    global auto_detect
    if direction == 'auto':
        auto_detect = not auto_detect
    elif direction == 'up':
        motor.set_motor_speed(0,100)
    elif direction == 'down':
        motor.set_motor_speed(0,-100)
    elif direction == 'right':
        motor.turn_right(10)
    elif direction == 'left':
        motor.turn_left(10)
    elif direction == 'stop':
        motor.stop_motor(0)
    elif direction == 'estop':
        motor.cleanup()
        
    return f"Moving {direction}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
