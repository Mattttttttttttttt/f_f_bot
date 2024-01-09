import telebot
from telebot import types
from glob import glob as glob
import PyPDF2
import os

API_Token = '6012439320:AAFtduiAl2VTvNkI7y8rrPES9WZkz_YbfDo' if 'AMVERA' in os.environ else '6856931870:AAF7-5nOZXru_0Ebm5ae4yDjmOwfVvF3iI4'
bot = telebot.TeleBot(API_Token)

def names():
    path = 'D:\Desktop\Программы Питон\поиск файлов бот\data'
    paths = glob(path + '\*')
    names = []
    for i in range(len(paths)):
        j = 1
        names_2 = []
        while True:
            names_2.append(paths[i][len(paths[i]) - j])
            costyl = '\ '
            if paths[i][len(paths[i]) - j] == costyl[0]: break
            j = j + 1
        names_2 = names_2[0:len(names_2) - 1]
        names.append(' ')
        for j in range(len(names_2)):
            names[i] = names[i] + names_2[len(names_2) - 1 - j]
        names[i] = names[i][1:len(names[i])]
    return(names)

def paths_pdf(name):
    pp = '/data' if 'AMVERA' in os.environ else 'D:\Desktop\Программы Питон\поиск файлов бот\data'
    base_path = pp + f'\\{name}'
    paths = glob(base_path + '/*pdf')
    pdf_list = []
    for f in paths:
        pdf_list.append(PyPDF2.PdfReader(f,'rb'))
    return(paths, pdf_list)

#поиск по названиюfghjkmnbgf
def func1(message, paths):
    text = message.text
    matches = 0
    g = 0
    for i in range(len(paths)):
        if text in paths[i]:
            if text == paths[i][49:len(paths[i])-4]:
                bot.send_message(message.chat.id, text='Полное совпадение по названию:')
                bot.send_document(message.chat.id, document=open(paths[i], 'rb'))
            else:
                if g == 0: bot.send_message(message.chat.id, text = 'Пересечение по названию:')
                g = 1
                bot.send_document(message.chat.id, document = open(paths[i], 'rb'))
            matches = 1
    if matches != 1:
        bot.send_message(message.chat.id, text = 'Совпадений нет, попробуйте ещё раз!')
        bot.send_message(message.chat.id, text='Введите название файла')
        bot.register_next_step_handler(message, func1)


#поиск по страницам
def func2(message, paths, pdf_list):
    text = message.text
    draft_path ='/data/drafts' if 'AMVERA' in os.environ else 'D:\Desktop\Программы Питон\поиск файлов бот\drafts'
    c = 0
    pages_list = []
    bot.send_message(message.chat.id, text = 'Обработка запроса (Это может занять время)')
    for i in range(len(pdf_list)):
        d_c = 0
        for j in range(len(pdf_list[i].pages)):
            if text in pdf_list[i].pages[j].extract_text():
                d_c = d_c + 1
                c = c + 1
                bot.send_message(message.chat.id, text = f'Совпадение № {c}')
                if d_c == 1:
                    bot.send_document(message.chat.id,document = open(paths[i], 'rb'))
                pdf_new = PyPDF2.PdfWriter()
                pdf_new.add_page(pdf_list[i].pages[j])
                comand_1 = f'''pdf_new.write('/data/drafts/page_{c}.pdf' if 'AMVERA' in os.environ else 'D:\Desktop\Программы Питон\поиск файлов бот\drafts\page_{c}.pdf')'''
                exec(comand_1)
                comand_2 = f'''bot.send_document(message.chat.id, document = open('/data/drafts/page_{c}.pdf' if 'AMVERA' in os.environ else 'D:\Desktop\Программы Питон\поиск файлов бот\drafts\page_{c}.pdf', 'rb'))'''
                exec(comand_2)
                comand_3 = f'''os.remove('/data/drafts/page_{c}.pdf' if 'AMVERA' in os.environ else 'D:\Desktop\Программы Питон\поиск файлов бот\drafts\page_{c}.pdf')'''
                exec(comand_3)
    if c == 0:
        bot.send_message(message.chat.id, text = 'Совпадений не найдено, попробуёте ещё раз')
        bot.send_message(message.chat.id, text='Введите ключевую фразу')
        bot.register_next_step_handler(message = message, callback =  func2, paths = paths, pdf_list = pdf_list)
    elif c!= 0: bot.send_message(message.chat.id, text = 'Обработка завершена')



@bot.message_handler(commands = ['start', 'help', 'back'])
def send_welcome(message):
    bot.send_message(chat_id = message.chat.id, text = 'Приветсвую! Бот имеет собственную базу данных, за вами только выбрать нужный раздел и искать в нём либо по содержанию файлов.\n Совет ищите по точной ключевой фразе или одному слову. Условно поиск рецепта пирога по заданному "мука яйца соль" вряд-ли что найдёт. А вот по "добавьте 20г муки" найти шансов больше))')
    markup = types.InlineKeyboardMarkup(row_width=1)
    name = names()
    for i in range(len(name)):
        if not name[i] == 'drafts':
            btn = types.InlineKeyboardButton(text = name[i], callback_data = name[i])
            markup.add(btn)
    bot.send_message(message.chat.id, text = 'Выберите раздел:',  reply_markup=markup)


@bot.callback_query_handler(func = lambda c: True)
def finding(c):
    bot.answer_callback_query(c.id, text = c.data)
    chat_id = c.message.chat.id
    name = c.data
    bot.send_message(chat_id, 'Введите ключевое слово или фразу для поиска')
    path, pdf = paths_pdf(name)
    bot.register_next_step_handler_by_chat_id(chat_id = chat_id, callback = func2, paths = path, pdf_list = pdf)
""""@bot.message_handler(commands = ['инструкция'])
def send_instruction(message):
    video = open('D:\Desktop\Программы Питон\поиск файлов бот\data\инструкция.MP4', 'rb')
    bot.send_video(message.chat.id, video = video)
@bot.message_handler(content_types = ['text'])
def answ(message):
    if message.text == 'Поиск по названию файла':
        bot.send_message(message.chat.id, text = 'Введите название файла')
        bot.register_next_step_handler(message, func1)
    if message.text == 'Поиск по содержанию':
        bot.send_message(message.chat.id, text = 'Как это работает? Я ищу вашу ключевую фразу в своих базах данных. Если я нахожу что-то, я скидываю вам номер сопадения, файл с совпадением и страницу на которой совпадение найдено. P.S. Если я скинул только страницу - значит в файле несколько страниц с совпадениями')
        bot.send_message(message.chat.id, text = 'Введите ключевую фразу')
        bot.register_next_step_handler(message, func2)
"""

p = 0
while p == 0:
    print('Processing')
    p = 1
bot.infinity_polling()