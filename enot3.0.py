from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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

        bot = Client("BotSession", self.api_id, self.hash)

        bot.start()
        bot.stop()
        print("Bot is Online")

############################ Helps #################################
        @bot.on_message(filters.command(self.commands, prefixes='/') & filters.all)
        def helper(bot, message):
            line = str(message.from_user.id) + ' ' + str(message.from_user.first_name)
            if line not in self.us:
                file = open('users.txt', 'a')
                file.write(str(message.from_user.id) + ' ' + str(message.from_user.first_name) + '\n')
                self.us.add(line)
                file.close()
            bot.send_message(message.chat.id, "Доброго дня, я Райдужний Єнот\nЧим можу допомогти?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="/help", callback_data='hel')]]))
            bot.delete_messages(message.chat.id, message.id)

##################### Calculator ###################################
        @bot.on_message(filters.text & filters.all)
        def cheker(bot, message):
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
                            bot.send_message(message.chat.id, f"+ {str(num)} грн")
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
                            bot.send_message(message.chat.id, f"+ {str(num)} грн")
                            self.prices.append(str(num))
                            self.file_prices = open("prices.txt", 'a')
                            self.file_prices.write(str(str(num)) + "\n")
                            self.file_prices.close()
                            self.file_prices.close()
                            file = open("price.txt", 'a')
                            file.write(str(num) + '\n')
                            file.close()
                except ValueError:
                    pass

        @bot.on_callback_query(filters.all)
        def callback(bot, callback_query: CallbackQuery):
            callback = callback_query.data
            if callback == 'hel' or callback == "back":
                bot.answer_callback_query(callback_query.id, text="Для звичайних користувачів плагін в розробці\n\nякщо ви є адміністратором нажміть адміністратор", show_alert=True)
                bot.edit_message_text(callback_query.message.chat.id,message_id=callback_query.message.id, text="Оберіть хто ви", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Користувач", callback_data='user'), InlineKeyboardButton(text="Адміністратор", callback_data="admin")]]))
            if callback_query.from_user.id in self.admins:
                if callback == 'admin':
                    bot.answer_callback_query(callback_query.id, text="Команди:\n +сумма\n`=` - загальна сумма\nadd user_id - дать права администраторa\ndel user_id - забрать права администратора", show_alert=True)
                    bot.edit_message_text(callback_query.message.chat.id, message_id=callback_query.message.id, text="Оберіть те що вам потрібно", reply_markup=self.keyboard)
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
                        self.tovars[arr[0]] = {"price": arr[1], "num": float(arr[2])}
                    file.close()
                    for line in tovaru:
                        self.tovars_text = self.tovars_text + line
                    bot.send_message(callback_query.message.chat.id, self.tovars_text)
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
                elif callback == "clear":
                    self.prices = []
                    self.price = []
                    file = open('prices.txt', 'w')
                    file.write('')
                    file.close()
                    file = open('price.txt', 'w')
                    file.write('0'+'\n')
                    file.close()
                    bot.send_message(callback_query.message.chat.id, "Історія продажу видалена")
                elif callback == "=":
                    self.sum = 0
                    for num in self.prices:
                        self.sum = self.sum + float(num)
                    bot.send_message(callback_query.message.chat.id, "Загальна сума : {} грн".format(self.sum))
                elif callback == "exit":
                    bot.delete_messages(callback_query.message.chat.id, callback_query.message.id)
                    bot.send_message(callback_query.message.chat.id, text="Гарного вам дня та успіху 🦝")

        bot.run()

if __name__ == "__main__":
    Bot()
