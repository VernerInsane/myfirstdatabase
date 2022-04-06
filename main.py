import os
import logging                  #импорт библиотек
import psycopg2
import telebot
from config import *
from flask import Flask, request
from telebot import util
from telebot import types

bot = telebot.TeleBot(TOKEN)  #создание бота
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)  #создане debug menu для отслеживания ошибок в работе

db_connection = psycopg2.connect(DB_URI, sslmode="require")  
db_object = db_connection.cursor()       #подключение к БД
def update_messages_count(user_id):
    db_object.execute(f"UPDATE users SET messages = messages + 1 WHERE id = {user_id}")
    #счётчик количества сообщений
    db_connection.commit()

@bot.message_handler(commands = ['start'])  #обработка команды start
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    sti = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True,row_width=4)
    item1 = types.KeyboardButton("Расскажи о Саянске")
    item2 = types.KeyboardButton("Расскажи о себе")
    item3 = types.KeyboardButton("Расскажи о достопремичательностях")
  

    markup.row(item1,item2)
    markup.row(item3)

    bot.send_message(message.chat.id, "Привет! Чем могу быть полезен?", reply_markup=markup, parse_mode=
    'html')

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")  #обращение к таблице в БД
    result = db_object.fetchone() 

    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s,%s,%s)" ,(user_id,username,0))
        db_connection.commit()

    update_messages_count(user_id)

@bot.message_handler(commands = ['stats'])  #обработка команды stats
def get_stats(message):
    db_object.execute("SELECT * FROM users ORDER BY messages DESC LIMIT 10")
    result = db_object.fetchall()

    if not result:
        bot.reply_to(message, "Данных нет...")
    else:
        reply_message = "- Top flooders:\n"
        for i, item in enumerate(result):
            reply_message += f'[{i +1}] {item[1].strip()} ({item[0]}) : {item[2]} сообщений.\n'
        bot.reply_to(message, reply_message)
    update_messages_count(message.from_user.id)
    
@bot.message_handler(func=lambda message: True,content_types=['text']) #создание неповторяемости счетчика
def message_from_user(message):
    user_id = message.from_user.id
    update_messages_count(user_id)

@bot.message_handler(commands=['help'])
def send_help(message):
  bot.reply_to(message,"Команда предусмотрена для дальнейшей разработки бота. Пожалуйста следуйте командам на месте клавиатуры😁")

@bot.message_handler(content_types=['text'])
def answer_toquest(message):
  if message.chat.type == 'private':
    if message.text == "Расскажи о Саянске":
      About_town=open("About_town.txt", 'rb').read()
      split_text = util.split_string(About_town,3000)

      for town in split_text:
        bot.send_message(message.chat.id, town)
      bot.send_message(message.chat.id,'https://www.admsayansk.ru/pub/img/News/6694/IMG_8420.jpg')

    elif message.text == 'Расскажи о себе':
      About_bot=open("About_helper.txt",'rb').read()
      split_helper = util.split_string(About_bot,3000)

      for helper in split_helper:
        bot.send_message(message.chat.id,helper)
    elif message.text == 'Расскажи о достопремичательностях':
      markup = types.ReplyKeyboardRemove()
      markup1 = types.ForceReply()
      attray= open('Attractions.txt','rb').read()
      split_attray=util.split_string(attray,1000)

      for att in split_attray:
        bot.send_message(message.chat.id,att)
    elif message.text == '/1':
      pro1=open("1pro.txt", 'rb').read()
      split_pro1 = util.split_string(pro1,3000)

      for pro1text in split_pro1:
        bot.send_message(message.chat.id, pro1text)
      bot.send_location(message.chat.id,54.10084688307593, 102.15750567338948)
      
      bot.send_photo(message.chat.id, 'https://sun9-6.userapi.com/impg/VErKSTcRGUytcOakDzigJ8hRDkqz4-qe08t84w/JQIzwcYtq7s.jpg?size=817x1080&quality=96&sign=157557d09f3f92e714e7bbcef6d127cf&type=album')
    elif message.text == '/2':
      pro2=open("2pro.txt", 'rb').read()
      split_pro2 = util.split_string(pro2,3000)

      for pro2text in split_pro2:
        bot.send_message(message.chat.id, pro2text)
      bot.send_location(message.chat.id,54.10665810630316, 102.16958808838609)
      
      bot.send_photo(message.chat.id, 'https://sun9-3.userapi.com/impg/hav7yYG3tH47mLmL4AsXTCXePTkaQYoo7bAivg/-TVR9WR34Ck.jpg?size=581x773&quality=96&sign=66b8a20dd3a932850684082fef098a43&type=album')
    elif message.text == '/3':
      pro3=open("3pro.txt", 'rb').read()
      split_pro3 = util.split_string(pro3,3000)

      for pro3text in split_pro3:
        bot.send_message(message.chat.id, pro3text)
      bot.send_location(message.chat.id,54.108597229677976, 102.16367186784939)
      
      bot.send_photo(message.chat.id, 'https://sun9-73.userapi.com/impg/eVh9W66pDWd1tmSvNaLAdf7jnC-ZEEcRoxzzxA/RRNNpa0WUl0.jpg?size=606x807&quality=96&sign=63d93c15b66b78f843b62b96e370c548&type=album')
    elif message.text == '/4':
      pro4=open("4pro.txt", 'rb').read()
      split_pro4 = util.split_string(pro4,3000)

      for pro4text in split_pro4:
        bot.send_message(message.chat.id, pro4text)
      bot.send_location(message.chat.id,54.1080434, 102.1780225)
      
      bot.send_photo(message.chat.id, 'https://sun9-69.userapi.com/impg/lPHH2zE0bj1wOqwMhkYOdUvVCCzyWJg1eQtmtA/vD6Vh0M75e4.jpg?size=671x1006&quality=96&sign=d3d59e7f513277c182c35fb056b62efd&type=album')
    elif message.text == '/5':
      pro5=open("5pro.txt", 'rb').read()
      split_pro5 = util.split_string(pro5,3000)

      for pro5text in split_pro5:
        bot.send_message(message.chat.id, pro5text)
      bot.send_location(message.chat.id,54.10187919110795, 102.15591491948202)
      
      bot.send_photo(message.chat.id, 'https://sun9-15.userapi.com/impg/7rUJY7p7Kz-VjNaZXBuasbt7ghf0puZ3H4iJRQ/xKm13L-yaW4.jpg?size=509x762&quality=96&sign=d81129643b559f5ded0bf51d4775f325&type=album')
    elif message.text == '/6':
      pro6=open("6pro.txt", 'rb').read()
      split_pro6 = util.split_string(pro6,3000)

      for pro6text in split_pro6:
        bot.send_message(message.chat.id, pro6text)
      bot.send_location(message.chat.id,54.108597229677976, 102.16367186784939)
      
      bot.send_photo(message.chat.id, 'https://sun9-53.userapi.com/impg/Ag7bH-NMIrwwToCWK30CYLUL_PNtt4k-LLwPIA/HJC32tQD37I.jpg?size=978x653&quality=96&sign=6f9a0137c2ee0ddb2b5ac419f028fab2&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-46.userapi.com/impg/qq81XzkfBXr3yTfag18HMYlsHeIf2mI-Et8gCw/_GODvZnQBL8.jpg?size=978x653&quality=96&sign=91803c0bddd9d55836976321e5350394&type=album')
    elif message.text == '/7':
      pro7=open("7pro.txt", 'rb').read()
      split_pro7 = util.split_string(pro7,3000)

      for pro7text in split_pro7:
        bot.send_message(message.chat.id, pro7text)
      bot.send_location(message.chat.id,54.08197316377667, 102.12768741292248)
      bot.send_photo(message.chat.id, 'https://sun9-86.userapi.com/impg/9fPXKkftAkOrzFaYtA_osUSnqKzMrqzT6L8LBw/J5-3CRGjwpU.jpg?size=851x628&quality=96&sign=4255d5cdf37c4716aa0dbdc60bf4211a&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-38.userapi.com/impg/K75nVFlzh5V2FQ0Rvlyou15MHDPITYI7pREogQ/ElSeiME6pac.jpg?size=298x223&quality=96&sign=0af1be9ab5f1de09b3a555dce721f0a0&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-37.userapi.com/impg/qZk_7UxEWSesrHPQ76IvE26ID4DWzrMRISWhmg/H3fPvGSGXoQ.jpg?size=807x571&quality=96&sign=2ae7d4d6ca243794f2064dc3b46d641c&type=album')
    elif message.text == '/8':
      pro8=open("8pro.txt", 'rb').read()
      split_pro8 = util.split_string(pro8,3000)

      for pro8text in split_pro8:
        bot.send_message(message.chat.id, pro8text)
      bot.send_location(message.chat.id,54.11030689375414, 102.15960924415099)
      
      bot.send_photo(message.chat.id, 'https://sun9-48.userapi.com/impg/Tx8AlwHd1eT-V8S_-ARuSSVdS2Iasl27IxAVoA/jI-gnmbnBlc.jpg?size=621x415&quality=96&sign=5cbcaa77d3047e150af766cd0340df19&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-32.userapi.com/impg/H32zabbixvhniDVSL-vRYYkk0BOr8vYaCKVl8A/bOl_Bqce4vw.jpg?size=807x607&quality=96&sign=276aeefc133bb6181f938ce4d4077cab&type=album')
    elif message.text == '/9':
      pro9=open("9pro.txt", 'rb').read()
      split_pro9 = util.split_string(pro9,3000)

      for pro9text in split_pro9:
        bot.send_message(message.chat.id, pro9text)
      bot.send_location(message.chat.id,54.11445982567459, 102.16161997231224)

      bot.send_photo(message.chat.id, 'https://sun9-36.userapi.com/impg/g-rrqHsSRLomFNN8qn9xVq2FXdSi0zpfgh2w2A/2YmEuwQqVvI.jpg?size=688x460&quality=96&sign=0a08b9f68ab1cf8718e8c8f05a77e812&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-63.userapi.com/impg/zA6gXZcuW9IQuviHpE7do0szxXp6Yg4h_XfAVg/0-r7G9a52Nk.jpg?size=668x447&quality=96&sign=1af264265e609d2fcd97d849448797b4&type=album')
    elif message.text == '/10':
      pro10=open("10pro.txt", 'rb').read()
      split_pro10 = util.split_string(pro10,3000)

      for pro10text in split_pro10:
        bot.send_message(message.chat.id, pro10text)
      bot.send_location(message.chat.id,54.11265998226437, 102.18326682103789)
      
      bot.send_photo(message.chat.id, 'https://sun9-19.userapi.com/impg/cqKUguddqRqPshCKrUY0XILiYlUfugDhgdRS8w/V0vEed4pa-Y.jpg?size=807x455&quality=96&sign=6d447792aa1d1f77c4938974c618bc84&type=album')
    elif message.text == '/11':
      pro11=open("11pro.txt", 'rb').read()
      split_pro11 = util.split_string(pro11,3000)

      for pro11text in split_pro11:
        bot.send_message(message.chat.id, pro11text)
      bot.send_location(message.chat.id,54.11419602426144, 102.17425167532633)
      
      bot.send_photo(message.chat.id, 'https://sun9-9.userapi.com/impg/DQEPTtIjpXVzpuN22ET1mDXsiwiz-VCQmP1_sQ/csOeu53Kh-0.jpg?size=807x622&quality=96&sign=8a7ff33235d55e1b417e3efacb34fe97&type=album')
    elif message.text == '/12':
      pro12=open("12pro.txt", 'rb').read()
      split_pro12 = util.split_string(pro12,3000)

      for pro12text in split_pro12:
        bot.send_message(message.chat.id, pro12text)
      bot.send_location(message.chat.id,54.10188318371019, 102.15584795894044)
      
      bot.send_photo(message.chat.id, 'https://sun9-28.userapi.com/impg/QbuP2XowHnoO5qIcohHcmKSrQrRFAeh4Jr3rYw/kQt2A8SC4oE.jpg?size=585x388&quality=96&sign=60db672826c8c6ade8d503b07eae0970&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-63.userapi.com/impg/f7UGsBhuc1mSAgJBu7Hr-Dy_smP4kBVgANzdUQ/h8jtWjVLiic.jpg?size=570x381&quality=96&sign=64f33d3a35b718d27c15dd80681f3975&type=album')
    elif message.text == '/13':
      pro13=open("13pro.txt", 'rb').read()
      split_pro13 = util.split_string(pro13,3000)

      for pro13text in split_pro13:
        bot.send_message(message.chat.id, pro13text)
      bot.send_location(message.chat.id,54.10631991921747, 102.1806858425237)
      
      bot.send_photo(message.chat.id, 'https://sun9-34.userapi.com/impg/PQlmnDiOHFQ11NmEVD-4N1l_Ox68wZkZwZb7cA/KprQGYrm0Jk.jpg?size=699x525&quality=96&sign=f9b00cf84b593dda536fc850bbdae882&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-76.userapi.com/impg/q7BY-HBwj3A4DKscs0Ergajog1IiLW_1xTBAmQ/z90bLdiHbm0.jpg?size=807x540&quality=96&sign=8019aa3da0b0aa31ab41d1a425be6586&type=album')
    elif message.text == '/14':
      pro14=open("14pro.txt", 'rb').read()
      split_pro14 = util.split_string(pro14,3000)

      for pro14text in split_pro14:
        bot.send_message(message.chat.id, pro14text)
      bot.send_location(message.chat.id,54.11035324714662, 102.15959753043795)
      
      bot.send_photo(message.chat.id, 'https://sun9-48.userapi.com/impg/kQduMdtTxvsT3RKJXRA_77K8_4KaylcJXAPkBA/1PEWwjjBCnk.jpg?size=807x538&quality=96&sign=f3a45468d285cbc77ed1e7c5056ae04d&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-61.userapi.com/impg/Qnx_x37yCn9RkN0qP_JUn27oneVE3xKyCOa1AA/bUlYDRlIv8U.jpg?size=807x539&quality=96&sign=ceaf6fa53d3a842ea04ec9fd525deeca&type=album')
    elif message.text == '/15':
      pro15=open("15pro.txt", 'rb').read()
      split_pro15 = util.split_string(pro15,3000)

      for pro15text in split_pro15:
        bot.send_message(message.chat.id, pro15text)
      bot.send_location(message.chat.id,54.10630491457263, 102.15690756282292)
      
      bot.send_photo(message.chat.id, 'https://sun9-68.userapi.com/impg/3FcgtE0gcDgnfd1Geq641riChS3vzo8bb5TA6w/sQMDmOEzGB0.jpg?size=807x539&quality=96&sign=e66321631216766fc290e21c6f2565ad&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-50.userapi.com/impg/lmtl1f8LDh85SGeIsMSrgqsoy65c_Gl6ey5rYA/LUR_JhlYGB4.jpg?size=807x536&quality=96&sign=d5692afbb37d96ffd30c151fff14e67f&type=album')
    elif message.text == '/16':
      pro16=open("16pro.txt", 'rb').read()
      split_pro16 = util.split_string(pro16,3000)

      for pro16text in split_pro16:
        bot.send_message(message.chat.id, pro16text)
      bot.send_location(message.chat.id,54.11197156315281, 102.16832771027555)
      
      bot.send_photo(message.chat.id, 'https://sun9-21.userapi.com/impg/83SLCCfDK7a-qdKA4ZF00h8DTTj1cXeOtLRyUA/Ms2PBeSlowA.jpg?size=807x538&quality=96&sign=48df664b81082b42227a04518a0456cb&type=album')
      bot.send_photo(message.chat.id, 'https://sun9-38.userapi.com/impg/Q1Z9uCEuNJXj4QXxBG5b11TfOQTQNpvKjt5DyQ/SZx6OKuyUb0.jpg?size=807x540&quality=96&sign=704382d5132dab01bb856cc9370773a3&type=album')
    
    else:
      bot.send_message(message.chat.id,"Прошу прощения {0.first_name}, не знаю что ответить.".format(message.from_user))


@server.route(f'/{TOKEN}', methods = ['POST'])      #работа с сервером
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == '__main__':      #подключение к Heroku
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host = '0.0.0.0', port=int(os.environ.get('PORT',5000)))

