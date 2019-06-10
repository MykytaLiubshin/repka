import telebot
import time
import requests
import urllib

#My links Bank:
currency_link = "https://finance.i.ua/bank/10/"
tarasivka_kardachi_link = 'http://poezdato.net/raspisanie-poezdov/tarasovka,kievskaya-obl--karavaevy-dachi/'
kardachi_tarasivka_link = "http://poizdato.net/rozklad-poizdiv/karavaievi-dachi--tarasivka,kyivska-obl/"

def CurrencyCheck(link):

    f = urllib.request.urlopen(link)
    myfile = f.read()
    lst=str(myfile)
    lst=lst.split('<span>')
    arr=[]
    arr1=[]
    array=[]
    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i]=lst[i].split('</span>')
    for i in lst:
        if i[0].isdigit:
            array.append(i[0])

    for i in range(1,7):
        arr.append(array[-i])
    for i in range(1,7):
        arr1.append(arr[-i])

    dollar = [arr1[0],arr1[1]]
    euro = [arr1[2],arr1[3]]
    return[dollar,euro]

def TrainCheck(link):

    
    f = urllib.request.urlopen(link)
    myfile = f.read()
    lst=str(myfile)
    lst=lst.split('<span class="_time">')
    arr=[]
    arr1=[]
    array=[]
    timeof=[]
    
    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i]=lst[i].split('</span>')
        
    for i in lst:
        if i[0].isdigit:
            array.append(i[0])
            
    respond='The full train schedule:'
    respond+='\n'
    
    for i in range(1,len(array)):
        
        if i%2==0:

            respond += str(int(i/2))
            respond += '. '
            if((i/2)<10):
                respond += ' '
            respond += array[i-1]
            respond += '---------------'
            respond += array[i]
            respond += '\n'
        
    return(respond)

def NearestTrain(link):
    
    f = urllib.request.urlopen(link)
    myfile = f.read()
    lst=str(myfile)
    lst=lst.split('<span class="_time">')
    
    arr=[]
    arr1=[]
    array=[]
    timeof=[]
    
    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i]=lst[i].split('</span>')
        
    for i in lst:
        if i[0].isdigit:
            array.append(i[0])
            
    for i in range(1,len(array)):
        times=array[i].split('.')
        times=int(times[0])*60+int(times[1])
        
        if((i+1)%2==0):
            timeof.append(times)
        
        CurrentTime = str(time.asctime())
        CurrentTime = CurrentTime.split(' ')
        CurrentTime= CurrentTime[3]
        CurrentTime = str(CurrentTime).split(':')
        CurrentTime = int(CurrentTime[0])*60+int(CurrentTime[1])
        
        
    ThreeNearest = []
    IdOfNearest=0
    TimeDifference = []
    counter = 0
    
    for i in range(len(timeof)):
        TimeDifference.append(timeof[i] - CurrentTime)
        
    for i in range(len(TimeDifference)):
        IdOfNearest+=1
        
        if counter<3:
            if TimeDifference[i]>0:
                counter +=1
                ThreeNearest.append(IdOfNearest)
    
    respond1 = "The three nearest trains are: "
    respond1 += '\n'
    
    for i in range(3):
        
        respond1 += array[ThreeNearest[i]*2-1]
        respond1 += '---------------'
        respond1 += array[ThreeNearest[i]*2]
        respond1 += '\n'
        
    return(respond1)

print(CurrencyCheck(currency_link))

bot_token = "745661558:AAEMcMTj7ewXtVtnZ-qYuYMhSqyLom5NC7E"

bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')

@bot.message_handler(commands=['train_shedule_tar'])
def send_welcome(message):
    bot.reply_to(message, TrainCheck(tarasivka_kardachi_link))

@bot.message_handler(commands=['train_shedule_kar'])
def send_welcome(message):
    bot.reply_to(message, TrainCheck(kardachi_tarasivka_link))

@bot.message_handler(commands=['nearest_tarasivka'])
def send_welcome(message):
    bot.reply_to(message, NearestTrain(tarasivka_kardachi_link))
    
@bot.message_handler(commands=['nearest_kardachi'])
def send_welcome(message):
    bot.reply_to(message, NearestTrain(kardachi_tarasivka_link))

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'To use this bot, send it a username')

    

@bot.message_handler(commands=['currency'])
def send_currency(message):
    #| -- --  Dollar -- --  | -- -- -- Euro -- -- --|
    #| -To Buy-|-To Sell- - | -  To Buy -|- To Sell |
    #|  27.7500  |  28.1000 | 31.4000  |   32.0000  |
   
    message1 = '| -- -- -- Dollar -- -- -|- -- -- -- Euro -- -- --|'
    message1+= '\n'
    message1+= '|-To Buy- -To Sell-|- -To Buy- -To Sell|'
    message1+= '\n'
    message1+= '|'
    message1+= str(CurrencyCheck(currency_link)[0][0])
    message1+= '|'
    message1+= str(CurrencyCheck(currency_link)[0][1])
    message1+= '|'
    message1+= str(CurrencyCheck(currency_link)[1][0])
    message1+= '|'
    message1+= str(CurrencyCheck(currency_link)[1][1])
    message1+= '|'


    bot.reply_to(message, message1)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
