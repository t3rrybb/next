import argparse
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
import random
import sys


def full_link(base, href):
    """
    Expand href to be a full link by prefixing it with the given base URI if applicable.

    :param base: Base URI without any trailing '/', e.g. http://www.google.com.
    :param href: The URL from href tag.
    :return: The full link where applicable or href as is.
    """
    if href.startswith('/'):
        link = base + href
    else:
        link = href

    return link


def pick(size: int, choice: int) -> int:
    """
    Return the index of one element in a list based on the given choice.

    :param size: The size of the list of elements.
    :param choice: Which element to pick, e.g. 1 indicates the 1st element, and 2 the second etc while -1 the last;
    if None or 0, a random one.
    :return: The index of the element in the list, starting from 0 (not 1).
    """
    if not choice or choice == 0:
        index = random.randint(0, size - 1)
    elif 0 < choice < size:
        index = choice - 1
    elif size < choice:
        index = size - 1
    elif choice < 0 and abs(choice) < size:
        index = size + choice
    elif choice < 0 and abs(choice) > size:
        index = 0

    return index


def scrape(url, proxy, regexp):
    """
    Scrape the url to find links matching the pattern specified by a regular expression.
    :param url: The url to scrape.
    :param proxy: A web proxy to use.
    :param regexp: A regular expression to match any found links with.
    :return: A ResultSet of matching PageElements.
    """
    if proxy:
        proxies = {
            'http': proxy,
            'https': proxy
        }
    else:
        proxies = None

    if regexp:
        pattern = re.compile(regexp)
    else:
        pattern = True

    resp = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(resp.text, "html.parser")

    rs = soup.find_all('a', href=pattern)
    resp.close()

    return rs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A tool to scrape websites for the next link")
    parser.add_argument("url", help="the http url to scrape")
    parser.add_argument("-x", "--proxy", help="the proxy to use")
    parser.add_argument("-e", "--regexp", help="the regular expression to match links with")
    parser.add_argument("-s", "--select", type=int, help="the link to select from the matches")
    args = parser.parse_args()

    parsed_uri = urlparse(args.url)
    base_uri = f'{parsed_uri.scheme}://{parsed_uri.netloc}'

    rs = scrape(args.url, args.proxy, args.regexp)
    size = len(rs)

    if size > 0:
        i = pick(size, args.select)
        print(full_link(base_uri, rs[i]['href']))
    else:
        print("No link found!", file=sys.stderr)
