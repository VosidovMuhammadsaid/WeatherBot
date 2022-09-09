from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
import telebot


config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('57a510163dc11f413822bf0538d632b6',config_dict)
mgr = owm.weather_manager()

bot = telebot.TeleBot("2019591321:AAEKiWhzkPFqhJc6q9kPJHQw8Nkk64BXd44", parse_mode=None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}!\nЯ - Погода бот, бот созданный для показа погоды.")
	bot.send_message(message.chat.id,f"{message.from_user.first_name}, напиши название своего города, либо населённого пункта:")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	observation = mgr.weather_at_place(message.text)
	w = observation.weather
	temp="Температура воздуха",w.temperature('celsius')['temp'],"°C"
	bot.send_message(message.chat.id,("В "+observation.location.name+" сейчас " + w.detailed_status+"\nОблочность составляет "+str(w.clouds)+"%\nВлажность составляет "+str(w.humidity)+"%\nCкорость ветра "+str(w.wind()['speed'])+" м/с\nТемпература воздуха "+str(w.temperature('celsius')['temp'])+"°C"))

	if w.temperature('celsius')['temp']>25:
		bot.send_message(message.chat.id,"На улице жара одевай всё что хочешь :)🔥")
	if w.temperature('celsius')['temp']>15 and w.temperature('celsius')['temp']<25:
		bot.send_message(message.chat.id,"Температура довольно таки тёплая. ☀️")
	if w.temperature('celsius')['temp']<15:
		bot.send_message(message.chat.id,"Сегодня прохладно надень куртку.🌁")

bot.infinity_polling()