from getpass import getpass
from package import parseUrl
from bs4 import BeautifulSoup
import requests

## ask user login info
# @param    loginLink
#           link of login web page
def login(url, loginLink):
    userName = ""
    password = ""
    loginDict= {}

    print("Please enter user name(lastname.#): ", end = "")
    userName = input()
    password = getpass(prompt = 'Please enter password (for privacy, password will be invisible): ')
    print(loginLink)
    urlSoup = parseUrl.parseUrl(url)
    csrf = urlSoup.find('meta', attrs = {"name" : "csrf-token"})
    print(csrf)
    csrfToken = csrf.get('content')
    print(csrfToken)

    loginSoup = parseUrl.parseUrl(loginLink)
    print (loginSoup)
    loginAction = loginSoup.find('form', attrs = {"id": "login", "method": "POST"})
    loginActionLink = loginSoup.get('action')
    print (loginActionLink)
    
    loginDict['j_username'] = userName
    loginDict['j_password'] = password
    loginDict['csrf_token'] = csrfToken
    
    print("request login session...", end = "")
    loginSession = requests.session()
    print("Done!")
    print("send POST...", end = "")
    loginSession.post(loginActionLink, data = loginDict)
    print("Done!")
    loggedPage = loginSession.get(url)
    print(loggedPage.text)
