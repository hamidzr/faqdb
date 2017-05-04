#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler)
import logging
import csv

## to make it utf-8
import sys, sqlite3, os
reload(sys)
sys.setdefaultencoding('utf-8')

#hazm
from hazm import *

# felan send messages to the group
test_group_chat_id = -195462829
TARGET_CHAT = -195462829


#init db
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

engine = create_engine('sqlite+pysqlite:///main.db', module=sqlite, connect_args={'check_same_thread': False},)
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
	date= Column(Integer)
	sender_username = Column(String)
	sender_name = Column(String)
	sender_id = Column(Integer)
	chat_title = Column(String)
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


# end of init

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)
# GENDER = range(4)

# custom functions start here


def save_message(message):
	# save to db\
	message = Message(body=message.text, sender_username= message.from_user.username, sender_id= message.from_user.id, chat_title= message.chat.title, chat_id=message.chat.id, message_id=message.message_id, date= message.date, sender_name = message.from_user.first_name + ' ' + message.from_user.last_name)
	session.add(message)
	session.commit()
	return message
	
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
	update.message.reply_text(update.message.text + ' ' + username)
	latest_messages = session.query(Message).order_by('date').limit(5)
	bot.sendMessage(chat_id= test_group_chat_id, text= latest_messages[0].body)
	bot.sendMessage(chat_id= test_group_chat_id, text= latest_messages[1].body)
	bot.sendMessage(chat_id= test_group_chat_id, text= latest_messages[3].body)


# def help(bot, update):
	# update.message.reply_text('Help!')


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def base_logic(bot, update):
	# print(update.message.from_user)
	# if update.message.chat.id != TARGET_CHAT:
	# 	return
	# bot.sendMessage(chat_id= test_group_chat_id, text= 'saving: '+ update.message.text)
	save_message(update.message)

def main():
	# Create the EventHandler and pass it your bot's token.
	updater = Updater("244680876:AAHJYczo4r_RmC20LsRr7_BMFNgGRm_UB3k")

	# Get the dispatcher to register handlers
	dp = updater.dispatcher

	# on different commands - answer in Telegram
	dp.add_handler(CommandHandler("start", start))
	# dp.add_handler(CommandHandler("addKeyword", addKeyword))
	# dp.add_handler(CommandHandler("getAnswers", getAnswers))
	# dp.add_handler(CommandHandler("topKeywords", topKeywords))
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
