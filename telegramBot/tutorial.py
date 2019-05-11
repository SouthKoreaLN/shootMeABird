from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
def main():
    updater = Updater('836127070:AAH9qhHE8ClBzlJosL4jOtW1KZ4MslVaLHA')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
