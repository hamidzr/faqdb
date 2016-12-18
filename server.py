#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

## to make it utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#hazm
from hazm import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# custom functions

def save_message():
	# save to db
	pass

def detect_keywords(string):
	keywords = ['آزادسازی مدرک', 'ایتالیا', 'اسکالرشیپ', 'فلوشیپ', 'فاند ', 'پکیج رزومه ', 'fellowship', 'scholarship ', 'کانال اپلای', 'نمرات تافل ایلتس مورد نیاز امریکا', 'ایمیل زدن', 'ایمیل', 'ویزای EB1', 'انواع بورس', 'اطلاعات دانشگاه', 'زمانبدی پذیرش', 'نحوه اخذ کمک هزینه فوق لیسانس دکتری', 'GRE', 'GPA', 'نتایج اپلای', 'اساتید امریکا', 'رشته حساس', 'زمانبدی پذیرش', 'آزادسازی مدرک', 'ranking', 'انواع بورس', 'بحث داغ', 'زبان غذا', 'مصاحبه', 'ایمیل زدن', 'کسری خدمت', 'مطالب مفید', 'wes org', 'تبدیل نمره ایران به آمریکا', 'ردگیری ایمیل ها', 'نتیجه نتایج پذیرش آمریکا', 'تهیه متن آماده جهت تسریع ایمیل Gmail', 'اقامت دائم کاری استرالیا', 'فاند هزینه', 'مدارک کاریابی', 'تبدیل معدل', 'ویزای EB1', 'دیتابیس', 'Cover letter', 'فاکتور پذیرش', 'GPA Calculator', 'توضیح فاندها', 'TPO', 'GMAT']
	normalizer = Normalizer()   
	msg = normalizer.normalize(string)
	found_keywords = []
	for key in keywords:
		if key in msg:
			found_keywords.append(key)
	# aString = string.split()
	# return list(set(aString) & set(keywords))
	return found_keywords




# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')

def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def base_logic(bot, update):
	detected_keywords = detect_keywords(update.message.text)
	msg_keywords = str(detected_keywords).strip('[]')
	update.message.reply_text(msg_keywords)
	print msg_keywords
	if 'soal' in update.message.text:
		update.message.reply_text('soal porside shod!')
		bot.sendMessage(chat_id= update.message.chat.id, text= 'soal added')


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("244680876:AAHJYczo4r_RmC20LsRr7_BMFNgGRm_UB3k")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # base logic
    dp.add_handler(MessageHandler(Filters.text, base_logic))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()