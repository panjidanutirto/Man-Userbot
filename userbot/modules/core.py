import os
from pathlib import Path

from userbot.events import register
from userbot.utils import load_module

DELETE_TIMEOUT = 5


@register(outgoing=True, pattern=r"^\.install$")
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            await event.edit("`Installing Modules...`")
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "userbot/modules/",  # pylint:disable=E0602
                )
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit(
                    "Berhasil Menginstall Plugin `{}`".format(
                        os.path.basename(downloaded_file_name)
                    )
                )
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! Plugin ini sebelumnya sudah terinstall...")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)


@register(outgoing=True, pattern=r"^\.send (?P<shortname>\w+)$")
async def send(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    input_str = event.pattern_match["shortname"]
    the_plugin_file = "./userbot/modules/{}.py".format(input_str)
    start = datetime.now()
    await event.client.send_file(  # pylint:disable=E0602
        event.chat_id,
        the_plugin_file,
        force_document=True,
        allow_cache=False,
        reply_to=message_id,
    )
    end = datetime.now()
    time_taken_in_ms = (end - start).seconds
    await event.edit("Diupload {} di {} detik".format(input_str, time_taken_in_ms))
