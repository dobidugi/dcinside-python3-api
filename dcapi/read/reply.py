# -*- coding:utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup

# 갤러리의 영문이름과 원하는 글의 고유변호를 받습니다.
# 해당 글의 댓글들을 볼수있습니다.
# gall_name : 갤러리 영문이름
# post_num : 포스트 번호

def pars_nick(req): # 닉네임들 파싱
    nick_list = []
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    nick = soup.find_all('a',{'class':'nick'})
    for i in nick:
        nick_list.append(i.text)
    return nick_list

def pars_replycount(req):
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    count = soup.find_all('span',{'class':'point-red'})
    return count[0].text

def pars_reply(req):
    count = 0
    count = int(pars_replycount(req))
    reply_list = []
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    nick = soup.find_all('li',{'class':'comment'})
    for i in range(0,count):
        reply_list.append(nick[i].find('p',{'class':'txt'}).text)
    return reply_list

def _req(gall_name,post_num):
    _headers = {
        "User-Agent" : "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
    }
    _url = "http://m.dcinside.com/board/"+gall_name+"/"+post_num
    req = requests.get(url=_url,headers=_headers)
    nick_list = []
    content_list = []
    nick_list = pars_nick(req)
    content_list = pars_reply(req)
    data = {}
    for i in range(0,int(pars_replycount(req))):
        data[i] = [nick_list[i],content_list[i]]
    
    return data


def main(gall_name,post_num):
    return _req(gall_name,post_num)
    
# 해당글의 댓글들을 가져옵니다. (인덱스는 0번부터 시작합니다)
#data = dcapi.read.reply("programming","931271")
#print(data)
# => {0: ['ㅇㅇ(121.134)', 'for문 두개로 해결하고 싶은거야?'], 1: ['ㅇㅇ(121.134)', 'list에 들어가는 순서는 어떻게 하고싶은거야?'], 2: ['ㅇㅇ(121.134)', 'm = len(mat)if m == 0:코드끝n = len(mat[0])if k > min(m,n):코드 끝우선 인풋 정합성 확인'], 3: ['ㅇㅇ(175.211)', 'list에 들어가는 순서 상관 없음. for문
# while문 몇개를 쓰던 상관없음'], 4: ['ㅇㅇ(175.211)', '아니 저렇게 간단하게 끝난다고?!']}
#print(data[0]) 
# 0번째 댓글의 정보들을 가져옵니다
# =>['ㅇㅇ(121.134)', 'for문 두개로 해결하고 싶은거야?']
#print(data[0][0])
# => ㅇㅇ(121.134) 0번째의 작성자 정보만 가져옵니다
