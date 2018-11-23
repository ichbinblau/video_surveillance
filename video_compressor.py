import time
import redis
import json
import os
import cv2
import pickle
import subprocess
from mqtt_pub_sub import MqttClient

CAMERA_REQUEST_VID_WIDTH = 640
CAMERA_REQUEST_VID_HEIGHT = 480
OUTPUT_RATE = 20
VIDEO_SERVER_PATH = "web/video/"

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def convert2mp4(filename):
    subprocess.call([
        'ffmpeg',
        '-loglevel', 'panic',
        '-i', filename,
        '-an',
        '-vcodec', 'libx264',
        '-crf', '24',
        "{}_h264.mp4".format(os.path.splitext(filename)[0])
        ])


def frames2video(cam_id, timestamp):
    start = time.time()
    filename = os.path.join(VIDEO_SERVER_PATH, "cam{}_{}.mp4".format(cam_id, timestamp))
    print(filename)
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fourcc = 0x00000021
    video_writer = cv2.VideoWriter(filename, fourcc, OUTPUT_RATE, (CAMERA_REQUEST_VID_WIDTH, CAMERA_REQUEST_VID_HEIGHT))

    key = "cam{}".format(cam_id)
    #print(key, timestamp, timestamp-10000, timestamp+10000)
    obj_lst = r.zrangebyscore(key, timestamp-8000, timestamp+8000)
    print("Video length: {} seconds".format(len(obj_lst)//OUTPUT_RATE))
    for frame in obj_lst:
        video_writer.write(pickle.loads(frame))

    video_writer.release()
    #mid = time.time()
    #convert2mp4(filename)
    end = time.time()
    print("Time consumed for converting {} is {} seconds".format(filename, end-start))


def on_message(client, userdata, message):
    # print("%s %s" % (message.topic, message.payload))
    payload = json.loads(message.payload.decode())
    print(payload)
    try:
        frames2video(payload['camera_id'], payload['timestamp'])
    except Exception as e:
        # the exception must be handled otherwise it will quit the callback
        print(e.message)


mqttc = MqttClient(name="compressor", sub_only=True)
mqttc.start()
mqttc.subscribe("detected_objects", on_message=on_message)


try:
    while True:
        time.sleep(0.1)  
except KeyboardInterrupt:
    mqttc.stop()
