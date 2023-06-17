import mysql.connector

connector = mysql.connector.connect(
    host     = "localhost",
    user     = "root",
    password = "112358",
    database = "resim_deneme"
)

cursor = connector.cursor()

def insertBlob(id:31, filename):
    # insert image into database
    with open(filename, 'rb') as file:
        binary = file.read()
    
    sql = "INSERT INTO images(id, photo) VALUES (%s, %s)"
    values = (id, binary)
    cursor.execute(sql, values)
    try:
        connector.commit()
        print(f"{cursor.rowcount} tane kayıt eklendi")
        print(f"son eklenen kaydın id : {cursor.lastrowid}")
    except mysql.connector.Error as e:
        print("Error :",e)
    finally:
        print("işlem başarılı")
        
def retrieveBlob(id=31):
    
    sql = "SELECT photo FROM images WHERE id = %s"
    values = (id,)
    cursor.execute(sql, values)
    try:
        photo = cursor.fetchone()[0]
        with open("deneme.jpg", "wb") as file:
            file.write(photo)
    except mysql.connector.Error as e:
        print("Error :",e)
    finally:
        print("işlem başarılı")
        
#insertBlob(31, "atam.jpg")

retrieveBlob(31)