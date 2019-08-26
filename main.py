from requests_html import HTMLSession
import re
import speech_recognition as sr
import pyttsx3
import SearchEngine
import webbrowser


lang = "en"
site = ["Wikipedia"]
func_list = [
    SearchEngine.wiki
]

# Get the keyword from microphone.
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1.0)
    print("Say something:")
    audio = r.listen(source)

print("progressing...")
keyword = ""
try:
    keyword = r.recognize_google(audio, language=lang)
    print("You said:", keyword)
except Exception as e:
    print(e)

# Find the answer from the internet.
session = HTMLSession()

url = "https://www.google.com/search?q=" + keyword
response = session.get(url)
# print(url)

url = ""
content = "I don't know."
index = 0

ifM9O = response.html.find("div[class='ifM9O'] a")
if len(ifM9O) > 0:
    for i in ifM9O:
        if i.text == "Wikipedia":
            url = i.attrs["href"]

if url == "":
    a_list = response.html.find("a")
    print(a_list)
    for a in a_list:
        print(a.text)
        match = re.findall("|".join(site), a.text)
        if len(match) > 0:
            url = a.attrs["href"]
            index = site.index(match[0])
            break

# Special for site to find the content.
if url != "":
    print(url)
    webbrowser.open(url)
    content = func_list[index](url)
    content = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", content)
    print(".\n".join(content.split(".")))

# Speak the answer.
engine = pyttsx3.init()
engine.setProperty('rate', 120)
engine.setProperty('voice', engine.getProperty('voices')[1].id)
engine.say(content)
engine.runAndWait()
