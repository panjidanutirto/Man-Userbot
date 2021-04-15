# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing commands for keeping global notes. """

from sqlalchemy.orm.exc import UnmappedInstanceError

from userbot import BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"\$\w*", ignore_unsafe=True, disable_errors=True)
async def on_snip(event):
    """ custom logic. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip.f_mesg_id:
        msg_o = await event.client.get_messages(
            entity=BOTLOG_CHATID, ids=int(snip.f_mesg_id)
        )
        await event.client.send_message(
            event.chat_id, msg_o.message, reply_to=message_id_to_reply, file=msg_o.media
        )
    elif snip and snip.reply:
        await event.client.send_message(
            event.chat_id, snip.reply, reply_to=message_id_to_reply
        )


@register(outgoing=True, pattern=r"^\.custom (\w*)")
async def on_snip_save(event):
    """ For .snip command, saves custom for future use. """
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#COSTUM\n**KEYWORD:** {keyword}"
                "\n\nPesan berikut disimpan sebagai data, tolong JANGAN dihapus !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID, messages=msg, from_peer=event.chat_id, silent=True
            )
            msg_id = msg_o.id
        else:
            return await event.edit(
                "`Untuk menyimpan command costum dengan media, BOTLOG_CHATID harus disetel.`"
            )
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Command Berhasil {}. Gunakan` `${}` `untuk menggunakannya`"
    try:
        if add_snip(keyword, string, msg_id) is False:
            await event.edit(success.format("diupdate", keyword))
        else:
            await event.edit(success.format("disimpan", keyword))
    except UnmappedInstanceError:
        return await event.edit(f"`Command` `{keyword}` `sudah ada.`")


@register(outgoing=True, pattern=r"^\.listcustom$")
async def on_snip_list(event):
    """ For .custom command, lists custom saved by you. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")

    message = "`Tidak ada Command Custom yang disimpan.`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`Tidak ada Command Custom yang disimpan.`":
            message = "**✥ Daftar Command Yang di Costum :**\n"
            message += f"✣ `${a_snip.snip}`\n"
        else:
            message += f"✣ `${a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern=r"^\.delcustom (\w*)")
async def on_snip_delete(event):
    """ For .delcustom command, deletes a custom command. """
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        return await event.edit("`Running on Non-SQL mode!`")
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`Berhasil Menghapus Command Custom :` **{name}**")
    else:
        await event.edit(f"`Tidak dapat menemukan custom :` **{name}**")


CMD_HELP.update(
    {
        "custom": "**Plugin : **`custom`\
        \n\n  •  **Syntax :** `.custom` <nama> <data> atau membalas pesan dengan .custom <nama>\
        \n  •  **Function : **Menyimpan pesan custom sebagai (catatan global). (bisa dengan gambar, docs, dan stickers!)\
        \n\n  •  **Syntax :** `.listcustom`\
        \n  •  **Function : **Mendapat semua command custom yang disimpan.\
        \n\n  •  **Syntax :** `.delcustom` <nama_custom>\
        \n  •  **Function : **Menghapus command custom yang ditentukan.\
        \n\n  •  **NOTE : Untuk Menggunakan Command Custom Menggunakan awalan $**\
    "
    }
)
