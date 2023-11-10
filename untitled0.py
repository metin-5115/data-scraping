
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
from urllib.request import urlopen
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

u=[]
for i in range(2,10):
    
    url="https://www.trendyol.com/erkek-t-shirt-x-g2-c73?pi="+str(i)
    header={"User_Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}
    r=requests.get(url,headers=header)
    soup=BeautifulSoup(r.content,"lxml")
    ürünler=soup.find_all("div",attrs={"class":"p-card-wrppr with-campaign-view"})
    u.append(ürünler)
     
def flatten_extend(matrix):
     flat_list = []
     for row in matrix:
         flat_list.extend(row)
     return flat_list
 
print(len(flatten_extend(u)))
a=flatten_extend(u)   

final_dict={}
result_dict={}
attr_list=[]
links=[]
sd=a[0:10]
c=0
for ürün in sd:
    temp_list=[]
    i=ürün.find_all("div",attrs={"class":"p-card-chldrn-cntnr card-border"})
    i2=i[0].find_all("a")
    link_devam=i2[0].get("href")
    link_basi="https://www.trendyol.com/"
    link_tamami=link_basi+link_devam
    link_tamami=link_tamami.split("?")[0]
    links.append(link_tamami)
        
#her kıyafetin özelliklerini toplu olarak dict'e atma
for m in links:
    c+=1
    detay=requests.get(m)
    detay_soup=BeautifulSoup(detay.content, "html.parser")
    
    lk=detay_soup.find_all("main",{"id":"product-detail-app"})
    lk1=lk[0].find_all("div",{"class":"product-detail-container"})
    lk2=lk1[0].find_all("article",{"class":"pr-rnr-w"})
    lk3=lk2[0].find_all("div",{"class":"pr-rnr-cn gnr-cnt-br"})
    
    s6=detay_soup.find_all("ul",attrs={"class":"detail-attr-container"}) 
    l1=s6[0].find_all("li",attrs={"class":"detail-attr-item"})

    attr_list.append(s6)
    final_dict[c]=l1
    
    lk=detay_soup.find_all("main",{"id":"product-detail-app"})


    
    
    
#her kıyafetin görselinin hem linkini alıp hem de bilgisayara kaydetme
u=1
new_links=[]
like_sonucu=[]
for k in links:
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(k,None,headers) 
    response = urllib.request.urlopen(request)
    data = response.read() 

    page_soup=BeautifulSoup(data,"html.parser")
    s1=page_soup.find_all("div",{"class":"gallery-container"})
    s2=s1[0].find("div",{"class":"gallery-modal hidden"}) 
    s3=s2.find("div",{"class":"gallery-modal-content"})
    s4=s3.find_all("img")
    img_src=s4[0].get("src")
    
    filename=str(u)
    u+=1
    img_file=open("C:\\Users\\MTN\\spyder project\\clothes\\trendyol_imgs\\"+filename+".jpg","wb")
    img_file.write(urllib.request.urlopen(img_src).read())
    img_file.close()
    
    
    base_url=k
    extra_path = "/yorumlar?"
    full_url = base_url + extra_path
    new_links.append(full_url)
    
    
    

#like sayısı alma 
for x in new_links:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(x)

    comment_button=driver.find_element(By.CLASS_NAME, "ps-stars__count")
    print(comment_button.text)

    #driver.quit()

          
    


    
        
#her kıyafet özelliğini teker teker alıp dict'e kaydetme    
attribute_list=["Renk","Ortam"]

rmv_img_list=[]
cnt=0
for i in final_dict:
    temp_dct={}
    cnt+=1
    lst=final_dict[i]
    for j in lst:
        st=""
        q1=j.find_all("span")
        temp_dct[q1[0].text]=  q1[1].text
    if len(temp_dct) < len(attribute_list):
        rmv_img_list.append(cnt)
        continue
    else:
        result_dict[cnt]=temp_dct
        
#sadece gerekli özellikleri ayıklama
last_dict={}
for j in result_dict.keys():
    tmp_d={}
    trs=result_dict[j]
    try:
        tmp_d[attribute_list[0]]=trs[attribute_list[0]]
        tmp_d[attribute_list[1]]=trs[attribute_list[1]]
        
    except:
        rmv_img_list.append(j)
        continue
    last_dict[j]=tmp_d

print("solo")

#gereksiz fotoları silme
for m in rmv_img_list:
    os.remove("C:\\Users\\MTN\\spyder project\\clothes\\trendyol_imgs\\"+str(m)+".jpg")
    

    