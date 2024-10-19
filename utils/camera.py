import cv2
import time
from datetime import datetime

fps = 0
current_time = ""

def generate_frames(camera_slot):
    global fps, current_time
    camera = cv2.VideoCapture(camera_slot)
    prev_time = time.time()

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def get_camera_info(camera_slot):
    global fps, current_time
    camera_framerate = fps
    time_info = current_time

    return {
        'camera_slot': camera_slot,
        'camera_framerate': int(camera_framerate),
        'current_time': time_info
    }
