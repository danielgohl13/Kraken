# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 27th January 2018
# ----------------------------------------------

import csv

import cv2
import numpy as np
import tensorflow as tf

from utils import visualization_utils as vis_util
size_ratio = 1.0


def targeted_object_counting(input_video, detection_graph, category_index, is_color_recognition_enabled, targeted_object, fps, width, height):

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_movie = cv2.VideoWriter(
        "processed.mp4", fourcc, fps, (width, height))
    # input video
    cap = cv2.VideoCapture(input_video)

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name(
                'detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name(
                'detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name(
                'detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')

            # for all the frames that are extracted from input video
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    print("fim")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores,
                        detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, the_result = \
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        cap.get(1),
                        input_frame,
                        1,
                        is_color_recognition_enabled,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        targeted_objects=targeted_object,
                        use_normalized_coordinates=True,
                        line_thickness=3
                    )

                if not the_result:
                    cv2.putText(input_frame, "...", (10, 35), font,
                                0.8, (0, 255, 255), 2, cv2.FONT_HERSHEY_SIMPLEX)
                else:
                    cv2.putText(input_frame, the_result, (10, 35), font,
                                0.8, (0, 255, 255), 2, cv2.FONT_HERSHEY_SIMPLEX)

                cv2.imshow('object counting', input_frame)

                output_movie.write(input_frame)
                print(".", end="")

                if cap.isOpened():
                    # get vcap property
                    width = int(cap.get(3))
                    height = int(cap.get(4))

                new_boxes = []
                for i, box in enumerate(np.squeeze(boxes)):
                    if np.squeeze(scores)[i] > 0.5:
                        new_boxes.append([
                            size_ratio * (box[3]-box[1]),
                            size_ratio * (box[2]-box[0]),
                            np.squeeze(scores)[i]
                        ])

                with open('web/assets/report.csv', 'wb') as fout:
                    np.savetxt(fout, new_boxes,
                               delimiter=',', header='x,y,accuracy', comments='')
                    fout.seek(-1, 2)
                    fout.truncate()

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()


def cumulative_object_counting_x_axis(input_video, detection_graph, category_index, is_color_recognition_enabled, fps, width, height, roi, deviation):
    total_passed_vehicle = 0

    # initialize .csv
    with open('report.csv', 'w') as f:
        writer = csv.writer(f)
        csv_line = "x,y,accuracy"
        writer.writerows([csv_line.split(',')])

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_movie = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

    # input video
    cap = cv2.VideoCapture(input_video)

    total_passed_vehicle = 0
    speed = "waiting..."
    direction = "waiting..."
    size = "waiting..."
    color = "waiting..."
    counting_mode = "..."
    width_heigh_taken = True
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name(
                'detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name(
                'detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name(
                'detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')

            # for all the frames that are extracted from input video
            while(cap.isOpened()):
                ret, frame = cap.read()

                if not ret:
                    print("\nfim de jogo...")
                    break

                input_frame = frame

                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(input_frame, axis=0)

                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores,
                        detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Visualization of the results of a detection.
                counter, csv_line, counting_mode = \
                    vis_util.visualize_boxes_and_labels_on_image_array_x_axis(
                        cap.get(1),
                        input_frame,
                        1,
                        is_color_recognition_enabled,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        x_reference=roi,
                        deviation=deviation,
                        use_normalized_coordinates=True,
                        line_thickness=4
                    )

                # when the vehicle passed over line and counted, make the color of ROI line green
                if counter == 1:
                    cv2.line(input_frame, (roi, 0),
                             (roi, height), (0, 0xFF, 0), 5)
                else:
                    cv2.line(input_frame, (roi, 0),
                             (roi, height), (0, 0, 0xFF), 5)

                total_passed_vehicle = total_passed_vehicle + counter

                # insert information text to video frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(
                    input_frame,
                    'Peixes detectados: ' + str(total_passed_vehicle),
                    (10, 35),
                    font,
                    0.8,
                    (0, 0xFF, 0xFF),
                    2,
                    cv2.FONT_HERSHEY_SIMPLEX,
                )
                # add this part to count objects

                cv2.putText(
                    input_frame,
                    '',
                    (545, roi-10),
                    font,
                    0.6,
                    (0, 0, 0xFF),
                    2,
                    cv2.LINE_AA,
                )

                output_movie.write(input_frame)
                print(".", end="")
                cv2.imshow('object counting', input_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                '''if(csv_line != "not_available"):
                        with open('traffic_measurement.csv', 'a') as f:
                                writer = csv.writer(f)                          
                                size, direction = csv_line.split(',')                                             
                                writer.writerows([csv_line.split(',')])         '''

            cap.release()
            cv2.destroyAllWindows()
