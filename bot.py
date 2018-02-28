# bot modules
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ParseMode
import logging

# my files
from settings import TELEGRAM_API_TOKEN
from commands_message import get_answer_command, get_answer_message, mode_of_bot 


logging.basicConfig(format='%(name)s + %(levelname)s + %(message)s', level=logging.INFO, filename='bot.log')


def command_message(bot, update):
    text = update.message.text.strip()
    text = text.split(' ')[0]

    answer_text, keyboard = get_answer_command(bot, update.effective_user, text)
    if type(answer_text) == list:
        for text_answer in answer_text:
            update.message.reply_text(text_answer, reply_markup=keyboard)
    else:
        update.message.reply_text(answer_text, reply_markup=keyboard)


def text_message(bot, update):
    text = update.message.text.strip()

    answer_text, keyboard = get_answer_message(bot, text)
    if type(answer_text) == list:
        for text_answer in answer_text:
            update.message.reply_text(text_answer, reply_markup=keyboard, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(answer_text, reply_markup=keyboard)


def main():
    updater = Updater(TELEGRAM_API_TOKEN)

    updater.bot.mode = mode_of_bot.EMPTY
    #updater.bot.test = {'test_step': 0, 'test_variant': 0, 'test_answers': []}

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.command, command_message))
    dp.add_handler(MessageHandler(Filters.text, text_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
