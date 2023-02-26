import telebot

TOKEN = '6286901568:AAFzrvo_RZ9sr8VL4rnflrYn_0k1juTvd9o'

admin_id = 1149042468

bot = telebot.TeleBot(TOKEN)

blocked_users = []

def send_to_admin(message):
    user_info = f'{message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username} [{message.from_user.id}]):'
    text = f'{user_info} {message.text}'
    bot.send_message(admin_id, text)

@bot.message_handler(commands=['ban'])
def handle_ban(message):
    # Check if the user is the admin
    if message.chat.id != admin_id:
        bot.reply_to(message, "This command is only available to administrators")
        return

    # Split the command text into parts
    command_parts = message.text.split()

    if len(command_parts) < 2:
        # If no user ID is specified for blocking, send an error message
        bot.reply_to(message, "You must specify a user ID to block")
        return

    # Get the user ID to be blocked
    user_id = command_parts[1]

    try:
        # Check if the user with the given ID exists
        user = bot.get_chat(user_id)
    except telebot.apihelper.ApiException:
        # If the user is not found, send an error message
        bot.reply_to(message, f"User with ID {user_id} not found")
        return

    # Add the user to the blocked users list
    blocked_users.append(user.id)

    # Send a message to the user about the block
    bot.send_message(user_id, "You have been blocked by the administrator")

    # Send a message to the admin about the block
    user_info = f'{user.first_name} {user.last_name} (@{user.username} [{user.id}]):'
    bot.send_message(admin_id, f"{user_info} has been blocked")

@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_message(message):
    # If the message is from the admin, don't process it
    if message.chat.id == admin_id:
        return

    # If the user is blocked, don't process the message
    if message.chat.id in blocked_users:
        return

    # Send a message to the admin
    user_info = f'{message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username} [{message.from_user.id}]):'
    text = f'{user_info} {message.text}'
    bot.send_message(admin_id, text)

@bot.message_handler(content_types=['text', 'photo', 'video'])
def handle_message(message):
    # If the message is from the admin, don't process it
    if message.chat.id == admin_id:
        return

    # If the user is blocked, don't process the message
    if message.chat.id in blocked_users:
        return

    # Build the user info string
    user_info = f'{message.from_user.first_name} {message.from_user.last_name} (@{message.from_user.username} [{message.from_user.id}]):'

    # If the message contains an image or video, send a message with the user info and media file
    if message.content_type in ['photo', 'video']:
        text = user_info + f'\n{message.caption}' if message.caption else user_info
        if message.content_type == 'photo':
            bot.send_photo(admin_id, message.photo[-1].file_id, caption=text)
        elif message.content_type == 'video':
            bot.send_video(admin_id, message.video.file_id, caption=text)
    else:
        # If the message only contains text, send a message with the user info and text
        text = user_info + f'\n{message.text}'
        bot.send_message(admin_id, text)


bot.polling(none_stop=True)
