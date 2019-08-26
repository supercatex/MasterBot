from requests_html import HTMLSession
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import re


# Get the keyword from microphone.
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1.0)
    print("Say something:")
    audio = r.record(source, offset=None, duration=None)

keyword = ""
try:
    keyword = r.recognize_google(audio, language="zh-TW")
    print("Google Speech Recognition thinks you said " + keyword)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
print(keyword)

# Find the answer from the internet.
session = HTMLSession()

url = "https://www.google.com.tw/search?q=" + keyword + "+百度知道"
print(url)
response = session.get(url)
a_list = response.html.find("a")
url = ""
for a in a_list:
    if re.findall("百度知道", a.text):
        url = a.attrs["href"]
        break

response = session.get(url)
c_list = response.html.find("div")
content = ""
for c in c_list:
    if "id" in c.attrs and re.findall("best-content-", c.attrs["id"]):
        content = "\n".join(c.text.split("\n")[1:])
        break
print(content)

# Speak the answer.
tts = gTTS(text=content, lang="zh-tw")
tts.save("response.mp3")
playsound("response.mp3")
