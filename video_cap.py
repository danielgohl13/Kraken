import csv
import cv2
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'X264')
output_movie = cv2.VideoWriter('videocap.mp4', fourcc, 20.00, (640, 480))
# input video
cap = cv2.VideoCapture("http://192.168.2.109:8080/video.mp4")


# for all the frames that are extracted from input video
while(cap.isOpened()):
    ret, frame = cap.read()                

    if not  ret:
        print("end of the cap")
        break
    
    input_frame = frame

    
    cv2.imshow('object counting',input_frame)

    output_movie.write(input_frame)
    print ("writing frame")


    if cap.isOpened(): 
        # get vcap property 
        width = int(cap.get(3))
        height = int(cap.get(4))


    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

