from datetime import datetime
import logging
from logging import debug, info
from pathlib import Path
import random
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, PicklePersistence
import yaml  # pyyaml
import os
import json

TOKEN_FILE = 'token.txt'
TOKEN = Path(TOKEN_FILE).read_text().strip()
PORT = int(os.environ.get('PORT', 5000))

class Question:

    def __init__(self, qid, question, answer,category,type):
        self.qid = qid
        self.text = question
        self.answer = answer
        self.category = category
        self.type = type

QUESTIONS = {}

filelist = [file.replace(".json","") for file in os.listdir("data/")]
col=2
row=int(len(filelist)/col)
if len(filelist)%col==0:
    filelist_sorted = [filelist[r*2:(r+1)*2] for r in range(0,row)]
else:
    filelist_sorted = [filelist[r*2:(r+1)*2] for r in range(0,row)]
    filelist_sorted.append([filelist[row*2:len(filelist)]])


def start(update, context):
    """Command handler for command /start"""
    #print(context.user_data)
    msg = update.message
    user = msg.from_user

    if 'quiz' in context.user_data:
        context.user_data.pop('quiz')

    if 'username' not in context.user_data:
        context.user_data['username'] = user.username
    
    print(filelist_sorted)
    msg.bot.send_message(msg.chat_id,
        text=f'Let\'s start!',
        reply_markup=telegram.ReplyKeyboardMarkup(filelist_sorted))
        #[["wk1_req","wk2_req"],["wk3_req","t1_extra"],["kr_guess_eng","current_week"]]))


def common_message(update, context):
    """General response handler"""
    print(context.user_data,update.message)
    msg = update.message
    user = msg.from_user
    
    if 'quiz' not in context.user_data:
        QUESTIONS.update({q['id']: Question(q['id'], q['eng'], q['kr'],q['category'],q['type']) for q in json.load(open("data/"+msg.text+'.json', encoding='utf-8'))})
        #print(QUESTIONS)
        context.user_data['quiz'] = {}
        context.user_data['quiz']["answers"] = {}
        
        msg.bot.send_message(msg.chat_id,
            text=f'Select quiz type:',
            reply_markup=telegram.ReplyKeyboardMarkup([["random_10","random_20"],["random_50","all"]]))
        
    elif "choice" not in context.user_data['quiz']:
        starttime = datetime.now()
        context.user_data['quiz']['starttime'] = starttime
        choice = msg.text
        context.user_data['quiz']['choice'] = choice
        
        msg.bot.send_message(msg.chat_id,
            text=f'Chosen: {choice}\nstart time: {starttime}',
            reply_markup=telegram.ReplyKeyboardRemove())
        
    else:
        # save response
        context.user_data['quiz']['answers'][context.user_data['quiz']['current_qid']] = msg.text
    
    # check if there's previous question anot
    if len(context.user_data['quiz']['answers'])>0:
        curr_id = context.user_data['quiz']['current_qid']
        #print(QUESTIONS[curr_id].answer,context.user_data['quiz']['answers'][curr_id])
        if QUESTIONS[curr_id].answer==context.user_data['quiz']['answers'][curr_id]:
            msg.bot.send_message(msg.chat_id, text=f'Ans correct! {QUESTIONS[curr_id].text} - {QUESTIONS[curr_id].answer}',
            reply_markup=telegram.ReplyKeyboardRemove())
        else:
            msg.bot.send_message(msg.chat_id, text=f'Ans WRONG! {QUESTIONS[curr_id].text} - {QUESTIONS[curr_id].answer}',
            reply_markup=telegram.ReplyKeyboardRemove())
    
    # ask the question
    questions_left = set(QUESTIONS) - set(context.user_data['quiz']['answers'])
    if context.user_data['quiz']['choice']=="random_10":
        qns_size = 10
    elif context.user_data['quiz']['choice']=="random_20":
        qns_size = 20
    elif context.user_data['quiz']['choice']=="random_50":
        qns_size = 50
    else:
        qns_size = len(set(QUESTIONS))
    
    if len(context.user_data['quiz']['answers']) < qns_size:

        question = QUESTIONS[random.sample(questions_left, 1)[0]]

        msg.bot.send_message(msg.chat_id,
            text=f'{question.text}\n',
            reply_markup=telegram.ReplyKeyboardRemove())
        context.user_data['quiz']['current_qid'] = question.qid

    else:
        msg.bot.send_message(msg.chat_id,
            text="END!",
            reply_markup=telegram.ReplyKeyboardRemove())
        context.user_data.pop('quiz')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(None, common_message))
    #updater.start_polling()
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://arcane-cove-33393.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()