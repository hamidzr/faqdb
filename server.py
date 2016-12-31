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
from hazm import *

# felan send messages to the group
test_group_chat_id = -195462829


#init db
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

engine = create_engine('sqlite+pysqlite:///test.db', module=sqlite, connect_args={'check_same_thread': False},)
# engine = create_engine('sqlalchemy.db', echo=True)

#create session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

#base class
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# end init db

#define classes
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# keywords_messages_association_table = Table('keywords_messages_association', Base.metadata,
#     Column('message_id', Integer, ForeignKey('messages.id')),
#     Column('keyword_id', Integer, ForeignKey('keywords.id'))
# )
  

class Message(Base):
	__tablename__ = 'messages'
	id = Column(Integer, primary_key=True)
	body = Column(String)
	chat_id = Column(Integer)
	message_id = Column(Integer)
	keywords = relationship("KeywordsMessagesAssociation", back_populates="message")

	# or use 	backref="messages" on one

class Keyword(Base):
	__tablename__ = 'keywords'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	messages = relationship("KeywordsMessagesAssociation", back_populates="keyword")	

class KeywordsMessagesAssociation(Base):
    __tablename__ = 'keywords_messages_association'
    message_id = Column(Integer, ForeignKey('messages.id'), primary_key=True)
    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)
    count = Column(Integer)
    keyword = relationship("Keyword", back_populates="messages")
    message = relationship("Message", back_populates="keywords")  


#create all tables /db
Base.metadata.create_all(engine)


#start a session? 
session = Session()


if len(session.query(Keyword).all()) < 5:
	#seed db
	keywords = ['آزادسازی مدرک', 'ایتالیا', 'اسکالرشیپ', 'فلوشیپ', 'فاند', 'پکیج رزومه', 'fellowship', 'scholarship', 'کانال اپلای', 'تافل', 'ایلتس', 'امریکا', 'ایمیل', 'ویزای eb1', 'انواع بورس', 'اطلاعات دانشگاه', 'زمانبدی پذیرش', 'فوق لیسانس', 'دکتری', 'کمک هزینه', 'gre', 'gpa', 'نتایج اپلای', 'اساتید امریکا', 'رشته حساس', 'زمانبدی پذیرش', 'آزادسازی مدرک', 'ranking', 'انواع بورس', 'بحث داغ', 'زبان غذا', 'مصاحبه', 'ایمیل زدن', 'کسری خدمت', 'مطالب مفید', 'wes org', 'تبدیل نمره ایران به آمریکا', 'ردگیری ایمیل ها', 'نتیجه نتایج پذیرش آمریکا', 'تهیه متن آماده جهت تسریع ایمیل gmail', 'اقامت دائم کاری استرالیا', 'فاند هزینه', 'مدارک کاریابی', 'تبدیل معدل', 'ویزای eb1', 'دیتابیس', 'cover letter', 'فاکتور پذیرش', 'gpa calculator', 'توضیح فاندها', 'tpo', 'gmat', 'پذيرش', 'فاند', 'بورسيه', 'ارشد', 'دكترا', 'آمريكا', 'كانادا', 'اروپا', 'استراليا', 'اقامت', 'مهاجرت', 'آلمان', 'ايتاليا', 'مكاتبه', 'ادامه تحصيل', 'توصيه نامه', 'عنوان ايميل به استاد', ' حداقل معدل', 'انگیزه نامه', 'sop']
	for key in keywords:
		keyw = Keyword(name=key)
		session.add(keyw)
	session.commit()

# end of init

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
# GENDER = range(4)

# custom functions start here

keywords = []

def save_message(message):
	# save to db\
	message = Message(body=message.text, chat_id=message.chat.id, message_id=message.message_id)
	session.add(message)
	session.commit()
	return message


def update_keywords():
	global keywords
	for key in session.query(Keyword).all():
		keywords.append(key.name)

update_keywords()


tagger = POSTagger(model='resources/postagger.model')
stemmer = Stemmer()
def learn_keywords(string):
	#relys on hazm detecting that it is a noun
	tagged_msg = tagger.tag(word_tokenize(string))
	for word in tagged_msg:
		if word[1] == 'N':
			keyw = stemmer.stem(word[0])
			#dont learn if it is persian and less than 4 characters. mishod 3 roham begirim. this is the lazy way
			if len(keyw) > 3 :
				add_keyword(keyw)

def add_keyword(key):
	if len(key)>1 and not key in keywords:
		session.add(Keyword(name=key))
		update_keywords()
		return True


def detect_keywords(string):
	# todo: keyword e from kew class return kone
	# found_keywords = ''
	found_keywords = {}
	for key in keywords:
		rep = string.count(key)
		if rep > 0 :
			found_keywords[key]= rep

	#TODO az 1 kalame 2 ta keyword detect nakone
	# if key in found_keywords.keys()
	# keywordo bardash az to text baresh dare
	# import re
	# string = 'che khabara salam <asdf> golabi'
	# print re.sub('\s.+ala.+\s', ' * ', string)	

	return found_keywords

def get_command_query(string):
	msg = string.split()
	del msg[0]
	key = ' '.join(msg).strip()
	return key

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def start(bot, update):
    update.message.reply_text('Started!')
    username = update.message.from_user.username 
    update.message.reply_text(update.message.text + username)

# def help(bot, update):
    # update.message.reply_text('Help!')

def addKeyword(bot, update):
	update.message.from_user.username
	key = get_command_query(update.message.text)
	if add_new_keyword(key):
		update.message.reply_text('added keyword "' + key + '" ..')


def getAnswers(bot, update):
	msg = get_command_query(update.message.text)
	
	# get message keywords
	msg_keywords = detect_keywords(update.message.text)
	
	# search db for similar / relevant messages!!
	answers = []
	for keyw in msg_keywords:
		#todo refactor detect keyword ke real keyword() bargardone
		key = session.query(Keyword).filter_by(name=keyw).first()
		assocs = session.query(KeywordsMessagesAssociation).filter_by(keyword_id=key.id).limit(5)
		for assoc in assocs:
			answers.append(assoc.message.body)
	
	# return most relevant answers
	for answer in answers:
		update.message.reply_text(answer)


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
	learn_keywords(update.message.text)
	detected_keywords = detect_keywords(update.message.text)
	# msg_keywords = str(detected_keywords).strip('[]')
	
	if len(detected_keywords) > 0:
		msg = ''
		message = save_message(update.message)
		for key, value in detected_keywords.iteritems():
			msg += "#{0} {1}martabe ".format(key.replace (" ", "_"), value)
			#todo redundant, pass bokon
			keyw = session.query(Keyword).filter_by(name=key).first()
			#create association
			assoc = KeywordsMessagesAssociation(count=value)
			assoc.message = message
			assoc.keyword = keyw
			session.add(assoc)		

		bot.sendMessage(chat_id= test_group_chat_id, text= 'detected from chat: ' + update.message.chat.title)
		bot.sendMessage(chat_id= test_group_chat_id, text= msg)
		session.commit()
		# TODO use association proxy to do this better/easier
		# for association in message.keywords:
		# 	print association.keyword.name
	
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
	dp.add_handler(CommandHandler("getAnswers", getAnswers))
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
