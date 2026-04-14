import os
from pyrogram import Client, filters
from helper.date import add_date
from helper.database import uploadlimit, usertype, addpre
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, ForceReply)

# جلب أيدي الآدمن من المتغيرات البيئية
ADMIN = int(os.environ.get("ADMIN", 923943045))

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["warn"]))
async def warn(c, m):
    if len(m.command) >= 3:
        try:
            user_id = m.text.split(' ', 2)[1]
            reason = m.text.split(' ', 2)[2]
            await c.send_message(chat_id=int(user_id), text=reason)
            await m.reply_text("✅ User Notified Successfully")
        except Exception as e:
            await m.reply_text(f"❌ Error: {e}")
    else:
        await m.reply_text("⚠️ Usage: /warn user_id reason")

@Client.on_message(filters.private & filters.user(ADMIN) & filters.command(["addpremium"]))
async def buypremium(bot, message):
    # التأكد من أن الآدمن كتب الأيدي بعد الأمر
    if len(message.command) < 2:
        return await message.reply_text("⚠️ يرجى كتابة الأيدي بعد الأمر.\nمثال: `/addpremium 12345678`")
    
    user_id = message.command[1]
    
    # نرسل الأزرار ونضع الأيدي داخل الـ callback_data
    await message.reply_text(
        f"Choose Plan for: `{user_id}`",
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("VIP 1 (10GB)", callback_data=f"vip1_{user_id}"),
                InlineKeyboardButton("VIP 2 (50GB)", callback_data=f"vip2_{user_id}")
            ]
        ])
    )

@Client.on_callback_query(filters.regex(r'^vip1_'))
async def vip1(bot, update):
    # استخراج الأيدي من البيانات المخزنة في الزر
    user_id = int(update.data.split("_")[1])
    
    # تنفيذ عمليات قاعدة البيانات (10GB)
    limit = 10 * 1024 * 1024 * 1024  # 10 GB بالبايت
    uploadlimit(user_id, limit)
    usertype(user_id, "VIP1")
    addpre(user_id)
    
    await update.message.edit(f"✅ User {user_id} upgraded to VIP 1 (10GB)")
    try:
        await bot.send_message(user_id, "Hey! Your account has been upgraded to VIP 1.\nCheck your plan: /myplan")
    except:
        pass

@Client.on_callback_query(filters.regex(r'^vip2_'))
async def vip2(bot, update):
    # استخراج الأيدي من البيانات المخزنة في الزر
    user_id = int(update.data.split("_")[1])
    
    # تنفيذ عمليات قاعدة البيانات (50GB)
    limit = 50 * 1024 * 1024 * 1024  # 50 GB بالبايت
    uploadlimit(user_id, limit)
    usertype(user_id, "VIP2")
    addpre(user_id)
    
    await update.message.edit(f"✅ User {user_id} upgraded to VIP 2 (50GB)")
    try:
        await bot.send_message(user_id, "Hey! Your account has been upgraded to VIP 2.\nCheck your plan: /myplan")
    except:
        pass
