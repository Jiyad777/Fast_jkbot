from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest
from pyrogram import Client, enums, filters
from pyrogram.errors import UserNotParticipant
from info import FSUB_TEXT, AUTH_CHANNEL, ADMINS, REQ_LINK
from database.fsub_db import Fsub_DB

LINK = None

@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL))
async def filter_join_reqs(bot, message: ChatJoinRequest):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    date = message.date
    await Fsub_DB().add_user(user_id=str(user_id), username=username, first_name=first_name, date=date)

@Client.on_message(filters.command("total_requests") & filters.private & filters.user(ADMINS))
async def get_all_reqs(bot, message):
    total = await Fsub_DB().total_users()
    return await message.reply_text(f"<b>Total Requests: {total}</b>")

@Client.on_message(filters.command("delete_requests") & filters.private & filters.user(ADMINS))
async def delete_all_reqs(bot, message):
    total = await Fsub_DB().total_users()
    await Fsub_DB().purge_users()
    return await message.reply_text(f"<b>Successfully deleted all {total} requests...</b>")

async def Force_Sub(bot: Client, message: Message, file_id = False, mode = "checksub"):
    if not AUTH_CHANNEL: return True
    
    if not REQ_LINK or REQ_LINK == "":
        global LINK
        try:
            if LINK == None:
                ln = await bot.create_chat_invite_link(chat_id=AUTH_CHANNEL, creates_join_request=True)
                LINK = ln.invite_link
                link = ln.invite_link
                print("Created Invite Link !")
            else:
                link = LINK
            
        except Exception as e:
            print(f"Unable to create Invite link !\n\nError: {e}")
            return False
    else:
        link = REQ_LINK
    try:
        user = await Fsub_DB().get_user(str(message.from_user.id))
        if user and str(user["id"]) == str(message.from_user.id):
            return True
    except Exception as e:
        print(f"Error: {e}")
        await message.reply(text=f"Error: {e}", parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True)
        return False
    try:
        await bot.get_chat_member(chat_id=AUTH_CHANNEL, user_id=message.from_user.id)
        return True
    except UserNotParticipant:
        btn = [[InlineKeyboardButton("❆ Jᴏɪɴ Oᴜʀ Bᴀᴄᴋ-Uᴘ Cʜᴀɴɴᴇʟ ❆", url=link)]]
        if file_id != False: btn.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", callback_data=f"{mode}#{file_id}")])
        else: pass       
        await message.reply(text=FSUB_TEXT, reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.MARKDOWN)
        return False
