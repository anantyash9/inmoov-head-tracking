import cv2
import mediapipe as mp
from pprint import pprint
import serial_servo
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
import numpy as np
coords=[]
def distance(p1,p2):
    squared_dist = np.sum((p1-p2)**2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)
with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    
    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        d=0
        for i in mp_face_mesh.FACEMESH_FACE_OVAL:
            d+=distance(np.array([face_landmarks.landmark[i[0]].x, face_landmarks.landmark[i[0]].y,face_landmarks.landmark[i[0]].z]),np.array([face_landmarks.landmark[i[1]].x, face_landmarks.landmark[i[1]].y,face_landmarks.landmark[i[1]].z]))
        # print(d)
        if len(coords)==0:
            coords=np.array([np.array([face_landmarks.landmark[i[0]].x, face_landmarks.landmark[i[0]].y,face_landmarks.landmark[i[0]].z]) for i in mp_face_mesh.FACEMESH_FACE_OVAL])
        temp=np.array([np.array([face_landmarks.landmark[i[0]].x, face_landmarks.landmark[i[0]].y,face_landmarks.landmark[i[0]].z]) for i in mp_face_mesh.FACEMESH_FACE_OVAL])
        diff=abs(np.sum(coords-temp))
        # print(diff)
        coords=temp
        if(diff>4):
            print("new face")
        center=np.mean(coords,axis=0)
        face_yaw=73-((center[0]-0.5)*50)
        serial_servo.moov("face_yaw",face_yaw)
        face_pitch=95-((1-center[1])*60)
        serial_servo.moov("face_pitch",face_pitch)
        base_eye_pitch=30
        base_eye_yaw=80
        eye_pitch=base_eye_pitch+((0.5-center[1])*30)
        eye_yaw=base_eye_yaw-((0.5-center[0])*30)
        serial_servo.moov("eye_pitch",eye_pitch)
        serial_servo.moov("eye_yaw",eye_yaw)
        # print(face_landmarks[mp_face_mesh.FACEMESH_FACE_OVAL])
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_IRISES,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_iris_connections_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()