import cv2
import numpy as np
import mediapipe as mp
import ctypes
# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)
mp_drawing_styles = mp.solutions.drawing_styles
mp_drawing = mp.solutions.drawing_utils


# Define ergonomics analysis class
class Ergonomy:
    def __init__(self):
        self.trunk_angle_threshold = 20  # Angle in degrees for deviation from vertical
    def calculate_angle(self, point1, point2, point3):
        """Calculate angle between three points."""
        vector1 = point1 - point2
        vector2 = point3 - point2
        unit_vector1 = vector1 / np.linalg.norm(vector1)
        unit_vector2 = vector2 / np.linalg.norm(vector2)
        dot_product = np.dot(unit_vector1, unit_vector2)
        angle = np.arccos(dot_product) * (180 / np.pi)

        # Determine direction
        cross_product = np.cross(vector1, vector2)
        if np.isscalar(cross_product):  # If cross_product is scalar
            direction = 'positive x' if cross_product > 0 else 'negative x'
        else:  # If cross_product is a vector
            if cross_product.ndim == 0:  # Handling 0-dimensional array
                direction = 'positive x' if cross_product.item() > 0 else 'negative x'
            else:
                direction = 'positive x' if cross_product[2] > 0 else 'negative x'
        facing_direction = 'forward' if 0 <= angle <= 90 else 'backward'

        return angle, direction, facing_direction

    def assess_posture(self, landmarks):
        """Assess the posture based on landmarks."""
        shoulder = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                             landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
        hip = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y])
        knee = np.array([landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y])

        vertical_line = np.array([hip[0], 0])
        trunk_angle, direction, facing_direction = self.calculate_angle(shoulder, hip, vertical_line)

        posture = "Bad"
        if trunk_angle > 0 and trunk_angle < 70:
            posture = "Good"

        return posture, trunk_angle


def process_webcam():
    # Create an instance of the Ergonomy class
    ergonomy = Ergonomy()

    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # Set window properties
    cv2.namedWindow('Webcam Feed', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Webcam Feed', screen_width // 2, screen_height // 2)
    cv2.moveWindow('Webcam Feed', screen_width // 4, screen_height // 4)
    while True:
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

            # Set text color based on posture
            text_color = (0, 255, 0) if posture == "Good" else (0, 0, 255)

            # Display posture and trunk angle on the frame
            cv2.putText(frame, f'Posture: {posture}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)
            cv2.putText(frame, f'Trunk Angle: {trunk_angle:.2f}', (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, text_color, 2, cv2.LINE_AA)

        # Show the frame
        cv2.imshow('Webcam Feed', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close windows
    cap.release()
    cv2.destroyAllWindows()


# Call the function to start the webcam feed
process_webcam()
