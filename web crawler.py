import requests, sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('C:/Users/JYP/Documents/python/test')

url_lotto = 'http://www.taiwanlottery.com.tw/index_new.aspx'
url_invoice = 'http://invoice.etax.nat.gov.tw/'
html_lotto = requests.get(url_lotto)
html_invoice = requests.get(url_invoice)
html_invoice.encoding='UTF-8'
sp_lotto = BeautifulSoup(html_lotto.text, 'html.parser')
sp_invoice = BeautifulSoup(html_invoice.text, 'html.parser')
data_lotto = sp_lotto.select("#rightdown")
data_invoice = sp_invoice.select('#area1')

#print(data_invoice)

#威力彩
def lotto():
    data2 = data_lotto[0].find_all("div", {"class":"contents_box02"})
    data2_date = data2[0].find("span", {"class":"font_black15"})
    print("\n威力彩 %s" % data2_date.text)
    data2_1 = data2[0].find_all("div", {"class":"ball_green"})

    print("開出順序：", end="")
    for i in range(len(data2_1)-6):
        print(data2_1[i].text, end=" ")

    print("\n大小順序：", end="")
    number = ""
    for i in range(6,len(data2_1)):
        number += data2_1[i].text
        print(data2_1[i].text, end=" ")

    print("\n第二區：", end="")
    data2_3 = data2[0].find("div", {"class":"ball_red"})
    print(data2_3.text)

    datenumber = data2_date.text
    datenumber = datenumber.rsplit()
    #print(datenumber)
    #print(datenumber[1])
    secondarea = data2_3.text

    sqlstr = "select * from lotto where datenumber='{}'".format(datenumber[1])
    cursor = conn.execute(sqlstr)
    row = cursor.fetchone()

    if not row == None:
        print("{} 此資訊已存在".format(datenumber[1]))
    else:
        sqlstr = "insert into lotto values('{}','{}', '{}');".format(datenumber[1], number, secondarea)
        conn.execute(sqlstr)
        conn.commit()
    
    print("歷史紀錄:")
    sqlstr = "select * from lotto"
    cursor = conn.execute(sqlstr)
    for line in cursor:
        print(line)

#大樂透
def lotto2():
    data2 = data_lotto[0].find_all("div", {"class":"contents_box02"})
    data4_date = data2[2].find("span", {"class":"font_black15"})
    print("\n大樂透 %s" % data4_date.text)
    data4_1 = data2[2].find_all("div", {"class":"ball_yellow"})

    print("開出順序：", end="")
    for i in range(len(data4_1)-6):
        print(data4_1[i].text, end=" ")

    print("\n大小順序：", end="")
    number = ""
    for i in range(6,len(data4_1)):
        number += data4_1[i].text
        print(data4_1[i].text, end=" ")

    print("\n特別號：", end="")
    data4_3 = data2[2].find("div", {"class":"ball_red"})
    print(data4_3.text)

    datenumber = data4_date.text
    datenumber = datenumber.rsplit()
    #print(datenumber)
    #print(datenumber[1])
    special = data4_3.text

    sqlstr = "select * from lotto2 where datenumber='{}'".format(datenumber[1])
    cursor = conn.execute(sqlstr)
    row = cursor.fetchone()

    if not row == None:
        print("{} 此資訊已存在".format(datenumber[1]))
    else:
        sqlstr = "insert into lotto2 values('{}','{}', '{}');".format(datenumber[1], number, special)
        conn.execute(sqlstr)
        conn.commit()
        
    print("歷史紀錄:")
    sqlstr = "select * from lotto2"
    cursor = conn.execute(sqlstr)
    for line in cursor:
        print(line)

#發票
def invoice():
    data2_title = data_invoice[0].find_all("h2")
    data2_title = data2_title[1]
    print("\n發票 %s" % data2_title.text)
    data2 = data_invoice[0].find_all("span", {"class":"t18Red"})

    number = ""
    for i in range(len(data2)):
        number += data2[i].text+" "
        print(data2[i].text, end=" ")
    print()

    date = data2_title.text

    sqlstr = "select * from invoice where date='{}'".format(date)
    cursor = conn.execute(sqlstr)
    row = cursor.fetchone()

    if not row == None:
        print("{} 此資訊已存在".format(date))
    else:
        sqlstr = "insert into invoice values('{}','{}');".format(date, number)
        conn.execute(sqlstr)
        conn.commit()
    
    print("歷史紀錄:")
    sqlstr = "select * from invoice"
    cursor = conn.execute(sqlstr)
    for line in cursor:
        print(line)


lotto()
lotto2()
invoice()