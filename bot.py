import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging

load_dotenv()
TOKEN = os.getenv('TOKEN')
# PORT = int(os.environ.get('PORT', '8443'))
API_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'
APP_NAME = 'https://telegram-dict.herokuapp.com/'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
  welcome = 'Howdy, how are you doing?\n\nPlease note that this bot is still in trial.\n\nThis is a simple bot that brings dictionary to your Telegram. ;)\n\nSend a normal message with\n`define <space> <your word>`\nsyntax to see the magic.'
  context.bot.send_message(chat_id=update.effective_chat.id, text=welcome, parse_mode='markdown')

def define_cmd_handler(update, context):
  to_send = 'Define is not a command.\n\nUs\n`define <space> <yourword>`\nsyntax in a normal message.'
  context.bot.send_message(chat_id=update.effective_chat.id, text=to_send, parse_mode='markdown')

def error(update, context):
  """Log Errors caused by Updates."""
  logger.warning('Update "%s" caused error "%s"', update, context.error)

def handle_dict_req(update, context):
  _, word = update.message.text.lower().split("define ")
  print(word)
  req = API_URL + word.strip()
  res = requests.get(req)
  try:
    data = res.json()[0]
    submitted_word = data['word']
    phonetic_txt = data['phonetics'][0]['text']
    phonetic_audio = data['phonetics'][0]['audio']
    first_msg = f'*{submitted_word}*\n_{phonetic_txt}_ [audio]({phonetic_audio})'
    context.bot.send_message(chat_id=update.effective_chat.id, text=first_msg, parse_mode='markdown')
    for obj in data['meanings']:
      ps = obj['partOfSpeech']
      dfn = obj['definitions'][0]['definition']
      try:
        exmp = obj['definitions'][0]['example']
        second_msg = f'Part Of Speech:\n{ps}\n\nDefinition:\n{dfn}\n\nExample:\n{exmp}'
        context.bot.send_message(chat_id=update.effective_chat.id, text=second_msg)
      except:
        second_msg = f'Part Of Speech:\n{ps}\n\nDefinition:\n{dfn}'
        context.bot.send_message(chat_id=update.effective_chat.id, text=second_msg)
  except:
    context.bot.send_message(chat_id=update.effective_chat.id, text='your word is invalid. try a different word.')

def handle_edits(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="I do not care about edited messages.")

def main():
  updater = Updater(token=TOKEN)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start, filters=(~Filters.update.edited_message)))
  dp.add_handler(CommandHandler("help", help, filters=(~Filters.update.edited_message)))
  dp.add_handler(MessageHandler(Filters.text & (~Filters.command) & (~Filters.update.edited_message), handle_dict_req))
  dp.add_handler(MessageHandler(Filters.update.edited_message & (~Filters.command), handle_edits))
  dp.add_error_handler(error)

  # updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
    main()