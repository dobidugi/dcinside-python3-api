import requests
from bs4 import BeautifulSoup

# 갤러리 영문이름, 글번호, 댓글고유번호, 비밀번호를 받습니다.
# 해당글의 댓글을 삭제할수 있습니다.

#gall_namme : 갤러리 영문 이름
#post_num : 삭제할 글의 번호 
#reply_num : 댓글의 고유 번호
#password : 비밀번호

def getPagetokens(gall_name,post_num):
    _hd ={
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
    }
    url = "https://m.dcinside.com/board/"+gall_name+"/"+post_num
    req = requests.get(url=url,headers=_hd)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    csrf = soup.find_all("meta",{"name" : "csrf-token"}) # get csrf token
    board_id = soup.find_all("input",{"id" : "board_id"})
    return csrf[0].get("content"), board_id[0].get("value")

def getBlockKey(gall_name,post_num,csrf):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "https://m.dcinside.com/board/"+gall_name+"/"+post_num,
        "X-Requested-With" : "XMLHttpRequest",
        "X-CSRF-TOKEN" : csrf
    }
    _payload = {
        "token_verify" : "com_submitDel"
    }

    url = "https://m.dcinside.com/ajax/access"
    req = requests.post(url=url,headers=_hd,data=_payload)
    pars_key =  (req.text).split('"')
    return pars_key[5]

def deleteReply(gall_name,post_num,password,reply_num,csrf,block_key,board_id):
    _hd = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
        "Referer" : "https://m.dcinside.com/board/"+gall_name+"/"+post_num,
        "X-Requested-With" : "XMLHttpRequest",
        "Cookie" : "m_dcinisde_"+gall_name+"="+gall_name+";m_dcinside_lately="+gall_name,
        "X-CSRF-TOKEN" : csrf
    }
    _payload = {
        "_token" : "",
        "commentDel_pw" : password,
        "comment_no" : reply_num,
        "comment_ch" : "",
        "id" : gall_name,
        "no" : post_num,
        "best_chk" : "",
        "board_id" : board_id,
        "con_key" : block_key
    }

    url = "https://m.dcinside.com/del/comment"
    req = requests.post(url=url,headers=_hd,data=_payload)
    res = (req.text).split('"')
    res = res[2].split(':')
    res = res[1].split("}")
    if(res[0]=="true"):
        return "true"
    else:
        return "false"



def main(gall_name,post_num,reply_num,password):
    csrf, board_id = getPagetokens(gall_name,post_num)
    block_key = getBlockKey(gall_name,post_num,csrf)
    res = deleteReply(gall_name,post_num,password,reply_num,csrf,block_key,board_id)
    return res


#### dcapi.delete.reply(gall_name,post_num,reply_num,password)
#```python
#비로그인(유동) 댓글을 삭제할수있습니다.
#result = dcapi.delete.reply("programming","993951","3809972","1234")
#print(result)
# -> true
# 글삭제 성공시 true 실패시 false값이 리턴됩니다.
#```
