import mysql.connector

peopleDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "FaceRecognition"
)

Cursor = peopleDB.cursor()

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

insertPerson("Jackie", "Avner", "ReferencePhotos/Jackie Avner.PNG")
insertPerson("Brian", "Avner", "ReferencePhotos/Brian Avner.jpg")
insertPerson("David", "Avner", "ReferencePhotos/David Avner.PNG")