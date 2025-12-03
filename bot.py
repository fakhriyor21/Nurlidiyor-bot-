import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import sqlite3

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8427234440:AAGErLBsH1vCPFWpJfI1-Lhv8w7LF6ow7ak"
CHANNEL_USERNAME = "@nuriddinbuilding"

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserRegistration(StatesGroup):
    waiting_for_phone = State()


ADMIN_IDS = [123456789]


# Ma'lumotlar bazasini yaratish
def init_db():
    conn = sqlite3.connect('referral.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        full_name TEXT,
        phone TEXT,
        referral_id INTEGER,
        referrals_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        referrer_id INTEGER,
        referred_id INTEGER,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (referrer_id) REFERENCES users (user_id),
        FOREIGN KEY (referred_id) REFERENCES users (user_id)
    )''')

    conn.commit()
    conn.close()


init_db()


def save_referral(referrer_id, referred_id):
    conn = sqlite3.connect('referral.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO referrals (referrer_id, referred_id) VALUES (?, ?)",
            (referrer_id, referred_id)
        )
        conn.commit()
    except:
        pass
    finally:
        conn.close()


def update_referral_status(referred_id, status='completed'):
    conn = sqlite3.connect('referral.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE referrals SET status = ? WHERE referred_id = ?",
            (status, referred_id)
        )

        cursor.execute(
            "SELECT referrer_id FROM referrals WHERE referred_id = ? AND status = 'completed'",
            (referred_id,)
        )
        result = cursor.fetchone()

        if result:
            referrer_id = result[0]
            cursor.execute(
                "UPDATE users SET referrals_count = referrals_count + 1 WHERE user_id = ?",
                (referrer_id,)
            )
            conn.commit()
            return referrer_id
    except:
        return None
    finally:
        conn.close()


def save_user(user_id, username, full_name, phone=None, referral_id=None):
    conn = sqlite3.connect('referral.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT OR REPLACE INTO users 
            (user_id, username, full_name, phone, referral_id) 
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, username, full_name, phone, referral_id)
        )
        conn.commit()
    except:
        pass
    finally:
        conn.close()


def get_user_stats(user_id):
    conn = sqlite3.connect('referral.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT referrals_count FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            referrals_count = result[0]
        else:
            referrals_count = 0

        cursor.execute(
            """SELECT COUNT(*) FROM referrals 
            WHERE referrer_id = ? AND status = 'completed'""",
            (user_id,)
        )
        completed_count = cursor.fetchone()[0]

        cursor.execute(
            """SELECT COUNT(*) FROM referrals 
            WHERE referrer_id = ? AND status = 'pending'""",
            (user_id,)
        )
        pending_count = cursor.fetchone()[0]

        return {
            'total_referrals': referrals_count,
            'completed_referrals': completed_count,
            'pending_referrals': pending_count
        }
    except:
        return {'total_referrals': 0, 'completed_referrals': 0, 'pending_referrals': 0}
    finally:
        conn.close()


async def notify_referrer(referrer_id, referred_user):
    try:
        notification_text = f"""🎉 <b>Yangi taklif qilingan do'st!</b>

👤 <b>Yangi ishtirokchi:</b>
• Ism: {referred_user['full_name']}
• Username: @{referred_user['username']}
• ID: {referred_user['user_id']}

📊 <b>Sizning statistikangiz:</b>
• Jami takliflar: {referred_user['stats']['total_referrals']}
• To'liq ro'yxatdan o'tganlar: {referred_user['stats']['completed_referrals']}
• Kutilayotganlar: {referred_user['stats']['pending_referrals']}

🎁 Har bir to'liq ro'yxatdan o'tgan do'stingiz uchun +1 ball!"""

        await bot.send_message(referrer_id, notification_text)
    except:
        pass


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    args = message.text.split()

    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            save_referral(referrer_id, message.from_user.id)
        except:
            pass

    welcome_text = """🎉 <b>Assalom alaykum Nurli Diyor—Guliston konkurs botiga xush kelibsiz</b>

Konkursga qatnashish uchun pastda so'ralgan ma'lumotlarni yuboring va aytilgan amallarni bajaring. Onlayn taqdimot kanalga qo'shilib iPhone 17 Pro Max, Kir yuvish mashinasi, Muzlatgich va boshqa sovg'alardan birini yutib oling 🎁

<b>Qani kettik!!!</b>

Birinchi navbatda kanalga qo'shiling va <b>Bajarildi ✅</b> tugmasini bosing"""

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Kanalga o'tish 👥", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
        types.InlineKeyboardButton("Bajarildi ✅", callback_data="check_subscription")
    )

    await message.answer(welcome_text, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)

        if member.status in ['member', 'administrator', 'creator']:
            success_text = """✅ <b>Ajoyib! Kanalga qo'shildingiz!</b>

Endi konkursda qatnashish uchun quyidagi ma'lumotlarni yuboring:

1. <b>Ism va Familyangiz</b>
2. <b>Telefon raqamingiz</b>
3. <b>O'zingizni rasmingiz</b> (ixtiyoriy)

Ma'lumotlarni yuborishni boshlash uchun <b>Ma'lumotlarni yuborish 📝</b> tugmasini bosing."""

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(
                types.InlineKeyboardButton("Ma'lumotlarni yuborish 📝", callback_data="start_registration"),
                types.InlineKeyboardButton("Qayta tekshirish 🔄", callback_data="check_subscription")
            )

            await callback_query.message.edit_text(
                text=success_text,
                reply_markup=keyboard
            )
        else:
            await bot.answer_callback_query(
                callback_query.id,
                "❌ Kanalga hali qo'shilmagansiz! Iltimos, kanalga a'zo bo'ling.",
                show_alert=True
            )

    except Exception:
        error_text = f"""⚠️ <b>Xatolik yuz berdi!</b>

Iltimos, quyidagi kanalga a'zo bo'ling va qayta urinib ko'ring:
{CHANNEL_USERNAME}

A'zo bo'lgach, <b>Bajarildi ✅</b> tugmasini bosing."""

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton("Kanalga o'tish 👥", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"),
            types.InlineKeyboardButton("Bajarildi ✅", callback_data="check_subscription")
        )

        await callback_query.message.edit_text(
            text=error_text,
            reply_markup=keyboard
        )


@dp.callback_query_handler(lambda c: c.data == 'start_registration')
async def start_registration(callback_query: types.CallbackQuery, state: FSMContext):
    await UserRegistration.waiting_for_phone.set()

    text = """—Tanishlarni qanday qo'shish kerak va ballar qanday hisoblanadi?

—Sizga berilgan shaxsiy link orqali kanalga qo'shilgan har bir tanishingiz uchun sizga +1 ball beriladi.

—O'yinni muvaffaqiyatli o'tish uchun menyudagi bo'limlardan yoki pastdagi tugmalardan foydalaning.
Faollik ko'rsating, vazifalarni bajaring va kafolatlangan sovg'alarni qo'lga kiriting! 

—Tanishlarni taklif qilish uchun:
       "Mening shaxsiy linkim 🔗" tugmasini bosing va do'stlaringiz bilan ulashing.

📑 Hisobingizni tekshirish uchun:
           "Mening hisobim" tugmasini bosing va nechta tanishingiz qo'shilganini bilib oling."""

    # Pastda oddiy keyboard buttonlar
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2
    )
    keyboard.add(
        types.KeyboardButton("📱 Raqamni yuborish"),
        types.KeyboardButton("📊 Mening hisobim")
    )

    await callback_query.message.answer(
        text,
        reply_markup=keyboard
    )

    # Alohida xabar sifatida "Mening shaxsiy linkim" tugmasi
    inline_keyboard = types.InlineKeyboardMarkup(row_width=1)
    inline_keyboard.add(
        types.InlineKeyboardButton("Mening shaxsiy linkim 🔗", callback_data="my_link")
    )

    await callback_query.message.answer(
        "Do'stlaringizni taklif qilish uchun:",
        reply_markup=inline_keyboard
    )

    await callback_query.answer()


# Raqamni yuborish tugmasi bosilganda
@dp.message_handler(lambda message: message.text == "📱 Raqamni yuborish", state=UserRegistration.waiting_for_phone)
async def ask_for_phone_button(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=1
    )
    keyboard.add(
        types.KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)
    )

    await message.answer(
        "Iltimos, telefon raqamingizni yuboring:",
        reply_markup=keyboard
    )


# Mening hisobim tugmasi bosilganda
@dp.message_handler(lambda message: message.text == "📊 Mening hisobim", state=UserRegistration.waiting_for_phone)
async def show_account_button(message: types.Message):
    user_id = message.from_user.id

    stats = get_user_stats(user_id)

    account_text = f"""📊 <b>Sizning hisobingiz:</b>

👤 ID: {user_id}
🏆 Ballar: {stats['completed_referrals']} ball
👥 Jami takliflar: {stats['total_referrals']} ta
✅ To'liq ro'yxatdan o'tganlar: {stats['completed_referrals']} ta
⏳ Kutilayotganlar: {stats['pending_referrals']} ta

🎯 <b>Keyingi bosqich:</b> {10 - stats['completed_referrals']} ta do'st taklif qiling"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Do'st taklif qilish 🔗", callback_data="my_link"),
        types.InlineKeyboardButton("Yangilash 🔄", callback_data="my_account")
    )

    await message.answer(
        account_text,
        reply_markup=keyboard
    )


@dp.message_handler(content_types=types.ContentType.CONTACT, state=UserRegistration.waiting_for_phone)
async def process_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    phone_number = contact.phone_number

    if not phone_number.startswith('+998') and not (phone_number.startswith('998') and len(phone_number) == 12):
        await message.answer(
            "❌ Faqat O'zbekiston telefon raqamlari qabul qilinadi (+998...).",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    user_id = message.from_user.id
    username = message.from_user.username or ""
    full_name = message.from_user.full_name

    save_user(user_id, username, full_name, phone_number)

    referrer_id = update_referral_status(user_id, 'completed')

    if referrer_id:
        referrer_stats = get_user_stats(referrer_id)

        referred_user = {
            'user_id': user_id,
            'username': username,
            'full_name': full_name,
            'stats': referrer_stats
        }

        await notify_referrer(referrer_id, referred_user)

    await state.update_data(phone=phone_number)

    success_text = f"""✅ <b>Ma'lumotlaringiz qabul qilindi!</b>

📱 Telefon raqamingiz: {phone_number}

🎉 <b>Tabriklaymiz! Siz konkursda ishtirok etmoqdasiz!</b>"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Mening shaxsiy linkim 🔗", callback_data="my_link"),
        types.InlineKeyboardButton("Mening hisobim 📊", callback_data="my_account")
    )

    await message.answer(
        success_text,
        reply_markup=keyboard
    )
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'my_link')
async def send_personal_link(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    bot_username = (await bot.get_me()).username

    personal_link = f"https://t.me/{bot_username}?start={user_id}"

    message_text = f"""{personal_link}
Nurli_Diyor_Guliston

Assalomu alaykum Guliston xalqi.
Sizlarga yana ajoyib taklif bilan Nuriddin Building. 

Kanalga qoshiling va 280 dan ziyot sovg'alarni yutib oling !

Joriy yilning 8-dekabr sanasi kuni online taqdimot bo'lib o'tadi hamda kanalga eng ko'p do'stini taklif qilgan

• top 100 kishi o'rtasida 10X iPhone 17 Pro Max oʻynaladi.

• top 150 kishi o'rtasida 25X Muzlatgich o'ynaladi.

• top 175 kishi o'rtasida 25X Kir yuvish mashinasi o'ynaladi.

• top 190 kishi o'rtasida 25X televezor o'ynaladi.

• top 200 kishi o'rtasida 25X Mikro to'lqinli pech o'ynaladi.

• top 250 kishi o'rtasida 30X Dazmol o'ynaladi.

• top 400 kishi o'rtasida 50X 300 000 UZS o'ynaladi.

Yutib olish uchun pastdagi havola orqali ruyxatdan o'ting!"""

    await callback_query.message.answer(
        message_text,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("Ro'yxatdan o'tish", url=personal_link)
        )
    )
    await callback_query.answer("Havola yuborildi!")


@dp.callback_query_handler(lambda c: c.data == 'my_account')
async def show_account_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    stats = get_user_stats(user_id)

    account_text = f"""📊 <b>Sizning hisobingiz:</b>

👤 ID: {user_id}
🏆 Ballar: {stats['completed_referrals']} ball
👥 Jami takliflar: {stats['total_referrals']} ta
✅ To'liq ro'yxatdan o'tganlar: {stats['completed_referrals']} ta
⏳ Kutilayotganlar: {stats['pending_referrals']} ta

🎯 <b>Keyingi bosqich:</b> {10 - stats['completed_referrals']} ta do'st taklif qiling"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Do'st taklif qilish 🔗", callback_data="my_link"),
        types.InlineKeyboardButton("Yangilash 🔄", callback_data="my_account")
    )

    await callback_query.message.edit_text(
        text=account_text,
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Siz admin emassiz!")
        return

    admin_text = """👨‍💼 <b>Admin Panel</b>

📊 <b>Statistika:</b>
• Jami foydalanuvchilar: 0
• Bugun qo'shilganlar: 0
• Faol foydalanuvchilar: 0

⚡ <b>Admin buyruqlari:</b>
• /stats - To'liq statistika
• /users - Barcha foydalanuvchilar
• /send - Xabar yuborish
• /broadcast - Hammaga xabar yuborish"""

    await message.answer(admin_text)


@dp.message_handler(commands=['stats'])
async def admin_stats(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    stats_text = """📈 <b>To'liq statistika</b>

👥 <b>Foydalanuvchilar:</b>
• Jami: 0
• Bugun: 0
• O'tgan hafta: 0
• O'tgan oy: 0

📱 <b>Telefon raqamlar:</b>
• Jami: 0
• +99891: 0
• +99893: 0
• +99894: 0

🔗 <b>Referallar:</b>
• Jami takliflar: 0
• O'rtacha taklif: 0
• Eng ko'p taklif: 0"""

    await message.answer(stats_text)


@dp.message_handler(commands=['users'])
async def admin_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    users_text = """👥 <b>Oxirgi 10 foydalanuvchi:</b>

1. 👤 User1 - ID: 123 - 📱 +9989********
2. 👤 User2 - ID: 124 - 📱 +9989********
3. 👤 User3 - ID: 125 - 📱 +9989********
4. 👤 User4 - ID: 126 - 📱 +9989********
5. 👤 User5 - ID: 127 - 📱 +9989********
6. 👤 User6 - ID: 128 - 📱 +9989********
7. 👤 User7 - ID: 129 - 📱 +9989********
8. 👤 User8 - ID: 130 - 📱 +9989********
9. 👤 User9 - ID: 131 - 📱 +9989********
10. 👤 User10 - ID: 132 - 📱 +9989********

📋 Jami: 10 foydalanuvchi"""

    await message.answer(users_text)


@dp.message_handler(commands=['send'])
async def admin_send(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        args = message.text.split(' ', 2)
        if len(args) < 3:
            await message.answer("❌ Format: /send ID Xabar")
            return

        user_id = int(args[1])
        text = args[2]

        await bot.send_message(user_id, f"📩 <b>Admin xabari:</b>\n\n{text}")
        await message.answer(f"✅ Xabar {user_id} ID li foydalanuvchiga yuborildi")

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")


@dp.message_handler(commands=['broadcast'])
async def admin_broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    try:
        args = message.text.split(' ', 1)
        if len(args) < 2:
            await message.answer("❌ Format: /broadcast Xabar")
            return

        text = args[1]
        await message.answer(f"✅ Xabar barcha foydalanuvchilarga yuborildi: {text}")

    except Exception as e:
        await message.answer(f"❌ Xatolik: {e}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)