import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from fake_useragent import UserAgent
import time
import logging
from bs4 import BeautifulSoup
import random
import re
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_proxies(url):
    # Fetches and filters proxy addresses from given URL
    logging.info(f"Fetching proxies from {url}...")
    session = create_session()
    
    try:
        response = session.get(
            url, 
            timeout=15,
            headers=get_random_headers()
        )
        response.raise_for_status()
        
        proxy_pattern = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(?:\d{2,5})'
        matches = re.findall(proxy_pattern, response.text)
        
        valid_proxies = []
        for proxy in matches:
            if validate_proxy_format(proxy):
                valid_proxies.append(proxy)
        
        logging.info(f"Found {len(valid_proxies)} proxies from {url}")
        time.sleep(random.uniform(1, 2))
        return valid_proxies
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching proxies from {url}: {str(e)}")
        return []

def validate_proxy_format(proxy):
    try:
        ip, port = proxy.split(':')
        port = int(port)
        return 1 <= port <= 65535 and all(0 <= int(x) <= 255 for x in ip.split('.'))
    except:
        return False

def get_random_headers():
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
    }

def check_proxy(proxy, test_urls=None):
    # Tests if proxy is working with urls
    if test_urls is None:
        test_urls = ['https://market.yandex.ru/', 'https://www.yandex.com']
    
    if not proxy.startswith(('http://', 'https://')):
        proxy = f'http://{proxy}'
    
    proxies = {'http': proxy, 'https': proxy}
    session = create_session()

    for url in test_urls:
        try:
            response = session.get(
                url,
                proxies=proxies,
                timeout=10,
                headers=get_random_headers(),
                verify=False
            )
            if response.status_code != 200:
                return False
            time.sleep(random.uniform(1, 2))
        except:
            return False
    
    return True

def main():
    # List of proxy sources to fetch from
    proxy_sources = [
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=sg&proxy_format=protocolipport&format=text&timeout=20000',
        'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ae&proxy_format=protocolipport&format=text&timeout=20000',
        'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=in&proxy_format=protocolipport&format=text&timeout=20000',
        'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=gb&proxy_format=protocolipport&format=text&timeout=20000',
        'https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=us&proxy_format=protocolipport&format=text&timeout=20000',
        'https://www.proxy-list.download/api/v1/get?type=http',
        'https://www.proxy-list.download/api/v1/get?type=https',
        'https://www.proxy-list.download/api/v1/get?type=socks4',
        'https://www.proxy-list.download/api/v1/get?type=socks5',
        'https://www.fast-proxy.net/',
        'https://free-proxy-list.net/',
        'https://www.us-proxy.org/',
        'https://uk-proxy.uk/',
        'https://www.hidemyass.com/proxy/',
    ]
    
    all_proxies = []
    total_sources = len(proxy_sources)
    
    for idx, url in enumerate(proxy_sources, 1):
        proxies = fetch_proxies(url)
        all_proxies.extend(proxies)
        logging.info(f"Progress: {idx}/{total_sources} sources processed")
    
    unique_proxies = list(set(all_proxies))
    
    if not unique_proxies:
        logging.error("No proxies fetched. Exiting.")
        return
        
    with open('proxy.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_proxies))
    logging.info(f"Saved {len(unique_proxies)} unique proxies to proxy.txt")
    
    logging.info(f"Testing {len(unique_proxies)} unique proxies...")
    
    working = []
    with ThreadPoolExecutor(max_workers=4000) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in unique_proxies}
        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                if future.result():
                    working.append(proxy)
                    logging.info(f"Working proxy found: {proxy}")
            except Exception as e:
                logging.error(f"Error checking {proxy}: {str(e)}")

    if working:
        with open('working_proxies.txt', 'w') as f:
            f.write('\n'.join(working))
        logging.info(f"Saved {len(working)} working proxies")
    else:
        logging.warning("No working proxies found")

if __name__ == "__main__":
    main()