import urllib.request
from bs4 import BeautifulSoup

# parse url link to readable bs4 content
# @param    url
#           The url needed to be parsed
# @return   soup
#           parsed url
def parseUrl(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup
