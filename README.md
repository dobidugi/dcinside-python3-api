# dcinside-python3api
 # 아직 개발중
 
##### dcinside python3 전용 비공식 API 입니다.

# 사용법
###### 프로젝트에 dcapi 폴더를 포함해준후 선언해줍니다.
```python
import dcapi
```

#### dcapi.write.post(gall_name,usid,password,title,content)
```python
#비로그인(유동) 상태에서 글을 작성할수있습니다.
dcapi.write.post("programming","nick","password","subject","content")
#리턴값은 따로없습니다
```
#### dcapi.read.post(gall_name,post_num)
```python
# 게시글의 고유번호를 이용해 게시글의 정보를 가져옵니다
data = dcapi.read.post("programming","930329")
print(data)
# -> {'post_num': '930329', 'title': '제목입니다', 'writer': '닉네임', 'time': '2018-11-16 21:28:46', 'ip': '(218.153)', 'view_num': '44', 'comment_num': '0', 'up': '1', 'down': '2', 'gonic_up': '0', 'content': '내용이고요 '}
print(data['post_num'],data['title'],data['content']) # 게시글의 원하는 정보만 사용할수도 있습니다.
# -> 930329 제목입니다 내용이고요
```
#### dcapi.read.reply(gall_name,post_num)
```python
# 해당글의 댓글들을 가져옵니다. (인덱스는 0번부터 시작합니다)
#data = dcapi.read.reply("programming","931271")
print(data)
# => {0: ['ㅇㅇ(121.134)', 'for문 두개로 해결하고 싶은거야?'], 1: ['ㅇㅇ(121.134)', 'list에 들어가는 순서는 어떻게 하고싶은거야?'], 2: ['ㅇㅇ(121.134)', 'm = len(mat)if m == 0:코드끝n = len(mat[0])if k > min(m,n):코드 끝우선 인풋 정합성 확인'], 3: ['ㅇㅇ(175.211)', 'list에 들어가는 순서 상관 없음. for문
# while문 몇개를 쓰던 상관없음'], 4: ['ㅇㅇ(175.211)', '아니 저렇게 간단하게 끝난다고?!']}
print(data[0]) 
# 0번째 댓글의 정보들을 가져옵니다
# =>['ㅇㅇ(121.134)', 'for문 두개로 해결하고 싶은거야?']
print(data[0][0])
# => ㅇㅇ(121.134) 0번째의 작성자 정보만 가져옵니다
```

#### dcapi.read.title(gall_name,start_page,end_page)
```python
# 해당 갤러리 글들의 제목들을 가져옵니다.
data = dcapi.read.title("programming")
print(data)
# -> {1: ['첫번째글제목'],['두번째글제목'], ... }
# 페이지 구간을 적어줄수있습니다
data = dcapi.read.title("programming",1,5) # 1페이지부터 5페이지까지 제목들을 가져오기
print(data)
# -> {1: ['첫번째글제목'],['두번째글제목'], ... ,2 : ['첫번째글제목'],['두번째글제목'], ... }
print(data[2]) # 다수의 페이지를 가져와 원하는 페이지들의 제목만 볼수도있습니다.
# -> {2 : ['첫번째글제목'],['두번째글제목'], ... }
print(data[2][10]) # 원하는 페이지에 원하는 인덱스의 제목만도 가져올수있습니다.
# -> 10번째글의 제목입니다.
```
