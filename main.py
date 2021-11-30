import telebot
import config
import os
import datetime
from telebot import types


#Наш ТОКЕН

bot = telebot.TeleBot(config.TOKEN)

#Действия на команду старт

@bot.message_handler(commands = ['start'])

def welcome(message):

	#Проверяем естьли клиент в базе. Если нету - создаем папку.

	name='{0.first_name}'.format(message.from_user,bot.get_me()) 
	namelist= 'coachlist/' + name
	print (namelist)
	
	if os.path.exists(namelist):
		print ('Клиент есть в базе данных')
	else:
		os.mkdir('coachlist/{0.first_name}'.format(message.from_user, bot.get_me()))
		os.mkdir('coachlist/{0.first_name}/otchet'.format(message.from_user, bot.get_me()))


	#Открываем наш стикер

	sticker = open('static/welcome.png', 'rb')


	#Создаем клавиатуру Главного меню

	markup_main=types.ReplyKeyboardMarkup(resize_keyboard = True)
	item_programm = types.KeyboardButton(text ='Моя программа')
	item_yes = types.KeyboardButton(text ='Отправить отчет')
	item_no = types.KeyboardButton(text ='Инфо')
	markup_main.add(item_programm,item_yes,item_no)

	#Ответ бота на стартовую команду
	bot.send_sticker(message.chat.id, sticker)
	bot.send_message(message.chat.id, 'Привет! Я, {0.first_name}, создан, что бы принимать твои отчеты о соблюдаемой диете.💪\nТак что не тяни, а отсылай свой отчет прямо сейчас!💥'.format(message.from_user, bot.get_me()), parse_mode = 'html',reply_markup = markup_main)




#Действие на наши сообщения

@bot.message_handler(content_types = ['text'])

def get_text(message):
	if message.text == 'Отправить отчет':
		
		markup_second=types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_no = types.KeyboardButton(text ='Назад')
		markup_second.add(item_no)

		bot.send_message(message.chat.id, 'Что бы отправить своему тренеру скриншот с отчетом - просто нажми на скрепку в правом нижнем углу экрана и прикрепи фото 😉')
		bot.send_message(message.chat.id, 'Справился?',reply_markup = markup_second)


	elif message.text == 'Инфо':
		markup_third=types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_no = types.KeyboardButton(text ='Назад')
		markup_third.add(item_no)

		bot.send_message(message.chat.id, 'Тренер FitHaus 🟨 & Adrenaline 🟥\nТренерский стаж - 2 года 📘\nInstagramm: @Just1uck 🖌\nViber: +380954671375 📞',reply_markup = markup_third)


	elif message.text == 'Назад':
		markup_four=types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_yes = types.KeyboardButton(text ='Отправить отчет')
		item_no = types.KeyboardButton(text ='Инфо')
		item_programm = types.KeyboardButton(text ='Моя программа')
		markup_four.add(item_programm,item_yes,item_no)

		bot.send_message(message.chat.id, 'Вы вернулись в главное меню ',reply_markup = markup_four)

	elif message.text == 'Моя программа':

		#Клавиатура

		markup_third=types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_no = types.KeyboardButton(text ='Назад')
		markup_third.add(item_no)

		#Inline Кнопки

		markup_inline_one =types.InlineKeyboardMarkup()
		item_day1 = types.InlineKeyboardButton('Day1',callback_data='Day1')
		item_day2 = types.InlineKeyboardButton('Day2',callback_data='Day2')
		item_day3 = types.InlineKeyboardButton('Day3',callback_data='Day3')

		markup_inline_one.add(item_day2,item_day3)
		

		# Сбрасываем программу тренировок
		
		programm_name='{0.first_name}'.format(message.from_user,bot.get_me()) 
		programm_path = 'coachlist/'+programm_name+'/programm/programm.jpg'
		if os.path.exists(programm_path):
			programm = open(programm_path, 'rb')
			bot.send_photo(message.chat.id, programm,reply_markup = markup_inline_one)
			bot.send_message(message.chat.id, 'Вот ваша программа тренировок',reply_markup = markup_third)
			
		else:
			bot.send_message(message.chat.id, 'К сожалению у вас нету программы тренировок.',reply_markup = markup_third)

#Сохраняем отчеты

@bot.message_handler(content_types=['photo'])
def get_photo(message):
	bot.send_message(message.chat.id, 'Хорошо, я сохранил это фото и отправил твоему тренеру.\nВскоре он рассмотрит его и ответит тебе лично!')
	file_photo = bot.get_file(message.photo[-1].file_id)
	#print(file_photo)

	filename, file_extension = os.path.splitext(file_photo.file_path)
	#print (file_extension)
	date = datetime.datetime.now().strftime('%m-%d_%H-%M')

	a= '{0.first_name}'.format(message.from_user, bot.get_me())
	b= a + date

	downloaded_file_photo = bot.download_file(file_photo.file_path)
	srcc = 'coachlist/' + a +'/otchet/'
	src = srcc + b + file_extension
	print (src)
	with open (src,'wb') as new_file:
		new_file.write(downloaded_file_photo)





@bot.callback_query_handler(func=lambda call: True)


def callback_inline(call):
	if call.message:
		name='{0.first_name}'.format(call.message.from_user,bot.get_me()) 
		name11='coachlist/'+name+'/programm/programm.jpg'
		name22='coachlist/'+name+'/programm/programm2.jpg'		
		name33='coachlist/'+name+'/programm/programm3.jpg'


		if call.data == 'Day1':
			programm1 = open (name11,'rb')
		
			markup_inline_one =types.InlineKeyboardMarkup()
			item_day1 = types.InlineKeyboardButton('Day1',callback_data='Day1')
			item_day2 = types.InlineKeyboardButton('Day2',callback_data='Day2')
			item_day3 = types.InlineKeyboardButton('Day3',callback_data='Day3')

			markup_inline_one.add(item_day2,item_day3)

			bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id, media=telebot.types.InputMediaPhoto(programm1),reply_markup=markup_inline_one)



		elif call.data == 'Day2':
			programm2 = open (name22,'rb')
		
			markup_inline_one =types.InlineKeyboardMarkup()
			item_day1 = types.InlineKeyboardButton('Day1',callback_data='Day1')
			item_day2 = types.InlineKeyboardButton('Day2',callback_data='Day2')
			item_day3 = types.InlineKeyboardButton('Day3',callback_data='Day3')

			markup_inline_one.add(item_day1,item_day3)

			bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id, media=telebot.types.InputMediaPhoto(programm2),reply_markup=markup_inline_one)


		elif call.data == 'Day3':
			programm3 = open (name33,'rb')
		
			markup_inline_one =types.InlineKeyboardMarkup()
			item_day1 = types.InlineKeyboardButton('Day1',callback_data='Day1')
			item_day2 = types.InlineKeyboardButton('Day2',callback_data='Day2')
			item_day3 = types.InlineKeyboardButton('Day3',callback_data='Day3')

			markup_inline_one.add(item_day1,item_day2)

			bot.edit_message_media(chat_id=call.message.chat.id,message_id=call.message.message_id, media=telebot.types.InputMediaPhoto(programm3),reply_markup=markup_inline_one)



		#if call.data == "next":
		#		programm2 = open(programm_path2, 'rb')
		#	bot.edit_message_photo(chat_id=call.message.chat.id, message_id=call.message.message_id, programm2)
		#elif call.data == "back":
		#	bot.send_message(call.message.chat.id,'Привет')













#Поддержка работы бота
bot.polling(non_stop=True)
