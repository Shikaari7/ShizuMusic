import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import Message

from ShizuMusic import bot

# Stores running tagall tasks
TAGALL_STATUS = {}


@bot.on_message(filters.command(["tagall", "all"]))
async def tagall_cmd(_, message: Message):
    chat = message.chat

    if chat.type.name == "PRIVATE":
        return await message.reply_text(
            "❌ This command only works in groups."
        )

    user = message.from_user

    if not user:
        return

    member = await bot.get_chat_member(chat.id, user.id)

    if member.status not in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
    ):
        return await message.reply_text(
            "❌ Only group admins can use this command."
        )

    if TAGALL_STATUS.get(chat.id):
        return await message.reply_text(
            "⚠️ Tag All is already running."
        )

    TAGALL_STATUS[chat.id] = True

    try:
        reason = " ".join(message.command[1:])

        if reason:
            header = (
                f"<b>📢 TAG ALL</b>\n\n"
                f"<b>Message:</b> {reason}\n\n"
            )
        else:
            header = "<b>📢 TAG ALL</b>\n\n"

        members = []

        async for member in bot.get_chat_members(chat.id):
            if member.user.is_bot:
                continue

            members.append(member.user)

        sent = 0
        text = header

        for user in members:

            if not TAGALL_STATUS.get(chat.id):
                await message.reply_text("🛑 Tag All cancelled.")
                return

            mention = (
                f'<a href="tg://user?id={user.id}">'
                f'{user.first_name}</a>'
            )

            text += f"{mention} "

            sent += 1

            if sent % 5 == 0:
                try:
                    await bot.send_message(
                        chat.id,
                        text,
                        parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True,
                    )
                except Exception:
                    pass

                text = header
                await asyncio.sleep(2)

        if text != header:
            try:
                await bot.send_message(
                    chat.id,
                    text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception:
                pass

        await message.reply_text(
            f"✅ Successfully tagged {len(members)} members."
        )

    finally:
        TAGALL_STATUS.pop(chat.id, None)


@bot.on_message(filters.command(["canceltag", "stoptag"]))
async def cancel_tagall(_, message: Message):

    chat = message.chat

    if chat.type.name == "PRIVATE":
        return

    user = message.from_user

    if not user:
        return

    member = await bot.get_chat_member(chat.id, user.id)

    if member.status not in (
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
    ):
        return await message.reply_text(
            "❌ Only group admins can cancel Tag All."
        )

    if not TAGALL_STATUS.get(chat.id):
        return await message.reply_text(
            "⚠️ No Tag All is running."
        )

    TAGALL_STATUS.pop(chat.id, None)

    await message.reply_text(
        "🛑 Tag All has been cancelled."
    )
