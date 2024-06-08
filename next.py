import argparse
import requests
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A tool to scrape websites for the next link")
    parser.add_argument("url", help="the http url to scrape")
    parser.add_argument("-x", "--proxy", help="the proxy to use")
    parser.add_argument("-e", "--regexp", help="the regular expression to match")
    args = parser.parse_args()

    if args.proxy:
        proxies = {
            'http': args.proxy,
            'https': args.proxy
        }
    else:
        proxies = None

    if args.regexp:
        pattern = re.compile(args.regexp)
    else:
        pattern = True

    resp = requests.get(args.url, proxies=proxies)
    soup = BeautifulSoup(resp.text, "html.parser")
    for a in soup.find_all('a', href=pattern):
        print(a['href'])

    resp.close()