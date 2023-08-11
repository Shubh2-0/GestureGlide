import random  # Import the random module to generate random numbers
import cv2  # Import the OpenCV library for computer vision tasks
import cvzone  # Import the cvzone library for additional computer vision utilities
from cvzone.HandTrackingModule import HandDetector  # Import the HandDetector module for hand tracking
import time  # Import the time module for time-related operations

# Open the camera
camera = cv2.VideoCapture(0)  # Initialize webcam capture
camera.set(3, 640)  # Set webcam width
camera.set(4, 480)  # Set webcam height

# Initialize hand detector
hand_detector = HandDetector(maxHands=1)  # Initialize HandDetector to track one hand

# Initialize variables
game_time = 0  # Initialize a variable to track game time
show_game_result = False  # Flag to indicate if the game result is shown
game_started = False  # Flag to indicate if the game has started
scores = [0, 0]  # Initialize scores for AI and Player

while True:
    # Load background image
    background_image = cv2.imread("resources/bg.png")  # Load the background image

    # Capture video from the camera
    success, frame = camera.read()  # Capture a frame from the webcam

    # Resize and crop the captured frame
    scaled_frame = cv2.resize(frame, (0, 0), None, 0.875, 0.875)  # Resize the frame
    cropped_frame = scaled_frame[:, 80:480]  # Crop the frame

    # Find hands in the resized frame
    detected_hands, _ = hand_detector.findHands(cropped_frame)  # Detect hands in the resized frame

    if game_started:
        if not show_game_result:
            # Calculate the time elapsed since the game started
            game_time = time.time() - start_time  # Calculate elapsed time

            # Display the timer on the screen
            cv2.putText(background_image, str(int(game_time)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if game_time > 3:
                show_game_result = True
                game_time = 0

                if detected_hands:
                    player_choice = None  # Initialize the player's choice
                    hand = detected_hands[0]  # Get the first detected hand
                    finger_states = hand_detector.fingersUp(hand)  # Detect finger positions

                    # Determine player's choice based on finger positions
                    if finger_states == [0, 0, 0, 0, 0]:
                        player_choice = 1  # Player selects Rock
                    elif finger_states == [1, 1, 1, 1, 1]:
                        player_choice = 2  # Player selects Paper
                    elif finger_states == [0, 1, 1, 0, 0]:
                        player_choice = 3  # Player selects Scissors

                    # Generate a random AI choice
                    ai_choice = random.randint(1, 3)  # Randomly select AI's choice
                    ai_image = cv2.imread(f'resources/{ai_choice}.png', cv2.IMREAD_UNCHANGED)
                    background_image = cvzone.overlayPNG(background_image, ai_image, (149, 310))

                    # Update scores based on the game result
                    if (player_choice == 1 and ai_choice == 3) or \
                            (player_choice == 2 and ai_choice == 1) or \
                            (player_choice == 3 and ai_choice == 2):
                        scores[1] += 1  # Player wins
                    elif (player_choice == 3 and ai_choice == 1) or \
                            (player_choice == 1 and ai_choice == 2) or \
                            (player_choice == 2 and ai_choice == 3):
                        scores[0] += 1  # AI wins

    # Display the scaled camera feed on the background
    background_image[234:654, 795:1195] = cropped_frame

    if show_game_result:
        background_image = cvzone.overlayPNG(background_image, ai_image, (149, 310))

    # Display the scores on the image
    cv2.putText(background_image, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(background_image, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Display the images
    cv2.imshow("Background", background_image)  # Display the combined image

    # Wait for the 'x' key press to start the game
    key = cv2.waitKey(1)
    if key == ord('x'):
        game_started = True
        start_time = time.time()  # Record the start time
        show_game_result = False
