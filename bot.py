import telebot
import time
import datetime
import schedule
from threading import Thread

# heroku ps:scale worker=1 - Запуск бота на хероку

bot = telebot.TeleBot('TOKEN', threaded=True, num_threads=2)

# Переменные для отправки расписания
time_now = time.strftime('%H:%M')  # Получение времени на данный момент
# datetime.datetime.now().weekday()  # Номер дня недели по счёту
send_schedule_morning_at = '04:00'  # Время для отправки расписания утром
send_schedule_evening_at = '16:30'  # Время для отправки расписания вечером
current_week = 2  # Числитель/знаменатель
# Словарь дней и рассписания (цифры - день недели по счёту) (Для меня)
days = {
    0:
        {
            'Числитель': 'На этой неделе ЧИСЛИТЕЛЬ! \
Сегодня понедельник, вообще нужно работать, но отдыхай. Хорошего дня тебе)',
            'Знаменатель': 'На этой неделе ЗНАМЕНАТЕЛЬ! \
Сегодня понедельник, вообще нужно работать, но отдыхай. Хорошего дня тебе)'
        },
    1: {'Числитель':
        '''11:25 - Компьютерные сети, ауд. 36 (1)
12:55 - Мат. анализ
14:30 - Англ. язык''',
        "Знаменатель":
        '''12:55 - Групповая динамика и коммуникации
14:30 - Англ. язык'''},
    2: {'Числитель': '''8:00 - Мат. анализ (практика)
9:35 - Мат. анализ (лекция)
11:25 - Дискретные структуры (лекция)''',
        'Знаменатель': '''8:00 - Мат. анализ (практика)
9:35 - Мат. анализ (лекция)
11:25 - Дискретные структуры (лекция)
12:55 - Дискретные структуры (лабараторки)'''},
    3: {'Числитель': """8:00 - Дискретные структуры (лабараторки)
9:35 - Архитектура компьютера (лабы)
11:25 - Комп. сети (лабы)
12:55 - Физ-ра""",
        'Знаменатель': """8:00 - Дискретные структуры (лабараторки)
9:35 - Архитектура компьютера (лабы)
11:25 - Комп. сети (лабы)
12:55 - Физ-ра"""},
    4: {"Числитель": """9:35 - Мат. анализ (практика)
11:25 - Англ. язык""",
        "Знаменатель": """9:35 - Групповая динамика и коммуникации (практика)
11:25 - Англ. язык
12:55 - Архитектура компьютера (лабы)"""},
    5: {"Числитель": """8:00 - Арихитектуры компьютера (лекция)
9:35 - Физ-ра""",
        "Знаменатель": """8:00 - Арихитектуры компьютера (лекция)
9:35 - Физ-ра"""},
    6: {"Числитель: ": "Эх... Воскресенье... Короче, сегодня ты отдыхаешь)))",
        "Знаменатель": "Эх... Воскресенье... Короче, сегодня ты отдыхаешь)))"}
}


# Принимает комманду /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ах ты ленивая жопа... Ладно, буду присылать тебе расписание каждый день...')
    print(f'Чат: {message.chat.title}, ID: {message.chat.id}\nОт кого: {message.from_user.username}\nТекст:\
{message.text}\n')


@bot.message_handler(commands=['clock'])
def clock_schedule(message):
    print(f'Чат: {message.chat.title}, ID: {message.chat.id}\nОт кого: {message.from_user.username}\nТекст:\
{message.text}\n')
    clock = """Расписание звонков:
1. 8:00 - 9:20 
2. 9:35 - 10:55 
3. 11:25 - 12:45 
4. 12:55 - 14:15 
5. 14:30 - 15:50"""
    bot.send_message(message.chat.id, clock)


@bot.message_handler(commands=['today'])
def today_schedule(message):
    print(f'Чат: {message.chat.title}, ID: {message.chat.id}\nОт кого: {message.from_user.username}\nТекст:\
{message.text}\n')
    response = "Расписание на сегодня:\n"
        if current_week == 1:
            bot.send_message(message.chat.id, response + days.get(datetime.datetime.now().weekday())['Числитель'])
        else:
            bot.send_message(message.chat.id, response + days.get(datetime.datetime.now().weekday())['Знаменатель'])


@bot.message_handler(commands=['tomorrow'])
def tomorrow_schedule(message):
    print(f'Чат: {message.chat.title}, ID: {message.chat.id}\nОт кого: {message.from_user.username}\nТекст:\
{message.text}\n')
    response = 'Расписание на завтра:\n'
    if current_week == 1:
        if datetime.datetime.today().weekday() == 6:
            bot.send_message(message.chat.id, response + days.get(0)['Числитель'])
        else:
            bot.send_message(message.chat.id, response + days.get(datetime.datetime.now().weekday() + 1)['Числитель'])
    else:
        if datetime.datetime.today().weekday() == 6:
            bot.send_message(message.chat.id, response + days.get(0)["Знаменатель"])
        else:
            bot.send_message(message.chat.id, response + days.get(datetime.datetime.now().weekday() + 1)['Знаменатель'])


# Типа логгер сообщений
@bot.message_handler(content_types=['text'])
def take_message(message):
    print(f'Чат: {message.chat.title}, ID: {message.chat.id}\nОт кого: {message.from_user.username}\nТекст:\
{message.text}\n')


# Изменение числителя/знаментеля
def change_current_week():
    global current_week
    if current_week == 1:
        current_week = 2
    else:
        current_week = 1


# Отправка расписания утром
def send_schedule_morning():
    response = 'Расписание на сегодня:\n'
    if current_week == 1:
        bot.send_message(my_id, response + days.get(datetime.datetime.now().weekday())['Числитель'])
        bot.send_message(ip2_id, response + days.get(datetime.datetime.now().weekday())['Числитель'])
    else:
        bot.send_message(my_id, response + days.get(datetime.datetime.now().weekday())['Знаменатель'])
        bot.send_message(ip2_id, response + days.get(datetime.datetime.now().weekday())['Знаменатель'])


# Отправка расписания вечером на завтрашний день
def send_schedule_evening():
    response = 'Расписание на завтра:\n'
    if current_week == 1:
        if datetime.datetime.today().weekday() == 6:
            bot.send_message(my_id, response + days.get(0)['Числитель'])
            bot.send_message(ip2_id, response + days.get(0)['Числитель'])
        else:
            bot.send_message(my_id, response + days.get(datetime.datetime.now().weekday() + 1)['Числитель'])
            bot.send_message(ip2_id, response + days.get(datetime.datetime.now().weekday() + 1)['Числитель'])
    else:
        if datetime.datetime.today().weekday() == 6:
            bot.send_message(my_id, response + days.get(0)['Знаменатель'])
            bot.send_message(ip2_id, response + days.get(0)['Знаменатель'])
        else:
            bot.send_message(my_id, response + days.get(datetime.datetime.now().weekday() + 1)['Знаменатель'])
            bot.send_message(ip2_id, response + days.get(datetime.datetime.now().weekday() + 1)['Знаменатель'])


# Запуск бота
def run_bot():

    bot.send_message(my_id, 'Бот запущен!')

    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(15)


# Переодизация отпраки расписания
def run_schedule(morning, evening):

    schedule.every().sunday.at('16:00').do(change_current_week)
    schedule.every().day.at(morning).do(send_schedule_morning)
    schedule.every().day.at(evening).do(send_schedule_evening)

    while True:
        schedule.run_pending()
        time.sleep(1)


# Ответ на комманду /stop
@bot.message_handler(commands=['stop'])
def stop_message(message):
    print(f'Чат: {message.chat.title}\nОт кого: {message.from_user.username}\nТекст: {message.text}\n')
    bot.send_message(message.chat.id, 'Поздравляю! Ты больше не ленивая жопа!')


if __name__ == '__main__':
    Thread(target=run_bot).start()
    Thread(target=run_schedule, args=(send_schedule_morning_at, send_schedule_evening_at)).start()
