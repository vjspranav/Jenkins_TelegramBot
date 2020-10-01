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
import json

with open("config.json") as json_config_file:
    config = json.load(json_config_file)

jenkins_url = config["jenkins"]["host"]
jenkins_user = config["jenkins"]["user"]
jenkins_pass = config["jenkins"]["pass"]

def jenbuild(token, job, device, buildWithParameters = True):
    jenkins_job_name = job
    jenkins_params = {'token': token, 'device': device}

    try:
        auth = (jenkins_user, jenkins_pass)
        crumb_data = requests.get("{0}/crumbIssuer/api/json".format(jenkins_url), auth = auth, headers={'content-type': 'application/json'})
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

token = config["telegram"]["token"]

bot = telegram.Bot(token=token)
print(bot.get_me())
updater = Updater(token=token, use_context=True)
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Welcome to the Jenkins bot.")

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
    h="""
Usage:
/build devicename - trigger build for devicename
/buildno for no parameter builds
"""
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

