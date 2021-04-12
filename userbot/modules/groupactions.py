from asyncio import sleep

from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChannelParticipantsKicked,
    ChatBannedRights,
)

from userbot import CMD_HELP

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


@register(outgoing=True, pattern=r"^\.kickall ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await edit_or_reply(event, "`I don't think this is a group.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(
            event, "`You are not admin of this chat to perform this action`"
        )
        return
    result = await event.client(
        functions.channels.GetParticipantRequest(
            channel=event.chat_id, user_id=event.client.uid
        )
    )
    if not result.participant.admin_rights.ban_users:
        return await edit_or_reply(
            event, "`It seems like you dont have ban users permission in this group.`"
        )
    catevent = await edit_or_reply(event, "`Kicking...`")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client.kick_participant(event.chat_id, user.id)
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await catevent.edit(
        f"`Sucessfully i have completed kickall process with {success} members kicked out of {total} members`"
    )


@register(outgoing=True, pattern=r"^\.banall ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_group:
        await edit_or_reply(event, "`I don't think this is a group.`")
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(
            event, "`You are not admin of this chat to perform this action`"
        )
        return
    result = await event.client(
        functions.channels.GetParticipantRequest(
            channel=event.chat_id, user_id=event.client.uid
        )
    )
    if not result:
        return await edit_or_reply(
            event, "`It seems like you dont have ban users permission in this group.`"
        )
    catevent = await edit_or_reply(event, "`banning...`")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await catevent.edit(
        f"`Sucessfully i have completed banall process with {success} members banned out of {total} members`"
    )


@register(outgoing=True, pattern=r"^\.unbanall ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        LOGS.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            return False
        et = await edit_or_reply(event, "Searching Participant Lists.")
        p = 0
        async for i in event.client.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            rights = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await event.client(
                    functions.channels.EditBannedRequest(event.chat_id, i, rights)
                )
            except Exception as ex:
                await et.edit(str(ex))
            else:
                p += 1
        await et.edit("{}: {} unbanned".format(event.chat_id, p))


CMD_HELP.update(
    {
        "kangban": "**Plugin : **`kangban`\
        \n\n  •  **Syntax :** `.banall`\
        \n  •  **Function : **To ban all users except admins from the chat.\
    "
    }
)
