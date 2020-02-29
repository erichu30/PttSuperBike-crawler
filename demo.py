#抓取PTT重機板的網頁原始碼
import urllib.request as req


def getArticles(url):
    #建立一個Reques物件，附加Request Heade資訊
    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"     
        #繞過ptt詢問是否成年詢問畫面
        ,"cookie":"over18=1"
    })

    #使用此Requset物件去打開網址
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    #解析source code，取得每篇文章標題(使用beautifulsoup4)
    import bs4
    root = bs4.BeautifulSoup(data, "html.parser")
    #print(root.title.string)    #SuperBike版(標籤為<title></title>)

    titles = root.find_all("div", class_="title")   #尋找class="title"的div標籤
    link = root.find()

    #印出所有非已刪除文章的標題，透過判斷是否有<a>
    for title in titles:
        if title.a != None:
            print(title.a.string)

    #找到內文是< 上頁的a標籤
    nextLink = root.find("a", string = "‹ 上頁")
    #輸出nextLink的href標籤
    return nextLink["href"]


urlPage = "https://www.ptt.cc/bbs/SuperBike/index.html"

#取得總共的頁數
tempString = getArticles(urlPage).replace("/bbs/SuperBike/index", "")
cnt = tempString.replace(".html", "")
count = int(cnt) +1

while count>0:
    urlPage = "https://www.ptt.cc" + getArticles(urlPage)
    count-=1

    


