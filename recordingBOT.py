import telebot
import json
import threading
import numpy as np
from utils.keep_alive import keep_alive
from utils.buttons_utils import STUDY_SEMESTER_BUTTONS, LECTURES_TRAINS_BUTTONS, FIRST_SEMESTER_BUTTONS, \
    SECOND_SEMESTER_BUTTONS, THIRD_SEMESTER_BUTTONS, FORTH_SEMESTER_BUTTONS, FIFTH_SEMESTER_BUTTONS, \
    SIXTH_SEMESTER_BUTTONS, OPTINAL_SEMESTER_BUTTONS

keep_alive()
bot = telebot.TeleBot("INERT-TOKEN-HERE")

try:
    with open('utils/session_to_messages.json', 'r') as fh:
        session_to_messages = json.load(fh, parse_int=int)

    with open('utils/authorized_usrs.json', 'r') as fh:
        authorized_usrs = json.load(fh)
        print(authorized_usrs)
      
except:
    session_to_messages = {}

InlineKeyboardButton = telebot.types.InlineKeyboardButton


# Given user chat ID check if user authorized to use the bot
def verify_usr(usr_chat_id):
    if not str(usr_chat_id) in authorized_usrs:
        return 0

    # if exists, send pre-made message.
    return authorized_usrs[str(usr_chat_id)]


# check whether current session exists in list, if not create a new entity.
# session is used to store all messages sent from / to user to delete them on each stage.
def session_exists(chat_id):
    if str(chat_id) not in session_to_messages:
        session_to_messages[str(chat_id)] = []
    clear_chat(chat_id)


# clear chat with given chat_id user.
def clear_chat(chat_id):
    message_cache = session_to_messages[str(chat_id)]
    for msg in message_cache:
        try:
            bot.delete_message(chat_id=chat_id, message_id=msg)
        except:
            pass

    message_cache.clear()


# add message to cache of current user ID.
def add_message_cache(message, chat_id=0):
    if not type(message) == int:
        chat_id = message.chat.id
        message = message.message_id
    message_cache = session_to_messages[str(chat_id)]
    message_cache.append(message)


# start command.
@bot.message_handler(commands=['start'])
def greet_msg(msg):

    # user verification.
    session_exists(msg.chat.id)
    chat_id = msg.chat.id
    usr_message = verify_usr(chat_id)
    if usr_message == 0:
        bot.send_message(chat_id, "Sorry I cannot speak to strangers.  🤭🤫")
        return
    # user verification

    add_message_cache(msg)
    add_message_cache(bot.send_message(chat_id, f'{usr_message}, Im here to serve you'))
    main_menu(msg)
    

# main menu - after verification a list of available semesters will be printed.
def main_menu(msg):
    # user verification
    chat_id = msg.chat.id
    if verify_usr(chat_id) == 0:
        bot.send_message(chat_id, "Sorry I cannot speak to strangers.  🤭🤫")
        return
    # user verification

    # add inline keyboard buttons with list of given semesters.
    keys = [[InlineKeyboardButton(text=button_text, callback_data=f'menu:{button_id}') for button_id, button_text in
             STUDY_SEMESTER_BUTTONS.items()]]
    keys = np.array_split(keys[0], 4)
  
    reply_markup = telebot.types.InlineKeyboardMarkup(keys, row_width=2)

    add_message_cache(bot.send_message(chat_id, "Pick desired semester", reply_markup=reply_markup))


# the next handler will be triggered if a callback text starts with menu, indicates a subject needs to be selected now.
@bot.callback_query_handler(func=lambda c: c.data.startswith('menu:'))
def course_selection(call):
    chat_id = call.message.chat.id
    clear_chat(chat_id)
    # button_id - selected semester.
    button_id = call.data.split(':')[1]

    # user verification.
    if verify_usr(chat_id) == 0:
        bot.send_message(chat_id, "Sorry I cannot speak to strangers.  🤭🤫")
        return
    # user verification
      
    semester_menu_ref = [FIRST_SEMESTER_BUTTONS, SECOND_SEMESTER_BUTTONS, THIRD_SEMESTER_BUTTONS, FORTH_SEMESTER_BUTTONS,
                        FIFTH_SEMESTER_BUTTONS, SIXTH_SEMESTER_BUTTONS, OPTINAL_SEMESTER_BUTTONS]

    # inline keyboard keys initialization
    keys = [[InlineKeyboardButton(text=button_text, callback_data=f'course_selection:{button_id}') for
             button_id, button_text in semester_menu_ref[int(button_id)].items()]]
    # split array for better preview in telegram.
    keys = np.array_split(keys[0], 2)
  
    reply_markup = telebot.types.InlineKeyboardMarkup(keys)
    add_message_cache(bot.send_message(chat_id, "Choose desired subject:", reply_markup=reply_markup))


# the next handler will be triggered if a callback text starts with course_selection,
# indicates the user should select whether he wants exercises or lecturer's recordings.
@bot.callback_query_handler(func=lambda c: c.data.startswith('course_selection:'))
def lectures_exercise_selection(call):
    chat_id = call.message.chat.id
    clear_chat(chat_id)
    subject_id = call.data.split(':')[1]

    # user verification
    if verify_usr(chat_id) == 0:
        bot.send_message(chat_id, "Sorry I cannot speak to strangers.  🤭🤫")
        return
    # user verification

    keys = [[InlineKeyboardButton(text=button_text, callback_data=f'lectures_exercise:{subject_id}_{button_id}') for
             button_id, button_text in LECTURES_TRAINS_BUTTONS.items()]]

    reply_markup = telebot.types.InlineKeyboardMarkup(keys)
    add_message_cache(bot.send_message(chat_id, "Choose recording type:", reply_markup=reply_markup))


# the next handler will be triggered if a callback text starts with lectures_exercise,
# the bot will now copy (forward could also be used here) all messages from pre-maid groups into the chat.
#
# Logic: the logic is pretty easy, each course has it's own ID assigned in buttons_utils.py.
#        furthermore, lectures assinged to be 1, and exercises 2.
#        a pre-maid group with all the recordings will be made before hand with "YOUR_GROUP_IDENTIFIER_SUBJECTID_1/2"
#        for example, subject = Linear algebra, SUBJECT_ID = 'LA', let's assume the user requested lecturers so 1
#        finally we get "@YOUR_GROUP_IDENTIFIER_LA_1" - that should be channel's name.
@bot.callback_query_handler(func=lambda c: c.data.startswith('lectures_exercise:'))
def forward_recordings(call):
    chat_id = call.message.chat.id
    clear_chat(chat_id)
    desired_recording_index = call.data.split(':')[1]
  
    if verify_usr(chat_id) == 0:
        bot.send_message(chat_id, "Sorry I cannot speak to strangers.  🤭🤫")
        return
      
    print(desired_recording_index)

    # copy all messages from group/channel into current chat.
    # TODO - find a way to list all messages in channel.
    for message_id in range(2, 20):
        try:
            add_message_cache(bot.copy_message(chat_id=chat_id,
                                               from_chat_id=f'@YOUR_GROUP_IDENTIFIER{desired_recording_index}',
                                               message_id=message_id).message_id, chat_id)
        except:
            pass

    keys = [[InlineKeyboardButton(text="Back", callback_data='start')]]
    reply_markup = telebot.types.InlineKeyboardMarkup(keys)
    add_message_cache(bot.send_message(chat_id, 'Thank you for using me!', reply_markup=reply_markup))


# the next handler will be used if return button was clicked.
@bot.callback_query_handler(func=lambda c: c.data == 'start')
def return_button(call):
    clear_chat(call.message.chat.id)
    main_menu(call.message)


# updates the json file with the current DB in-case the bot goes offline, saves progress to file.
def update_session_db():
    threading.Timer(1.0, update_session_db).start()
    with open('utils/session_to_messages.json', 'w') as fh:
        json.dump(session_to_messages, fh)


update_session_db()
bot.polling()
