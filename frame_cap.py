#!/usr/bin/env python3
import time
import urllib.request
import sys

import cv2
import numpy as np

import object_count


def frame_cap(ip, fps: int = 24, timeout: float = 5.0):
    path_in = "http://" + ip + "/shot.jpg"
    path_out = "cam.mp4"

    frame_array = []
    start = time.time()
    size = (0, 0)
    while (time.time() - start < timeout):
        print(".", end="")
        # reading each FRAME
        RESP = urllib.request.urlopen(path_in)
        FRAME = np.asarray(bytearray(RESP.read()), dtype="uint8")
        FRAME = cv2.imdecode(FRAME, cv2.IMREAD_COLOR)

        height, width, layers = FRAME.shape
        size = (width, height)

        cv2.imshow("imagem", FRAME)

        # inserting the frames into an image array
        frame_array.append(FRAME)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(1/fps)

    out = cv2.VideoWriter(path_out, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for img in frame_array:
        # writing to a image array
        out.write(img)

    out.release()
    cv2.destroyAllWindows()
    print("object counting...")
    object_count.process(path_out)


if __name__ == "__main__":
    frame_cap(ip=sys.argv[1], fps=int(sys.argv[2]), timeout=int(sys.argv[3]))
