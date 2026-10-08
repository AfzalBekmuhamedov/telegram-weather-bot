import os
from dotenv import load_dotenv
from datetime import datetime
from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery
import requests

load_dotenv()

TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY")

params = {
    'units':'metric',
    'appid':API_KEY
}

bot = TeleBot(TOKEN)

user_lang = {}

texts = {
    "uz":{
        "welcome":"Salom,\nTilni tanlang / Dil seçin / Select language",
        "enter_city_name":"Shahar nomini kiriting !",
        "wrong_city":"Shahar nomi noto'g'ri",
        "weather_btn":"Ob-havoni ko'rish 🌦",
        "city": "Shahar",
        "country": "Davlat",
        "condition": "Holat",
        "temp": "Harorat",
        "wind": "Shamol",
        "sunrise": "Quyosh chiqishi",
        "sunset": "Quyosh botishi"
    },
    "en":{
        "welcome":"Welcome,\nSelect language",
        "enter_city_name":"Enter the city name!",
        "wrong_city":"City name is wrong !",
        "weather_btn":"See weather info 🌦",
        "city": "City",
        "country": "Country",
        "condition": "Condition",
        "temp": "Temperature",
        "wind": "Wind",
        "sunrise": "Sunrise",
        "sunset": "Sunset"
    },
    "tr": {
        "welcome": "Merhaba,\nDil seçin",
        "enter_city_name": "Şehrin adını yazın!",
        "wrong_city": "Yanlış şehir adı!",
        "weather_btn": "Hava durumu bilgilerini al 🌦",
        "city": "Şehir",
        "country": "Ülke",
        "condition": "Durum",
        "temp": "Sıcaklık",
        "wind": "Rüzgar",
        "sunrise": "Gün doğumu",
        "sunset":"Gün batımı"
    }
}

def lang_button():
    inline = InlineKeyboardMarkup()
    uz = InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="uz")
    tr = InlineKeyboardButton("🇹🇷 Türkçe", callback_data="tr")
    en= InlineKeyboardButton("🇬🇧 English", callback_data="en")
    inline.add(uz,tr,en)
    return inline

@bot.message_handler(commands=['start'])
def commands(message:Message):
    chat_id = message.chat.id
    if message.text == "/start":
        bot.send_message(chat_id, texts["uz"]["welcome"],reply_markup=lang_button())


@bot.callback_query_handler(func=lambda call:True)
def set_language(call:CallbackQuery):
    chat_id = call.message.chat.id
    lang = call.data
    user_lang[chat_id] = lang
    bot.delete_message(chat_id,call.message.id)
    bot.send_message( chat_id,texts[lang]["enter_city_name"])

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id, "uz")

    if message.text == texts[lang]["weather_btn"]:
         msg = bot.send_message(chat_id, texts[lang]["enter_city_name"], reply_markup=ReplyKeyboardRemove())
         bot.register_next_step_handler(msg, weather_info)
    else:
         weather_info(message)

def weather_info(message: Message):
    chat_id = message.chat.id
    lang = user_lang.get(chat_id, "uz")
    city = message.text

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                **params,
                "q": city,
                "lang": lang
            }
        )
        data = response.json()
        if data.get("cod") != 200:
            raise Exception("City not found")

        name = data['name']
        country = data['sys']['country']
        condition = data['weather'][0]['description']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        timezone = data["timezone"]
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + timezone).strftime("%H:%M")
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + timezone).strftime("%H:%M")


        bot.send_message(
            chat_id,
            f"{texts[lang]['city']}: {name}\n"
            f"{texts[lang]['country']}: {country}\n"
            f"{texts[lang]['condition']}: {condition}\n"
            f"{texts[lang]['temp']}: {temp}°C\n"
            f"{texts[lang]['wind']}: {wind} m/s\n"
            f"{texts[lang]['sunrise']}: {sunrise}\n"
            f"{texts[lang]['sunset']}: {sunset}"

        )

    except:
        bot.send_message(chat_id, texts[lang]["wrong_city"])


# if __name__ == "__main__":
#     print("Bot ishga tushdi")
#     bot.infinity_polling()

