import subprocess
from mitmproxy import http
from urllib.parse import urlparse, urlunparse
from datetime import datetime


class RequestInterceptor:
    def __init__(self):
        self.success_file_name = datetime.now().strftime('%Y_%m_%d') + '_success.txt'
        self.target_url = "https://example.com"  # 대상 url

        self.max_age_seconds = 60  # 일정 시간(초) 지난 패킷만 저장
        self.requests_with_custom_header = {}   # request custom header 저장 딕셔너리
        self.replacement_text = "aaaaaaaaaa"
    def request(self, flow: http.HTTPFlow) -> None:
        # request 라이브러리에서 발생한 패킷 감지
        if 'cdn-cgi' in flow.request.pretty_url:
            pass
        elif 'X-Custom-Header' in flow.request.headers:
            custom_header_value = flow.request.headers.get('X-Custom-Header')
            self.requests_with_custom_header[custom_header_value] = str(flow.request) + "\n" + flow.request.text

        # target url만 필터링
        elif self.target_url in flow.request.pretty_url:
            # method 확인
            if flow.request.method == "GET":
                # GET 요청에서는 쿼리 파라미터 저장
                # query_params = flow.request.qery.items()
                if self.replacement_text in flow.request.pretty_url.lower():
                    # replacement_text 문자열의 위치 확인
                    index = flow.request.pretty_url.find(self.replacement_text)
                    if index != -1:  # 문자열이 발견되면
                        params_index = flow.request.pretty_url.find('?')    # url 확인
                        if params_index != -1:
                        
                            url = flow.request.pretty_url[:params_index]
                            get_first = flow.request.pretty_url[params_index + 1:index]
                            get_last = flow.request.pretty_url[index + len(self.replacement_text):]

                            self.forward_data = ["GET",url, get_first, get_last]
                            self.process = subprocess.Popen(["python", "./SQL_injection.py"] + self.forward_data)
                        
            elif flow.request.method == "POST":
                if self.replacement_text in flow.request.text:
                # "aaaaaaaaa" 문자열의 위치 확인
                    index = flow.request.text.find(self.replacement_text)
                    if index != -1:  # 문자열이 발견되면   
                        url = flow.request.pretty_url
                        post_first = flow.request.text[:index]
                        post_last = flow.request.text[index + len(self.replacement_text):]
                    
                        self.forward_data = ["POST", url, post_first, post_last]
                        self.process = subprocess.Popen(["python", "./SQL_injection.py"] + self.forward_data)

                
    # response 값 체크
    def response(self, flow:http.HTTPFlow) -> None:      

        custom_header_value = flow.request.headers.get('X-Custom-Header') # request에 해당하는 X-Custom-Header의 값을 들고옴
        if custom_header_value in self.requests_with_custom_header:

            # 해당하는 커스텀 헤더를 가진 요청에 대한 응답 처리
            current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # 현재 시간 기록


             # 문자열을 datetime 객체로 변환
            current_time = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M:%S')
            custom_time = datetime.strptime(custom_header_value, '%Y-%m-%d %H:%M:%S')   
                
            time_difference = current_time - custom_time    # 패킷의 응답 시간

            if time_difference.seconds >= 20:   # 응답시간
                original_request = self.requests_with_custom_header.pop(custom_header_value)
                print(f"Response for request with custom header '{custom_header_value}'")
                print(f"original_requests : {original_request}" )
                with open(f'{self.success_file_name}','a') as f:
                    f.write(f'Timestamp : {custom_header_value}\n')
                    f.write(f"{original_request}\n")
                    f.write(f"----------------------------\n\n")
                f.close()


    # 연결 끊기
    def close_connection(self):
        if hasattr(self, "process"):
            self.process.kill()
    
addons = [RequestInterceptor()]

if __name__ == "__main__":
    from mitmproxy.tools.main import mitmweb

    mitmweb(["-s", __file__])