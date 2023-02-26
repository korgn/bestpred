import telebot

TOKEN = '6286901568:AAFzrvo_RZ9sr8VL4rnflrYn_0k1juTvd9o'

admin_id = 1149042468

bot = telebot.TeleBot(TOKEN)

blocked_users = []

def send_to_admin(message):
    user_info = f'{message.from_user.username} [{message.from_user.id}]'
    text = f'{user_info}: {message.text}'
    bot.send_message(admin_id, text)

@bot.message_handler(commands=['ban'])
def handle_ban(message):
    # Перевірка, чи користувач є адміном
    if message.chat.id != admin_id:
        bot.reply_to(message, "Ця команда доступна тільки адміністраторам")
        return
    # Розбиваємо текст команди на частини
    command_parts = message.text.split()
    if len(command_parts) < 2:
        # Якщо не вказано ID користувача для блокування, відправляємо повідомлення про помилку
        bot.reply_to(message, "Ви повинні вказати ID користувача для блокування")
        return
    # Отримуємо ID користувача, якого потрібно заблокувати
    user_id = command_parts[1]
    try:
        # Перевіряємо, чи користувач з таким ID існує
        user = bot.get_chat(user_id)
    except telebot.apihelper.ApiException:
        # Якщо користувача не знайдено, відправляємо повідомлення про помилку
        bot.reply_to(message, f"Користувача з ID {user_id} не знайдено")
        return
    # Додавання користувача до списку
    blocked_users.append(user.id)
    # Відправлення повідомлення про блокування користувачу
    bot.send_message(user_id, "Ви були заблоковані адміністратором")
    # Відправлення повідомлення адміну про блокування користувача
    bot.send_message(admin_id, f"Користувач {user.username} [{user_id}] був заблокований")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Якщо користувач заблокований адміном, то повідомлення не буде оброблено
    if message.chat.id in blocked_users:
        return
    # Відправлення повідомлення адміну
    send_to_admin(message)

bot.polling(none_stop=True) # запускаємо бота в постійному режимі