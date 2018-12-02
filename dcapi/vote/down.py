# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

#gall_namme : 갤러리 영문 이름
#post_num : 비추천할 글번호

def reqRecommend(gall_name,post_num,csrf):
    url = "http://m.dcinside.com/ajax/nonrecommend"
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/board/"+gall_name+"/"+post_num,
        "X-CSRF-TOKEN" : csrf,
        "X-Requested-With" : "XMLHttpRequest"
    }
    _payload = {
        "type" : "nonrecommend_join",
        "id" : gall_name,
        "no" : post_num
    }
    req = requests.post(url=url,headers=_hd,data=_payload)
    pars = (req.text).split('"')
    pars = pars[2].split(':')
    result = pars[1].split(',')
    return result[0]
    

def getKey(gall_name,post_num): # get csrf 
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/board/"+gall_name
    }
    
    url = "http://m.dcinside.com/board/"+gall_name+"/"+post_num
    req = requests.get(url=url,headers=_hd)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    csrf = soup.find_all("meta",{"name" : "csrf-token"})
    return csrf[0].get("content")

def main(gall_name,post_num):
    csrf = getKey(gall_name,post_num)
    return reqRecommend(gall_name,post_num,csrf)

# 해당글을 비추천합니다.
#res = dcapi.vote.down("programming","12345")
#print(res)
# -> true
# 성공시 true값을 반환합니다.