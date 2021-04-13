# Recode by @mrismanaziz
# @SharingUserbot

import os
import asyncio
import PIL
import cv2
import time
import random
import re
from userbot.utils import progress
from userbot.events import register
from userbot import CMD_HELP, bot


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)


@register(outgoing=True, pattern=r"^\.rst(?: |$)(.*)")
async def rastick(animu):
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`No text given, hence no stickers...`")
            return
    animus = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    try:
        await sticcers[0].click(
            animu.chat_id,
            reply_to=animu.reply_to_msg_id,
            silent=True if animu.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await animu.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )
    await animu.delete()


@register(outgoing=True, pattern=r"^\.honka(?: |$)(.*)")
async def frg(animu):
    text = animu.pattern_match.group(1)
    if not text:
        await animumedit("`Silahkan Masukan Kata!`")
    else:
        sticcers = await bot.inline_query("honka_says_bot", f"{text}."
                                          )
    try:
        await sticcers[0].click(
            animu.chat_id,
            reply_to=animu.reply_to_msg_id,
            silent=True if animu.is_reply else False,
            hide_via=True,
        )
    except Exception:
        return await animu.edit(
            "`You cannot send inline results in this chat (caused by SendInlineBotResultRequest)`"
        )
    await animu.delete()


@register(outgoing=True, pattern=r"^\.rgif(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    reply = await event.get_reply_message()
    await event.edit("`Checking...`")
    download = await bot.download_media(reply.media)
    img = cv2.VideoCapture(download)
    ret, frame = img.read()
    cv2.imwrite("danish.png", frame)
    danish = PIL.Image.open("danish.png")
    dark, python = danish.size
    cobra = f"""ffmpeg -f lavfi -i color=c=00ff00:s={dark}x{python}:d=10 -loop 1 -i danish.png -filter_complex "[1]rotate=angle=PI*t:fillcolor=none:ow='hypot(iw,ih)':oh=ow[fg];[0][fg]overlay=x=(W-w)/2:y=(H-h)/2:shortest=1:format=auto,format=yuv420p" -movflags +faststart danish.mp4 -y"""
    await event.edit("```Processing ...```")
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    process = await asyncio.create_subprocess_shell(
        cobra, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    await event.edit("```Uploading...```")
    c_time = time.time()
    await event.client.send_file(event.chat_id, "danish.mp4", force_document=False, reply_to=event.reply_to_msg_id, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
        progress(d, t, event, c_time, "[UPLOAD]")
    ),)
    await event.delete()
    os.system("rm -f downloads/*.jpg")
    os.system("rm -f downloads/*.png")
    os.system("rm -f downloads/*.webp")
    os.system("rm -f *.jpg")
    os.system("rm -f *.png")
    os.remove("danish.mp4")


CMD_HELP.update(
    {
        "rgif": "**Plugin : **`rgif`\
        \n\n  •  **Syntax :** `.gif` <sambil reply ke media>\
        \n  •  **Function : **Untuk mengubah gambar jadi gif memutar.\
    "
    }
)


CMD_HELP.update(
    {
        "fun": "**Plugin : **`fun`\
        \n\n  •  **Syntax :** `.rst` <text>\
        \n  •  **Function : **Untuk membuat stiker teks dengan templat stiker acak.\
        \n\n  •  **Syntax :** `.honka` <text>\
        \n  •  **Function : **Untuk membuat stiker teks dengan templat stiker Honka bot.\
    "
    }
)
