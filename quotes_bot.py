#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler
import logging
import random

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def read_telegram_api_key():
    with open("telegram-api-key.txt", "r") as api_key_file:
        api_key = api_key_file.readline().strip()
        return api_key


def read_quotes():
    with open("quotes.txt", "r") as quotes:
        quotes = quotes.readlines()
        quotes = map(lambda x: x.strip(), quotes)
        quotes = list(filter(None, quotes)) # remove empty lines
        return quotes


def start(bot, update):
    update.message.reply_text("Hi, type /random to get a random quote")


def quote(bot, update):
    quotes = read_quotes()
    quote = random.choice(quotes)
    update.message.reply_text(quote)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    telegram_api_key = read_telegram_api_key()

    updater = Updater(telegram_api_key)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("random", quote))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    logger.info("Bot started")

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
