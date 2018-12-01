import requests
from bs4 import BeautifulSoup

#gall_name : 갤러리 영문이름
#post_num : 댓글을달 글의 번호

def pars_csrf(soup):
    csrf = soup.find_all("meta",{"name" : "csrf-token"})
    return csrf[0].get("content")

def getBlock_key(gall_name,post_num,csrf):
    _url = "http://m.dcinside.com/ajax/access"
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Refere" : "http://m.dcinside.com/board/"+gall_name+"/"+post_num,
        "X-CSRF-TOKEN" : csrf,
        "X-Requested-With" : "XMLHttpRequest"
    }
    _payload = {
        "token_verify" : "com_submit"
    }
    req = requests.post(url=_url,headers=_hd,data=_payload)
    pars_key = (req.text).split('"')
    return pars_key[5]

def pars_hide_key(soup):
    hide_key = soup.find_all("input",{"class" : "hide-robot"}) 
    return hide_key[0].get("name")

def getKey(gall_name,post_num): 
    _url = "http://m.dcinside.com/board/"+gall_name+"/"+post_num
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/board/"+gall_name
    }
    req = requests.get(url=_url,headers=_hd)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    csrf = pars_csrf(soup) # get csrf code
    block_key = getBlock_key(gall_name,post_num,csrf) # get block_key
    hide_key = pars_hide_key(soup) # get hide-robot key
    return csrf, block_key, hide_key

def write_reply(gall_name,post_num,usid,password,reply,csrf,block_key,hide_key):
    _url = "http://m.dcinside.com/ajax/comment-write"
    _hd = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "http://m.dcinside.com/board/"+gall_name+"/"+post_num,  
        "X-CSRF-TOKEN" :  csrf,
        "X-Requested-With" : "XMLHttpRequest",
        "Origin" : "http://m.dcinside.com",
        "Cookie" : "m_dcinisde_"+gall_name+"="+gall_name+";m_dcinside_lately="+gall_name
    }

    _payload = {
        "comment_memo" : reply,
        "comment_nick" : usid,
        "comment_pw" : password,
        "mode" : "com_write",
        "comment_no" : "",
        "id" : gall_name,
        "no" : post_num,
        "best_chk" : "",
        "subject" : "제목",
        "board_id" : "0",
        "reple_id" : "",
        "cpage" : "1",
        "con_key" : block_key,
        hide_key : "1",
    }
    req = requests.post(url=_url,headers=_hd,data=_payload)
    pars = req.text.split(':')
    result = pars[1].split(',')
    return result[0]



def main(gall_name,post_num,usid,password,reply):
    csrf,block_key,hide_key = getKey(gall_name,post_num)
    return write_reply(gall_name,post_num,usid,password,reply,csrf,block_key,hide_key)


#비로그인(유동) 상태에서 댓글을 달을수있습니다.
#result = dcapi.write.reply("programming","938896","nick","pass1234","test")
#print(result)
# -> true
#성공할시 true값이 리턴됩니다. 
