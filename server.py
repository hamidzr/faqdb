#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
import logging

## to make it utf-8
import sys, sqlite3, os
reload(sys)
sys.setdefaultencoding('utf-8')

#hazm
# from hazm import *

# felan send messages to the group
test_group_chat_id = -195462829


#prep db
if not (os.path.exists('faq.db')):
	conn = sqlite3.connect('faq.db')
	c = conn.cursor()
	# Create table
	c.execute('''CREATE TABLE messages
	             (id INTEGER PRIMARY KEY, body TEXT, chat_id INTEGER, message_id INTEGER)''')
	c.execute('''CREATE TABLE keywords
	             (id INTEGER PRIMARY KEY, name VARCHAR(100))''')
	c.execute('''CREATE TABLE keywords_messages_association
	             (keywords_id INTEGER, message_id INTEGER, count INTEGER)''')
	
	keywords = ['آزادسازی مدرک', 'ایتالیا', 'اسکالرشیپ', 'فلوشیپ', 'فاند', 'پکیج رزومه', 'fellowship', 'scholarship', 'کانال اپلای', 'تافل', 'ایلتس', 'امریکا', 'ایمیل', 'ویزای eb1', 'انواع بورس', 'اطلاعات دانشگاه', 'زمانبدی پذیرش', 'فوق لیسانس', 'دکتری', 'کمک هزینه', 'gre', 'gpa', 'نتایج اپلای', 'اساتید امریکا', 'رشته حساس', 'زمانبدی پذیرش', 'آزادسازی مدرک', 'ranking', 'انواع بورس', 'بحث داغ', 'زبان غذا', 'مصاحبه', 'ایمیل زدن', 'کسری خدمت', 'مطالب مفید', 'wes org', 'تبدیل نمره ایران به آمریکا', 'ردگیری ایمیل ها', 'نتیجه نتایج پذیرش آمریکا', 'تهیه متن آماده جهت تسریع ایمیل gmail', 'اقامت دائم کاری استرالیا', 'فاند هزینه', 'مدارک کاریابی', 'تبدیل معدل', 'ویزای eb1', 'دیتابیس', 'cover letter', 'فاکتور پذیرش', 'gpa calculator', 'توضیح فاندها', 'tpo', 'gmat', 'پذيرش', 'فاند', 'بورسيه', 'ارشد', 'دكترا', 'آمريكا', 'كانادا', 'اروپا', 'استراليا', 'اقامت', 'مهاجرت', 'آلمان', 'ايتاليا', 'مكاتبه', 'ادامه تحصيل', 'توصيه نامه', 'عنوان ايميل به استاد', ' حداقل معدل', 'انگیزه نامه', 'sop']

	for key in keywords:
		c.execute("INSERT INTO keywords VALUES (null, '{0}')".format(key))
	conn.commit()
	print 'seeding done'

# end of init

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# GENDER = range(4)

# custom functions start here

keywords = []

def save_message(message):
	# save to db
	# is it okay to call connect every time?! TODO
	conn = sqlite3.connect('faq.db')
	c = conn.cursor()
	c.execute("INSERT INTO messages VALUES (null,'{0}','{1}','{2}')".format(message.text, message.chat.id, message.message_id))
	conn.commit()
	print 'saved' + message.text


def update_keywords():
	global keywords
	conn = sqlite3.connect('faq.db')
	c = conn.cursor()
	c.execute("select name from keywords")
	for row in c.fetchall():
		keywords.append(row[0])
	print keywords
update_keywords()


def detect_keywords(string):
	
	# normalizer = Normalizer()   
	# msg = normalizer.normalize(string)
	# found_keywords = ''
	found_keywords = {}
	for key in keywords:
		rep = string.count(key)
		if rep > 0 :
			# found_keywords += "#{0} ".format(key.replace (" ", "_"))
			found_keywords[key]= rep
	# aString = string.split()
	# return list(set(aString) & set(keywords))
	return found_keywords




# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(bot, update):
    update.message.reply_text('Hi!')
    username = update.message.from_user.username 
    update.message.reply_text(update.message.text + username)
#     update.message.reply_text(str([u'\u0641\u0644\u0648\u0634\u06cc\u067e', u'\u0627\u06cc\u0645\u06cc\u0644', u'GPA']))

# def help(bot, update):
    # update.message.reply_text('Help!')

def addKeyword(bot, update):
	update.message.from_user.username
	msg = update.message.text.split()
	del msg[0]
	key = ' '.join(msg)
	update.message.reply_text('keyword ' + key + ' ..')
	conn = sqlite3.connect('faq.db')
	c = conn.cursor()
	c.execute("INSERT INTO keywords VALUES (null, '{0}')".format(key))
	conn.commit()
	update_keywords()

# def echo(bot, update):
    # update.message.reply_text(update.message.text)

# def keyword(bot, update):
#     reply_keyboard = [['Boy', 'Girl', 'Other']]

#     update.message.reply_text(
#         'Hi! My name is Professor Bot. I will hold a conversation with you. '
#         'Send /cancel to stop talking to me.\n\n'
#         'Are you a boy or a girl?',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

#     return GENDER


# def gender(bot, update):
#     user = update.message.from_user
#     logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
#     update.message.reply_text('I see! Please send me a photo of yourself, '
#                               'so I know what you look like, or send /skip if you don\'t want to.',
#                               reply_markup=ReplyKeyboardRemove())

#     return ConversationHandler.END

# def cancel(bot, update):
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation." % user.first_name)
#     update.message.reply_text('Bye! I hope we can talk again some day.',
#                               reply_markup=ReplyKeyboardRemove())
#     return ConversationHandler.END


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def base_logic(bot, update):
	detected_keywords = detect_keywords(update.message.text)
	# msg_keywords = str(detected_keywords).strip('[]')
	
	if len(detected_keywords) > 0:
		msg = ''
		for key, value in detected_keywords.iteritems():
			msg += "#{0} {1}martabe ".format(key.replace (" ", "_"), value)
		bot.sendMessage(chat_id= test_group_chat_id, text= 'detected from chat: ' + update.message.chat.title)
		bot.sendMessage(chat_id= test_group_chat_id, text= msg)
		save_message(update.message)
	
# 	if 'soal' in update.message.text:
		# update.message.reply_text('soal porside shod!')


def main():
    # Create the EventHandler and pass it your bot's token.
	updater = Updater("244680876:AAHJYczo4r_RmC20LsRr7_BMFNgGRm_UB3k")

    # Get the dispatcher to register handlers
	dp = updater.dispatcher

    # on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("addKeyword", addKeyword))
#     dp.add_handler(CommandHandler("help", help))

 #    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
	# conv_handler = ConversationHandler(
	# 	entry_points=[CommandHandler('keyword', keyword)],
	# 	states={
	#   		GENDER: [MessageHandler(Filters.text, gender)]
	# 	},
	# 	fallbacks=[CommandHandler('cancel', cancel)]
	# )

	# dp.add_handler(conv_handler)



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
