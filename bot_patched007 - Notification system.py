import telebot
import time
import requests
import urllib

from repka.parser import train_parser
from repka.constants import (
    CURRENCY_LINK,
    TARASOVKA_KARDACHI_LINK,
    KARDACHI_TARASOVKA_LINK
)
#My links Bank:

def CurrencyCheck(link):

    f = urllib.request.urlopen(link)
    myfile = f.read()
    lst = str(myfile).split('<span>')
    arr = []
    arr1 = []
    array = []
    lst = [str(lst[i]).split('</span>') for i in range(len(lst))]

    for i in lst:
        if i[0].isdigit():
            array.append(i[0])

    for i in range(1, 7):
        arr.append(array[-i])
    for i in range(1, 7):
        arr1.append(arr[-i])

    dollar = [arr1[0], arr1[1]]
    euro = [arr1[2], arr1[3]]
    return[dollar, euro]


def TrainCheck(link):

    f = urllib.request.urlopen(link)
    myfile = f.read()
    lst = str(myfile)
    lst = lst.split('<span class="_time">')
    arr = []
    arr1 = []
    array = []
    timeof = []

    for i in range(len(lst)):
        lst[i] = str(lst[i])
        lst[i] = lst[i].split('</span>')

    for i in lst:
        if i[0].isdigit:
            array.append(i[0])

    respond = 'The full train schedule:'
    respond += '\n'

    for i in range(1, len(array)):

        if i % 2 == 0:

            respond += str(int(i/2))
            respond += '. '
            if((i/2) < 10):
                respond += ' '
            respond += array[i-1]
            respond += '---------------'
            respond += array[i]
            respond += '\n'

    return(respond)


def NearestTrain(link):
    shedule = train_parser(KARDACHI_TARASOVKA_LINK)

    now = time.asctime(time.localtime()).split(' ')[3].split(':')

    now_mins = int(now[0])*60+int(now[1])
    times = {}

    for i, j in shedule.items():
        route_hours = int(float(i))
        route_minutes = float(i) - route_hours
        route_time = route_hours*60 + route_minutes
        times[str(i)] = route_time

    ans = [i for i, j in times.items() if j > now_mins]
    l = len(ans)
    ans = ans[:3] if l >= 3 else ans[:2] if l == 2 else ans

    r1 = 'route'
    r2 = r1+'s'
    resp = f"  {len(ans)} {r2 if len(ans)>1 else r1} available\n"

    for i in ans:
        resp += i + "-"*12 + shedule[i] + '\n'
    return resp


print(CurrencyCheck(CURRENCY_LINK))

bot_token = "745661558:AAEMcMTj7ewXtVtnZ-qYuYMhSqyLom5NC7E"

bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')


@bot.message_handler(commands=['train_shedule_tar'])
def send_welcome(message):
    bot.reply_to(message, TrainCheck(TARASOVKA_KARDACHI_LINK))


@bot.message_handler(commands=['train_shedule_kar'])
def send_welcome(message):
    bot.reply_to(message, TrainCheck(KARDACHI_TARASOVKA_LINK))


@bot.message_handler(commands=['nearest_tarasivka'])
def send_welcome(message):
    bot.reply_to(message, NearestTrain(TARASOVKA_KARDACHI_LINK))


@bot.message_handler(commands=['nearest_kardachi'])
def send_welcome(message):
    bot.reply_to(message, NearestTrain(KARDACHI_TARASOVKA_LINK))


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'To use this bot, send it a username')


@bot.message_handler(commands=['currency'])
def send_currency(message):
    std = '| -- -- -- Dollar -- -- -|- -- -- -- Euro -- -- --| \n \
        |-To Buy- -To Sell-|- -To Buy- -To Sell| \n'
    currency = CurrencyCheck(currency_link)
    #| -- --  Dollar -- --  | -- -- -- Euro -- -- --|
    #| -To Buy-|-To Sell- - | -  To Buy -|- To Sell |
    #|  27.7500  |  28.1000 | 31.4000  |   32.0000  |

    message1 = '{0}|{1}|{2}|{3}|{4}|'.format(
        str(currency[0][0]),
        str(currency[0][1]),
        str(currency[1][0]),
        str(currency[1][1])
    )
    bot.reply_to(message, message1)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
