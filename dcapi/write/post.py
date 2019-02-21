# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


#원하는 갤러리에 비로그인(유동)으로 글을 작성할수가 있습니다.
#gall_namme : 갤러리 영문 이름
#usid : 닉네임
#password : 비밀번호
#title : 글  제목
#content : 글 내용


def getBlock_key(gall_name,csrf):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/write/"+gall_name,
        "X-CSRF-TOKEN" : csrf,
        "X-Requested-With" : "XMLHttpRequest"
    }
    _url = "http://m.dcinside.com/ajax/access"
    
    _payload = {
        "token_verify" : "dc_check2"
    }

    req = requests.post(url=_url,headers=_hd,data=_payload)
    pars_key =  (req.text).split('"')

    return pars_key[5]

def getPageKey(gall_name): 
    _hd ={
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
    }
    url = "http://m.dcinside.com/write/"+gall_name
    req = requests.get(url=url,headers=_hd)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    code = soup.find_all("input",{"id" : "code"}) # get page random code 
    csrf = soup.find_all("meta",{"name" : "csrf-token"}) # get csrf code
    honey = soup.find_all("input",{"class" : "hide-robot"}) # get honey 
    return code[0].get("value"), csrf[0].get("content"), honey[0].get("name")
    
def check_filter(gall_name,id,title,content,csrf,rand_code):
    _hd = {
    "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    "Referer" : "http://m.dcinside.com/write/"+gall_name,
    "X-CSRF-TOKEN" : csrf,
    "X-Requested-With": "XMLHttpRequest",
    }

    _payload = {
        "subject" : title,
        "memo" : content,
        "id" : gall_name,
        "rand_code" : rand_code,
    }
    url = "http://m.dcinside.com/ajax/w_filter"
    req = requests.post(url=url,headers=_hd,data=_payload)

    
def write_post(gall_name,usid,password,title,content,rand_code,block_key,honey ):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/write/"+gall_name,
        "X-Requested-With": "XMLHttpRequest",
        "Origin": "http://m.dcinside.com",
        "Cookie" : "m_dcinisde_"+gall_name+"="+gall_name+";m_dcinside_lately="+gall_name
    }
    _payload = {
        "name" : usid,
        "password" : password,
        "subject" : title,
        "memo" : content,
        honey : "1",
        "id" : gall_name,
        "contentOrder" : "order_memo",
        "mode" : "write",
        "Block_key" : block_key,
        "bgm" : "",
        "iData" : "",
        "yData" : "",
        "tmp" : "",
        "mobile_key" : "mobile_nomember",
        "code" : rand_code,
        "GEY3JWF" : honey

    }

    _url = "http://upload.dcinside.com/write_new.php"
    req = requests.post(url=_url,headers=_hd,data=_payload)
    pars1 = (req.text).split("/")
    pars2 = pars1[5].split('"')
    return pars2[0]
    

def main(gall_name,usid,password,title,content):
    rand_code, csrf, honey = getPageKey(gall_name)
    block_key = getBlock_key(gall_name,csrf)
    check_filter(gall_name,id,title,content,csrf,rand_code)
    post_num = write_post(gall_name,usid,password,title,content,rand_code,block_key,honey)
    return post_num
    

#비로그인(유동) 상태에서 글을 작성할수있습니다.
#post_num = dcapi.write.post("programming","nick","password","subject","content")
#print(post_num)
# -> 12345
#성공시 작성한글의 글 번호가 리턴됩니다. 


