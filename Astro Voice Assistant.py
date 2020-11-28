from selenium import webdriver
import time
from datetime import datetime
import requests
import pyttsx3
import sys
import random
import winsound
import http.client
import azure.cognitiveservices.speech as speechsdk
import pyodbc 
from word2number import w2n
itemtext = ''
startup=''
check=0


cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-OP3MO6C\SQLEXPRESS;"
                      "Database=heyastron;"
                      "Trusted_Connection=yes;")




def textSpeech(speech):
    engine = pyttsx3.init()
    engine.setProperty('rate',150)
    engine.setProperty('volume', 3.0)
    tr_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_trTR_Tolga"
    engine.setProperty('voice', tr_voice_id)
    engine.say('')
    engine.say(speech)
    engine.runAndWait()


def speechToText():
    print('-----dinliyor-----')
    speech_key, service_region,lang= "51bc0ab8440c4215a56850623fdd654f", "westus",'tr-TR'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region,speech_recognition_language=lang)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Anlaşılan: {}".format(result.text))
        searchSubString(str(format(result.text)))
        
        
def speechToTextItem():
    global itemtext
    print('-----dinliyor-----')
    speech_key, service_region,lang= "51bc0ab8440c4215a56850623fdd654f", "westus",'tr-TR'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region,speech_recognition_language=lang)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    result = speech_recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("{}".format(result.text))
        itemtext = str(result.text)
        
    
        
def searchSubString(maintext):
    print(maintext)
    if 'zaman' in maintext or 'saat' in maintext:
        timer()
    elif 'hava' in maintext or 'durum' in maintext:
        weather()
    elif 'ara' in maintext or 'youtube'in maintext or 'video' in maintext or 'oynat' in maintext:
        search()
    elif 'kapa' in maintext or 'çık' in maintext or 'teşekkürler' in maintext or 'sağol' in maintext or 'görüşürüz' in maintext or 'hoşçakal' in maintext:
        selectFunction('exit')
    elif 'kayıp' in maintext or 'kaybol' in maintext or 'konum' in maintext or 'nerdeyim' in maintext or 'yer' in maintext:
        location()
    elif 'döviz' in maintext or 'para' in maintext or 'dolar' in maintext or 'borsa' in maintext:
        currency()
    elif 'haber' in maintext or 'güncel' in maintext or 'gazete' in maintext or 'gündem' in maintext:
        newspaper() 
    elif 'oyun' in maintext or 'oyna'in maintext or 'eğlence' in maintext or 'tahmin' in maintext:
        game()
    elif 'zar' in maintext  or 'iki' in maintext or 'zar at' in maintext:
        diceRoll()
    else:
        sqlSearch(maintext)
    
def sqlSearch(maintext):
    cursor = cnxn.cursor()
    cursor.execute('select question from question')
    for row in cursor:
         print(row,)
        
    ##speechToTextItem()
    itemtext=maintext
    cursor.execute("SELECT answer FROM answer a, question q WHERE question = '"+itemtext+"' AND a.id=q.answer_id")
    row = cursor.fetchone()
    print(row[0])
    textSpeech(row[0])
    speechToText()
     ##TEST LOOP
        ##END OF SQL 

def dontUnderstand(searchkey):
    searchthis=searchkey
    print("Anlaşılmadı. Web'de aramamı ister misiniz?")
    textSpeech("Anlaşılmadı. Web'de aramamı ister misiniz?") 
    speechToTextItem()
    if 'evet' in itemtext or 'aynen' in itemtext or 'oynat' in itemtext or 'ara' in itemtext:
        textSpeech('Tamamdır. Şunu aratıyorum.'),textSpeech(searchthis)    
        driver = webdriver.Chrome(executable_path=r'C:\Selenium\chromedriver.exe')
        driver.maximize_window()  
        driver.get('https://www.google.com')
        element = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[1]/div/div[1]/input')
        element.send_keys(searchthis)
        search_click = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div/div[3]/center/input[1]')
        search_click.click()
        speechToText()
    else:
        print('Tamam. Yeni komutları bekliyorum')
        textSpeech("Tamam. Yeni komutları bekliyorum")
        speechToText()   
        
def diceRoll():
    textSpeech('İki zar atıyorum')
    print('İki zar atıyorum')
    dice_one=random.randint(1,6)
    dice_two=random.randint(1,6)
    print(dice_one , 've' , dice_two , 'geldi')
    textSpeech(dice_one)
    textSpeech(dice_two)
    speechToText()
    
    
def game():
    numberToGuess=random.randint(0,100)
    userGuess=-1 
    print('1-100 arası bir sayı giriniz')
    textSpeech('1-100 arası bir sayı giriniz')
    while userGuess!=numberToGuess:
        speechToTextItem()
        itemtest = w2n.word_to_num(itemtext)
        ##userGuess=int(input("1-100 arası bir sayı giriniz"))
        if itemtest>numberToGuess:
            textSpeech('Çok büyük')
            print("Çok büyük!")
        elif itemtest<numberToGuess:
            textSpeech('Çok küçük')
            print("Çok küçük!")
        elif itemtest==numberToGuess:
            print("Güzel tahmin " + str(numberToGuess) + " doğru cevap.")
            textSpeech(str(numbertoGuess)),textSpeech("doğru cevap")
            break
            speechToText()

def exitted():
    textSpeech("Kendine iyi bak. Görüşürüz")
    sys.exit("Application terminated!")
    
def location():
    location=requests.get('http://ip-api.com/json/')   
    locationdata=location.json()
    locationcountry=str(locationdata["countryCode"])
    locationcity=str(locationdata["city"])
    textSpeech('Konumunuz.'),textSpeech(locationcountry),textSpeech(locationcity) 
    print("Ülkeniz: ",locationcountry,"\nŞehriniz: ",locationcity)
    speechToText()
        
def newspaper():
    conn = http.client.HTTPSConnection("api.hurriyet.com.tr")
    headers = {
    'accept': "application/json",
    'apikey': "43021464e9ea4a20bf52ac9979b3bee1"
    }
    ##textSpeech("Kaç tane haber okumamı istersiniz?")
    ##speechToTextItem()
    ##itemtest = w2n.word_to_num(itemtext)
    ##itemtest=str(itemtest)
    conn.request("GET", "/v1/articles?%24select=Description&%24top=1", headers=headers)
    res = conn.getresponse()
    data = res.read()
    newsdesc=(data.decode("utf-8"))
    ##while 
    gazeteozet=newsdesc[newsdesc.find(":")+1:newsdesc.find(".")]
    print(gazeteozet)
    textSpeech(gazeteozet)
    speechToText()
    
            
        
def weather():
    textSpeech('Lütfen şehir giriniz'),
    print('Lütfen şehir giriniz')
    speechToTextItem()
   ## weather=requests.get('https://api.openweathermap.org/data/2.5/weather?q='+itemtext+'&appid=f59eae46eb0be6273c18248c10c03608')  
    weather=requests.get('https://api.openweathermap.org/data/2.5/weather?q='+itemtext+'&APPID=8678c29ac4f178f3c635568531326278')
    weatherdata = weather.json()
    response=int(weatherdata.get('cod'))
    if response == 200:
        kelvint=float(weatherdata["main"].get('temp'))
        celcius=kelvint-273
        textSpeech('Hava sıcaklığı') ,textSpeech(itemtext),textSpeech(round(celcius,1)),textSpeech('derece')   
        print(itemtext+' hava sıcaklığı =',round(celcius,1))
    else:
        print('Söylenilen yer anlaşılamadı.')
        textSpeech('Söylenilen yer anlaşılamadı.')
        weather()
    speechToText()
      

def timer():
    timenow = datetime.now()
    textSpeech('Şu an saat.'),textSpeech(timenow.hour),textSpeech(':') ,textSpeech(timenow.minute) 
    print('saat suan ',timenow.hour,':',timenow.minute)
    speechToText()

    
def search():
    print('Ne aramamı istersiniz?')
    textSpeech('Ne aramamı istersiniz?') 
    speechToTextItem()
    textSpeech('Tamamdır. Şunu oynatıyorum.'),textSpeech(itemtext)
    driver = webdriver.Chrome(executable_path=r'C:\Selenium\chromedriver.exe')
    driver.set_window_position(-10000,0)
    driver.get('https://www.youtube.com')
    element = driver.find_element_by_id('search')
    element.send_keys(itemtext)
    s_click = driver.find_element_by_id('search-icon-legacy')
    s_click.click()
    time.sleep(1)
    firstvid = driver.find_element_by_id('dismissable')
    firstvid.click()
    driver.maximize_window() 
    speechToText()


def currency(): 
    textSpeech("Çevirmek istediğiniz para miktarını giriniz:")
    print('cevirmek istediğiniz para miktarını giriniz:   ')
    speechToTextItem()
    ceviri = w2n.word_to_num(itemtext)
    currencynow=requests.get('http://data.fixer.io/api/latest?access_key=0f9c2882c12ba6ca085ddd1cc40a45ba&symbols=USD,GBP,TRY')
    data =currencynow.json()
    usd=1/float(data["rates"].get('TRY'))*float(data["rates"].get('USD'))*ceviri
    eur=1/float(data["rates"].get('TRY'))*ceviri
    gbp=1/float(data["rates"].get('TRY'))*float(data["rates"].get('GBP'))*ceviri
    print('',ceviri,' = ',round(usd,2),'dolar\n',ceviri,' = ',round(eur,2),'euro\n',ceviri,' = ',round(gbp,2),'sterlin')
    textSpeech(cevirial),textSpeech('Türk lirası eşittir:'),textSpeech(round(usd,2)),textSpeech('dolar'),textSpeech(round(eur,2)),textSpeech('euro'),textSpeech(round(gbp,2)),textSpeech('sterlin')
    speechToText()
    


def startme():
    speechToTextItem()
    global check
    while check==0:
        if 'asistan' in itemtext:
            check=1
            break
        else:
            ##print('yanlış başlatma komutu')
            check=0
            startme()
    startsuccessful()     
    
def startsuccessful():    
       print('Merhaba. Ben asistanınız ASTRO. Sizlere nasıl yardımcı olabilirim?')
       textSpeech('Merhaba. Ben asistanınız ASTRO. Sizlere nasıl yardımcı olabilirim?')
       speechToText()
       
    
       
startsuccessful()       
