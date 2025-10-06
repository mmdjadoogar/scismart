
# import requests
from decouple import config
from telegram import Update
from telegram.ext import MessageHandler, Application, CommandHandler, filters, ContextTypes
from telegram import KeyboardButton, ReplyKeyboardMarkup  #, ReplyKeyboardRemove
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# import os.path
from google import genai
from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# import httpx
from telegram.ext import ConversationHandler
import re
from openai import OpenAI
import time



#  بیلبیلک های گوگل شیت:
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] #این آدرس شیته
SERVICE_ACCOUNT_FILE = 'sheets.json'#مسیر فایل سرویس اکانت شیت
credentials = None  # اول یه دست پاک میکنیم
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)         #  حالا اعتبارسنجی رو میسازیم
SAMPLE_SPREADSHEET_ID = config('SAMPLE_SPREADSHEET_ID')   #  شناسه ی شیتی که باهاش کار میکنیم
service = build("sheets", "v4", credentials=credentials)
sheet = service.spreadsheets()  #  اینم شیته که باهاش کار میکنیم

# # خواندن داده های شیت
# result = (
#         sheet.values()
#         .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A1")
#         .execute()
#     )

# values = result.get("values", [])  # اینجا سر و ته اضافی دیتارو میزنیم و یه لیست تر و تمیز ازش میسازیم


# بیلبیلک های جمنای
# GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
GEMINI_API_KEY = config('GEMINI_API_KEY')
# SYSTEM_PROMPT = "تو یک ربات تلگرامی به اسم غلامرضا هستی. دوستانه و مودب و خودمونی به زبان فارسی صحبت کن"
# SYSTEM_PROMPT_PERMANENT = "تو یک متخصص در حوزه ی علوم زیستی هستی و به سوالات در این زمینه پاسخ میدهی."
client = genai.Client(api_key=GEMINI_API_KEY)

LIARA_base_url = "https://ai.liara.ir/api/v1/68ce6cd35840ebce0ce602f5"

TOKEN = config('token')
BOT_USERNAME = '@SciSmartbot' # نام کاربری ربات
ADMIN_ID = [602439009, 493060465, 7524316121] # mmd(programer), sajad, dooste sajad

users_cupon = {}

# دکمه ها
main_menu = [
    [KeyboardButton("دوره جامع scismart🧬"), KeyboardButton("پروفایل کاربری👤")],
    [KeyboardButton("🎰 قرعه‌کشی، هدایا و جوایز  🥇"), KeyboardButton("مسابقه🏆")],
    [KeyboardButton("❤️ حامیان مالی و معنوی 💵"), KeyboardButton("پژوهشگاه رویان🎓")],
    [KeyboardButton("دریافت پروژه تحقیقاتی پژوهشی🥼")],
    [KeyboardButton("هوش مصنوعی📱"), KeyboardButton("مارو بشناس 👋")]
]

submenu_profile = [
    [KeyboardButton("نمایش پروفایل👤")],
    [KeyboardButton("ویرایش/ورود اطلاعات✍️")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

submenu_khali = [
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

submenu_about = [
    [KeyboardButton("درباره ما😎")],
    [KeyboardButton("پیام به ادمین💬")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

submenu_scismart = [
    [KeyboardButton("ثبت نام در دوره ی اصلی✍🏻")],
    [KeyboardButton("اطلاعات اساتیدℹ️"), KeyboardButton("اطلاعات دوره⁉️")],
    [KeyboardButton("دریافت گواهینامه 📜")],
    [KeyboardButton("ثبت‌نام در کارگاه‌های تقویتی تکمیلی 💪")],
    [KeyboardButton("بوت‌کمپ‌های تخصصی حضوری 🏢")],
    [KeyboardButton("جلسات ضبط‌شده و جزوات دوره‌ها 🖥")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

submenu_jozve_jalaseh = [
    [KeyboardButton("داکینگ مولکولی"), KeyboardButton("مهندسی بافت")],
    [KeyboardButton("بیوانفورماتیک"), KeyboardButton("پایتون و R")],
    [KeyboardButton("آموزش اکسل"), KeyboardButton("هوش مصنوعی در علم")],
    [KeyboardButton("لینکدین; ساخت پروفایل پژوهشی")],
    [KeyboardButton("جستجوی حرفه‌ای منابع")],
    [KeyboardButton("بازگشت به منوی قبل")]
]

submenu_hamyan = [
    [KeyboardButton("موسسه آناهید گستر خلیلی(دکتر خلیلی)🎓")],
    [KeyboardButton("همکاران تبلیغاتی🤝")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

enseraf_menu = [
    [KeyboardButton("انصراف❌")]
]

award_menu = [
    [KeyboardButton("دریافت لیست جوایز و شانس‌های من 🎁")],
    [KeyboardButton("دریافت لینک دعوت اختصاصی 🔗")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

award_coworkers_menu = [
    [KeyboardButton("دریافت لیست جوایز و شانس‌های من 🎁")],
    [KeyboardButton("همکاری‌های من")],
    [KeyboardButton("دریافت لینک دعوت اختصاصی 🔗")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]


admin_keys = [
        [KeyboardButton("فعال/غیرفعال کردن ربات")],
        [KeyboardButton("ارسال پیام همگانی")],
        [KeyboardButton("آمار ربات"), KeyboardButton("ثبت افراد در کارگاه ها")],
        [KeyboardButton("تایید ثبت نام رویان با کدملی")],
        [KeyboardButton("ارسال پیام به کاربران با کد ملی")],
        [KeyboardButton("لیست کاربرانی که جایزه دارند")],
        [KeyboardButton("بازگشت به منوی اصلی")]
]


virayesh_keys = [
        [KeyboardButton("خانم🤵‍♀"), KeyboardButton("آقا🤵🏼")],
        [KeyboardButton("انصراف❌")]
        ]


kargah_ha_keys = [
    [KeyboardButton("آموزش اکسل"), KeyboardButton("هوش مصنوعی در علم")],
    [KeyboardButton("لینکدین; ساخت پروفایل پژوهشی")],
    [KeyboardButton("جستجوی حرفه‌ای منابع")],
    [KeyboardButton("انصراف❌")]
]


AI_keys = [
    [KeyboardButton("Gemini"), KeyboardButton("ChatGPT")],
    [KeyboardButton("DeepSeek"), KeyboardButton("Grok")],
    [KeyboardButton("بازگشت به منو اصلی🔙")]
]

# تابع کمکی برای ارسال متن های بلند
async def send_long_message(update, text: str, chunk_size: int = 4000):
    for i in range(0, len(text), chunk_size):
        await update.message.reply_text(text[i:i+chunk_size])


#تابع استارت
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if bot_status(sheet) == "غیرفعال":
        await update.message.reply_text("ربات غیرفعال است.")
        return

    ref_args = context.args
    ref_user_id = str(update.effective_user.id)

    user_list = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet3!A4:A").execute()
    user_list = user_list.get("values", [])
    
    if str(update.effective_user.id) in [user[0] for user in user_list if user]:
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام مجدد👋")
        if ref_args:
            # if ref_args[0] != ref_user_id:
            #     pass
            if ref_args[0] == "2735982759385782763482754287":
                approve_users = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:R").execute().get("values", [])
                for user in approve_users:
                    if str(update.effective_user.id) in user:
                        approve = user[16] if len(user) > 16 else None
                        if str(approve) != "1":
                            try:
                                sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!Q{approve_users.index(user)+2}", valueInputOption="USER_ENTERED", body={"values": [[1]]}).execute()
                                await context.bot.send_message(chat_id=update.effective_chat.id, text="ثبت نام شما با موفقیت تایید شد ✅")
                            except Exception as e:
                                await context.bot.send_message(chat_id=ADMIN_ID, text=f"در تایید ثبت نام {update.effective_user.id} خطایی رخ داد: {e}")
                        else:
                            await context.bot.send_message(chat_id=update.effective_chat.id, text="ثبت نام شما قبلا تایید شده است ✅")
            if ref_args[0] == ref_user_id:
                try:
                    await context.bot.send_message(chat_id=ref_args[0], text="عزیزم خودت که نمیتونی با کد دعوت خودت وارد ربات بشی 😁")
                except Exception as e:
                    print(f"Error sending message to user: {e}")
                    
            if ref_args[0] == "87365083756023859873645837652893":
                try:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text="پرداخت با خطا مواجه شد\nبه ادمین ربات پیام دهید")
                except Exception as e:
                    print(f"Error sending message to user: {e}")

    else:
        # await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام کاربر جدید\nخیلی خوش اومدی✌️🏻")
        add_user_id_in_row(str(update.effective_user.id))
        
        sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet3!A4:A", valueInputOption="USER_ENTERED", body={"values": [[update.effective_user.id]]}).execute()

        if ref_args:
            referrer_id = ref_args[0]
            if referrer_id != ref_user_id:

                users_list = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:P").execute()
                users_list = users_list.get("values", [])

                for user in users_list:
                    if user[0] == referrer_id:
                        winn_chance = int(user[15])
                        
                        if winn_chance:
                            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!P{users_list.index(user)+2}", valueInputOption="USER_ENTERED", body={"values": [[winn_chance + 1]]}).execute()                     

                            hamkaran = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet4!B1:JZ").execute()
                            hamkaran = hamkaran.get("values", [])

                            for hamkar in hamkaran:

                                if str(ref_args[0]) in hamkar:

                                    col_index = hamkar.index(str(ref_args[0])) + 1
                                    col_letter = colnum_to_letter(col_index)

                                    col_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet4!{col_letter}:{col_letter}").execute()
                                    col_data = col_data.get("values", [])

                                    last_row = len(col_data) + 1

                                    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet4!{col_letter}{last_row}", valueInputOption="USER_ENTERED", body={"values": [[str(update.effective_user.id)]]}).execute()

                        else:
                            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!P{users_list.index(user)+2}", valueInputOption="USER_ENTERED", body={"values": [[1]]}).execute()

                            for hamkar in hamkaran:

                                if str(ref_args[0]) in hamkar:

                                    col_index = hamkar.index(str(ref_args[0])) + 1
                                    col_letter = colnum_to_letter(col_index)

                                    col_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet4!{col_letter}:{col_letter}").execute()
                                    col_data = col_data.get("values", [])

                                    last_row = len(col_data) + 1

                                    sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet4!{col_letter}{last_row}", valueInputOption="USER_ENTERED", body={"values": [[str(update.effective_user.id)]]}).execute()

                    
                        davat_shdeha = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet5!A:ZZZ").execute().get("values", [])[0]
                        if str(ref_args[0]) in davat_shdeha:
                            col_index = davat_shdeha.index(str(ref_args[0]))
                            col_letter = colnum_to_letter(col_index)

                            col_data = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet5!{col_letter}:{col_letter}").execute()
                            col_data = col_data.get("values", [])

                            last_row = len(col_data) + 1

                            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet5!{col_letter}{last_row}", valueInputOption="USER_ENTERED", body={"values": [[str(update.effective_user.id)]]}).execute()
                            
                            
                                
                await context.bot.send_message(chat_id=ref_args[0], text="کاربر جدیدی با کد دعوت شما وارد ربات شد و شما یک شانس جدید در قرعه کشی دریافت کردید\nبرای مشاهده ی شانس های قرعه کشی خود به بخش <b>قرعه کشی ، هدایا و جوایز</b> مراجعه کنید", parse_mode="HTML")

            else:
                await context.bot.send_message(chat_id=ref_args[0], text="عزیزم خودت که نمیتونی با کد دعوت خودت وارد ربات بشی 😁")


    #پیام خوش آمد گویی
    await context.bot.send_message(text = """
👋 سلام دوست عزیز، خوش اومدی به دنیای SciSmart

برای دسترسی به قسمت‌های مختلف ربات👇🏻

1⃣ اول باید بری پروفایلتو تکمیل کنی
2⃣ از قسمت 👈🏻 <b>«دوره جامع SciSmart 🧬»</b> 👈🏻 ثبت نام در دوره اصلی یا بخش دسترسی سریع (سمت چپ بخش تایپ)، هزینه دوره رو پرداخت و ثبت نامتو نهایی کنی❤️

‼️در غیر این صورت بخش‌های ربات غیرفعال هستن‼️

<b>به موارد زیر دقت کن</b>👇🏻

🔻با مرورگر خود تلگرام هزینه رو پرداخت کن که اتومات ثبت‌نامت نهایی بشه (چون که مرورگرهای دیگه، تلگرامو فیلتر کردن)
🔻در غیر این صورت، باید بصورت دستی به ادمین درخواست بدی که برات دستی رباتو فعال کنه


🔔 راستی یادت نره نوتیف ربات رو فعال کنی تا خبر <b><u>قرعه‌کشی‌ها، مسابقه‌ها و رویدادهای ویژه</u></b> رو از دست ندی!
                                   """,
                                   chat_id=update.effective_chat.id,
                                   reply_to_message_id=update.message.message_id,
                                   parse_mode="HTML")

    reply_markup = ReplyKeyboardMarkup(keyboard=main_menu,
                                       resize_keyboard=True,
                                       input_field_placeholder="یک گزینه را انتخاب کنید")
    # ارسال پیام با کلیدها
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="""
🤖 اینجا فقط یادگیری نیست، هوش مصنوعی هم همراهته!

🔸کافیه در دوره ثبت‌نام کنی و بعدش هر وقت سوالی داشتی، روی دکمه <b><u>«هوش مصنوعی»</u></b> بزنی و از هوش مصنوعی مورد علاقت سوالت رو بپرسی.
۴ تا هوش مصنوعی جذاب، رایگان در اختیارتن که بری لذتشو ببری 😉

🎓 تازه!
می‌تونی با صدا زدن اسم هوش مصنوعی خود دوره با نام «هوشا» در هر قسمتی و موقعیتی از ربات،  در مورد دوره scismart سوال کنی!

مثلا👇🏻
«هوشا، دوره کی برگزار میشه؟»
«هوشا، پروژه تحقیقاتی یعنی چی؟»
                                   """,
                                   reply_markup=reply_markup)


# تابع جابجایی بین دکمه ها
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id not in ADMIN_ID:
        if bot_status(sheet) == "غیرفعال":
            await update.message.reply_text("ربات غیرفعال است.")
            return

    if update.effective_user.id in ADMIN_ID:
        if update.message.reply_to_message:  
                return await admin_response(update, context)
    
    text = update.message.text
    

    if text == "مارو بشناس 👋":
        await update.message.reply_text(
            "📂 ما کی میباشیم؟(درباره ی ما):",
            reply_markup=ReplyKeyboardMarkup(submenu_about, resize_keyboard=True)
        )

    if text == "پیام به ادمین💬":
        return await feedback_message(update, context)
    
    if text == "درباره ما😎":
        for i in range(2, 17):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1003003640252",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_about, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'درباره ما': {e}")


    if text == "دوره جامع scismart🧬":
        await update.message.reply_text(
            "📂 دوره جامع scismart:",
            reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True)
        )
        
        
    #جلسات ضبط شده ی دوره ها
    if text == "جلسات ضبط‌شده و جزوات دوره‌ها 🖥":
        if is_approved_by_royan(update, context=context):
            await update.message.reply_text(
                "📂 جلسات ضبط‌شده و جزوات دوره‌ها:",
                reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True)
            )
            
        else:
            await update.message.reply_text(
                "باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True)
            )
            
            
    if text == "مهندسی بافت":
        if is_approved_by_royan(update, context=context):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002971470859",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'مهندسی بافت': {e}")
        else:
            await update.message.reply_text("باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
       
       
    if text == "داکینگ مولکولی":
        if is_approved_by_royan(update, context=context):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002912500702",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'داکینگ مولکولی': {e}")
        else:
            await update.message.reply_text("باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))         
                
    if text == "پایتون و R":

        if is_approved_by_royan(update, context=context):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002979112196",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'پایتون و R': {e}")
        else:
            await update.message.reply_text("باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))        
                
    if text == "بیوانفورماتیک":

        if is_approved_by_royan(update, context=context):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002954990298",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'بیوانفورماتیک': {e}")
        else:
            await update.message.reply_text("باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))        
                
    if text == "هوش مصنوعی در علم":

        if is_in_workshop(update, context=context, kargah_user=text):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1003038247209",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'هوش مصنوعی در علم': {e}")

        elif get_inviteds(update.effective_user.id) >= 5:
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1003038247209",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'هوش مصنوعی در علم': {e}")
        else:
            await update.message.reply_text("شما در این کارگاه ثبت‌نام نکرده‌اید.",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))        
    
    if text == "آموزش اکسل":

        if is_in_workshop(update, context=context, kargah_user=text):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1003034936559",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'آموزش اکسل': {e}")
                    
        elif get_inviteds(update.effective_user.id) >= 5:
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1003034936559",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'آموزش اکسل': {e}")
        else:
            await update.message.reply_text("شما در این کارگاه ثبت‌نام نکرده‌اید.",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
    
    if text == "لینکدین; ساخت پروفایل پژوهشی":

        if is_in_workshop(update, context=context, kargah_user=text):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002979995683",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'لینکدین; ساخت پروفایل پژوهشی': {e}")
                    
        elif get_inviteds(update.effective_user.id) >= 3:
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002979995683",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'لینکدین; ساخت پروفایل پژوهشی': {e}")
        else:
            await update.message.reply_text("شما در این کارگاه ثبت‌نام نکرده‌اید.",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))        
                
    if text == "جستجوی حرفه‌ای منابع":

        if is_in_workshop(update, context=context, kargah_user=text):
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002932760623",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'جستجوی حرفه‌ای منابع': {e}")
                    
        elif get_inviteds(update.effective_user.id) >= 3:
            for i in range(2, 27):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002932760623",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'جستجوی حرفه‌ای منابع': {e}")
                    
        else:
            await update.message.reply_text("شما در این کارگاه ثبت‌نام نکرده‌اید.",
                                            reply_markup=ReplyKeyboardMarkup(submenu_jozve_jalaseh, resize_keyboard=True))        
                
    if text == "بازگشت به منوی قبل":
        await update.message.reply_text(
            "به بخش دوره جامع scismart بازگشتید.",
            reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True)
        )

                
    if text == "اطلاعات دوره⁉️":
        for i in range(2, 17):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1002523917032",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'اطلاعات دوره⁉️': {e}")

    if text == "اطلاعات اساتیدℹ️":
        for i in range(2, 17):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1003014187035",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'اطلاعات اساتیدℹ️': {e}")

            
    if text == "ثبت نام در دوره ی اصلی✍🏻":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="برای ثبت نام در دوره ی اصلی روی لینک زیر کلیک کنید\n\n https://zarinp.al/747156",
                                       reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True))
            
   
    if text == "ثبت‌نام در کارگاه‌های تقویتی تکمیلی 💪":
        for i in range(2, 18):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1002999857032",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'ثبت‌نام در کارگاه‌های تقویتی تکمیلی 💪': {e}")


    #دریافت گواهی
    if text == "دریافت گواهینامه 📜":
        if  is_approved_by_royan(update, context=context):
            await update.message.reply_text(
                "بعد از پایان دوره میتونی از طریق لینک زیر گواهی پایان دوره رو دریافت کنی .",
                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True)
            )
        else:
            await update.message.reply_text(
                "باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                reply_markup=ReplyKeyboardMarkup(submenu_scismart, resize_keyboard=True)
            )

    if text == "❤️ حامیان مالی و معنوی 💵":
        await update.message.reply_text(
            "📂 حامیان مالی و معنوی:",
            reply_markup=ReplyKeyboardMarkup(submenu_hamyan, resize_keyboard=True)
        )

    if text == "همکاران تبلیغاتی🤝":
        for i in range(2, 17):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1002773557462",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_hamyan, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'همکاران تبلیغاتی🤝': {e}")

    if text == "موسسه آناهید گستر خلیلی(دکتر خلیلی)🎓":
        for i in range(2, 17):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1003041925955",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(submenu_hamyan, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'موسسه آناهید گستر خلیلی(دکتر خلیلی)🎓': {e}")

    if text == "پروفایل کاربری👤":
        await update.message.reply_text(
            "📂 پروفایل کاربری:",
            reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True)
        )

    if text == "نمایش پروفایل👤":
        

        # دریافت اطلاعات از Google Sheets
        sheet_data = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:Z")
        .execute()
        )
        sheet_data_value = sheet_data.get("values", [])



        # فرض بر این است که ستون اول (A) شامل user_id است
        user_id = str(update.effective_user.id)
        user_row = None
        for row in sheet_data_value:
            if len(row) > 0 and row[0] == user_id:
                user_row = row
                break

        if user_row:
            user_gender = user_row[1] if len(user_row) > 1 else ""
            user_name_and_lastname_farsi = user_row[2] if len(user_row) > 2 else ""
            user_name_and_lastname_english = user_row[3] if len(user_row) > 3 else ""
            user_birth_date = user_row[4] if len(user_row) > 4 else ""
            user_national_code = user_row[5] if len(user_row) > 5 else ""
            user_phone_number = user_row[6] if len(user_row) > 6 else ""
            user_field = user_row[7] if len(user_row) > 7 else ""
            user_specialization = user_row[8] if len(user_row) > 8 else ""
            user_education_level = user_row[9] if len(user_row) > 9 else ""
            user_term_number = user_row[10] if len(user_row) > 10 else ""
            user_university = user_row[11] if len(user_row) > 11 else ""
            user_address = user_row[12] if len(user_row) > 12 else ""
            user_email = user_row[13] if len(user_row) > 13 else ""

        
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"جنسیت: {user_gender}\n"
                                            f"(فارسی)نام و نام خانوادگی: {user_name_and_lastname_farsi}\n"
                                            f"نام و نام خانوادگی(انگلیسی): {user_name_and_lastname_english}\n"
                                            f"تاریخ تولد: {user_birth_date}\n"
                                            f"کد ملی: {user_national_code}\n"
                                            f"شماره تماس: {user_phone_number}\n"
                                            f"رشته: {user_field}\n"
                                            f"گرایش: {user_specialization}\n"
                                            f"مقطع: {user_education_level}\n"
                                            f"عدد ترم: {user_term_number}\n"
                                            f"نام دانشگاه: {user_university}\n"
                                            f"محل سکونت: {user_address}\n"
                                            f"ایمیل فعال: {user_email}",
                                       reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True))
        


        else:
            user_gender = user_name_and_lastname_farsi = user_name_and_lastname_english = user_birth_date = user_national_code = user_phone_number = ""
            user_field = user_specialization = user_education_level = user_term_number = ""
            user_university = user_address = user_email = ""
            
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f"جنسیت: {user_gender}\n"
                                            f"(فارسی) نام و نام خانوادگی: {user_name_and_lastname_farsi}\n"
                                            f"نام و نام خانوادگی(انگلیسی): {user_name_and_lastname_english}\n"
                                            f"تاریخ تولد: {user_birth_date}\n"
                                            f"کد ملی: {user_national_code}\n"
                                            f"شماره تماس: {user_phone_number}\n"
                                            f"رشته: {user_field}\n"
                                            f"گرایش: {user_specialization}\n"
                                            f"مقطع: {user_education_level}\n"
                                            f"عدد ترم: {user_term_number}\n"
                                            f"نام دانشگاه: {user_university}\n"
                                            f"محل سکونت: {user_address}\n"
                                            f"ایمیل فعال: {user_email}",
                                       reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True))




    if text == "ویرایش/ورود اطلاعات✍️":


        virayesh_keys = [[KeyboardButton("انصراف❌")]]

        await update.message.reply_text(
            "لطفاً اطلاعات جدید خود را وارد کنید:",
            reply_markup=ReplyKeyboardMarkup(virayesh_keys, resize_keyboard=True)
        )

        edit_profile_start(update, context)

    # elif text == "انصراف":
    #     await update.message.reply_text(
    #         "شما از ویرایش اطلاعات خود انصراف دادید",
    #         reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True)
    #     )


    if text == "مسابقه🏆":

        if is_approved_by_royan(update, context):
            for i in range(2, 18):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002757683581",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'مسابقه': {e}")

        else:
            await update.message.reply_text(
                "باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            )

    if text == "🎰 قرعه‌کشی، هدایا و جوایز  🥇":
        
        if is_hamkar(update.effective_user.id):
            await update.message.reply_text(
                "📂 قرعه کشی ، هدایا و جوایز:\n(شما همکار ما هستید ، برای مشاهده ی آمار همکاری به بخش همکاری های من مراجعه کنید)",
                reply_markup=ReplyKeyboardMarkup(award_coworkers_menu, resize_keyboard=True)
            )
        else:
            await update.message.reply_text(
                "📂 قرعه کشی ، هدایا و جوایز:",
                reply_markup=ReplyKeyboardMarkup(award_menu, resize_keyboard=True)
            )

    if text == "دریافت لیست جوایز و شانس‌های من 🎁":

        user_id_award = str(update.effective_user.id)

        award_list = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="sheet1!A2:P"
        ).execute().get("values", [])

        for row in award_list:
            if row and user_id_award == row[0]:
                award = row[14] if len(row) > 14 else None
                winn_chance = row[15] if len(row) > 15 else None

        if is_hamkar(update.effective_user.id):
            await update.message.reply_text(
                f"شما <b>{winn_chance}</b> شانس در قرعه کشی ما دارید\n\n"
                f"هدایا و جوایز تعلق گرفته به شما:\n🔸{award}",
                parse_mode="HTML",
                reply_markup=ReplyKeyboardMarkup(award_coworkers_menu, resize_keyboard=True)
            )
            for i in range(2, 18):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002937744945",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(award_coworkers_menu, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'دریافت لیست جوایز و شانس‌های من 🎁': {e}")
        else:
            await update.message.reply_text(
                f"شما <b>{winn_chance}</b> شانس در قرعه کشی ما دارید\n\n"
                f"هدایا و جوایز تعلق گرفته به شما:\n🔸{award}",
                parse_mode="HTML",
                reply_markup=ReplyKeyboardMarkup(award_menu, resize_keyboard=True)
            )
            for i in range(2, 18):
                try:
                    await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                    from_chat_id="-1002937744945",
                                                    message_id=i,
                                                    reply_markup=ReplyKeyboardMarkup(award_menu, resize_keyboard=True))
                except Exception as e:
                    print(f"Error copying message in 'دریافت لیست جوایز و شانس‌های من 🎁': {e}")



    if text == "همکاری‌های من":

        if is_hamkar(update.effective_user.id):

            hamkari_ha = get_refferer_chance(str(update.effective_user.id))

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                            text=f"شما <b>{hamkari_ha}</b> کاربر تایید شده دعوت کرده اید",
                                            parse_mode="HTML")

    if text == "دریافت لینک دعوت اختصاصی 🔗":
        await get_ref_link(update, context)
        

    if text == "پژوهشگاه رویان🎓":
        for i in range(2, 18):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1002967942981",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'پژوهشگاه رویان🎓': {e}")

    if text == "دریافت پروژه تحقیقاتی پژوهشی🥼":
        for i in range(2, 18):
            try:
                await context.bot.copy_message(chat_id=update.effective_chat.id,
                                                from_chat_id="-1003051081410",
                                                message_id=i,
                                                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
            except Exception as e:
                print(f"Error copying message in 'دریافت پروژه ی تحقیقاتی-پژوهشی🥼': {e}")

    if text == "هوش مصنوعی📱":
        if is_approved_by_royan(update, context):
            mahdodiat_user = get_user_cupon(str(update.effective_user.id))

            await context.bot.sendMessage(text=f"""
راهنمای استفاده :
<b>از طریق کلید ها میتونی هوش مصنوعی اشتراکی دلخواهت رو انتخاب کنی و ازش رایگان استفاده کنی.</b>
🔹سقف استفاده از هوش مصنوعی ۲۵ پیام در روز است .  
اما میتونی با دعوت 3 نفر در  ثبت نام دوره ظرفیت اون رو تا ۵۰ پیام افزایش بدی 
و دوتا از کارگاه های تقویتی تکمیلی رو رایگان دریافت کنی .

🔹اگر 5 نفر رو دعوت کنی ظرفیت استفاده از هوش مصنوعی تا ۷۵ پیام در روز افزایش پیدا می‌کنه و میتونی تمام کارگاه رو رایگان دریافت کنی .

تعداد پیام مجاز شما در حال حاضر : <b>{mahdodiat_user}</b> پیام است.
""",
                                   reply_markup=ReplyKeyboardMarkup(AI_keys, resize_keyboard=True),
                                   chat_id=update.effective_user.id,
                                   parse_mode="HTML")
        else:
            await update.message.reply_text(
                "باید در دوره ثبت‌نام نهایی (پرداخت) انجام بدید",
                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            )


    if text == "Gemini":
        await ai_chat_start(update, context)

    if text == "ChatGPT":
        await gpt_chat_start(update, context)

    if text == "DeepSeek":
        await deepseek_chat_start(update, context)

    if text == "Grok":
        await grok_chat_start(update, context)
        

    if text.startswith("هوشا"):

        user_text = update.message.text[len("هوشا"):].lstrip()

        SYSTEM_PROMPT = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="sheet2!B4"
        ).execute().get("values", [[]])[0][0]

        # پرامپت سیستمی رو به ابتدای متن کاربر اضافه می‌کنیم
        full_prompt = f"{SYSTEM_PROMPT}\n\nکاربر: {user_text}"

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",  # یا هر مدلی که خواستی
                contents=full_prompt
            )
            gemini_reply = response.text or "پاسخی از هوشا دریافت نشد."
        except Exception as e:
            gemini_reply = "خطا در ارتباط با هوشا"
            print(f"Error occurred while communicating with هوشا: {e}")

        await send_long_message(update, gemini_reply)

    if update.effective_user.id in ADMIN_ID:
        if text == "فعال/غیرفعال کردن ربات":
            status = bot_status(sheet)
            if status == "فعال":
                sheet.values().update(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range="sheet2!B1:C1",
                    valueInputOption="USER_ENTERED",
                    body={"values": [["غیرفعال"]]}

                ).execute()
                await update.message.reply_text("ربات غیرفعال شد.",
                                                reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
            elif status == "غیرفعال":
                sheet.values().update(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range="sheet2!B1:C1",
                    valueInputOption="USER_ENTERED",
                    body={"values": [["فعال"]]}

                ).execute()
                await update.message.reply_text("ربات فعال شد.", 
                                                reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
                

        if text == "ارسال پیام همگانی":
            return await message_get(update, context)

        if text == "آمار ربات":
            statuss = bot_status(sheet)
            users_number = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet2!B2:B3").execute()
            users_number = users_number.get("values", [])

            await update.message.reply_text(f"آمار ربات:\nوضعیت: {statuss}\nتعداد استارت های ربات: {users_number[0][0]}\nتعداد ثبت نامی ها: {users_number[1][0]}")

        
        if text == "ثبت افراد در کارگاه ها":
            return await admin_register_participants_start(update, context)

        if text == "تایید ثبت نام رویان با کدملی":
            return await admin_approve_with_national_code_start(update, context)

        if text == "ارسال پیام به کاربران با کد ملی":
            return await admin_send_national_code_start(update, context)

        if text == "لیست کاربرانی که جایزه دارند":
            return await admin_send_award_list(update, context)

        if text == "بازگشت به منوی اصلی":
            await update.message.reply_text("به منوی اصلی بازگشتید.",
                                            reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

            


    if text == "بازگشت به منو اصلی🔙":
            await update.message.reply_text(
                "به منوی اصلی بازگشتید",
                reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
            )


# تابع هلپ
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if bot_status(sheet) == "غیرفعال":
        await update.message.reply_text("ربات غیرفعال است.")
        return

    #پیام راهنمایی(هلپ)
    await context.bot.send_message(text = """تو میتونی وارد قسمت درباره ما بشی و به ادمین پیام بدی

یا اگر درمورد دوره سوال داری، هرجای ربات اول جملت بگی هوشا و بعد سوالتو بپرسی جوابتو میده

یا دیگه اگر خیلی نیاز به کمک داری مستقیم به ادمین آکادمی پیام بدی👇🏻
@BioSantezAc_admin""",
                                   chat_id=update.effective_chat.id,
                                   reply_to_message_id=update.message.message_id)


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if bot_status(sheet) == "غیرفعال":
        await update.message.reply_text("ربات غیرفعال است.")
        return

    await context.bot.send_message(text = "لینک ثبت نام دوره 👇🏻",
                                   chat_id=update.effective_chat.id,
                                   reply_to_message_id=update.message.message_id,
                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ثبت نام", url="https://zarinp.al/747156")]]))


def fa_to_en_numbers(text: str) -> str:
    # فارسی کننده ی اعداد
    mapping = {
        "۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4",
        "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",
        "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4",
        "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9",
    }
    return "".join(mapping.get(ch, ch) for ch in str(text))



GPT_CHAT, DEEPSEEK_CHAT, GROK_CHAT, GET_KARGAH_NAME, GET_NCODES, SEND_NATIONAL_CODE_ROYAN, FEEDBACK_MESSAGE, SEND_NATIONAL_CODE, SEND_NATIONAL_CODE_GETMESSAGE, MESSAGE_GET_ADMIN, SEND_TO_ALL, AI_CHAT, GENDER, NAME_AND_LASTNAME_FARSI, NAME_AND_LAST_NAME_ENGLISH, BIRTH_DATE, NATIONAL_CODE, PHONE_NUMBER, FIELD, SPECIALIZATION, EDUCATION_LEVEL, TERM_NUMBER, UNIVERSITY, ADDRESS, EMAIL = range(25)

async def edit_profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if bot_status(sheet) == "غیرفعال":
        await update.message.reply_text("ربات غیرفعال است.")
        return

    await update.message.reply_text(
        "اطلاعات جدید خود را وارد کنید:\nلطفا در وارد کردن اطلاعات دقت کافی به خرج دهید\n(اطلاعات نادرست، روند صدور گواهی و تشکیل تیم تحقیقاتی رو مختل میکنه)"
    )
    await update.message.reply_text("جنسیت: آقا/خانم\nلطفا از دکمه ها استفاده کنید:", reply_markup=ReplyKeyboardMarkup(virayesh_keys, resize_keyboard=True))
    return GENDER

async def edit_profile_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    
    if update.message.text not in ["خانم🤵‍♀", "آقا🤵🏼"]:
        await update.message.reply_text("لطفاً از دکمه ها استفاده کنید.")
        return GENDER
    
    context.user_data["gender"] = update.message.text
    await update.message.reply_text("نام و نام خانوادگی(فارسی):", reply_markup=ReplyKeyboardMarkup(enseraf_menu,resize_keyboard=True))
    return NAME_AND_LASTNAME_FARSI

async def edit_profile_name_and_lastname_farsi(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["name_and_lastname_farsi"] = update.message.text
    await update.message.reply_text("نام و نام خانوادگی(انگلیسی):\n(برای صدور گواهی انگلیسی ، حروف اول اسم و فامیل شما بزرگ باشد)", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return NAME_AND_LAST_NAME_ENGLISH


async def edit_profile_name_and_lastname_english(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["name_and_lastname_english"] = update.message.text
    await update.message.reply_text("تاریخ تولد:\nتاریخ تولد را باید به صورت: روز/ماه/سال وارد کنید\nمثلا: 1404/01/01", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return BIRTH_DATE

async def edit_profile_birth_date(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # بررسی انصراف
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    # تبدیل اعداد فارسی به انگلیسی
    text = update.message.text
    text = fa_to_en_numbers(text)

    # بررسی فرمت با regex (YYYY/MM/DD)
    pattern = r"^\d{4}/\d{2}/\d{2}$"
    if not re.match(pattern, text):
        await update.message.reply_text(
            "❌ تاریخ باید در قالب صحیح (مثال: 1378/05/11) وارد شود. دوباره تلاش کن."
        )
        return BIRTH_DATE   # دوباره همون مرحله

    # ذخیره تاریخ معتبر
    context.user_data["birth_date"] = text
    await update.message.reply_text(
        "کد ملی:\n(برای صدور انواع گواهی ملی و بین المللی میخوایم)",
        reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True)
    )
    return NATIONAL_CODE

async def edit_profile_national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    if len(update.message.text) != 10:
        await update.message.reply_text("❌ کد ملی باید 10 رقم باشد.")
        return NATIONAL_CODE

    context.user_data["national_code"] = fa_to_en_numbers(update.message.text)
    await update.message.reply_text("شماره تماس فعال:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return PHONE_NUMBER

async def edit_profile_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    if len(update.message.text) != 11:
        await update.message.reply_text("❌ شماره تماس باید 11 رقم باشد.")
        return PHONE_NUMBER

    context.user_data["phone_number"] = fa_to_en_numbers(update.message.text)
    await update.message.reply_text("رشته تحصیلی:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return FIELD

async def edit_profile_field(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["field"] = update.message.text
    await update.message.reply_text("گرایش:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return SPECIALIZATION

async def edit_profile_specialization(update: Update, context: ContextTypes.DEFAULT_TYPE):

    education_level_keys = [
        [KeyboardButton("کارشناسی"), KeyboardButton("کاردانی"), KeyboardButton("دبیرستان")],
        [KeyboardButton("استاد دانشگاه"), KeyboardButton("دکتری"), KeyboardButton("کارشناسی ارشد")],
        [KeyboardButton("انصراف❌")]
    ]
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["specialization"] = update.message.text
    await update.message.reply_text("مقطع تحصیلی:\n(لطفا از دکمه های استفاده کنید)", reply_markup=ReplyKeyboardMarkup(education_level_keys, resize_keyboard=True))
    return EDUCATION_LEVEL

async def edit_profile_education_level(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    if update.message.text not in ["دبیرستان", "کاردانی", "استاد دانشگاه", "کارشناسی", "کارشناسی ارشد", "دکتری"]:
        await update.message.reply_text("لطفاً فقط از دکمه ها استفاده کنید.")
        return EDUCATION_LEVEL

    context.user_data["education_level"] = update.message.text
    await update.message.reply_text("ترم چندمی؟\n(ترم 1 تا 15 قبوله فقط)", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return TERM_NUMBER

async def edit_profile_term_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    if fa_to_en_numbers(update.message.text) not in [str(i) for i in range(1, 16)]:
        await update.message.reply_text("داداش تو دیگه خیلی پیری واسه دوره های ما ، یه عدد معتبر از 1 تا 15 وارد کن")
        return TERM_NUMBER

    context.user_data["term_number"] = fa_to_en_numbers(update.message.text)
    await update.message.reply_text("نام دانشگاه:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return UNIVERSITY

async def edit_profile_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["university"] = update.message.text
    await update.message.reply_text("آدرس:\n(دقیق - برای پروژه های تحقیقاتی که قراره انتهای دوره به تناسب محل سکونت و استان داده بشه)", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return ADDRESS

async def edit_profile_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    context.user_data["address"] = update.message.text
    await update.message.reply_text("ایمیل فعال:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return EMAIL

async def edit_profile_email(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if bot_status == "غیرفعال":
        await update.message.reply_text("ربات غیرفعال است.")
        return

    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END
    
    text = update.message.text.strip()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(pattern, text):
        await update.message.reply_text(
            "❌ لطفاً یک ایمیل معتبر وارد کن (مثال: example@gmail.com)"
        )
        return EMAIL

    context.user_data["email"] = update.message.text

    # ثبت اطلاعات در گوگل شیت
    sheet_data = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:Z")
        .execute()
        )
    sheet_data_value = sheet_data.get("values", [])

    sheet_data2 = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet2!B6:B")
        .execute()
    )
    sheet_data2_value = sheet_data2.get("values", [])

    hamkaran = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet4!B1:JZ")
        .execute()
    )
    hamkaran = hamkaran.get("values", [])

    user_id = str(update.effective_user.id)
    user_row_index = None

    for idx, row in enumerate(sheet_data_value, start=2):  # چون از A2 شروع کردی
        try:
            if len(row) > 0 and row[0] == user_id:
                user_row_index = idx
                break
        except Exception as e:
            print(f"Error checking bot status: {e}")

    if user_row_index:
        user_row_gender = context.user_data.get("gender")
        user_row_name_and_lastname_farsi = context.user_data.get("name_and_lastname_farsi")
        user_row_name_and_lastname_english = context.user_data.get("name_and_lastname_english")
        user_row_birth_date = context.user_data.get("birth_date")
        user_row_national_code = context.user_data.get("national_code")
        user_row_phone_number = context.user_data.get("phone_number")
        user_row_field = context.user_data.get("field")
        user_row_specialization = context.user_data.get("specialization")
        user_row_education_level = context.user_data.get("education_level")
        user_row_term_number = context.user_data.get("term_number")
        user_row_university = context.user_data.get("university")
        user_row_address = context.user_data.get("address")
        user_row_email = context.user_data.get("email")

        baghali = [[
            user_id,
            user_row_gender,
            user_row_name_and_lastname_farsi,
            user_row_name_and_lastname_english,
            user_row_birth_date,
            user_row_national_code,
            user_row_phone_number,
            user_row_field,
            user_row_specialization,
            user_row_education_level,
            user_row_term_number,
            user_row_university,
            user_row_address,
            user_row_email
        ]]

        update_result = sheet.values().update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=f"sheet1!A{user_row_index}:Z{user_row_index}",
            valueInputOption="USER_ENTERED",
            body={"values": baghali}
        ).execute()
        
        await update.message.reply_text("اطلاعات با موفقیت ثبت شد.", reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True))
        if is_hamkar(update.effective_user.id):
            try:
                    
                await sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!S{hamkaran.index(str(update.effective_user.id))+2}", valueInputOption="USER_ENTERED", body={"values": [[1]]}).execute()
            except Exception as e:
                print(f"Error updating hamkaran status: {e}")
        return ConversationHandler.END  # پایان ویرایش اطلاعات
    else:
        user_row_gender = context.user_data.get("gender")
        user_row_name_and_lastname_farsi = context.user_data.get("name_and_lastname_farsi")
        user_row_name_and_lastname_english = context.user_data.get("name_and_lastname_english")
        user_row_birth_date = context.user_data.get("birth_date")
        user_row_national_code = context.user_data.get("national_code")
        user_row_phone_number = context.user_data.get("phone_number")
        user_row_field = context.user_data.get("field")
        user_row_specialization = context.user_data.get("specialization")
        user_row_education_level = context.user_data.get("education_level")
        user_row_term_number = context.user_data.get("term_number")
        user_row_university = context.user_data.get("university")
        user_row_address = context.user_data.get("address")
        user_row_email = context.user_data.get("email")

        user_row_chance = sheet_data2_value[0][0] if sheet_data2_value else ""
        user_row_award = "بدون جایزه"

        # یک ردیف کامل
        baghali = [[
            user_id,
            user_row_gender,
            user_row_name_and_lastname_farsi,
            user_row_name_and_lastname_english,
            user_row_birth_date,
            user_row_national_code,
            user_row_phone_number,
            user_row_field,
            user_row_specialization,
            user_row_education_level,
            user_row_term_number,
            user_row_university,
            user_row_address,
            user_row_email,
            user_row_award,
            user_row_chance
        ]]

        # اضافه کردن سطر جدید
        sheet.values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="sheet1!A2:Z",
            valueInputOption="USER_ENTERED",
            body={"values": baghali}
        ).execute()
        await update.message.reply_text("اطلاعات با موفقیت ثبت شد.", reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True))
        # if is_hamkar(update.effective_user.id):
        #     await sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!S{hamkaran.index(str(update.effective_user.id))+2}", valueInputOption="USER_ENTERED", body={"values": [[1]]}).execute()
        return ConversationHandler.END # پایان ویرایش اطلاعات



async def edit_profile_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_ID:
        await update.message.reply_text("عملیات ارسال پیام لغو شد", reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
    else:
        await update.message.reply_text("به منوی پروفایل کاربری برگشتیم.",
                                        reply_markup=ReplyKeyboardMarkup(submenu_profile, resize_keyboard=True))
    return ConversationHandler.END



def bot_status(sheet):
    try:
        result = sheet.values().get(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="sheet2!B1:C"
        ).execute()

        values = result.get("values", [])
        status = [row[0] for row in values if row]  # فقط سلول‌های پر

        if status:
            return status[0]
        return None
    except Exception as e:
        print(f"خطا در خواندن وضعیت ربات: {e}")
        return None




# تابع مدیریت ادمین
async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_ID:
                
        await update.message.reply_text("سلام سجاد وارد منوی ادمین شدی:", reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))        
        
    else:
        await update.message.reply_text("شما دسترسی به این منو ندارید.")
        return

        
        

async def message_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_ID:
        await update.message.reply_text("لطفا پیام خود را ارسال کنید:", reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
        return SEND_TO_ALL

async def send_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if update.message.text == "انصراف❌":
        await edit_profile_cancel(update, context)
        return ConversationHandler.END

    users_IDs = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet3!A4:A").execute()
    users_IDs = users_IDs.get("values", [])
    users_IDs = [user[0] for user in users_IDs if user]
    
    # تشخیص نوع پیام و ارسال به همه کاربران
    for user_id in users_IDs:
        try:
            # کپی کردن پیام به کاربر
            await update.message.copy(chat_id=user_id)
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_user.id, text=f"خطا در ارسال پیام به کاربر: {user_id}: {e}")

    await update.message.reply_text("پیام به همه کاربران ارسال شد.",
                                     reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
    return ConversationHandler.END



async def ai_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چت با هوش مصنوعی شروع شد. لطفا پیام خود را ارسال کنید:",
                                    reply_markup=ReplyKeyboardMarkup([["انصراف❌"]], resize_keyboard=True))
    return AI_CHAT

# تاریخچه گفتگو برای هر کاربر
chat_history = {}

def get_system_prompt():
    return sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet2!B5:B"
    ).execute().get("values", [[]])[0][0]

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_message == "انصراف❌":
        await ai_chat_end(update, context)
        return ConversationHandler.END
    
    if get_user_cupon(user_id) < 1:
        await update.message.reply_text("شما اعتبار کافی برای استفاده از این سرویس را ندارید.\n24 ساعت دیگر می‌توانید دوباره امتحان کنید.")
        await gpt_chat_end(update, context)
        return ConversationHandler.END

    # آماده‌سازی تاریخچه
    if user_id not in chat_history:
        chat_history[user_id] = []

    history_text = "\n".join(
        f"کاربر: {u}\nهوش مصنوعی: {g}" for u, g in chat_history[user_id]
    )
    SYSTEM_PROMPT_PERMANENT = get_system_prompt()
    full_prompt = (
        SYSTEM_PROMPT_PERMANENT
        + ("\n\n" + history_text if history_text else "")
        + f"\nکاربر: {user_message}\nهوش مصنوعی:"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        gemini_reply = response.text or "پاسخی از هوش مصنوعی دریافت نشد."
    except Exception as e:
        gemini_reply = "خطا در ارتباط با هوش مصنوعی"
        print(f"Error occurred while communicating with هوش مصنوعی: {e}")

    await send_long_message(update, gemini_reply)
    users_cupon[user_id]['value'] -= 1

    chat_history[user_id].append((user_message, gemini_reply))
    if len(chat_history[user_id]) > 20:
        chat_history[user_id] = chat_history[user_id][-20:]

    return AI_CHAT


async def ai_chat_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in chat_history:
        del chat_history[user_id]
    await update.message.reply_text("چت با هوش مصنوعی پایان یافت.",
                                    reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
    return ConversationHandler.END


global national_codes

async def admin_send_national_code_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا کد ملی کاربران را ارسال کنید:\n(هر کدوم تو یک خط)",
                                    reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return SEND_NATIONAL_CODE_GETMESSAGE

async def admin_send_national_code_getmessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف":
        await admin_send_national_code_cancel(update, context)
        return ConversationHandler.END

    lines = update.message.text.strip().splitlines()  # حذف فاصله‌های اضافه و جداسازی خط‌ها
    global national_codes
    national_codes = [line.strip() for line in lines if line.strip()]

    await update.message.reply_text("پیام خود را ارسال کنید:",
                                    reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    
    return SEND_NATIONAL_CODE

async def admin_send_national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "انصراف":
        await admin_send_national_code_cancel(update, context)
        return ConversationHandler.END
    
    admin_message = update.message.text

    # گرفتن داده‌ها از شیت
    user_unpaired_ids = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, 
        range="sheet1!A2:G"
    ).execute()
    user_unpaired_ids = user_unpaired_ids.get("values", [])
    global national_codes
    user_paired_ids = []
    for row in user_unpaired_ids:
        national_code = row[5] if len(row) > 5 else None
        telegram_id   = row[0] if len(row) > 0 else None
        
        if national_code in national_codes:
            user_paired_ids.append(telegram_id)

    # ارسال پیام به کاربران
    for tg_id in user_paired_ids:
        try:
            await context.bot.send_message(chat_id=tg_id, text=admin_message)
        except Exception as e:
            context.bot.send_message(chat_id=update.effective_user.id, text=f"خطا در ارسال پیام به کاربر: {tg_id}: {e}")

    await update.message.reply_text(
        "پیام به کاربران با کد ملی ارسال شد.",
        reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True)
    )

    # خالی کردن لیست کدملی‌ها
    national_codes.clear()
    return ConversationHandler.END


async def admin_send_national_code_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات ارسال کد ملی لغو شد.",
                                    reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
    return ConversationHandler.END




async def admin_send_award_list(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet1!A2:O"
    ).execute()
    user_data = user_data.get("values", [])

    national_code_list = []

    for row in user_data:
        name_lastname = row[2] if len(row) > 2 else None
        national_code = row[5] if len(row) > 5 else None
        phone_number = row[6] if len(row) > 6 else None
        award = row[14] if len(row) > 14 else None
        if award:
            await update.message.reply_text(f"کاربر: {name_lastname}\nکد ملی: {national_code}\nشماره تلفن: {phone_number}\nجایزه ها: {award}")
            national_code_list.append(national_code)

    N_code_message = ""
    for N_code in national_code_list:
        N_code_message += f"{N_code}\n"
    await context.bot.send_message(chat_id=update.message.chat_id, text=N_code_message)

async def feedback_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا پیام خود را وارد کنید:",
                                    reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return FEEDBACK_MESSAGE

async def feedback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    msg = update.message

    if msg.text == "انصراف❌":
        await feedback_cancel(update, context)
        return ConversationHandler.END

    for admin_id in ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=f"📩 پیام جدید از {user.full_name} ({user.id}):"
            )

            sent = await context.bot.copy_message(
                    chat_id=admin_id,
                    from_chat_id=msg.chat_id,
                    message_id=msg.message_id
                )
            
            # ذخیره‌ی آیدی کاربر اصلی
            context.bot_data[sent.message_id] = user.id
            
        except Exception as e:
            context.bot.send_message(chat_id=admin_id, text=f"خطا در ارسال پیام کاربر به {admin_id}: {e}")
      
    await update.message.reply_text("پیام شما به ادمین ارسال شد.",
                                    reply_markup=ReplyKeyboardMarkup(submenu_about, resize_keyboard=True))
    return ConversationHandler.END

async def feedback_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عملیات ارسال پیام لغو شد.",
                                    reply_markup=ReplyKeyboardMarkup(submenu_about, resize_keyboard=True))
    return ConversationHandler.END

async def admin_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    replied_msg_id = update.message.reply_to_message.message_id
    user_id = context.bot_data.get(replied_msg_id)

    if not user_id:
        
        await update.message.reply_text("❌ شناسه‌ی کاربر پیدا نشد.")
        return
        
    else:
        # کپی کردن پیام ادمین برای کاربر
        await context.bot.copy_message(
            chat_id=user_id,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        await update.message.reply_text("با موفقیت ارسال شد")



async def get_ref_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sabt_nam_shode = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:A").execute()
    sabt_nam_shode = sabt_nam_shode.get("values", [])

    if update.effective_user.id in [int(item[0]) for item in sabt_nam_shode]:
            
        user_id = str(update.effective_user.id)
        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start={user_id}"

        if is_hamkar(update.effective_user.id):
            await update.message.reply_text(
                f"🔗 لینک دعوت اختصاصی شما:\n{link}",
                reply_markup=ReplyKeyboardMarkup(award_coworkers_menu, resize_keyboard=True)
            )
        else:
            await update.message.reply_text(
                f"🔗 لینک دعوت اختصاصی شما:\n{link}",
                reply_markup=ReplyKeyboardMarkup(award_menu, resize_keyboard=True)
            )

    else:
        await update.message.reply_text("برای دریافت لینک دعوت، لطفا ابتدا اطلاعات پروفایل خود را کامل کنید")
        return

def is_approved_by_royan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:

    user_approval_list = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet1!A2:Q").execute()
    users_approval = user_approval_list.get("values", [])

    for user in users_approval:
        if user[0] == str(update.effective_user.id):
            approved = user[16] if len(user) > 16 else None
            if approved == "1":
                return True
            else:
                return False
            
            

async def admin_approve_with_national_code_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفا کد ملی کاربران را وارد کنید:\nهرکدوم تو یک خط",
                                    reply_markup=ReplyKeyboardMarkup(enseraf_menu, resize_keyboard=True))
    return SEND_NATIONAL_CODE_ROYAN


async def admin_approve_with_national_code(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        return await admin_approve_with_national_code_cancel(update, context)
    
    national_codes = update.message.text
    national_codes = update.message.text.splitlines()
    users_Ncode = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet1!A2:T"
    ).execute()
    users_Ncode = users_Ncode.get("values", [])

    for user in users_Ncode:
        code = user[5] if len(user) > 5 else None
        name = user[2] if len(user) > 2 else None
        user_id = user[0] if len(user) > 0 else None

        if code in national_codes:
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"sheet1!Q{users_Ncode.index(user)+2}", valueInputOption="USER_ENTERED", body={"values": [[1]]}).execute()

            refferer_id = find_owner_by_ref(user_id)

            if refferer_id:
                increment_refferer_chance(refferer_id)
                
            inviter_id = find_inviter_by_ref(user_id)
            
            if inviter_id:
                increment_inviter_chance(inviter_id)

            try:
                await context.bot.sendMessage(text=f"کاربر: {name} با کدملی: {code} تایید شد.",
                                          chat_id=update.effective_chat.id)
            except Exception as e:
                update.message.reply_text(f"خطا در تایید کاربر با کدملی: {code} خطا: {e}")
                

    await context.bot.sendMessage(text="<b>عملیات تایید کاربران پایان یافت</b>",
                                   reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True),
                                   chat_id=update.effective_chat.id,
                                   parse_mode="HTML")
    return ConversationHandler.END


async def admin_approve_with_national_code_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(text="<b>عملیات تایید کاربران لغو شد</b>",
                                          reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True),
                                          parse_mode="HTML",
                                          chat_id=update.effective_chat.id)
    return ConversationHandler.END



def colnum_to_letter(n):

    result = ""
    while n >= 0:
        result = chr(n % 26 + ord('A')) + result
        n = n // 26 - 1

    return result


def find_owner_by_ref(ref_id):
    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet4!B1:ZZ"
    ).execute().get("values", [])

    if not data:
        return None

    headers = data[0]   # ردیف اول = شناسه‌ی کاربران
    columns = list(zip(*data))  # تبدیل سطرها به ستون‌ها

    # بررسی هر ستون
    for i, col in enumerate(columns):
        if ref_id in col[1:]:  # [1:] یعنی زیر هدر
            
            return headers[i]  # همون شناسه‌ی کاربر

    return None


def increment_refferer_chance(user_id):

    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A2:T"   # ستون A تا T
    ).execute().get("values", [])

    if not data:
        return False

    for i, row in enumerate(data, start=2):
        if len(row) > 0 and row[0] == str(user_id):
            current_value = 0
            if len(row) >= 20 and row[19].isdigit():
                current_value = int(row[19])

            new_value = current_value + 1

            # آپدیت ستون T
            sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=f"Sheet1!T{i}",
                valueInputOption="USER_ENTERED",
                body={"values": [[new_value]]}
            ).execute()

            return True

    return False



def find_inviter_by_ref(ref_id):
    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet5!A1:ZZZ"
    ).execute().get("values", [])

    if not data:
        return None

    headers = data[0]   # ردیف اول = شناسه‌ی کاربران
    columns = list(zip(*data))  # تبدیل سطرها به ستون‌ها

    # بررسی هر ستون
    for i, col in enumerate(columns):
        if ref_id in col[1:]:  # [1:] یعنی زیر هدر
            
            return headers[i]  # همون شناسه‌ی کاربر

    return None


def increment_inviter_chance(user_id):

    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A2:S"   # ستون A تا T
    ).execute().get("values", [])

    if not data:
        return False

    for i, row in enumerate(data, start=2):
        if len(row) > 0 and row[0] == str(user_id):
            current_value = 0
            if len(row) >= 20 and row[19].isdigit():
                current_value = int(row[19])

            new_value = current_value + 1

            # آپدیت ستون S
            sheet.values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=f"Sheet1!S{i}",
                valueInputOption="USER_ENTERED",
                body={"values": [[new_value]]}
            ).execute()

            return True

    return False


def get_refferer_chance(user_id):
    
    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A2:T"
    ).execute().get("values", [])

    for i, row in enumerate(data, start=2):
        if len(row) > 0 and row[0] == str(user_id):
          
            if len(row) > 19:
                return row[19]
            else:
                return None

    return None


global kargah

async def admin_register_participants_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(text="لطفا کارگاهی که میخواهید افراد را در آن ثبت نام کنید انتخاب کنید:",
                                   chat_id=update.effective_chat.id,
                                   reply_markup=ReplyKeyboardMarkup(kargah_ha_keys, resize_keyboard=True))
    return GET_KARGAH_NAME


async def admin_register_participants_getNcode(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.text == "انصراف❌":
        await admin_register_participants_cancel(update, context)
        return ConversationHandler.END

    global kargah
    kargah = update.message.text
    
    await context.bot.sendMessage(text="لطفا کد ملی شرکت‌کنندگان را ارسال کنید:",
                                   chat_id=update.effective_chat.id,
                                   reply_markup=ReplyKeyboardMarkup(enseraf_menu , resize_keyboard=True))
    return GET_NCODES


async def admin_register_participants_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    add_workshop_to_users(update.message.text)

    await context.bot.sendMessage(text="عملیات ثبت نام با موفقیت انجام شد.",
                                   chat_id=update.effective_chat.id,
                                   reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
    return ConversationHandler.END


async def admin_register_participants_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.sendMessage(text="عملیات ثبت نام لغو شد.",
                                   chat_id=update.effective_chat.id,
                                   reply_markup=ReplyKeyboardMarkup(admin_keys, resize_keyboard=True))
    return ConversationHandler.END


def add_workshop_to_users(national_codes_text):

    national_codes = [code.strip() for code in national_codes_text.splitlines() if code.strip()]

    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A2:R"
    ).execute().get("values", [])

    updated_users = []

    for i, row in enumerate(data, start=2):
        if len(row) > 5:
            national_code = row[5]
            if national_code in national_codes:

                workshops = row[17] if len(row) > 17 else ""

                workshops_list = [w.strip() for w in workshops.split(",") if w.strip()]

                if str(kargah) not in workshops_list:
                    workshops_list.append(str(kargah))

                new_value = ",".join(workshops_list)

                sheet.values().update(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=f"Sheet1!R{i}",
                    valueInputOption="USER_ENTERED",
                    body={"values": [[new_value]]}
                ).execute()

                updated_users.append(national_code)


def is_in_workshop(update: Update, context: ContextTypes.DEFAULT_TYPE, kargah_user) -> bool:

    user_data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet1!A2:R"
    ).execute()
    user_data = user_data.get("values", [])

    for row in user_data:
        if row[0] == str(update.effective_user.id):
            workshops = row[17] if len(row) > 17 else ""
            workshops_list = [w.strip() for w in workshops.split(",") if w.strip()]
            if kargah_user in workshops_list:
                return True
            else:
                return False
    return False


    """gpt chat
    """
async def gpt_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چت با هوش مصنوعی شروع شد. لطفا پیام خود را ارسال کنید:",
                                    reply_markup=ReplyKeyboardMarkup([["انصراف❌"]], resize_keyboard=True))
    return GPT_CHAT


async def gpt_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_message == "انصراف❌":
        await gpt_chat_end(update, context)
        return ConversationHandler.END

    if get_user_cupon(user_id) < 1:
        await update.message.reply_text("شما اعتبار کافی برای استفاده از این سرویس را ندارید.\n24 ساعت دیگر می‌توانید دوباره امتحان کنید.")
        await gpt_chat_end(update, context)
        return ConversationHandler.END

    # آماده‌سازی تاریخچه
    if user_id not in chat_history:
        chat_history[user_id] = []

    history_text = "\n".join(
        f"کاربر: {u}\nهوش مصنوعی: {g}" for u, g in chat_history[user_id]
    )
    SYSTEM_PROMPT_PERMANENT = get_system_prompt()
    full_prompt = (
        SYSTEM_PROMPT_PERMANENT
        + ("\n\n" + history_text if history_text else "")
        + f"\nکاربر: {user_message}\nهوش مصنوعی:"
    )

    try:
        client = OpenAI(
        base_url=LIARA_base_url,
        api_key=config('LIARA_API_KEY'),
        )

        completion = client.chat.completions.create(
        model="openai/gpt-5-nano",
        messages=[
            {
            "role": "user",
            "content": f'{full_prompt}'
            }
        ]
        )
        gpt_reply = completion.choices[0].message.content
        
    except Exception as e:
        gpt_reply = "خطا در ارتباط با هوش مصنوعی"
        print(f"Error occurred while communicating with هوش مصنوعی: {e}")

    await send_long_message(update, gpt_reply)
    users_cupon[user_id]['value'] -= 1
    print(f"User {user_id} remaining cupon: {users_cupon[user_id]['value']}")

    chat_history[user_id].append((user_message, gpt_reply))
    if len(chat_history[user_id]) > 20:
        chat_history[user_id] = chat_history[user_id][-20:]

    return GPT_CHAT


async def gpt_chat_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in chat_history:
        del chat_history[user_id]
    await update.message.reply_text("چت با هوش مصنوعی پایان یافت.",
                                    reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
    return ConversationHandler.END

    """gpt chat
    """




    """deepseek
    """
async def deepseek_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چت با هوش مصنوعی شروع شد. لطفا پیام خود را ارسال کنید:",
                                    reply_markup=ReplyKeyboardMarkup([["انصراف❌"]], resize_keyboard=True))
    return DEEPSEEK_CHAT


async def deepseek_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_message == "انصراف❌":
        await deepseek_chat_end(update, context)
        return ConversationHandler.END
    
    if get_user_cupon(user_id) < 1:
        await update.message.reply_text("شما اعتبار کافی برای استفاده از این سرویس را ندارید.\n24 ساعت دیگر می‌توانید دوباره امتحان کنید.")
        await gpt_chat_end(update, context)
        return ConversationHandler.END

    # آماده‌سازی تاریخچه
    if user_id not in chat_history:
        chat_history[user_id] = []

    history_text = "\n".join(
        f"کاربر: {u}\nهوش مصنوعی: {g}" for u, g in chat_history[user_id]
    )
    SYSTEM_PROMPT_PERMANENT = get_system_prompt()
    full_prompt = (
        SYSTEM_PROMPT_PERMANENT
        + ("\n\n" + history_text if history_text else "")
        + f"\nکاربر: {user_message}\nهوش مصنوعی:"
    )

    try:
        client = OpenAI(
        base_url=LIARA_base_url,
        api_key=config('LIARA_API_KEY'),
        )

        completion = client.chat.completions.create(
        model="deepseek/deepseek-r1-distill-llama-70b",
        messages=[
            {
            "role": "user",
            "content": f'{full_prompt}'
            }
        ]
        )
        gpt_reply = completion.choices[0].message.content
        
    except Exception as e:
        gpt_reply = "خطا در ارتباط با هوش مصنوعی"
        print(f"Error occurred while communicating with هوش مصنوعی: {e}")

    await send_long_message(update, gpt_reply)
    users_cupon[user_id]['value'] -= 1
    print(f"User {user_id} remaining cupon: {users_cupon[user_id]['value']}")

    chat_history[user_id].append((user_message, gpt_reply))
    if len(chat_history[user_id]) > 20:
        chat_history[user_id] = chat_history[user_id][-20:]

    return DEEPSEEK_CHAT


async def deepseek_chat_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in chat_history:
        del chat_history[user_id]
    await update.message.reply_text("چت با هوش مصنوعی پایان یافت.",
                                    reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
    return ConversationHandler.END

    """deepseek
    """
    
    
    

    """Grok
    """
async def grok_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("چت با هوش مصنوعی شروع شد. لطفا پیام خود را ارسال کنید:",
                                    reply_markup=ReplyKeyboardMarkup([["انصراف❌"]], resize_keyboard=True))
    return GROK_CHAT


async def grok_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_message == "انصراف❌":
        await grok_chat_end(update, context)
        return ConversationHandler.END
    
    if get_user_cupon(user_id) < 1:
        await update.message.reply_text("شما اعتبار کافی برای استفاده از این سرویس را ندارید.\n24 ساعت دیگر می‌توانید دوباره امتحان کنید.")
        await gpt_chat_end(update, context)
        return ConversationHandler.END

    # آماده‌سازی تاریخچه
    if user_id not in chat_history:
        chat_history[user_id] = []

    history_text = "\n".join(
        f"کاربر: {u}\nهوش مصنوعی: {g}" for u, g in chat_history[user_id]
    )
    SYSTEM_PROMPT_PERMANENT = get_system_prompt()
    full_prompt = (
        SYSTEM_PROMPT_PERMANENT
        + ("\n\n" + history_text if history_text else "")
        + f"\nکاربر: {user_message}\nهوش مصنوعی:"
    )

    try:
        client = OpenAI(
        base_url=LIARA_base_url,
        api_key=config('LIARA_API_KEY'),
        )

        completion = client.chat.completions.create(
        model="x-ai/grok-3-mini-beta",
        messages=[
            {
            "role": "user",
            "content": f'{full_prompt}'
            }
        ]
        )
        gpt_reply = completion.choices[0].message.content
        
    except Exception as e:
        gpt_reply = "خطا در ارتباط با هوش مصنوعی"
        print(f"Error occurred while communicating with هوش مصنوعی: {e}")

    await send_long_message(update, gpt_reply)
    users_cupon[user_id]['value'] -= 1
    print(f"User {user_id} remaining cupon: {users_cupon[user_id]['value']}")

    chat_history[user_id].append((user_message, gpt_reply))
    if len(chat_history[user_id]) > 20:
        chat_history[user_id] = chat_history[user_id][-20:]

    return GROK_CHAT


async def grok_chat_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in chat_history:
        del chat_history[user_id]
    await update.message.reply_text("چت با هوش مصنوعی پایان یافت.",
                                    reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
    return ConversationHandler.END

    """Grok
    """   
   
   
   
    
def is_hamkar(user_id):
    hamkaran = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="sheet4!B1:JZ").execute()
    hamkaran = hamkaran.get("values", [])

    for hamkar in hamkaran:
        if str(user_id) in str(hamkar):
            return True
    return False


def get_inviteds(user_id):
    data = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="Sheet1!A2:T"
    ).execute().get("values", [])
    
    for row in data:
        try:
            if len(row) > 0 and row[0] == str(user_id):
                inviteds = row[18]

                return int(inviteds)
        except Exception as e:
            print(f"Error occurred while getting inviteds for user {user_id}: {e}")
    return 0



def get_user_cupon(user_id):
    current_time = time.time()
    invite_status = get_inviteds(str(user_id))
    mahdodiat = 0
    
    if invite_status >= 5:
        mahdodiat = 75
    elif invite_status >= 3:
        mahdodiat = 50
    else:
        mahdodiat = 25       
    
    if user_id not in users_cupon:
        # کاربر جدید
        users_cupon[user_id] = {"value": mahdodiat, "last_update": current_time}
        return users_cupon[user_id]["value"]

    user = users_cupon[user_id]

    # بررسی کنیم آیا 24 ساعت گذشته؟
    if current_time - user["last_update"] >= 24 * 60 * 60:
        user["value"] = mahdodiat
        user["last_update"] = current_time

    return user["value"]


def add_user_id_in_row(user_id: str):
    """آیدی کاربر را در سطر 1 و آخرین ستون خالی اضافه می‌کند (اگر وجود نداشته باشد)"""
    result = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet5!A1:ZZZ"
    ).execute()
    
    values = result.get("values", [[]])
    row_values = values[0] if values else []

    # بررسی وجود کاربر
    if str(user_id) in row_values:
        return
    
    # اضافه کردن به انتهای سطر
    row_values.append(str(user_id))

    sheet.values().update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        range="sheet5!A1:ZZZ",
        valueInputOption="USER_ENTERED",
        body={"values": [row_values]}
    ).execute()


    
kargah_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ثبت افراد در کارگاه ها$"), admin_register_participants_start)],
    states={
        GET_KARGAH_NAME: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_register_participants_getNcode)],
        GET_NCODES: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_register_participants_end)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), admin_register_participants_cancel)],
)


feedback_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^پیام به ادمین💬$"), feedback_start)],
    states={
        FEEDBACK_MESSAGE: [MessageHandler(filters.ALL & ~filters.COMMAND, feedback_message)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), feedback_cancel)],
)


AI_chat_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Gemini$"), ai_chat_start)],
    states={
        AI_CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ai_chat)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), ai_chat_end)],
)


GPT_chat_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ChatGPT$"), gpt_chat_start)],
    states={
        GPT_CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_chat)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), gpt_chat_end)],
)


deepseek_chat_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^DeepSeek$"), deepseek_chat_start)],
    states={
        DEEPSEEK_CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deepseek_chat)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), deepseek_chat_end)],
)


grok_chat_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^Grok$"), grok_chat_start)],
    states={
        GROK_CHAT: [MessageHandler(filters.TEXT & ~filters.COMMAND, grok_chat)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), grok_chat_end)],
)


broadcast_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ارسال پیام همگانی$"), message_get)],
    states={
        SEND_TO_ALL: [MessageHandler(filters.ALL & ~filters.COMMAND, send_to_all)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), edit_profile_cancel)],
)

admin_approve_with_national_code_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^تایید ثبت نام رویان با کدملی$"), admin_approve_with_national_code_start)],
    states={
        SEND_NATIONAL_CODE_ROYAN: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_approve_with_national_code)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), admin_approve_with_national_code_cancel)],
)

admin_send_with_national_code = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ارسال پیام به کاربران با کد ملی$"), admin_send_national_code_start)],
    states={
        SEND_NATIONAL_CODE: [MessageHandler(filters.ALL & ~filters.COMMAND, admin_send_national_code)],
        SEND_NATIONAL_CODE_GETMESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, admin_send_national_code_getmessage)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), admin_send_national_code_cancel)],
)

edit_profile_conv = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ویرایش/ورود اطلاعات✍️$"), edit_profile_start)],
    states={
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_gender)],
        NAME_AND_LASTNAME_FARSI: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_name_and_lastname_farsi)],
        NAME_AND_LAST_NAME_ENGLISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_name_and_lastname_english)],
        BIRTH_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_birth_date)],
        NATIONAL_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_national_code)],
        PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_phone_number)],
        FIELD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_field)],
        SPECIALIZATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_specialization)],
        EDUCATION_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_education_level)],
        TERM_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_term_number)],
        UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_university)],
        ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_address)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_profile_email)],
    },
    fallbacks=[MessageHandler(filters.Regex("^انصراف❌$"), edit_profile_cancel)],
)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'update {update} caused error {context.error}')


if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    print("Bot is starting...")
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("register", register_command))
    application.add_handler(broadcast_conv)
    application.add_handler(admin_send_with_national_code)
    application.add_handler(admin_approve_with_national_code_conv)
    application.add_handler(kargah_conv)
    application.add_handler(edit_profile_conv)
    application.add_handler(feedback_conv)
    application.add_handler(AI_chat_conv)
    application.add_handler(GPT_chat_conv)
    application.add_handler(deepseek_chat_conv)
    application.add_handler(grok_chat_conv)
    application.add_handler(CommandHandler("admin", admin_handler))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, menu_handler))
    application.add_error_handler(error_handler)
    print("Bot is polling...")
    application.run_polling()
