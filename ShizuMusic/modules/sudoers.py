from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

import config
from ShizuMusic import bot
from ShizuMusic.utils.db import (
    add_sudo,
    remove_sudo,
    is_sudo,
    get_sudo_users,
)


def sudo_filter(_, __, message):
    if not message.from_user:
        return False

    if message.from_user.id == config.OWNER_ID:
        return True

    return is_sudo(message.from_user.id)


sudo = filters.create(sudo_filter)


@bot.on_message(filters.command("addsudo") & filters.user(config.OWNER_ID))
async def addsudo(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await bot.get_users(int(message.command[1]))
    else:
        return await message.reply_text(
            "Reply to a user or give a user ID."
        )

    if user.id == config.OWNER_ID:
        return await message.reply_text("Owner is already supreme.")

    if is_sudo(user.id):
        return await message.reply_text("User is already sudo.")

    add_sudo(user.id)

    await message.reply_text(
        f"✅ Added <b>{user.mention}</b> as Sudo User.",
        parse_mode=ParseMode.HTML,
    )


@bot.on_message(filters.command("delsudo") & filters.user(config.OWNER_ID))
async def delsudo(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) > 1:
        user = await bot.get_users(int(message.command[1]))
    else:
        return await message.reply_text(
            "Reply to a user or give a user ID."
        )

    if not is_sudo(user.id):
        return await message.reply_text("User is not sudo.")

    remove_sudo(user.id)

    await message.reply_text(
        f"✅ Removed <b>{user.mention}</b> from Sudo Users.",
        parse_mode=ParseMode.HTML,
    )


@bot.on_message(filters.command(["sudolist", "listsudo"]))
async def sudolist(_, message: Message):
    ids = get_sudo_users()

    text = "<b>🛡 Sudo Users</b>\n\n"

    if not ids:
        text += "No sudo users."
    else:
        for uid in ids:
            try:
                user = await bot.get_users(uid)
                text += f"• {user.mention} (<code>{uid}</code>)\n"
            except Exception:
                text += f"• <code>{uid}</code>\n"

    await message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
    )


@bot.on_message(filters.command("issudo"))
async def issudo_cmd(_, message: Message):
    uid = message.from_user.id

    if uid == config.OWNER_ID:
        return await message.reply_text("👑 You are the Owner.")

    if is_sudo(uid):
        return await message.reply_text("✅ You are a Sudo User.")

    await message.reply_text("❌ You are not a Sudo User.")
