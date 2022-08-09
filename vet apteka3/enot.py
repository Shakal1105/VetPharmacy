from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

class Bot():
    def __init__(self):
        ###########не трогать##########
        self.api_id = 9958356
        self.hash = "8895b2a2b674f00658660440ef8adcbb"
        #############значения##########
        self.admins = [697798016, 897669172, 478323960]
        self.tovars = {}
        self.price = []

        self.pricex = 0
        self.county = 0
        self.arr = []
        self.target = ""
        self.callback = ""

        self.update_oblik = InlineKeyboardMarkup([[InlineKeyboardButton(text="Меню", callback_data='admin'), InlineKeyboardButton(text="Сума всього", callback_data="sumalloblik")]])
       ###############################
        self.commands = ["start", "help"]
        self.keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="+сумма детальніше", callback_data="sum")],
                                              [InlineKeyboardButton(text="Список товарів", callback_data="products"),
                                               InlineKeyboardButton(text="Список Користувачів", callback_data="users")],
                                              [InlineKeyboardButton(text="Список продажу в грн за день",
                                                                    callback_data='money')], [
                                                  InlineKeyboardButton(text="Видалити історію заробітку за день",
                                                                       callback_data="clear")],
                                              [InlineKeyboardButton(text="= Загальна сума", callback_data="=")],
                                              [InlineKeyboardButton(text="Назад", callback_data="back"),
                                               InlineKeyboardButton(text="Завершити роботу", callback_data="exit")]])
        self.keyboard_user = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Відвідати сайт", url="https://62cdf5192251b.site123.me/")],
             [InlineKeyboardButton(text="Завершити роботу", callback_data="exit")]])
        file = open('price.txt', 'r')
        self.us = set()
        for line in file:
            self.us.add(line.strip())
        file.close()
        ###########bot#################
        self.vet()

    def obliksave(self):
        oblik = open("oblik.txt", 'w')
        for i in self.tovars:
            oblik.write(i + ' ' + str(self.tovars[i]['count']) + ' ' + str(self.tovars[i]['price']) + '\n')
        oblik.close()

    def oblikopen(self):
        self.arr = []
        self.update_oblik = InlineKeyboardMarkup([[InlineKeyboardButton(text="Меню", callback_data='admin'), InlineKeyboardButton(text="Сума всього", callback_data="sumalloblik")]])
        file = open("oblik.txt", 'r')
        for i in file:
            tri = i.replace('\n', '').split(" ")
            self.tovars[tri[0]] = {"count": int(tri[1]), "price": float(tri[2])}
            self.arr.append(tri[0])
            self.update_oblik.add(InlineKeyboardButton(text=tri[0], callback_data=tri[0]))
        file.close()

    def vet(self):
        self.oblikopen()
        self.file_prices = open("prices.txt", 'r')
        self.prices = []
        for price in self.file_prices:
            self.prices.append(price.strip())
        self.file_prices.close()

        bot = TeleBot("5554216479:AAETVvLqz9xJPEp_jO0gfx4GyAN_t-IBYFs")

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
            bot.send_message(message.chat.id, "Доброго дня, я Райдужний Єнот\nЧим можу допомогти?",
                             reply_markup=InlineKeyboardMarkup(
                                 [[InlineKeyboardButton(text="Розпочати", callback_data='hel')]]))
            bot.delete_message(message.chat.id, message.id)

        @bot.message_handler(commands=["add"])
        def oblikadd(mess):
            self.name = mess.text[4:].replace(" ", "")
            if self.name == "" or self.name in self.arr:
                pass
            else:
                self.arr.append(self.name)
                print(self.arr)
                self.button = InlineKeyboardButton(text=self.name, callback_data=self.name)
                self.tovars[self.name] = {"price": self.pricex, "count": self.county}
                self.update_oblik.add(self.button)
                bot.delete_message(mess.chat.id, message_id=mess.id)
                self.obliksave()
        ##################### Calculator ###################################
        @bot.message_handler(content_types=["text"])
        def cheker(message):
            if self.target == "price":
                self.target = ''
                try:
                    self.pricex=float(message.text)
                    self.tovars[self.callback] = {"price":self.pricex, "count":self.county}
                    self.obliksave()
                    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
                except ValueError:
                    pass

            elif self.target == "count":
                self.target = ''
                try:
                    self.county = int(message.text)
                    self.tovars[self.callback] = {"price": self.pricex, "count": self.county}
                    self.obliksave()
                    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
                except ValueError:
                    pass

            else:pass
            if message.from_user.id in self.admins:
                try:
                    if message.text == "add":
                        self.admins.append(int(message.text[3:]))
                        bot.send_message(message.chat.id,
                                         'користувач {} отримав права администратора'.format(message.text[3:]))
                    elif message.text == "del":
                        self.admins.remove(int(message.texr[3:]))
                        bot.send_message(message.chat.id,
                                         "користувач {} лишился прав администратора".format(message.text[3:]))
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
                            file.write(str(num) + ' Terminal\n')
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
                except ValueError:
                    pass
            else:
                bot.send_message(message.chat.id, "Доброго дня будьласка користуйтесь кнопками задля навігації")

        @bot.callback_query_handler(func=lambda callback_query: True)
        def callback(callback_query: CallbackQuery):
            try:
                spisok = ["count11", "price11", "deltovaroblik"]
                if callback_query.data not in spisok: self.callback = callback_query.data
                print(self.callback)
                if callback_query.data == "deltovaroblik":
                    self.arr.remove(self.callback)
                    print(self.arr)
                    self.tovars.pop(self.callback)
                    self.update_oblik = InlineKeyboardMarkup([[InlineKeyboardButton(text="Меню", callback_data='admin'), InlineKeyboardButton(text="Сума всього", callback_data="sumalloblik")]])
                    self.obliksave()
                    self.oblikopen()
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text="Список Товарів (щоб додати введіть /add name)", reply_markup=self.update_oblik)
                if callback_query.data == 'sumalloblik':
                    self.all = 0
                    for i in self.tovars:
                        self.all = self.all + self.tovars[i]['count']*self.tovars[i]['price']
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text=f"Сума всіх одиниць товарів: {self.all}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Назад", callback_data='products')]]))
                if callback_query.data == 'price11':
                    self.target = "price"
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id,
                                               text=f"Введіть ціну за одиницю товару {self.callback}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Назад", callback_data=self.callback)]]))
                elif callback_query.data == "count11":
                    self.target = "count"
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id,
                                               text=f"Введіть кількість одиниць товару {self.callback}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Назад", callback_data=self.callback)]]))
                elif self.callback in self.arr:
                    self.pricex = self.tovars[self.callback]['price']
                    self.county = self.tovars[self.callback]['count']
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text=f"{self.callback} ціна: {self.tovars[self.callback]['price']}|| кількість: {self.tovars[self.callback]['count']}|| ціна за все: {self.tovars[self.callback]['count']*self.tovars[self.callback]['price']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Змінити ціну", callback_data="price11"),InlineKeyboardButton(text="Змінити кількість",callback_data="count11")],[InlineKeyboardButton(text="Назад",callback_data="products"),InlineKeyboardButton(text="Головне меню", callback_data="admin")],[InlineKeyboardButton(text='Видалити', callback_data='deltovaroblik')]]))
                if self.callback == "products":
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id, text="Список Товарів (щоб додати введіть /add name)", reply_markup=self.update_oblik)
                callback = callback_query.data
                if callback == 'hel' or callback == "back":
                    bot.answer_callback_query(callback_query.id,
                                              text="Для звичайних користувачів плагін в розробці\n\nякщо ви є адміністратором нажміть адміністратор",
                                              show_alert=True)
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, text="Оберіть хто ви",
                                          message_id=callback_query.message.id, reply_markup=InlineKeyboardMarkup([[
                                                                                                                       InlineKeyboardButton(
                                                                                                                           text="Користувач",
                                                                                                                           callback_data='user'),
                                                                                                                       InlineKeyboardButton(
                                                                                                                           text="Адміністратор",
                                                                                                                           callback_data="admin")]]))
                if callback_query.from_user.id in self.admins:
                    if callback == 'admin':
                        bot.answer_callback_query(callback_query.id,
                                                  text="Команди:\n +сумма\n`=` - загальна сумма\nadd user_id - дать права администраторa\ndel user_id - забрать права администратора",
                                                  show_alert=True)
                        bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                              message_id=callback_query.message.id, text="Оберіть те що вам потрібно",
                                              reply_markup=self.keyboard)
                    if callback == "sum":
                        bot.answer_callback_query(callback_query.id,
                                                  text="Для того щоб вносити грощі до нотатки потрібно написати + сума наприклад\n+123\n\nякщо по терміналу в кінці обов'язково  +\n+1823+\n\nЯкщо копійки\n+194.13  - обовьязково крапка",
                                                  show_alert=True)
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
                        bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                              message_id=callback_query.message.id, text="Оберіть те що вам потрібно",
                                              reply_markup=self.keyboard)
                    elif callback == "clear":
                        bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                              text="Ви точно хочете видалити історію продажу?",
                                              message_id=callback_query.message.id, reply_markup=InlineKeyboardMarkup([[
                                                                                                                           InlineKeyboardButton(
                                                                                                                               text="Так",
                                                                                                                               callback_data='yesdel'),
                                                                                                                           InlineKeyboardButton(
                                                                                                                               text="Ні",
                                                                                                                               callback_data="admin")]]))
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
                            long = len(element) - 8
                            if element[long:] == "Terminal":
                                terminal = terminal + float(element[:long])
                            else:
                                kasa = kasa + float(element)
                        bot.send_message(callback_query.message.chat.id,
                                         "Загальна сума ==> {} грн\nТермінал ==> {} грн\nКаса ==> {} грн".format(
                                             self.sum, terminal, kasa))
                    elif callback == "exit":
                        bot.delete_message(callback_query.message.chat.id, callback_query.message.id)
                        bot.send_message(callback_query.message.chat.id, text="Гарного вам дня та успіху 🦝")
                if callback == "user":
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id,
                                          text="Можливості користувача:", reply_markup=self.keyboard_user)
                elif callback == "exit":
                    bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.id,
                                          text="Гарного вам дня та успіху 🦝")

            except Exception as e:
                bot.answer_callback_query(callback_query.id, text=e)
                callback = "error"
                pass

        bot.polling(none_stop=True)


if __name__ == "__main__":
    Bot()
