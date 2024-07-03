from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from urllib.parse import urlparse

def process_urls(browser, urls_path):
    # 이미 방문한 URL을 저장하는 set 생성
    visited_urls = set()
    
    with open(urls_path, 'r') as urls_file:
        for url in urls_file:
            url = url.strip()
            try:
                # 이미 방문한 URL인지 확인
                if url in visited_urls:
                    print("URL already visited, skipping...")
                    continue
                
                browser.get(url)
                try:
                    alert = browser.switch_to.alert
                    alert.accept()
                except NoAlertPresentException:
                    pass
                input_elements = browser.find_elements(By.XPATH, "//input[not(@type='hidden') and not(@type='checkbox') and not(@type='submit') and not(@type='file') and not(@type='button')] | //textarea")
                if len(input_elements) == 0:
                    print("No input elements found, skipping...")
                    continue
                else:
                    for element in input_elements:
                        if element.get_attribute("value"):
                            continue 
                        element.send_keys("aaaaaaaaaa")
                        element.send_keys(Keys.SPACE)
                    element.send_keys(Keys.ENTER)
                    try:
                        alert = browser.switch_to.alert
                        alert.accept()
                    except NoAlertPresentException:
                        pass
                    print("Injected URL : ", browser.current_url)
                    
                # 처리한 URL을 방문한 URL 목록에 추가
                visited_urls.add(url)
                
            except Exception as e:
                print("An error occurred while processing URL:", url)
                print("Exception:", str(e))

