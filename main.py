#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

import setupInfo
import re
from telegram import Update, constants
from telegram.utils.helpers import mention_markdown
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters, CallbackContext,
                          ConversationHandler,
    PicklePersistence,
)
GETEEDITION = 1
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

PALAVRAS = "palavras"

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Esse Bot Marca a Morgana quando alguém fala uma palavra que caia '
                              'no filtro.\n'
                              '/changelist Inicia edição de lista de palavras\n'
                              '/cancel Cancela edição de palavras'
                              'Comandos do modo de edição:\n'
                              '"add <regex>" - Adiciona regex(es) separados por ";" ao filtro.\n'
                              '"ls" Para Listar os regex existentes.\n'
                              '"ls <palavra>" Para Listar retornar o(s) regex(es) que dão match.\n'
                              '"rm <indice>" Para remover um regex da lista.\n'
                              '"mv <indice> <regex>" Para altesrar um regex da lista.')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    pp = PicklePersistence(filename='botData.pickle')
    updater = Updater(setupInfo.TOKEN, persistence=pp, use_context=True)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.bot_data[PALAVRAS] = dispatcher.bot_data.get(PALAVRAS, [])
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('changelist', change_list)],
        states={
            GETEEDITION: [
                MessageHandler(Filters.regex( re.compile('^add .*$', re.IGNORECASE)), new_word),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(
        MessageHandler(Filters.regex(re.compile(r'.*\bLarissa\b.*', re.IGNORECASE)), que_larissa)
    )
    dispatcher.add_handler(
        MessageHandler(Filters.regex(r'.*\b[A-Z]\w+el\b.*'), que_daniel)
    )
    dispatcher.add_handler(
        MessageHandler(
            (Filters.text | Filters.caption) & ~Filters.command, filterPutaria))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()