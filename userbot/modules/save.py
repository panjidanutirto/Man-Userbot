# Copyright (C) 2020 TeamUltroid
# Recode by @mrismanaziz
# @SharingUserbot

from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.save(?: |$)(.*)", disable_errors=True)
async def saf(e):
    x = await e.get_reply_message()
    if not x:
        return await eod(
            e,
            "Balas ke Pesan Apa Saja untuk menyimpannya ke pesan simpanan Anda",
            time=5,
        )
    await bot.send_message("me", x)
    await eod(e, "Message saved at saved messages", time=5)


CMD_HELP.update(
    {
        "save": "**Plugin : **`save`\
        \n\n  •  **Syntax :** `.save` <sambil reply ke pesan>\
        \n  •  **Function : **Untuk Menyimpan pesan ke pesan tersimpan telegram.\
    "
    }
)
