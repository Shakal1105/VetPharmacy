from pyrogram import Client, filters
import re

class Bot():
    def __init__(self):
        ###########не трогать##########
        self.api_id = 9958356
        self.hash = "8895b2a2b674f00658660440ef8adcbb"
        #############значения##########
        self.admins = [697798016, 897669172, 689859950]
        self.tovars = {"tovar":{"num":"num", "price":"price"},}
        self.price = []
        ###############################
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
##################### clear prices ######################
        @bot.on_message(filters.command("clear", prefixes='*'))
        def clear(bot, message):
            if message.from_user.id in self.admins:
                self.prices = []
                self.price = []
                file = open('prices.txt', 'w')
                file.write('')
                file.close()
                file = open('price.txt', 'w')
                file.write('')
                file.close()
                bot.send_message(message.chat.id, "История продаж очищена")
###################### Spiski ###########################
        @bot.on_message(filters.command('prices', prefixes="*") & filters.all)
        def prices(bot, message):
            if message.from_user.id in self.admins:
                self.tovars_text = ""
                file = open('price.txt', 'r')
                for line in file:
                    self.tovars_text = self.tovars_text + line
                bot.send_message(message.chat.id, self.tovars_text)

        @bot.on_message(filters.command('tovars', prefixes="*") & filters.all)
        def tovars(bot, message):
            if message.from_user.id in self.admins:
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
                bot.send_message(message.chat.id, self.tovars_text)
############################ Helps #################################
        @bot.on_message(filters.command("help".lower(), prefixes='*') & filters.all)
        def helper(bot, message):
            if message.from_user.id in self.admins:
                bot.send_message(message.chat.id,
                             "commands:\n +0 - для плюсования продажи подробнее отправь `help+`\n`*clear` - для очистки списка продаж на сегодня\n`=` - для вивода общей суми продаж за день\n`*tovars` - для вивода списка товаров\n`*prices` - для вивода всех продаж за день")

        @bot.on_message(filters.command("help".lower(), prefixes='/') & filters.all)
        def helper(bot, message):
            bot.send_message(message.chat.id, "commands:\n`*help` \nstatus:\n / - all users; + - цена продажи товара; = - сумаб; * - команди адміна")
######################### Summ ##############################
        @bot.on_message(filters.command("", prefixes='=') & filters.all)
        def summ(bot, message):
            if message.from_user.id in self.admins:
                self.sum=0
                for num in self.prices:
                    self.sum = self.sum + float(num)
                bot.send_message(message.chat.id, "общая сумма : {}".format(self.sum))
##################### Calculator ###################################
        @bot.on_message(filters.text & filters.all)
        def cheker(bot, message):
            if message.from_user.id in self.admins:
                try:
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
                    elif message.text == 'help+':
                        bot.send_message(message.chat.id, 'начните писать суму полученую за товар после + например\n+111.11\n+ 121\n\nесли оплата прошла по терминалу в конце добавте + например\n+111+\n+ 12.12 +')
                    else: bot.send_message(message.chat.id, "Ознакомтесь с командами админа `*help`")
                except ValueError:
                    pass
            else:bot.send_message(message.chat.id, 'Ознакомтесь з командами бота `/help`')


        bot.run()




if __name__ == "__main__":
    Bot()
