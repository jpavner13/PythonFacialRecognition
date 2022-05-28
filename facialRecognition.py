import cv2
import numpy as np
import face_recognition
import os
import mysql.connector

def facialRecognition():
    peopleDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "FaceRecognition"
    )

    Cursor = peopleDB.cursor(buffered=True)

    def insertPerson(first, last, imagePath):
        with open(imagePath, "rb") as File:
            BinaryData = File.read()
        SQLStatement = "INSERT INTO people (first_name, last_name, person_image) VALUES (%s, %s, %s)"
        Cursor.execute(SQLStatement, (first, last, BinaryData))
        peopleDB.commit()

    def getPersonImage(firstName, lastName):
        SQLRetrieveStatement = "SELECT * FROM people WHERE first_name = %s AND last_name = %s"
        Cursor.execute(SQLRetrieveStatement, (firstName, lastName))
        Result = Cursor.fetchone()
        first = Result[1]
        last = Result[2]
        fileData = Result[3]
        StoreFilePath = "ImageOutputs/" + first + " " + last + ".jpg".format(str(firstName))
        with open(StoreFilePath, "wb") as File:
            File.write(fileData)
            File.close()

    Cursor.execute("SELECT first_name, last_name FROM people")
    firstNames = []
    lastNames = []
    for x in Cursor:
        firstNames.append(x[0])
        lastNames.append(x[1])

    count = 0
    for name in firstNames:
        getPersonImage(firstNames[count], lastNames[count])
        count += 1

    path = 'ImageOutputs'
    images = []
    classNames = []
    myList = os.listdir(path)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print("Encoding Complete")
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurrFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurrFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame, facesCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1,x1,y2,x2 = faceLoc
                y1, x1, y2, x2 = y1 * 4, x1 * 4, y2 * 4, x2 * 4
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
                filledHeight = 40
                cv2.rectangle(img, (x1,y2 - filledHeight),(x2,y2),(0,255,0),cv2.FILLED)
                fontScale = 0
                if (((x1 - x2) * .003) < 1):
                    fontScale = ((x1 - x2) * .003)
                else:
                    fontScale = 1
                cv2.putText(img,name,(x2+6, y2-6),cv2.FONT_HERSHEY_COMPLEX,fontScale,(0,0,0),2)

        cv2.imshow('Webcam',img)
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.destroyAllWindows()
            break
