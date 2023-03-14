import telebot

TOKEN = '6286901568:AAFzrvo_RZ9sr8VL4rnflrYn_0k1juTvd9o'
admin_id = [1380896061, 699916411, 1149042468]

bot = telebot.TeleBot(TOKEN)

blocked_users = []

def send_to_admin(message):
    user_info = f'{message.from_user.first_name} (@{message.from_user.username} [{message.from_user.id}]):'
    text = f'{user_info} {message.text}'
    bot.send_message(admin_id, text)

@bot.message_handler(commands=['ban'])
def handle_ban(message):
    # Check if the user is the admin
  if message.chat.id == admin_id[0] or admin_id[1] or admin_id[2]:

    # Split the command text into parts
    command_parts = message.text.split()

    if len(command_parts) < 2:
        # If no user ID is specified for blocking, send an error message
        bot.reply_to(message, "Укажи ID після команди ban ніби заблокувати.")
        return

    # Get the user ID to be blocked
    user_id = command_parts[1]

    try:
        # Check if the user with the given ID exists
        user = bot.get_chat(user_id)
    except telebot.apihelper.ApiException:
        # If the user is not found, send an error message
        bot.reply_to(message, f"Людину з подібним ID {user_id} не знайдено.")
        return

    # Add the user to the blocked users list
    blocked_users.append(user.id)

    # Send a message to the user about the block
    bot.send_message(user_id, "Ви були заблоковані у цьому боті.")

    # Send a message to the admin about the block
    user_info = f'{user.first_name} (@{user.username} [{user.id}]):'
    bot.send_message(admin_id, f"{user_info} заблокован.")
  else:
    bot.reply_to(message, "Цю команду може виконати лише адміністратор бота.")
    return

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # If the message is from the admin, don't process it
    if message.chat.id in admin_id:
        return

    # If the user is blocked, don't process the message
    if message.chat.id in blocked_users:
        return
    
    user_info = f'{message.from_user.first_name} (@{message.from_user.username} [{message.from_user.id}]):'

    bot.send_message(admin_id[0], f'{user_info}')
    bot.forward_message(admin_id[0], message.chat.id, message.message_id)
    
    bot.send_message(admin_id[1], f'{user_info}')
    bot.forward_message(admin_id[1], message.chat.id, message.message_id)
    
    bot.send_message(admin_id[2], f'{user_info}')
    bot.forward_message(admin_id[2], message.chat.id, message.message_id)

bot.polling(none_stop=True)

