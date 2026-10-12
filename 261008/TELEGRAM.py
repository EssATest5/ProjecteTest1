import telebot
import random
import time

TOKEN = '6369783957:AAHPPLtQzNzKySXbeECdJCTSQf0SUT69Vqg'
CHAT ID = '8889270294'

bot = telebot. TeleBot (TOKEN)

@bot. message_handler (commands=[' start' ])
def start (message) :
temperatura = random. randint (15, 35)
humitat = random. randint (30, 90)

bot.send message(CHAT_ID, f'T={temperatura} C H={humitat} %')
time.sleep(1)

bot.infinity_polling()