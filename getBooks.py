import requests 
from bs4 import BeautifulSoup 
from PIL import Image
from io import BytesIO
from pathlib import Path


def main():
    i = 1
    current_page = 1
    last_page    = 5
    book_num     = 1

    while current_page <= last_page: 

        web  = requests.get(f"https://www.kitapyurdu.com/index.php?route=product/best_sellers&page={current_page}&list_id=16&filter_in_stock=1&limit=100").content
        soup = BeautifulSoup(web,'html.parser')

        all = soup.find_all("div" , {"class": "image"})
        images = []
        Books = []
        
        # o sayfadaki tüm kitaplar elimizde. 
        for element in all:
            
            
            # sayfadaki tek tek tüm kitapların url bilgileri diğer fonksiyona verilerek ayrıştırma yapılır. 
            book_url  = element.find("a",{"class": "pr-img-link"})["href"]
            image_url = element.find("a",{"class": "pr-img-link"}).find_next()["src"]  # image içerisinde olduğu için find_next demek zorunda kaldık
                
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img.save(f"./Library/images/img_{book_num}.png",format="PNG")
            book_num+=1       
            book = getBookInfos(book_url)
            print(book)
            #saveBook(book)
            
                
            # IPython.display.Image("https://img.kitapyurdu.com/v1/getimage/fn:11631602/wi:100", width = 250)
            
            break
            
        
        current_page +=1
        break
    
def saveBook(book: dict):
    return 

def getBookPics(image_url,book_num):
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save(f"./Library/images/img_{book_num}.png",format="PNG")
    book_num+=1 
    """
    

def getBookInfos(url):
    
    # Buradaki url kitabın kendi bilgilerinin olduğu sayfa.
    # Bu sayfadan kitabın tüm bilgilerini alacağız. 
    # Bunları bir dictionary içerisinde tutup return edeceğiz. 
    
    
    tempBook = {}
    web  = requests.get(url).content
    soup = BeautifulSoup(web,'html.parser')
    
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
        tempBook[key.text] = value.text
    
    return tempBook    
    
main()