# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 14:06:50 2019
I used one Chinese website called zhenai, so there are some chinese characters in the html.
@author: kxF1205
"""

import requests
from bs4 import BeautifulSoup
import ssl
import sys,os
import re






def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error! Internet disconnected"

def getImg(t,lst):
    soup = BeautifulSoup(html,'html.parser')
    all_link = soup.find_all("div",class_="list-item")
    for person_link in all_link:
        #the list info is used to save the informations of persons 
        info= []
        if(person_link.img):
            img_url = person_link.img
            info.append(img_url['src'])
        if(person_link.tbody):
            ga=person_link.tbody.find_all("td")
            #find the gender
            if("男士" in ga[0].get_text()):
                img_gender = "0"#the gender is male
            if("女士"in ga[0].get_text()):
                img_gender='1'#the gender is female
            info.append(img_gender)
            #find the age
            img_age=re.findall(r'\d+',(ga[2].get_text()))
            info.append(img_age[0])
        #save one person's info to the list
        if(info):#info is not empty
            lst.append(info)
    return lst

def make_dir(p):
    path = p
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

#open the url of image saved in the imglist, and then save the images 
def save_img(path,plist):
    x = 1#set the number of the images
    for p in plist:
        try:
            imgres = requests.get(p[0])
            img = imgres.content
            with open(os.path.join(path,str(p[1])+'-'+str(p[2])+'_'+str(x)+'.jpg'),'wb') as f:
                #the format of the name:gender-name_number(图片名称格式：性别-年龄_序号)
                f.write(img)
                f.close()
            x= x+1
        except:
            print("Error! Cannot save the image")
    return x
        
    
if __name__=='__main__':
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'http://www.zhenai.com/zhenghun/beijing/2'
    html = getHTMLText(url)
    lst=[]
    imglist = getImg(html,lst)
    path = make_dir(sys.argv[1])
    save_img(path,imglist)
    


