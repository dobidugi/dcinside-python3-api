# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

# 해당 갤러리의 제목들을 가져와 페이지별로 딕셔너리에 담습니다.
# page is key title_list is value
# gall_name  : 갤러리 영문이름
# start_page : 시작페이지
# end_page : 마지막 페이지

def _req(gall_name,page,return_data):
    _headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    _url = "http://gall.dcinside.com/board/lists/?id="+gall_name+"&page="+str(page)
    req = requests.get(url=_url,headers=_headers)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    list_title1 = soup.find_all('td',{'class':'gall_tit ub-word'})
    temp = []
    for i in  range(0,50):
        temp.append(list_title1[i].find('a').getText())
    return_data[page] = temp

def main(gall_name,start_page=1,end_page=1):
    print("hello")
    start = start_page
    end = end_page + 1
    return_data = { }
    for i in range(start,end):
        _req(gall_name,i,return_data)
    return return_data

# 해당 갤러리 글들의 제목들을 가져옵니다.
# data = dcapi.read.title("programming")
# print(data)
# -> {1: ['첫번째글'],['두번째글'], ... }
# 가져오고싶은 페이지 구간을 적어줄수있습니다
# data = dcapi.read.title("programming",1,5) # 1페이지부터 5페이지까지 제목들을 가져오기
# print(data)
# -> {1: ['첫번째글'],['두번째글'], ... ,2 : ['첫번째글'],['두번째글'], ... }
# print(data[2]) # 다수의 페이지를 가져와 원하는 페이지들의 제목만 볼수도있습니다.
# -> {2 : ['첫번째글'],['두번째글'], ... }
# print(data[2][10]) # 원하는 페이지에 원하는 인덱스의 제목만도 가져올수있습니다.
# -> 10번째글의 제목입니다.