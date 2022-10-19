# import the necessary packages
from PIL import Image
import webbrowser
from base64 import b64encode
import json
import io
import os
import re 
import pyscreenshot as Imagegrab
import urllib
from bs4 import BeautifulSoup
import requests
import cv2
import pytesseract
from googleapiclient.discovery import build


WORDS_TO_STRIP = [
    'who','following','eliminated','viewer',
    'this','is','was',
    '?', ',','what', 'these', 'which','not','q1.','q2.','q3.','q4.','q5.','q6.','q7.','q8.','q9.','q10.','&']




my_api_key = "AIzaSyAlq_YIrc48RheVReuO_gdGxjuWZVgp-sI"
my_cse_id = "017443262401049596954:bxztx4rhphm"

def get_question():
        # part of the screen
        im=Imagegrab.grab(bbox=(1,280,360,700))
        im.save('box.png')
        img = cv2.imread('box.png')
        text = pytesseract.image_to_string(img)
        question = "\n".join(text[:-3])
        #print(question)
        options = "\n".join(text[-4:-1]).strip("?")
        print(question+ "\n"+options)
        words = [word for word in question.split() if word.lower()not in WORDS_TO_STRIP]
        query = ' '.join(words)
        print(query)
        k=re.split('\n+', options)
        a = k[0].strip('A.')
        b = k[1].strip('B.')
        c = k[2].strip('C.')
        al=len(a)
        bl=len(b)
        cl=len(c)
        fv=min(al,bl,cl)
        if fv>7 :
           fv=7
        a = a[0:fv]
        b = b[0:fv]
        c = c[0:fv]
        def google_search(search_term, api_key, cse_id, **kwargs):
            service = build("customsearch", "v1", developerKey=api_key)
            res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
            return res['items']


        results = google_search(query, my_api_key, my_cse_id, num=10)
        fp = open('tg.txt',"w")
        for result in results:
            print(result,file = fp)
        fp.close()
        fp = open('tg.txt',"rt") 
        contents = fp.read()
        print('##########$$$$$$PARTIAL$$$$$$$$########')
        print(a,end="------->  ")
        print(len(re.findall(a,contents,re.IGNORECASE)))
        print(b,end="----------> ")
        print(len(re.findall(b,contents,re.IGNORECASE)))
        print(c,end="-------------> ")
        print(len(re.findall(c,contents,re.IGNORECASE)))
        print('________ FOR complete scan BELOW ____________')		        
        a = k[0].strip('A.')
        b = k[1].strip('B.')
        c = k[2].strip('C.')
        print(a,end="--------> ")
        print(len(re.findall(a,contents,re.IGNORECASE)))
        print(b,end="----------->  ")
        print(len(re.findall(b,contents,re.IGNORECASE)))
        print(c,end="-------------->  ")
        print(len(re.findall(c,contents,re.IGNORECASE)))
        sun = query+" OR "+'"'+k[0].strip('A.')+'"'+' OR '+'"'+k[1].strip('B.')+'"'+' OR '+'"'+k[2].strip('C.')+'"'
        print(sun)
        url1 = 'https://www.google.com/search?hl=en&q='+sun+'&btnG=Google+Search&tbs=0&safe=off&tbm='
        url2 = 'https://www.google.com/search?hl=en&q='+query+'&btnG=Google+Search&tbs=0&safe=off&tbm='
        webbrowser.open_new(url1)




while(True):
    key_pressed = input('Press ENTER to screenshot live game')
    if key_pressed == '':
        get_question()
