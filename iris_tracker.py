import cv2
import mediapipe as mp

class Iris_Detector:
    def __init__(self):
        self.mp_face=mp.solutions.face_mesh
        self.face=self.mp_face.FaceMesh(static_image_mode=True,max_num_faces=1, refine_landmarks=True)#confidence params
        self.mp_drawing=mp.solutions.drawing_utils
        self.mp_styles=mp.solutions.drawing_styles

    def get_iris_info(self, image):
        results=self.face.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image.flags.writeable = True
        face_lms=[]
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # self.mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face.FACEMESH_TESSELATION,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_styles
                #     .get_default_face_mesh_tesselation_style())
                # self.mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face.FACEMESH_CONTOURS,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_styles
                #     .get_default_face_mesh_contours_style())
                # self.mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face.FACEMESH_IRISES,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_styles
                #     .get_default_face_mesh_iris_connections_style())
                lms_pos=[[round(lm.x*image.shape[1]),round(lm.y*image.shape[0])] for lm in face_landmarks.landmark]
                face_lms=lms_pos
        return face_lms

    def get_average(self,lst):
        x_lst=[pos[0] for pos in lst]
        y_lst=[pos[1] for pos in lst]
        avg_x=round(sum(x_lst)/len(x_lst))
        avg_y=round(sum(y_lst)/len(y_lst))
        return (avg_x,avg_y)