import telebot
import time
import requests
import urllib

from parser import (
    _train_parser,
    nearest_parser,
    currency_parser
)
from constants import (
    CURRENCY_LINK,
    TARASOVKA_KARDACHI_LINK,
    KARDACHI_TARASOVKA_LINK
)
#My links Bank:

def CurrencyCheck(link):
    return [float(val) for val in currency_parser(link)]


def TrainCheck(link):
    shedule = _train_parser(link)
    ans = "Current train shedule\n"
    for i,j in shedule.items():
        ans += f'|{i}-----{j}|\n'
    return ans


def NearestTrain(link):
    return nearest_parser(link)


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
    currency = CurrencyCheck(CURRENCY_LINK)
    std =      '| -- -- -- Dollar -- -- --|-- -- -- -- Euro -- -- -|\n'
    std +=     '|  -To Buy- | -To Sell- | -To Buy-| -To Sell- | \n'

    message1 = '|   %.2f   |   %.2f   |   %.2f   |   %.2f   |'%(
        currency[0],
        currency[1],
        currency[2],
        currency[3]
    )
    message1 = std + message1
    bot.reply_to(message, message1)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)
