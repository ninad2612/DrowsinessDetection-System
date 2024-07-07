import cv2
import numpy as np
import dlib
from imutils import face_utils
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame  

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("DrowsinessDetection-System/shape_predictor_68_face_landmarks.dat")

sleep = 0
drowsy = 0
active = 0
status = ""
color = (0, 0, 0)

# Initialize pygame for playing audio
pygame.mixer.init()

def compute(ptA, ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

def blinked(a, b, c, d, e, f):
    up = compute(b, d) + compute(c, e)
    down = compute(a, f)
    ratio = up / (2.0 * down)

    if ratio > 0.25:
        return 2
    elif ratio > 0.21 and ratio <= 0.25:
        return 1
    else:
        return 0

def play_audio():
    pygame.mixer.music.load("F:\d\DrowsinessDetection-System\mixkit-alert-alarm-1005.wav")  # Replace with your audio file path
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

def update_frame():
    global sleep, drowsy, active
    ret, frame = cap.read()
    if not ret:
        print("Error: Couldn't read frame from the camera.")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        if left_blink == 0 or right_blink == 0:
            sleep += 1
            drowsy = 0
            active = 0
            if sleep > 6:
                status_var.set("SLEEPING !!!")
                status_label.config(foreground="red")
                play_audio()

        elif left_blink == 1 or right_blink == 1:
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                status_var.set("Drowsy !")
                status_label.config(foreground="blue")
                stop_audio()

        else:
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                status_var.set("Active")
                status_label.config(foreground="green")
                stop_audio()

        update_image(face_frame)

    root.after(10, update_frame)

def update_image(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel.config(image=img)

root = tk.Tk()
root.title("Drowsiness Detection")

status_var = tk.StringVar()
status_label = ttk.Label(root, textvariable=status_var, font=("Helvetica", 16))
status_label.pack(pady=10)

panel = ttk.Label(root)
panel.pack()

update_frame()

root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
root.mainloop()

cap.release()
pygame.mixer.quit()
