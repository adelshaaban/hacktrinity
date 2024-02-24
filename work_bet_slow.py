import cv2
import os
from fastapi.responses import FileResponse
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils

# Define ergonomics analysis class
class Ergonomy:
    def __init__(self):
        self.trunk_angle_threshold = 10  # Angle in degrees for deviation from vertical

    def calculate_angle(self, point1, point2, point3):
        """Calculate angle between three points."""
        vector1 = point1 - point2
        vector2 = point3 - point2
        unit_vector1 = vector1 / np.linalg.norm(vector1)
        unit_vector2 = vector2 / np.linalg.norm(vector2)
        dot_product = np.dot(unit_vector1, unit_vector2)
        angle = np.arccos(dot_product) * (180 / np.pi)
        return angle

    def assess_posture(self, landmarks):
        """Assess the posture based on landmarks."""
        shoulder = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
        hip = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y])
        knee = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y])

        vertical_line = np.array([hip[0], 0])
        trunk_angle = self.calculate_angle(shoulder, hip, vertical_line)

        posture = "Bad" if abs(80 - trunk_angle) <= self.trunk_angle_threshold else "Good"
        return posture, trunk_angle
    
    def process_video(videofile, filename):
        result = []
        result.clear()
        # Open the video file
        cap = cv2.VideoCapture(videofile)

        # Check if the video opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
            exit()

        # Create an instance of the Ergonomy class
        ergonomy = Ergonomy()

        # Initialize variables for video output
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_video_path = f'edited_video/{filename}.avi'
        output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        # Read frames from the video
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame and detect the pose
            results = pose.process(frame_rgb)

            # Check if any poses are detected
            if results.pose_landmarks:
                # Draw pose landmarks on the frame
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                # Assess the posture
                posture, trunk_angle = ergonomy.assess_posture(results.pose_landmarks)

                result.append(posture)

                if posture == "Good":
                    text_color = (0,255,0)
                else:
                    text_color =(0,0,255)
                
                posture_position = (10,50)
                trunk_angle_position = (10,150)
                # Provide feedback on the frame
                # cv2.putText(frame, f'Posture: {posture}, Trunk Angle: {trunk_angle:.2f}', (10, 30),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                


            cv2.putText(frame, f'Posture: {posture}', posture_position,
                        cv2.FONT_HERSHEY_SIMPLEX, 2, text_color, 5, cv2.LINE_AA)

            cv2.putText(frame, f'Trunk Angle: {trunk_angle:.2f}', trunk_angle_position,
                        cv2.FONT_HERSHEY_SIMPLEX, 2, text_color, 5, cv2.LINE_AA) 
            
            # Write the frame to the output video
            output_video.write(frame)

        # Release the video capture object and video writer
        cap.release()
        output_video.release()
        cv2.destroyAllWindows()

        # Convert the AVI file to MP4 using FFmpeg
        output_mp4_path = f'edited_video/{filename}.mp4'
        os.system(f'ffmpeg -i {output_video_path} -c:v libx264 -preset slow -crf 22 -c:a aac -b:a 192k {output_mp4_path}')
        verdict = 0
        if len(result) > 0:
            verdict = (result.count("Good")/len(result)) * 100
        # Return the path to the processed MP4 video file
        return output_mp4_path,verdict,result
