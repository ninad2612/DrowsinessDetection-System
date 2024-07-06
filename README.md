# Drowsiness Detection System

This Python script uses computer vision techniques to detect drowsiness based on facial landmarks. It utilizes the `dlib` library for face detection and facial landmark estimation, `OpenCV` for video capture and image processing, and `tkinter` for the GUI interface.

Requirements:

Make sure you have the following Python libraries installed:

- opencv-python
- numpy
- dlib
- imutils
- Pillow (imported as Image and ImageTk from PIL)

You can install these dependencies using pip:

pip install -r requirements.txt

Usage:

1. Download the `shape_predictor_68_face_landmarks.dat` file and place it in the same directory as the script. The Explaination of this is given in shape_predictor_68_face_landmarks.txt

2. Run the script:

python drowsiness_detection.py

3. Once the script starts, it will open a GUI window showing the camera feed. The status label at the top will indicate whether the person is awake, drowsy, or asleep based on their blinking patterns.

4. To exit the application, simply close the GUI window.

Notes:

- Ensure your camera is connected and accessible by OpenCV.
- The script calculates blink ratios to determine if the person's eyes are closed or open.
- Adjust the threshold values (sleep > 6, drowsy > 6, active > 6) in the script based on your testing environment and requirements.
