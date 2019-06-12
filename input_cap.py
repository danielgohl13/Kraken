#!/usr/bin/env python3
import time
import urllib.request
import sys

import cv2
import numpy as np

import object_count

def input_vid(vid_path):
    print("object counting...")
    object_count.process(vid_path)


if __name__ == "__main__":
    input_vid(vid_path=sys.argv[1])
