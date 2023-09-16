TOKEN="6507116889:AAHN26jCzNfPVREu_lU6JYHT9LXqV6cxZOQ"

from telegram import(
    Update
)
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, CommandHandler,CallbackContext
from telegram import KeyboardButton, ReplyKeyboardMarkup
from likedb import DB

db = DB('db.json')
def start(update:Update,context:CallbackContext):
    bot=context.bot
    chat_id=update.message.chat.id
    user = update.effective_user
    
    ans = db.search(chat_id)
    print(ans)
    if ans==False:
        text=f"Salom {user.first_name}! Botga xush kelibsiz!"
    else:
        text=f"Salom {user.first_name}! Botga qaytganingizdan xo'rsanman!"
    db.add_user(chat_id)
    MAIN_KEYBOARD=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Like"),
            KeyboardButton(text="Dislike")
        ]],resize_keyboard=True)
    bot.send_message(chat_id,text,reply_markup=MAIN_KEYBOARD)
updater=Updater(TOKEN)

def addlikes(update:Update,context:CallbackContext):
    bot=context.bot
    chat_id=update.message.chat.id
    message=update.message
    data=db.get_likes()
    print(message)
    if message.text=="Like":
        like=db.add_like(chat_id)
        print(like)
    elif message.text=="Dislike":
        dislike=db.add_dislike(chat_id)
    like=data[str(chat_id)]["like"]
    dislike=data[str(chat_id)]["dislike"] 
    text=f"LIKE: {like}\nDISLIKE: {dislike}"
    bot.send_message(chat_id,text)

dp=updater.dispatcher
dp.add_handler(CommandHandler("start",start))
dp.add_handler(MessageHandler(Filters.text,addlikes))

updater.start_polling()
updater.idle()