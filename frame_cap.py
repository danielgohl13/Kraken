#!/usr/bin/env python3
import time
import urllib.request

import cv2
import numpy as np
import object_count

PATH_IN = "http://192.168.0.100:8080/shot.jpg"
PATH_OUT = "cam.mp4"
FPS = 15.0
TIMEOUT = 8.0

FRAME_ARRAY = []
START = time.time()
while True:
    #reading each FRAME
    RESP = urllib.request.urlopen(PATH_IN)
    FRAME = np.asarray(bytearray(RESP.read()), dtype="uint8")
    FRAME = cv2.imdecode(FRAME, cv2.IMREAD_COLOR)

    height, width, layers = FRAME.shape
    size = (width,height)

    cv2.imshow("imagem", FRAME)

    #inserting the frames into an image array
    FRAME_ARRAY.append(FRAME)

    if (cv2.waitKey(1) & 0xFF == ord('q')) or (time.time() - START >= TIMEOUT):
        break

    time.sleep(1/FPS)

out = cv2.VideoWriter(PATH_OUT, cv2.VideoWriter_fourcc(*'mp4v'), FPS, size)

for img in FRAME_ARRAY:
    # writing to a image array
    out.write(img)
out.release()

object_count.process(PATH_OUT)
