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

config={}
with open("config.json") as json_config_file:
    config = json.load(json_config_file)

jenkins_url = config["jenkins"]["host"]
jenkins_user = config["jenkins"]["user"]
jenkins_pass = config["jenkins"]["pass"]

'''
For Pipeline builds Replace
    requests.get
with
    requests.post
'''
def jenbuild(token, job, jenkins_params, buildWithParameters = True):
    jenkins_job_name = job
    jenkins_params['token'] = token

    try:
        auth = (jenkins_user, jenkins_pass)
        crumb_data = requests.get("{0}/crumbIssuer/api/json".format(jenkins_url), auth = auth, headers={'content-type': 'application/json'})
        if str(crumb_data.status_code) == "200":

                if buildWithParameters:
                        data = requests.get("{0}/job/{1}/buildWithParameters".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})
                else:
                        data = requests.get("{0}/job/{1}/build".format(jenkins_url, jenkins_job_name), auth=auth, params=jenkins_params, headers={'content-type': 'application/json', 'Jenkins-Crumb':crumb_data.json()['crumb']})

                if str(data.status_code) == "201":
                 print("Triggered Jenkins job.")
                 return True
                else:
                 print("Failed to trigger Jenkins job.")
                 return False

        else:
                print("Couldn't fetch Jenkins crumb data.")
                raise

    except Exception as e:
        print ("Failed triggering Jenkins job")
        print ("Error: " + str(e))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Add telegram id's separated with comma to which you want to restrict bot to
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
        user_id = update.effective_user.id
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

'''
    For example you have a choice jenkins parameter named
    clean :
        yes
        no
    as choices then,
    p1="clean"
    param1="yes"
    if no value is passed it'll be yes by default
    and so on for any extra parameters to be added.
    
    To use:
        /build <paramname> <paramvalue>
    Example, Let's say we have two params, clean(with yes/no) and device(any string):
        /build device enchilada clean yes
        
    Has for p1 and p2 (two parameters), to extend/add more arguments 
    just copy paste and extend at 3 places where comments have been provided for help.

'''
# Add a coment below before @restricted to allow access to everyone
@restricted
def build(update, context):
    inp = update.message.text
    jenkins_job_name ="<your jenkins job name>"
    #[1/3] Add p3 and param3 here below
    p1="<name of parameter1>"
    p2="<name of parameter2>"
    param1="<default value of param1>"
    param2="<default value of param1>"
    l="Starting Job\n"
    sent=context.bot.send_message(chat_id=update.effective_chat.id, text=l)

    #[2/3] Add if conditions for p3 and param3 here below
    if p1 in inp:
        param1 = inp.split(" ")[inp.split(" ").index(p1) + 1]
        l+="With " + p1 +" = " + param1 + "\n" 
        sent.edit_text(l)

    if p2 in inp:
        param2 = inp.split(" ")[inp.split(" ").index(p2) + 1]
        l+="With " + p2 +" = " + param2 + "\n" 
        sent.edit_text(l)
    
    #[3/3] Add p3 and param3 here as done for p1, p2
    params={
        p1:param1,
        p2:param2
        }
    success= "\n" + inp + " triggered"
    fail="\nSomething went wrong for job " + inp
    # Generate a random token key and set it for jenkins build and add below
    if jenbuild("<Jenkins Job token>", jenkins_job_name, params, True):
        sent.edit_text(l+success)
    else:
        sent.edit_text(l+fail)

def help(update, context):
    h="""
Usage:
/build <param> <param value> - trigger build with paramvalue for param
- Multiple parameters (as supported by job) in any order can be provided
/buildno for no parameter builds
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=h)

# Add a coment below before @restricted to allow access to everyone
@restricted
def buildno(update, context):
    jenkins_job_name ="<your jenkins job name>"
    success="Jenkins job started"
    fail="Jenkins job could not be started"
    params={}
    # Generate a random token key and set it for jenkins build
    if jenbuild("<Jenkins Job token>", jenkins_job_name, params, False):
        context.bot.send_message(chat_id=update.effective_chat.id, text=success)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=fail)

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
