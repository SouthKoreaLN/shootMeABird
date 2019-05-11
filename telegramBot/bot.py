from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import json
import numpy as np

apikey = '3ae2daad-ad9b-45e8-92a9-706338586d0a'
botToken = '836127070:AAH9qhHE8ClBzlJosL4jOtW1KZ4MslVaLHA'
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

def get_waifu(update,context):
    print("get_waifu")
    
    payment_id = context.user_data['payment_id']

    info = chargeInfo(payment_id)
    if info['data']['status'] == 'paid':
        pass
    else:
        update.message.reply_text("you didn't pay!")

def request_waifu(update,context):
    print("request_waifu")

    cost = calculate_cost()
    update.message.reply_text("it will cost you %.2f"%cost+' USD')

    charge = generateCharge(cost)
    payreq = charge['data']['lightning_invoice']['payreq']
    
    update.message.reply_text("your payreq here")
    update.message.reply_text(payreq)
    
    payment_id = charge['data']['id']
    
    context.user_data['payment_id'] = payment_id

if __name__ == "__main__":
    updater = Updater(botToken,use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('test',test))
    dp.add_handler(CommandHandler('request_waifu',request_waifu))
    dp.add_handler(CommandHandler('get_waifu',get_waifu)) 

    updater.start_polling()
    updater.idle()