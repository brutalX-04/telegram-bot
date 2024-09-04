# --> Module
import os
import re
import json
import time
import random
import logging
import requests
from bs4 import BeautifulSoup as bs
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler


FIRST = range(1)
rd    = random.choice

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# --> Handle Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	user = update.effective_user
	username = user.username
	text=f"Hi, @{username}\nWelcome to bot Fake Mail.\n\nBot ini dibuat untuk memudahkan pengguna dalam mendapatkan email sementara, Bot ini terintegrasi dengan web 1SECMAIL"
	
	button1 = InlineKeyboardButton("Owner", callback_data="Owner")
	button2 = InlineKeyboardButton("Create Mail", callback_data="Create")
	button3 = InlineKeyboardButton("Renew Mail", callback_data="Renew")
	button4 = InlineKeyboardButton("Donate", callback_data="Donate")

	keyboard = InlineKeyboardMarkup([[button1],[button2,button3],[button4]])

	await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)
	sendStatus(f'New users : {username}')



# --> Info Owner
async def owner(update, context):
	text = 'Author : Rizky Nurahman  \n\n``  github : [brutalX](https://github.com/brutalX-04)``  \n `` Facebook : [brutalid](https://www.facebook.com/brutalid.xyz) \n `` Telegram : [brutalX](https://t.me/brutalX_04)`` \n `` Instagram : [brutalid](https://www.instagram.com/brutalid_/)``'
	await context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode='Markdown')



# --> Create Fake Email
async def create(update, context):
	ab     = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	bc     = str(time.time()).split('.')[1]
	domain = rd(['1secmail.com','1secmail.org','1secmail.net','ezztt.com','vzumm.com','txcct.com','icznn.com'])
	mail   = ''.join([rd(ab).lower() for i in range(6)]) + bc + '@' + domain
	text   = 'Succes Create Fake Mail\nMail : %s \n\nPlease wait min 10 seccond to GET OTP'%(mail)

	button1 = InlineKeyboardButton("GET OTP", callback_data="Otp|%s"%(mail))

	keyboard = InlineKeyboardMarkup([[button1]])
	await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)



# --> Get Otp
async def getOtp(update, context, mail):
	name, domain = mail.split('@')
	get = requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}').json()

	if len(get) < 1:
		await context.bot.send_message(chat_id=update.effective_chat.id, text='Not message in mail box')

	else:
		idMail  = get[0]['id']
		getFull = bs(requests.get(f'https://www.1secmail.com/mailbox/?action=readMessageFull&id={idMail}&login={name}&domain={domain}').text, 'html.parser')
		body    = getFull.find('div', id='messageBody')
		try:
			title   = getFull.find('div', id='message').find('td').text
			content = re.sub(r'\s{2,}', ' ', body.find('div').text)
			text    = 'From : %s\nContent : %s'%(title,content)
			await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

		except:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=re.sub(r'\s{2,}', ' ', body.text))



# --> Bot Send User Status
def sendStatus(text):
	key = 'bot-token'
	requests.get('https://api.telegram.org/bot%s/sendMessage?chat_id=6628876249&text=%s'%(key,text))



# --> Handle Button Click
async def button_click(update, context):
    query = update.callback_query
    function = query.data
    if 'Owner' in function:
    	await owner(update, context)

    elif 'Create' in function:
    	await create(update, context)

    elif 'Otp|' in function:
    	await getOtp(update, context, function.split('|')[1])

    elif 'Renew' in function:
    	text = 'Please send message,\n\n#renew|yourmail@mail.com'
    	await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    elif 'Donate' in function:
    	text = 'Dana : 085219809271 \nVisa : 4889506084301286 \nBtc  : 12gnDFsBfJGLA64vs2884QxVa6hw8Xcfb2'
    	await context.bot.send_message(chat_id=update.effective_chat.id, text=text)



# --> All Message
async def echo(update, context):
	text  = update.message.text

	if '#renew|' in text:
		mail = text.split('|')[1]
		text   = 'Succes Renew Fake Mail\nMail : %s \n\nPlease wait min 10 seccond to GET OTP'%(mail)
		button1 = InlineKeyboardButton("GET OTP", callback_data="Otp|%s"%(mail))
		keyboard = InlineKeyboardMarkup([[button1]])
		await context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=keyboard)

	else:
		text1 = 'Hello !\nPlease send /start to menu'
		await context.bot.send_message(chat_id=update.effective_chat.id, text=text1)



# --> Running
if __name__ == '__main__':
	try:
		os.listdir('DATA')
	except:
		os.system('mkdir DATA')
	application = ApplicationBuilder().token('token-bot').build()


	application.add_handler(CallbackQueryHandler(button_click))
	start_handler = CommandHandler('start', start)
	echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
	application.add_handler(start_handler)
	application.add_handler(echo_handler)
    
	application.run_polling()
