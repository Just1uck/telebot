import telebot
import config
import random
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler (commands=['start'])
def welcomme (message):
	sticker = open('static/welcome.png', 'rb')
	bot.send_sticker(message.chat.id, sticker)

	#Клавиатура
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = telebot.types.ReplyKeyboardButton(" Рандомное число")
	item2 = telebot.types.ReplyKeyboardButton(" Как дела? ")
	markup.add(item1,item2)


	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()), parse_mode = 'html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala (message):
	if message.chat.type == 'private':
		if message.text == ' Рандомное число':
			bot.send_message(message.chat.id, str(rando.randit(0,100)))
		elif message.text == ' Как дела?':
			bot.send_message(message.chat.id, 'Отлично, сам как?')
		else:
			bot.send_message(message.chat.id, 'Не знаю что ответить?')





#RUN
bot.polling(non_stop=True)


