import cv2
import math
import numpy as np
import serial_servo
import mediapipe as mp
import screeninfo
mp_pose = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles
pose= mp_pose.FaceDetection(
    model_selection=0, min_detection_confidence=0.9)
cap= cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.detections:
      if len(results.detections)==2:
        print("original",results.detections)
        results.detections.sort(key=lambda x:x.location_data.relative_bounding_box.height,reverse=True)
        print("sorted",results.detections)
      biggest_face=[results.detections[0]]
      for detection in biggest_face:
        #take the largest dectection
        # print(detection.location_data.relative_bounding_box)
        center_x=detection.location_data.relative_bounding_box.xmin+(detection.location_data.relative_bounding_box.width/2)
        center_y=detection.location_data.relative_bounding_box.ymin+(detection.location_data.relative_bounding_box.height/2)
        face_yaw=73-((center_x-0.5)*50)
        serial_servo.moov("face_yaw",face_yaw)
        face_pitch=95-((1-center_y)*60)
        serial_servo.moov("face_pitch",face_pitch)
        base_eye_pitch=30
        base_eye_yaw=80
        eye_pitch=base_eye_pitch+((0.5-center_y)*30)
        eye_yaw=base_eye_yaw-((0.5-center_x)*30)
        serial_servo.moov("eye_pitch",eye_pitch)
        serial_servo.moov("eye_yaw",eye_yaw)
        mp_drawing.draw_detection(frame, detection)
    bigger = cv2.resize(frame, (1920, 1080))    
    cv2.imshow("image", bigger)
    cv2.waitKey(1)