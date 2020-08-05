# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 14:13:49 2020

@author: vjspranav
"""

import logging
import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler
from functools import wraps
import requests

jenkins_url = (your jenkins url)
jenkins_user = (your jenkins username)
jenkins_pwd = (your jenkins password)

def jenbuild(token, job, device, buildWithParameters = True):
    jenkins_job_name = job
    jenkins_params = {'token': token, 'device': device}

    try:
        auth= (jenkins_user, jenkins_pwd)
        crumb_data= requests.get("{0}/crumbIssuer/api/json".format(jenkins_url), auth = auth, headers={'content-type': 'application/json'})
        if str(crumb_data.status_code) == "200":

                if buildWithParameters:
                        data = requests.get("{0}/job/{1}/buildWithParameters".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})
                else:
                        data = requests.get("{0}/job/{1}/build".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})

                if str(data.status_code) == "201":
                 print ("Jenkins job is triggered")
                 return True
                else:
                 print ("Failed to trigger the Jenkins job")
                 return False

        else:
                print("Couldn't fetch Jenkins-Crumb")
                raise

    except Exception as e:
        print ("Failed triggering the Jenkins job")
        print ("Error: " + str(e))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

restricted_ids = []
conf = {}
conf['restricted_ids'] = restricted_ids

# Append the chat ids or the group id to which you want to restrict the bot access
# restricted_ids.append()

TOKEN=(Your Bot Token)

bot = telegram.Bot(token=TOKEN)
print(bot.get_me())
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def restricted(func):
    """Restrict usage of func to allowed users only and replies if necessary"""
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_chat.id
        if user_id not in conf['restricted_ids']:
            print(user_id, " is not in ", conf['restricted_ids'])
            print("WARNING: Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('User disallowed.')
            return  # quit function
        return func(update, context, *args, **kwargs)
    return wrapped

def start(update, context):
    user_id = update.effective_chat.id
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello There welcome to Jenkins Bot")

# Add a coment below before @restricted to allow access to everyone
@restricted
def build(update, context):
    inp = update.message.text
    if len(inp.split(" ")) == 1:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Device name not provided")
        return
    inp = inp.split(" ")[1]
    suc="Build triggered for " + inp
    fai="Something went wrong for " + inp
    if jenbuild((Token generated in jenkins build), (Job Name), inp):
        context.bot.send_message(chat_id=update.effective_chat.id, text=suc)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=fai)

def help(update, context):
    h="Yo Looks like you need help\n/build devicename - to trigger build for devicename where it is a parameter\n/buildno for no parameter builds\nPeace"
    context.bot.send_message(chat_id=update.effective_chat.id, text=h)

# Add a coment below before @restricted to allow access to everyone
@restricted
def buildno(update, context):
    user_id = update.effective_chat.id
    suc="Build Started for all Devices "
    fai="Something went wrong"
    if jenbuild(()Token generated in jenkins build, (Job Name), 'null', False):
        context.bot.send_message(chat_id=update.effective_chat.id, text=suc)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=fai)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

build_handler = CommandHandler('build', build)
dispatcher.add_handler(build_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

buildno_handler = CommandHandler('buildno', buildno)
dispatcher.add_handler(buildno_handler)

def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

