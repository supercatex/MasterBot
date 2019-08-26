import re
from requests_html import HTMLSession, HTML


def wiki(url):
    content = ""
    session = HTMLSession()
    response = session.get(url)
    c_list = response.html.find("div[id='mw-content-text'] > div > p")
    for c in c_list:
        if len(c.text) > 10:
            content += c.text
            break
    return content
