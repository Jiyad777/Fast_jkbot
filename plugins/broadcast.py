from pyrogram import Client, filters
import datetime, asyncio, time
from database.users_chats_db import db
from info import ADMINS

lock = asyncio.Lock()
        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast(bot, message):
    if lock.locked():
        await message.reply_message("already old broadcast is pending")
    all_users = await db.get_all_users()
    total_users = await db.total_users_count()
    b_msg = message.reply_to_message
    sts = await message.reply_text('Broadcasting your messages...')
    done = 0
    blocked = 0
    deleted = 0
    failed =0
    success = 0
    start_time = time.time()
    async with lock:
        async for i in users:
            user = i['id']
            try:
                await b_msg.copy(chat_id=int(user))
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await b_msg.copy(chat_id=int(user))
                success += 1
            except InputUserDeactivated:
                await db.delete_user(int(user))
                deleted += 1
            except UserIsBlocked:
                blocked += 1
            except PeerIdInvalid:
                await db.delete_user(int(int(user)))
                failed += 1
            except Exception as e:
                failed += 1
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await message.reply_text(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")




