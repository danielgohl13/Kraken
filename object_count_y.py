# Imports
import sys

import cv2

from api import object_counting_api
# Object detection imports
from utils import backbone


def process(input_video):
    vcap = cv2.VideoCapture(input_video) 

    if vcap.isOpened(): 
        # get vcap property 
        width = int(vcap.get(3))
        height = int(vcap.get(4))

        is_color_recognition_enabled = 0 # set it to 1 for enabling the color prediction for the detected objects
        roi = 200 # roi line position
        deviation = 3 # the constant that represents the object counting area

        # it gives me 0.0 :/
        fps = int(vcap.get(5))

    detection_graph, category_index = backbone.set_model('peixe_v2_coco_t2')
    #object_counting_api.object_counting(input_video, detection_graph, category_index, 0) # for counting all the objects, disabled color prediction

    #object_counting_api.object_counting(input_video, detection_graph, category_index, 1) # for counting all the objects, enabled color prediction


    targeted_objects = "peixe" # (for counting targeted objects) change it with your targeted objects

    is_color_recognition_enabled = 0

    object_counting_api.cumulative_object_counting_x_axis(input_video, detection_graph, category_index, is_color_recognition_enabled, fps, width, height, roi, deviation) # counting all the objects

if __name__ == "__main__":
    process(sys.argv[1])
