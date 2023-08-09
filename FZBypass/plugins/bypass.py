from FZBypass import Config, Bypass
from pyrogram.filters import command, private, user, text
from FZBypass.core.bypass_checker import direct_link_checker
from FZBypass.core.bot_utils import chat_and_topics
from FZBypass.core.exceptions import DDLException

@Bypass.on_message(command(['start']) & ~private)
async def start_msg(client, message):
    await message.reply('<b>FZ Bypass Bot! Up & Running!</b>')
    
@Bypass.on_message(command(['bypass', 'bp']) & text & chat_and_topics)
async def bypass_check(client, message):
    uid = message.from_user.id
    arg = message.text.split('\n')[0].split()
    if (reply_to := message.reply_to_message) and reply_to.text is not None:
        link = reply_to.text
    elif len(arg) > 1:
        link = arg[1]
    else:
        return await message.reply('<i>No Link Provided!</i>')
    try:
        parse_data = await direct_link_checker(link)
    except DDLException as error:
        return await message.reply(f"<b>{error}</b>")
    except Exception as e:
        return await message.reply(str(e))

    if parse_data:
        await message.reply(parse_data)
        

@Bypass.on_message(command(['log']) & user(Config.OWNER_ID))
async def send_logs(client, message):
    await message.reply_document('log.txt')
