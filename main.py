import cv2
import mediapipe as mp
import math
import pyautogui
from actions import perform_action

# Initialize MediaPipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9
)

def count_fingers(landmarks):
    """Count the number of extended fingers"""
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []
    
    # Thumb (special case - compare x coordinates)
    if landmarks[tip_ids[0]].x > landmarks[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    
    # Other fingers (compare y coordinates)
    for id in range(1, 5):
        if landmarks[tip_ids[id]].y < landmarks[tip_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def recognize_gesture(fingers):
    """Recognize specific gestures based on finger positions"""
    total_fingers = sum(fingers)
    
    if total_fingers == 0:
        return "Fist"
    elif total_fingers == 1:
        if fingers[1] == 1:  # Index finger
            return "Pointing"
        elif fingers[0] == 1:  # Thumb
            return "Thumbs Up"
        elif fingers[4] == 1 and total_fingers == 1:
            return "Pinky"
    elif total_fingers == 2:
        if fingers[1] == 1 and fingers[2] == 1:  # Index and Middle
            return "Peace Sign"
        elif fingers[0] == 1 and fingers[1] == 1:  # Thumb and Index
            return "OK Sign"
    
    elif total_fingers == 3:
        return "Three Fingers"
    elif total_fingers == 4:
        return "Four Fingers"
    elif total_fingers == 5:
        return "Open Hand"
    
    
    return "Unknown Gesture"

def calculate_distance(point1, point2):
    """Calculate distance between two points"""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def detect_pinch(landmarks):
    """Detect pinch gesture between thumb and index finger"""
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    
    
    distance = calculate_distance(thumb_tip, index_tip)
    
    # Adjust threshold based on your hand size
    pinch_threshold = 0.075
    if sum(fingers)==2:
        return distance < pinch_threshold
    else:
        return False

def draw_gesture_info(frame, gesture, fingers, is_pinching):
    """Draw gesture information on the frame"""
    # Draw gesture name
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Draw finger count
    cv2.putText(frame, f"Fingers: {sum(fingers)}", (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
    # Draw pinch status
    if is_pinching:
        cv2.putText(frame, "PINCH DETECTED!", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Draw individual finger status
    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    for i, (name, status) in enumerate(zip(finger_names, fingers)):
        color = (0, 255, 0) if status else (0, 0, 255)
        cv2.putText(frame, f"{name}: {'Up' if status else 'Down'}", 
                    (10, 150 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

def draw_hand_landmarks(frame, landmarks):
    """Draw custom hand landmarks with different colors for fingertips"""
    # Draw all landmarks
    for idx, landmark in enumerate(landmarks):
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        
        # Color fingertips differently
        if idx in [4, 8, 12, 16, 20]:  # Fingertips
            cv2.circle(frame, (x, y), 8, (0, 255, 255), -1)  # Yellow
        else:
            cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)  # Blue
    
    # Draw connections
    connections = mp_hands.HAND_CONNECTIONS
    for connection in connections:
        start_point = landmarks[connection[0]]
        end_point = landmarks[connection[1]]
        
        start_x = int(start_point.x * frame.shape[1])
        start_y = int(start_point.y * frame.shape[0])
        end_x = int(end_point.x * frame.shape[1])
        end_y = int(end_point.y * frame.shape[0])
        
        cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

# Initialize camera
cam = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

print("Advanced Gesture Recognition with MediaPipe")
print("Press 'q' to quit, 's' to save screenshot")
print("Try these gestures:")
print("- Fist (0 fingers)")
print("- Pointing (1 finger)")
print("- Peace sign (2 fingers)")
print("- OK sign (thumb + index)")
print("- Open hand (5 fingers)")
ga = False  # Global variable to track left click gesture cooldown
rga = False # Global variable to track right click gesture cooldown
minga = False # Global variable to track minimize gesture cooldown
nav = False # Global variable to track taskbar navigation gesture cooldown
ent = False # Global variable to track enter key gesture cooldown


while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (640, 480))
    
    # Convert BGR to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    results = hands.process(rgb_frame)
    
    # Draw hand landmarks and analyze gestures
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            # Draw custom hand landmarks
            draw_hand_landmarks(frame, hand_landmarks.landmark)
            
            # Count fingers
            fingers = count_fingers(hand_landmarks.landmark)
            
            # Recognize gesture
            gesture = recognize_gesture(fingers)
            
            # Detect pinch
            is_pinching = detect_pinch(hand_landmarks.landmark)
            
            # Draw gesture information
            draw_gesture_info(frame, gesture, fingers, is_pinching)

            #convert landmarks into Screen cordinates
            x=int(hand_landmarks.landmark[8].x * screen_width)
            y=int(hand_landmarks.landmark[8].y * screen_height)

            #current mouse position
            cur_x,cur_y=pyautogui.position()

            #target position from hand detection
            tar_x , tar_y= x , y
            
            #applying smoothness
            smooth_x = cur_x + (tar_x-cur_x)*0.1
            smooth_y = cur_y + (tar_y - cur_y)*0.1

            perform_action(gesture, fingers, is_pinching, smooth_x, smooth_y)
            
            
            

            
                    
                    

    # Add instructions
    cv2.putText(frame, "Show your hand to detect gestures", (10, frame.shape[0] - 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Display frame
    cv2.imshow("Gesture Recognition", frame)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("screenshot.png", frame)
        print("Screenshot saved as screenshot.png")
# Clean up
cam.release()
cv2.destroyAllWindows()