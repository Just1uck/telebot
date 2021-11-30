import os
import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

		#Начало работы с ботом

@bot.message_handler(commands = ['start'])
def welcome(message):

	sticker = open('static/welcome.png', 'rb')
	bot.send_sticker(message.chat.id, sticker)

	markup_welcome = types.ReplyKeyboardMarkup(resize_keyboard = True)
	item_yes = types.KeyboardButton(text ='Отправить отчет')
	item_no = types.KeyboardButton(text ='Инфо')

	markup_welcome.add(item_yes,item_no)
	bot.send_message(message.chat.id, 'Привет! Я, {0.first_name}, создан, что бы принимать твои отчеты о соблюдаемой диете.\nТак что не тяни, а отсылай свой отчет прямо сейчас!'.format(message.from_user, bot.get_me()), parse_mode = 'html',reply_markup = markup_welcome)

		#Ответ на сообщения

@bot.message_handler(content_types = ['text'])
def get_text(message):
	if message.text == 'Отправить отчет':
		bot.send_message(message.chat.id, 'Отлично, жду от тебя скриншот:')
	elif message.text == 'Инфо':
		bot.send_message(message.chat.id, 'Скоро тут будет подробная информация.')
	else:
		bot.send_message(message.chat.id, 'Не знаю я такой команды')


		#Получаем фото от человека и сохраняем его

@bot.message_handler(content_types=['photo'])
def get_photo(message):
	bot.send_message(message.chat.id, 'Хорошо, я сохранил это фото и отправил твоему тренеру.\nВскоре он рассмотрит его и ответит тебе лично!')
	file_photo = bot.get_file(message.photo[-1].file_id)
	#print(file_photo)

	filename, file_extension = os.path.splitext(file_photo.file_path)
	#print (file_extension)

	a= '{0.first_name}'.format(message.from_user, bot.get_me())

	downloaded_file_photo = bot.download_file(file_photo.file_path)
	src = 'photos/' + a + file_extension
	with open (src,'wb') as new_file:
		new_file.write(downloaded_file_photo)







bot.polling(non_stop=True)
