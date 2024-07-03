from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from urllib.parse import urlparse

def collect_links(browser, start_url, output_file_path):
    start_domain = urlparse(start_url).netloc  
    visited_urls = set()
    collected_urls = set()

    def start_collect_links(url):
        nonlocal visited_urls, collected_urls
        browser.get(url)
        try:
            alert = browser.switch_to.alert
            alert.accept()
        except NoAlertPresentException:
            pass
        try:    
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            links = browser.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                domain = urlparse(href).netloc
                if (href and domain == start_domain and
                    href not in visited_urls and 
                    href not in collected_urls and 
                    href.startswith('http') and 
                    'download' not in href):
                    collected_urls.add(href)
                    with open(output_file_path, 'a') as output_file:
                        output_file.write(href + '\n') 
                    print("Collected URL : ", href)
        except TimeoutException as e:
            print("TimeoutException occurred while collecting links for URL:", url)
            print("Message:", str(e))
        except Exception as e:
            print("An error occurred while collecting links for URL:", url)
            print("Message:", str(e))
        finally:
            visited_urls.add(url)

    start_collect_links(start_url)

    while collected_urls:
        url = collected_urls.pop()
        if url not in visited_urls:
            start_collect_links(url)