import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
mp_drawing_styles = mp.solutions.drawing_styles

# Drawing utility
mp_drawing = mp.solutions.drawing_utils

# Define ergonomics analysis class
class Ergonomy:
    def __init__(self):
        self.trunk_angle_threshold = 10  # Angle in degrees for deviation from vertical

    def calculate_angle(self, point1, point2, point3):
        #point 1 = shoulder, point 2 = hip, point 3 = vertical line
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

        posture = "Bad" if abs(90 - trunk_angle) <= self.trunk_angle_threshold else "Good"
        return posture, trunk_angle

# Open the video file
cap = cv2.VideoCapture('4.MOV')

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create an instance of the Ergonomy class
ergonomy = Ergonomy()

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
            landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style())

        # Assess the posture
        posture, trunk_angle = ergonomy.assess_posture(results.pose_landmarks)

        # Provide feedback on the frame
        cv2.putText(frame, f'Posture: {posture}, Trunk Angle: {trunk_angle:.2f}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Posture Analysis', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
