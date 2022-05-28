from tkinter import *
import mysql.connector
import cv2
from cv2 import *
import pygame
import pygame.camera
from facialRecognition import *

def inputWindow():
    screen1 = Toplevel(screen)

    peopleDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "FaceRecognition"
    )

    Cursor = peopleDB.cursor(buffered=True)

    screen1.title("Register")
    screen1.geometry("300x250")

    def insertPerson(first, last, imagePath):
        with open(imagePath, "rb") as File:
            BinaryData = File.read()
        SQLStatement = "INSERT INTO people (first_name, last_name, person_image) VALUES (%s, %s, %s)"
        Cursor.execute(SQLStatement, (first, last, BinaryData))
        peopleDB.commit()

    def onClick():
        firstname = firstName.get()
        lastname = lastName.get()

        Label(screen1, text = "Registration success! Welcome " + firstname + " " + lastname + "!").pack()

        insertPerson(firstname, lastname, "image.jpg")

    def takeSelfie():
        cam = cv2.VideoCapture(0)

        cv2.namedWindow("Webcam")

        img_counter = 0

        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        camera = pygame.camera.Camera(camlist[0], (640, 480))
        camera.start()

        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            if cv2.waitKey(1) & 0xFF == ord(' '):
                Image = camera.get_image()
                img_counter += 1
                cam.release()
                cv2.destroyAllWindows()
                pygame.image.save(Image, "image.jpg")
                break

        cv2.destroyAllWindows()

        print(Image)
        return Image

    global firstName
    global lastName
    firstName = StringVar()
    lastName = StringVar()

    Label(screen1, text = "Please enter details below").pack()
    Label(screen1, text = "").pack()

    Label(screen1, text = "First name *").pack()
    first_name_entry = Entry(screen1, textvariable = firstName).pack()

    Label(screen1, text = "Last name *").pack()
    last_name_entry = Entry(screen1, textvariable = lastName).pack()
    Label(screen1, text = "").pack()

    photo = Button(screen1, text = "Take selfie *", width = 10, height = 1, command = takeSelfie).pack()

    Button(screen1, text = "Register", width = 10, height = 1, command = onClick).pack()

    label = Label(screen1, text = '')

    screen1.mainloop()

def main_screen():
    global screen
    screen = Tk()

    screen.title("Facial Recognition")
    screen.geometry("300x250")

    def Register():
        inputWindow()

    def recognize():
        facialRecognition()

    Label(screen, text = "Please select from below:").pack()
    Label(screen, text = "").pack()

    Button(screen, text = "Register", width = 15, height = 5, command = Register).pack()
    Button(screen, text = "Run Face Recognition", width = 15, height = 5, command = recognize).pack()

    label = Label(screen, text = '')

    screen.mainloop()