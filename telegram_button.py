import telebot

bot_api = "7092626455:AAFz5FkyHIu3dYzYIFwBswaS6kydL4afb8Q"
chat_id = "-4017828034" 
image_path = "detected_faces\\detected_face_20240226-120705.jpg"

bot = telebot.TeleBot(bot_api)

# Create keyboard 
keyboard = telebot.types.InlineKeyboardMarkup()
button_Approve = telebot.types.InlineKeyboardButton(text='Approve', callback_data='Approve')
button_Decline = telebot.types.InlineKeyboardButton(text='Decline', callback_data='Decline') 
keyboard.add(button_Approve, button_Decline)

# Send image
photo = open(image_path, 'rb')  
bot.send_photo(chat_id, photo, reply_markup=keyboard)

# Callback handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Approve':
        bot.send_message(chat_id, "You've approved the entry ✅")
        print("User selected Approve ✅") 
    elif call.data == 'Decline':
        bot.send_message(chat_id, "Entry declined ❌")
        print("User selected Decline ❌")
    
    # Remove keyboard
    bot.edit_message_reply_markup(chat_id, call.message.message_id) 

bot.polling()