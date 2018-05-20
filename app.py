import logging
from random import randint
from queue import Queue
from threading import Thread
from telegram import Bot,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters


ask_repeat = False
repeat = 1000
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '603527144:AAFKPweONf2c4hixHpaB_6rWzNZhRkh5_Z4'


def start(bot, update):
    update.message.reply_text('با زدن عبارت Simulate/ میتونید قضیه مونتی هال رو شبیه سازی کنید')
    update.message.reply_text('با زدن عبارت About/ میتونید درباره مونتی هال بیشتر بدونید')

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)

    custom_keyboard = [
        ['/Simulate'],
        ['/About']
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=id, text="انتخاب کنید", reply_markup=reply_markup)



def board(bot, update):

    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)
    #########
    user = update.message.from_user
    user = str(user)
    ###########
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=id, text="آماده سازی", reply_markup=reply_markup)

    try:
        master_counter = 0
        first_choice = 0
        sec_choice = 0
        rechoice = 0
     
        while master_counter < repeat:

            list = ["null", "null", "null"]
            list[randint(0, 2)] = "Gold"
            for item in range(3):
                if list[item] == "Gold":
                    prize = item
                else:
                    list[item] = "Empty"

            c = randint(0, 2)

            empty = ['null', 'null']
            j = 0
            k = 0
            for item in list:
                if item == "Empty":
                    empty[j] = k
                    j = j + 1
                k = k + 1

            while True:
                omitted = int(empty[randint(0, 1)])
                if omitted != c:
                    break

            for next_choice in range(3):
                if next_choice != omitted and next_choice != c:
                    changed = next_choice

            for me in range(3):
                if me != omitted and me != changed:
                    choose_again = me

            print("Test no: " + str(master_counter + 1))
            print("first choice : " + str(c + 1))
            print("Removed Option : " + str(omitted + 1))
            print("Choice changed to : " + str(changed + 1))
            print("Prize was in : " + str(prize + 1))
            print("----------------------------")

            if c == prize:
                first_choice += 1

            if changed == prize:
                sec_choice += 1

            if choose_again == prize:
                rechoice += 1

            master_counter += 1

        a="FINAL RESULTS:"
        b="1.No change: " + str(first_choice / repeat * 100) + "% won"
        c="2.Changed: " + str(sec_choice / repeat * 100) + "% won"
        d="3.Choose Again: " + str(rechoice / repeat * 100) + "% won"

        bot.send_message(chat_id=id, text=a)
        bot.send_message(chat_id=id, text=b)
        bot.send_message(chat_id=id, text=c)
        bot.send_message(chat_id=id, text=d)

    except:
        print("failed")


def about(bot, update):
    update.message.reply_text("https://fa.wikipedia.org/wiki/مسئله_مونتی_هال")


def simulate(bot, update):
    global ask_repeat
    bot = Bot(TOKEN)
    id = update.message.from_user.id
    id = int(id)
    #########
    user = update.message.from_user
    user = str(user)
    ###########
    reply_markup = ReplyKeyboardRemove()
    bot.send_message(chat_id=id, text="تعداد دفعات تکرار را مشخص کنید", reply_markup=reply_markup)
    ask_repeat=True

def echo(bot, update):
    global repeat
    global ask_repeat
    if ask_repeat:
        try:
            repeat = int(update.message.text)
            ask_repeat = False
            board(bot,update)
        except:
            update.message.reply_text("از دستور راهنمایی استفاده کنید")
            update.message.reply_text("/start")



def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", start))
        dp.add_handler(CommandHandler("simulate", simulate))
        dp.add_handler(CommandHandler("about", about))

        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()