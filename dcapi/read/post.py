# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 갤러리 영문이름과 원하는 읽고자 하는 글의 번호를 받습니다.
# gall_name : 갤러리 영문이름
# post_num : 포스트 번호

def pars_title(soup): # 제목 
    title = soup.find_all("span",{"class":"title_subject"})
    return title[0].getText()

def pars_writer(soup): # 글쓴이 
    writer = soup.find_all("span",{"class" : "nickname"})
    return writer[0].get('title')

def pars_time(soup): # 작성시간
    time = soup.find_all("span",{"class" : "gall_date"})
    return time[0].get('title')

def pars_ip(soup): # IP 
    ip = soup.find_all("span",{"class" : "ip"})
    return ip[0].getText()

def pars_view(soup): # 조회수
    view = soup.find_all("span",{"class" : "gall_count"})
    view = view[0].getText()
    view = view.split("조회 ")
    return view[1]

def pars_comment(soup): # 댓글수
    comment = soup.find_all("span",{"class" : "gall_comment"})
    comment = comment[0].getText()
    comment = comment.split("댓글 ")
    return comment[1]

def pars_up(soup,post_num): # 추천수
    up = soup.find_all("p",{"id" : "recommend_view_up_"+str(post_num)})
    return up[0].getText()

def pars_down(soup,post_num): # 비추천수
    down = soup.find_all("p",{"id" : "recommend_view_down_"+str(post_num)})
    return down[0].getText()

def pars_gonic_up(soup,post_num): # 고닉 추천수
    gonic_up = soup.find_all("span",{"id" : "recommend_view_up_fix_"+str(post_num)})
    return gonic_up[0].getText()

def pars_content(soup): # 내용
    content = soup.find_all("div",{"style" : "overflow:hidden;"})
    return content[0].getText()

def pars(req,data): 
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    data["title"] = pars_title(soup)
    data["writer"] = pars_writer(soup)
    data["time"] = pars_time(soup)
    data["ip"] = pars_ip(soup)
    data["view_num"] = pars_view(soup)
    data["comment_num"] = pars_comment(soup)
    data["up"] = pars_up(soup,data["post_num"])
    data["down"] = pars_down(soup,data["post_num"])
    data["gonic_up"] = pars_gonic_up(soup,data["post_num"])
    data["content"] = pars_content(soup)

def _req(gall_name,post_num,data):
    _headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    _url = "http://gall.dcinside.com/board/view/?id="+gall_name+"&no="+str(post_num)+"&page=1"
    req = requests.get(url=_url,headers=_headers)
    pars(req,data)



def main(gall_name,post_num):
    data = { }
    data["post_num"] = post_num
    _req(gall_name,post_num,data)

    return data

# 게시글의 고유번호를 이용해 게시글의 정보를 가져옵니다
#data = dcapi.read.post("programming","930329")
#print(data)
# -> {'post_num': '930329', 'title': '제목입니다', 'writer': '닉네임', 'time': '2018-11-16 21:28:46', 'ip': '(218.153)', 'view_num': '44', 'comment_num': '0', 'up': '1', 'down': '2', 'gonic_up': '0', 'content': '내용이고요 '}
#print(data['post_num'],data['title'],data['content']) # 게시글의 원하는 정보만 사용할수도 있습니다.
# -> 930329 제목입니다 내용이고요