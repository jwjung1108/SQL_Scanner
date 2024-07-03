from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time
import threading


start_url = 'https://example.com'   # input your url
urls_path = 'urls.txt'
mitmproxy_address = "127.0.0.1:8080"

def run_crawling():
    print("Starting crawling...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(options=chrome_options)

    import Crawling
    Crawling.collect_links(browser, start_url, urls_path)
    browser.quit()
    print("*****************************")
    print("Crawling finished.")
    print("*****************************")

def run_injection():
    print("Starting injection...")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument(f"--proxy-server=http://{mitmproxy_address}")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_options)

    import input
    input.process_urls(browser, urls_path)
    browser.quit()
    print("*****************************")
    print("Injection finished.")
    print("*****************************")

if __name__ == "__main__":
    print("*****************************")
    print("Welcome to SQL Fuzzer")
    print("Starting!!!!")
    print("*****************************")

    crawling_thread = threading.Thread(target=run_crawling)
    injection_thread = threading.Thread(target=run_injection)

    crawling_thread.start()
    time.sleep(3)
    injection_thread.start()

    crawling_thread.join()
    injection_thread.join()

    os.remove(urls_path)
    print("All tasks completed.")