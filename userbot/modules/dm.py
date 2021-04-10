# Copyright (C) 2020 TeamUltroid
# Recode by @mrismanaziz
# @SharingUserbot

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.dm ?(.*)", disable_errors=True)
async def dm(e):
    d = e.pattern_match.group(1)
    c = d.split(" ")
    try:
        chat_id = await get_user_id(c[0])
    except Exception as ex:
        return await eod(e, "`" + str(ex) + "`", time=5)
    msg = ""
    masg = await e.get_reply_message()
    if e.reply_to_msg_id:
        await bot.send_message(chat_id, masg)
        await eod(e, "`⚜️Pesan Terkirim!`", time=4)
    for i in c[1:]:
        msg += i + " "
    if msg == "":
        return
    try:
        await bot.send_message(chat_id, msg)
        await eod(e, "`⚜️Pesan Terkirim!⚜️`", time=4)
    except BaseException:
        await eod(
            e,
            "`.help dm`",
            time=4,
        )


CMD_HELP.update(
    {
        "dm": "**Plugin : **`dm`\
        \n\n  •  **Syntax :** `.dm` <username/id> <reply/type>\
        \n  •  **Function : **Untuk Mengirim Pesan Langsung ke Pengguna.\
    "
    }
)
