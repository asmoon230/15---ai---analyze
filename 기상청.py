# API 호출을 위한 모듈을 불러옴
from urllib.request import urlopen

# 변수 선언
domain = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min?"
tm = "tm1=202302132200&tm2=202302132210&"
stn_id = "stn=104&"
option = "disp=0&help=0&authKey="
auth = "lp1YG3hzTjGdWBt4c24xFw"

url = domain + tm + stn_id + option + auth

# f라는 이름으로 url 호출
with urlopen(url) as f:
    
    html = f.read()
    print(html)