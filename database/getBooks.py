import requests 
from bs4 import BeautifulSoup 
from PIL import Image
from io import BytesIO
from pathlib import Path

import mysql.connector

connection = mysql.connector.connect(
    host     = "localhost",     
    user     = "root",
    password = "112358",
    database = "kutuphane"
)

cursor = connection.cursor()

    
def scrap_books():
    sayac = 100
    current_page = 1
    last_page    = 5
    book_num     = 1

    while current_page <= last_page: 

        web  = requests.get(f"https://www.kitapyurdu.com/index.php?route=product/best_sellers&page={current_page}&list_id=16&filter_in_stock=1&limit=100").content
        soup = BeautifulSoup(web,'html.parser')

        all = soup.find_all("div" , {"class": "image"})
        
        # o sayfadaki tüm kitaplar elimizde. 
        for element in all:
            
            # sayfadaki tek tek tüm kitapların url bilgileri diğer fonksiyona verilerek ayrıştırma işlemi yapılacak. 
            
            book_url  = element.find("a",{"class": "pr-img-link"})["href"]
            image_url = element.find("a",{"class": "pr-img-link"}).find_next()["src"]  # image içerisinde olduğu için find_next demek zorunda kaldık
                
            img_content = requests.get(image_url).content         
            img = Image.open(BytesIO(img_content))
            
            path = Path(f"images/img_{book_num}.png")
            img.save(path,format="PNG")
                  
            
            book = getBookInfos(book_url)
            print(book)
            saveBook(book,path)
            
            if book_num == sayac:
                break
                
            book_num+=1 
            
        current_page +=1
               
    
def saveBook(book: dict, path):
     
    # kitap bilgilerini alıp veritabanına kaydedeceğiz.
    
    secilenler = ["ISBN", "Adı", "Yazar", "Yayınevi", "Çevirmen", "Yayın Tarihi", "Orijinal Adı", "Dil", "Sayfa Sayısı", "Cilt Tipi", "Boyut", "Kategori"]
    
    with open(path, 'rb') as file:
        byte_data = file.read()
    
    # kitap bilgileri bir dictionary içerisinde tutuluyor.  
    # verileri tek tek alalım.
    
    for key in secilenler:
        # eğer seçmek istediklerimiz gelen bilgilerde yoksa onun yerine None yazalım.
        if key not in book.keys():
            book[key] = None
        # varsa bir şey yapmaya gerek yok.  
    
    
    try : 
        isbn        = book["ISBN"]
        ad          = book["Adı"]
        yazar       = book["Yazar"] 
        yayinevi    = book["Yayınevi"]
        cevirmen    = book["Çevirmen"] 
        tarihi      = book["Yayın Tarihi"]
        orjinal     = book["Orijinal Adı"]
        dil         = book["Dil"]   
        sayfa       = book["Sayfa Sayısı"] 
        cilt        = book["Cilt Tipi"]
        boyut       = book["Boyut"] 
        kategori    = 'book["Kategori"]'
    except KeyError as e:
        print("Bir kitap bilgisi eksik")
        print(e)
    
    sql = "INSERT INTO kitaplar (ISBN, Adı, Yazar, Yayınevi, Çevirmen, Yayın_Tarihi, Orijinal_Adı, Dil, Sayfa_Sayısı, Cilt_Tipi, Boyut, Resim, Kategori) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (isbn, ad , yazar, yayinevi, cevirmen, tarihi, orjinal, dil, sayfa, cilt, boyut, byte_data, kategori )
    cursor.execute(sql, values)

    try:
        connection.commit()
        print(f"{cursor.rowcount} tane kayıt eklendi")
        print(f"son eklenen kaydın id : {cursor.lastrowid}")
    except mysql.connector.Error as e:
        print("Error :",e)
    finally:
        print("işlem başarılı")


def getBookInfos(url):
    
    # Buradaki url kitabın kendi bilgilerinin olduğu sayfa.
    # Bu sayfadan kitabın tüm bilgilerini alacağız. 
    # Bunları bir dictionary içerisinde tutup return edeceğiz. 
    
    
    tempBook = {}
    web  = requests.get(url).text
    soup = BeautifulSoup(web,'html.parser', from_encoding= 'utf-8')
    
    # KİTAP ADI 
    header = soup.find("div",{"class":"pr_header"}).text.strip()
    # YAZAR VE YAYINEVİ 
    producers = soup.find_all("a",{"class": "pr_producers__link"})
    yazar = producers[0].text.strip()
    yayınevi = producers[1].text.strip()

    # ----------------------    
    tempBook["Adı"] = header
    tempBook["Yazar"] = yazar
    tempBook["Yayınevi"] = yayınevi    

    # bilgilerin olduğu kısmı table olarak adlandırıp 
    others = soup.find("div",{"class": "attributes"}) # kitap bilgileri
    # her bir tr satırını alacağız.
    table = others.find_all("tr")

    
    for td in table:
        # bu satırlar arasında dolanıp satır bilgilerini key value şeklinde (sayfa : 200) ayırıp dictionary nesnemize atacağız.  
        key = td.find("td")
        value = key.find_next("td")
        tempBook[key.text.replace(":", "")] = value.text
    
    return tempBook    
    
    
def main():
    scrap_books()
    
    # veritabanı bağlantısı test et 
    #cursor.execute("SELECT * FROM kitaplar")
    
    
main()


"""
'Adı': 'İnsanlığımı Yitirirken', 
'Yazar': 'Osamu Dazai',
'ISBN:': '9786258401479', 
'Yayınevi': 'İTHAKİ YAYINLARI', 
'Çevirmen:': ' Peren Ercan', 
'Yayın Tarihi:': '28.12.2022', 
'Orijinal Adı:': 'Ningen Şikkaku (人間失格)', 
'Dil:': 'TÜRKÇE', 
'Sayfa Sayısı:': '128', 
'Cilt Tipi:': 'Karton Kapak', 
# 'Kağıt Cinsi:': 'Kitap Kağıdı', 
'Boyut:': '12.5 x 19.5 cm'
""" 