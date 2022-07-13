from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time

class Bot():
    def __init__(self):
        ###########не трогать##########
        self.api_id = 9958356
        self.hash = "8895b2a2b674f00658660440ef8adcbb"
        #############значения##########
        self.admins = [697798016, 897669172]
        self.tovars = {"tovar":{"num":"num", "price":"price"},}
        self.price = []
        ###############################
        self.commands = ["start", "help"]
        self.keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="+сумма детальніше", callback_data="sum")],[InlineKeyboardButton(text="Список товарів", callback_data="products"),InlineKeyboardButton(text="Список Користувачів", callback_data="users")],[InlineKeyboardButton(text="Список продажу в грн за день", callback_data='money')],[InlineKeyboardButton(text="Видалити історію заробітку за день", callback_data="clear")],[InlineKeyboardButton(text="= Загальна сума", callback_data="=")],[InlineKeyboardButton(text="Назад", callback_data="back"), InlineKeyboardButton(text="Завершити роботу",callback_data="exit")]])
        self.keyboard_user = InlineKeyboardMarkup([[InlineKeyboardButton(text="Відвідати сайт", url="https://62cdf5192251b.site123.me/")],[InlineKeyboardButton(text="Завершити роботу",callback_data="exit")]])
        file = open('users.txt', 'r')
        self.us = set()
        for line in file:
            self.us.add(line.strip())
        file.close()
        ###########bot#################
        self.vet()

    def vet(self):
        self.file_prices = open("prices.txt", 'r')
        self.prices = []
        for price in self.file_prices:
            self.prices.append(price.strip())
        self.file_prices.close()

        bot = TeleBot("5554216479:AAE5fMHhD3s0Oyt1sYJwuD4Ucg5Oy3g5GoA")

        print("Bot is Online")

############################ Helps #################################
        @bot.message_handler(commands=self.commands)
        def helper(message):
            line = str(message.from_user.id) + ' ' + str(message.from_user.first_name)
            if line not in self.us:
                file = open('users.txt', 'a')
                file.write(str(message.from_user.id) + ' ' + str(message.from_user.first_name) + '\n')
                self.us.add(line)
                file.close()
            bot.send_message(message.chat.id, "Доброго дня, я Райдужний Єнот\nЧим можу допомогти?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="/help", callback_data='hel')]]))
            bot.delete_message(message.chat.id, message.id)

##################### Calculator ###################################
        @bot.message_handler(content_types=["text"])
        def cheker(message):
            if message.from_user.id in self.admins:
                try:
                    if message.text == "add":
                        self.admins.append(int(message.text[3:]))
                        bot.send_message(message.chat.id, 'користувач {} отримав права администратора'.format(message.text[3:]))
                    elif message.text == "del":
                        self.admins.remove(int(message.texr[3:]))
                        bot.send_message(message.chat.id, "користувач {} лишился прав администратора".format(message.text[3:]))
                    if message.text[0] == "+":
                        if message.text[-1] == '+':
                            num = message.text[1:]
                            num = float(num[:-1])
                            self.price.append(str(num) + " Terminal")
                            bot.send_message(message.chat.id, f"+ {str(num)} грн (Terminal)")
                            self.prices.append(str(num))
                            self.file_prices = open("prices.txt", 'a')
                            self.file_prices.write(str(num) + "\n")
                            self.file_prices.close()
                            file = open("price.txt", 'a')
                            file.write(str(num)+' Terminal\n')
                            file.close()
                        else:
                            num = float(message.text[1:])
                            self.price.append(str(num))
                            bot.send_message(message.chat.id, f"+ {str(num)} грн (Kasa)")
                            self.prices.append(str(num))
                            self.file_prices = open("prices.txt", 'a')
                            self.file_prices.write(str(str(num)) + "\n")
                            self.file_prices.close()
                            self.file_prices.close()
                            file = open("price.txt", 'a')
                            file.write(str(num) + '\n')
                            file.close()
                        bot.delete_message(message.chat.id, message.id)
                    else:bot.send_message(message.chat.id, text="Оберіть те що вам потрібно", reply_markup=self.keyboard)
                except ValueError:
                    pass
            else:
                bot.send_message(message.chat.id, "Доброго дня будьласка користуйтесь кнопками задля навігації")

        @bot.callback_query_handler(func=lambda callback_query: True)
        def callback(callback_query: CallbackQuery):
            try:
                callback = callback_query.data
                if callback == 'hel' or callback == "back":
                    bot.answer_callback_query(callback_query.id, text="Для звичайних користувачів плагін в розробці\n\nякщо ви є адміністратором нажміть адміністратор", show_alert=True)
                    bot.edit_message_text(chat_id=callback_query.message.chat.id,text="Оберіть хто ви", message_id=callback_query.message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Користувач", callback_data='user'), InlineKeyboardButton(text="Адміністратор", callback_data="admin")]]))
                if callback_query.from_user.id in self.admins:
                    if callback == 'admin':
                        bot.answer_callback_query(callback_query.id, text="Команди:\n +сумма\n`=` - загальна сумма\nadd user_id - дать права администраторa\ndel user_id - забрать права администратора", show_alert=True)
                        bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text="Оберіть те що вам потрібно", reply_markup=self.keyboard)
                    if callback == "sum":
                        bot.answer_callback_query(callback_query.id,text="Для того щоб вносити грощі до нотатки потрібно написати + сума наприклад\n+123\n\nякщо по терміналу в кінці обов'язково  +\n+1823+\n\nЯкщо копійки\n+194.13  - обовьязково крапка",show_alert=True)
                    elif callback == 'products':
                        self.tovars_text = ''
                        file = open('tovar.txt', 'r', encoding = "utf-8")
                        tovaru = []
                        for tov in file:
                            tovaru.append(tov)
                            stroka = tov.replace("\n", " ")
                            arr = stroka.split(" ")
                            self.tovars[arr[0]] = {"price": arr[1], "num": arr[2]}
                        file.close()
                        for line in tovaru:
                            self.tovars_text = self.tovars_text + line
                        bot.send_message(callback_query.message.chat.id, u"{}".format(self.tovars_text))
                    elif callback == 'users':
                        text = ''
                        for us in self.us:
                            text = text + us + '\n'
                        bot.send_message(callback_query.message.chat.id, text)
                    elif callback == 'money':
                        self.tovars_text = ""
                        file = open('price.txt', 'r')
                        for line in file:
                            self.tovars_text = self.tovars_text + line
                        bot.send_message(callback_query.message.chat.id, self.tovars_text)
                    elif callback == "yesdel":
                        self.prices = []
                        self.price = []
                        file = open('prices.txt', 'w')
                        file.write('')
                        file.close()
                        file = open('price.txt', 'w')
                        file.write('0' + '\n')
                        file.close()
                        bot.send_message(callback_query.message.chat.id, "Історія продажу видалена")
                        bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id,text="Оберіть те що вам потрібно", reply_markup=self.keyboard)
                    elif callback == "clear":
                        bot.edit_message_text(chat_id=callback_query.message.chat.id, text="Ви точно хочете видалити історію продажу?", message_id=callback_query.message.id, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Так",callback_data='yesdel'),InlineKeyboardButton(text="Ні",callback_data="admin")]]))
                    elif callback == "=":
                        arr = []
                        terminal = 0
                        kasa = 0
                        self.sum = 0
                        for num in self.prices:
                            self.sum = self.sum + float(num)
                        file = open('price.txt', "r")
                        for line in file:
                            arr.append(line.strip())
                        file.close()
                        for element in arr:
                            long = len(element)-8
                            if element[long:] == "Terminal":
                                terminal=terminal + float(element[:long])
                            else:
                                kasa=kasa+float(element)
                        bot.send_message(callback_query.message.chat.id, "Загальна сума ==> {} грн\nТермінал ==> {} грн\nКаса ==> {} грн".format(self.sum,terminal,kasa))
                    elif callback == "exit":
                        bot.delete_message(callback_query.message.chat.id, callback_query.message.id)
                        bot.send_message(callback_query.message.chat.id, text="Гарного вам дня та успіху 🦝")
                if callback == "user":
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text="Можливості користувача:", reply_markup=self.keyboard_user)
                elif callback == "exit":
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text="Гарного вам дня та успіху 🦝")
            
            except Exception as e:
                bot.answer_callback_query(callback_query.id, text=e)
                callback="error"
                pass
        bot.polling()
        
if __name__ == "__main__":
    Bot()
