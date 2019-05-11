#!/usr/bin/env python
# coding: utf-8

# In[1]:


from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler, MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup
import requests
import json
import numpy as np
import io
import qrcode
import os


apikey = '3ae2daad-ad9b-45e8-92a9-706338586d0a'
botToken = '836127070:AAH9qhHE8ClBzlJosL4jOtW1KZ4MslVaLHA'


# In[3]:


################# Payment functions ##############

def generateCharge(amount,currency="USD"):
    r = requests.post(url = "https://dev-api.opennode.co/v1/charges",
                  headers = {
                        'Content-Type': 'application/json',
                        'Authorization': apikey
                            },
                  data = json.dumps({
                        "amount": amount,
                        "currency": currency,
                        "callback_url": "https://site.com/?handler=opennode",
                        "success_url": "https://site.com/order/abc123"
                            })
                 )
    return r.json()

def paidCharges():
    r = requests.get(url = 'https://dev-api.opennode.co/v1/charges', 
                    headers={
                  'Content-Type': 'application/json',
                  'Authorization': apikey
                        }
                   )
    return r.json()

def chargeInfo(idx):
    r = requests.get(url = 'https://dev-api.opennode.co/v1/charge/'+idx, 
                   headers={
                          'Content-Type': 'application/json',
                          'Authorization': apikey
                        })
    return r.json()

def test(update,context):
    print("test")
    update.message.reply_text('test')
    
    
################# GAN functions ##############
def calculate_cost():
    return np.random.rand()

import traceback
def get_waifu(update, context):
    print("get_waifu")
    
    payment_id = context.user_data['payment_id']
    if context.user_data['sent'] == True:
        update.message.reply_text("you already got waifu!")
        return
    
    info = chargeInfo(payment_id)
    if info['data']['status'] == 'paid':
        try:
            r = requests.get(url="http://localhost:5000/")
            i = io.BytesIO(r.content)
            update.message.reply_photo(i)
        except:
            print("failed")
            update.message.reply_text("waifu retrieval failed :(")
            # traceback.print_exc()
        # print(r.status)
        context.user_data['sent'] = True
    else:
        update.message.reply_text("you didn't pay!")

iii = 0
def make_qrcode(payreq):
    global iii
    i = qrcode.make(payreq)
    filename = f"{iii}.png"
    i.save(filename)
    iii += 1
    return filename

def request_waifu(update,context):
    print("request_waifu")

    cost = calculate_cost()
    update.message.reply_text("it will cost you %.2f"%cost+' USD')

    charge = generateCharge(cost)
    payreq = charge['data']['lightning_invoice']['payreq']
    
    update.message.reply_text("your payreq here")
    update.message.reply_text(payreq)
    qrf = make_qrcode(payreq)
    # update.message.reply_photo(open(qrf, 'rb'))
    
    payment_id = charge['data']['id']
    
    context.user_data['payment_id'] = payment_id
    context.user_data['sent'] = False


def start(update, context):
    keyboard = [[KeyboardButton('/test'),#"Test", callback_data='/test'),
                 KeyboardButton('/request_waifu'),#"Request", callback_data='/request_waifu')],
                 KeyboardButton('/get_waifu')]]  #"Get", callback_data='/get_waifu')]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

#def button(update, context):
#    query = update.callback_query
#    query.edit_message_text(text=query.data)
    # if query.data == '/request_waifu': request_waifu(update, context)
    # if query.data == '/get_waifu': get_waifu(update, context)
    # if query.data == '/test': test(update, context)

def help(update, context):
    update.message.reply_text("Use /start to test this bot.")

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


updater = Updater(botToken,use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
#dp.add_handler(CallbackQueryHandler(button))
dp.add_handler(CommandHandler('help', help))
dp.add_error_handler(error)
dp.add_handler(CommandHandler('test',test))
dp.add_handler(CommandHandler('request_waifu',request_waifu))
dp.add_handler(CommandHandler('get_waifu',get_waifu))
updater.start_polling()
updater.idle()
