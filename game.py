# Import necessary libraries
import random  # Import the random module for generating random numbers
import cv2  # Import OpenCV for computer vision tasks
import cvzone  # Import the cvzone library for additional computer vision utilities
from cvzone.HandTrackingModule import HandDetector  # Import the HandDetector module for hand tracking
import time  # Import the time module for time-related operations

# Open the camera
cap = cv2.VideoCapture(0)  # Initialize webcam capture
cap.set(3, 640)  # Set webcam width
cap.set(4, 480)  # Set webcam height

# Initialize hand detector
detector = HandDetector(maxHands=1)  # Initialize HandDetector to track one hand

# Initialize variables
timer = 0  # Initialize a variable to track time
stateResult = False  # Flag to indicate if the game result is shown
startGame = False  # Flag to indicate if the game has started
scores = [0, 0]  # Initialize scores for AI and Player

while True:
    # Load background image
    imgBG = cv2.imread("resources/bg.png")  # Load the background image

    # Capture video from the camera
    success, img = cap.read()  # Capture a frame from the webcam

    # Resize and crop the captured frame
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)  # Resize the frame
    imgScaled = imgScaled[:, 80:480]  # Crop the frame

    # Find hands in the resized frame
    hands, img = detector.findHands(imgScaled)  # Detect hands in the resized frame

    if startGame:
        if stateResult is False:
            # Calculate the time elapsed since the game started
            timer = time.time() - initialTime  # Calculate elapsed time

            # Display the timer on the screen
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None  # Initialize the player's move
                    hand = hands[0]  # Get the first detected hand
                    fingers = detector.fingersUp(hand)  # Detect finger positions

                    # Determine player's move based on finger positions
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Player selects Rock
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Player selects Paper
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Player selects Scissors

                    # Generate a random AI move
                    randomNumber = random.randint(1, 3)  # Randomly select AI's move
                    imgAI = cv2.imread(f'resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Update scores based on the game result
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1  # Player wins

                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1  # AI wins

    # Display the scaled camera feed on the background
    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Display the scores on the image
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # Display the images
    cv2.imshow("BG", imgBG)  # Display the combined image

    # Wait for the 's' key press to start the game
    key = cv2.waitKey(1)
    if key == ord('x'):
        startGame = True
        initialTime = time.time()  # Record the start time
        stateResult = False
