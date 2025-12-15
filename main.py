import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from datetime import datetime
import json
import os

# Bot konfiguratsiyasi
API_TOKEN = '8290045354:AAE8tfNP4ZUVz2qICwex_K_vNxbSMwhH9sA'
CHANNEL_ID = '@testlar231'
CHANNEL_LINK = 'https://t.me/testlar231'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Ma'lumotlarni saqlash
TESTS_FILE = 'tests_db.json'
USERS_FILE = 'users_db.json'
REGISTRATIONS_FILE = 'registrations_db.json'

# Viloyatlar va tumanlar ro'yxati
REGIONS = {
    "Toshkent": ["Olmazor", "Bektemir", "Mirobod", "Mirzo Ulug'bek", "Sergeli", "Shayxontohur", "Chilonzor",
                 "Yashnobod", "Yakkasaroy", "Yunusobod"],
    "Andijon": ["Andijon shahri", "Asaka", "Baliqchi", "Bo'ston", "Buloqboshi", "Izboskan", "Jalaquduq", "Marhamat",
                "Oltinko'l", "Paxtaobod", "Qo'rg'ontepa", "Shahrixon", "Ulug'nor", "Xo'jaobod"],
    "Buxoro": ["Buxoro shahri", "Olot", "Buxoro tumani", "G'ijduvon", "Jondor", "Kogon", "Qorako'l", "Qorovulbozor",
               "Peshku", "Romitan", "Shofirkon", "Vobkent"],
    "Farg'ona": ["Farg'ona shahri", "Beshariq", "Bog'dod", "Buvayda", "Dang'ara", "Furqat", "Oltiariq", "Qo'shtepa",
                 "Quva", "Rishton", "So'x", "Toshloq", "Uchko'prik", "Yozyovon"],
    "Jizzax": ["Jizzax shahri", "Arnasoy", "Baxmal", "Do'stlik", "Forish", "G'allaorol", "Jizzax tumani", "Mirzacho'l",
               "Paxtakor", "Yangiobod", "Zafarobod", "Zarbdor", "Zomin"],
    "Xorazm": ["Urganch shahri", "Bog'ot", "Gurlan", "Qo'shko'pir", "Shovot", "Tuproqqala", "Urganch tumani",
               "Xazorasp", "Xiva", "Xonqa", "Yangiariq", "Yangibozor"],
    "Namangan": ["Namangan shahri", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Namangan tumani", "Norin", "Pop",
                 "To'raqo'rg'on", "Uchqo'rg'on", "Uychi", "Yangiqo'rg'on"],
    "Navoiy": ["Navoiy shahri", "Karmana", "Konimex", "Navbahor", "Nurota", "Qiziltepa", "Tomdi", "Uchquduq",
               "Xatirchi", "Zarafshon"],
    "Qashqadaryo": ["Qarshi shahri", "Chiroqchi", "Dehqonobod", "G'uzor", "Kasbi", "Kitob", "Koson", "Mirishkor",
                    "Muborak", "Nishon", "Qamashi", "Qarshi tumani", "Shahrisabz", "Yakkabog'"],
    "Samarqand": ["Samarqand shahri", "Bulung'ur", "Ishtixon", "Jomboy", "Kattaqo'rg'on", "Narpay", "Nurabod",
                  "Oqdaryo", "Paxtachi", "Payariq", "Pastdarg'om", "Samarqand tumani", "Toyloq", "Urgut"],
    "Sirdaryo": ["Guliston shahri", "Boyovut", "Guliston tumani", "Mirzaobod", "Oqoltin", "Sardoba", "Sayxunobod",
                 "Sirdaryo tumani", "Xovos"],
    "Surxondaryo": ["Termiz shahri", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo'rg'on", "Muzrabot", "Oltinsoy",
                    "Qiziriq", "Qumqo'rg'on", "Sariosiyo", "Sherobod", "Sho'rchi", "Termiz tumani", "Uzun"],
    "Toshkent viloyati": ["Angren", "Bekobod", "Bo'ka", "Bo'stonliq", "Chinoz", "Oqqo'rg'on", "Ohangaron", "Olmaliq",
                          "Parkent", "Piskent", "Qibray", "Quyi chirchiq", "O'rta chirchiq", "Toshkent tumani",
                          "Yangiyo'l", "Yuqori chirchiq", "Zangiota"],
    "Qoraqalpog'iston": ["Nukus shahri", "Amudaryo", "Beruniy", "Chimboy", "Ellikqala", "Kegeyli", "Mo'ynoq",
                         "Nukus tumani", "Qonliko'l", "Qo'ng'irot", "Shumanay", "Taxtako'pir", "To'rtko'l", "Xo'jayli"]
}


def load_data():
    """Ma'lumotlarni fayldan yuklash"""
    global tests_db, user_results, registrations
    try:
        if os.path.exists(TESTS_FILE):
            with open(TESTS_FILE, 'r', encoding='utf-8') as f:
                tests_db = json.load(f)
        else:
            tests_db = {}

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                user_results = json.load(f)
        else:
            user_results = {}

        if os.path.exists(REGISTRATIONS_FILE):
            with open(REGISTRATIONS_FILE, 'r', encoding='utf-8') as f:
                registrations = json.load(f)
        else:
            registrations = {}
    except Exception as e:
        print(f"📂 Ma'lumotlarni yuklashda xatolik: {e}")
        tests_db = {}
        user_results = {}
        registrations = {}


def save_data():
    """Ma'lumotlarni faylga saqlash"""
    try:
        with open(TESTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tests_db, f, ensure_ascii=False, indent=2)

        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_results, f, ensure_ascii=False, indent=2)

        with open(REGISTRATIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(registrations, f, ensure_ascii=False, indent=2)
        print("💾 Ma'lumotlar saqlandi")
    except Exception as e:
        print(f"❌ Ma'lumotlarni saqlashda xatolik: {e}")


# Dastlabki ma'lumotlarni yuklash
load_data()

# Adminlar ro'yxati
ADMINS = [6777571934]

# Ro'yxatdan o'tish bosqichlari
user_registration = {}

# Test javoblari uchun yangi interaktiv usul
user_test_states = {}

# Test qo'shish bosqichlari
admin_test_states = {}


# Asosiy klaviatura
def main_keyboard(user_id=None):
    """Asosiy klaviatura yaratish"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("🎯 Test topshirish"),
        KeyboardButton("📊 Mening natijalarim"),
        KeyboardButton("⭐ Reyting"),
        KeyboardButton("ℹ️ Yordam")
    ]

    # Agar user_id berilgan bo'lsa va admin bo'lsa
    if user_id and int(user_id) in ADMINS:
        buttons.append(KeyboardButton("👨‍🏫 Admin panel"))

    keyboard.add(*buttons)
    return keyboard


# Admin klaviatura
def admin_keyboard():
    """Admin klaviaturasi"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("➕ Test javoblarini kiritish"),
        KeyboardButton("📋 Mening testlarim"),
        KeyboardButton("🗑️ Test o'chirish"),
        KeyboardButton("📊 Statistika"),
        KeyboardButton("🏠 Bosh menyu"),
        KeyboardButton("👥 Foydalanuvchilar")
    ]
    keyboard.add(*buttons)
    return keyboard


# Start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Botni ishga tushirish"""
    user_id = str(message.from_user.id)

    # Foydalanuvchini qayd etish
    if user_id not in user_results:
        user_results[user_id] = {
            'username': message.from_user.username or message.from_user.full_name,
            'full_name': message.from_user.full_name,
            'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tests_taken': 0,
            'total_score': 0,
            'tests': {},
            'registered': False,
            'region': '',
            'district': ''
        }
        save_data()

    # Kanallikni tekshirish
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if chat_member.status not in ['left', 'kicked']:
            await message.answer(
                "🎉 **TestBotga xush kelibsiz!** 🌟\n\n"
                "🤖 **Bu bot orqali siz:**\n"
                "• 📚 PDF testlarni topshirishingiz mumkin\n"
                "• 📊 Natijalaringizni ko'rishingiz mumkin\n"
                "• ⭐ Reytingda o'ringa ega bo'lishingiz mumkin\n\n"
                "👇 **Test topshirish usullari:**\n"
                "1️⃣ **Bosqichma-bosqich:** '🎯 Test topshirish' tugmasi\n"
                "2️⃣ **Tezkor usul:** `KOD JAVOBLAR` formatida\n\n"
                "✨ **Misol:** `MATEM1 ABCDA`\n\n"
                "📣 **Kanal:** @testlar231\n\n"
                "Quyidagi tugmalardan foydalaning:",
                parse_mode='Markdown',
                reply_markup=main_keyboard(message.from_user.id)
            )

            # Agar ro'yxatdan o'tmagan bo'lsa
            if user_id not in registrations or not registrations[user_id].get('registered', False):
                await start_registration(message)
        else:
            await request_channel_subscription(message)
    except Exception as e:
        print(f"📡 Kanalni tekshirishda xatolik: {e}")
        await request_channel_subscription(message)


async def request_channel_subscription(message: types.Message):
    """Kanalga obuna qilishni so'rash"""
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=CHANNEL_LINK),
        InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subscription")
    )

    await message.answer(
        "👋 **TestBotga xush kelibsiz!** 🤖\n\n"
        f"📣 **Botdan to'liq foydalanish uchun kanalimizga obuna bo'ling:**\n"
        f"👉 {CHANNEL_ID}\n\n"
        "✨ **Kanalda nimalar bor?**\n"
        "• 📄 Barcha PDF test fayllari\n"
        "• 🔑 Test kodlari\n"
        "• 📊 Test natijalari statistikasi\n\n"
        "Kanalga obuna bo'lgach, '✅ Obunani tekshirish' tugmasini bosing va "
        "test topshirishni boshlang! 🚀",
        parse_mode='Markdown',
        reply_markup=keyboard
    )


async def start_registration(message: types.Message):
    """Ro'yxatdan o'tishni boshlash"""
    user_id = str(message.from_user.id)

    if user_id in registrations and registrations[user_id].get('registered', False):
        return

    user_registration[user_id] = {
        'step': 1,  # 1-ism, 2-viloyat, 3-tuman
        'data': {}
    }

    await message.answer(
        "👤 **Ro'yxatdan o'tish** 📝\n\n"
        "✨ **Botdan to'liq foydalanish uchun ro'yxatdan o'ting:**\n\n"
        "📌 **1-bosqich: Ism familiyangizni kiriting**\n\n"
        "💡 **Misol:** *Alijon Valiyev*, *Dilnoza Xolmatova*\n\n"
        "Ismingizni to'liq shaklda kiriting:",
        parse_mode='Markdown'
    )


# Ro'yxatdan o'tish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in user_registration)
async def process_registration(message: types.Message):
    """Ro'yxatdan o'tish jarayoni"""
    user_id = str(message.from_user.id)
    state = user_registration[user_id]
    step = state['step']

    if step == 1:  # Ism familiya
        full_name = message.text.strip()
        if len(full_name) < 3:
            await message.answer(
                "❌ **Ism familiya kamida 3 ta belgidan iborat bo'lishi kerak!**\n\n"
                "Iltimos, to'liq ism familiyangizni kiriting.\n"
                "💡 **Misol:** *Alijon Valiyev*",
                parse_mode='Markdown'
            )
            return

        state['data']['full_name'] = full_name
        state['step'] = 2

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        regions_list = list(REGIONS.keys())
        for i in range(0, len(regions_list), 2):
            row = regions_list[i:i + 2]
            keyboard.add(*[KeyboardButton(region) for region in row])

        await message.answer(
            f"✅ **Ism familiya qabul qilindi:** *{full_name}*\n\n"
            "📍 **2-bosqich: Viloyatingizni tanlang** 🗺️\n\n"
            "Quyidagi viloyatlardan birini tanlang:",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    elif step == 2:  # Viloyat
        region = message.text.strip()
        if region not in REGIONS:
            await message.answer(
                "❌ **Viloyat topilmadi!**\n\n"
                "Iltimos, ro'yxatdagi viloyatlardan birini tanlang.",
                parse_mode='Markdown'
            )
            return

        state['data']['region'] = region
        state['step'] = 3

        districts = REGIONS[region]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        for i in range(0, len(districts), 3):
            row = districts[i:i + 3]
            keyboard.add(*[KeyboardButton(district) for district in row])

        keyboard.add(KeyboardButton("🔙 Orqaga"))

        await message.answer(
            f"✅ **Viloyat qabul qilindi:** *{region}*\n\n"
            "🏘️ **3-bosqich: Tumaningizni tanlang**\n\n"
            "Quyidagi tumanlardan birini tanlang:",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    elif step == 3:  # Tuman
        if message.text == "🔙 Orqaga":
            state['step'] = 2
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            regions_list = list(REGIONS.keys())
            for i in range(0, len(regions_list), 2):
                row = regions_list[i:i + 2]
                keyboard.add(*[KeyboardButton(region) for region in row])

            await message.answer("Viloyatingizni qayta tanlang:", reply_markup=keyboard)
            return

        district = message.text.strip()
        region = state['data']['region']

        if district not in REGIONS[region]:
            await message.answer(
                "❌ **Tuman topilmadi!**\n\n"
                "Iltimos, ro'yxatdagi tumanlardan birini tanlang.",
                parse_mode='Markdown'
            )
            return

        state['data']['district'] = district

        registrations[user_id] = {
            'full_name': state['data']['full_name'],
            'region': region,
            'district': district,
            'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'registered': True,
            'username': message.from_user.username or message.from_user.full_name
        }

        # user_results ni yangilash
        if user_id in user_results:
            user_results[user_id]['full_name'] = state['data']['full_name']
            user_results[user_id]['region'] = region
            user_results[user_id]['district'] = district
            user_results[user_id]['registered'] = True
        else:
            user_results[user_id] = {
                'username': message.from_user.username or message.from_user.full_name,
                'full_name': state['data']['full_name'],
                'region': region,
                'district': district,
                'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'tests_taken': 0,
                'total_score': 0,
                'tests': {},
                'registered': True
            }

        save_data()
        del user_registration[user_id]

        await message.answer(
            f"🎉 **Tabriklaymiz! Muvaffaqiyatli ro'yxatdan o'tdingiz!** 🎊\n\n"
            f"👤 **Ism familiya:** *{state['data']['full_name']}*\n"
            f"📍 **Manzil:** *{region}, {district}*\n"
            f"📅 **Ro'yxatdan o'tilgan sana:** *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            "🚀 **Endi siz test topshira olasiz!**\n\n"
            "📚 **Test topshirish usullari:**\n"
            "1️⃣ **Bosqichma-bosqich:** '🎯 Test topshirish' tugmasini bosing\n"
            "2️⃣ **Tezkor usul:** `KOD JAVOBLAR` formatida yuboring\n\n"
            "💡 **Misol:** `MATEM1 ABCDA`\n\n"
            "✨ **Muvaffaqiyatlar tilaymiz!** 🌟",
            parse_mode='Markdown',
            reply_markup=main_keyboard(message.from_user.id)
        )


# Admin panel
@dp.message_handler(lambda message: message.text == "👨‍🏫 Admin panel")
async def admin_panel(message: types.Message):
    """Admin panelini ko'rsatish"""
    if message.from_user.id not in ADMINS:
        await message.answer(
            "❌ **Bu bo'lim faqat adminlar uchun!**\n\n"
            "Iltimos, asosiy menyudan foydalaning.",
            reply_markup=main_keyboard(message.from_user.id)
        )
        return

    admin_stats = f"👨‍🏫 **Admin Panel** 🛠️\n\n"
    admin_stats += f"📊 **Umumiy statistika:**\n"
    admin_stats += f"• 📚 Testlar soni: *{len(tests_db)}* ta\n"
    admin_stats += f"• 👥 Jami foydalanuvchilar: *{len(registrations)}* ta\n"
    admin_stats += f"• ✅ Test topshirganlar: *{sum(1 for u in user_results.values() if u.get('tests_taken', 0) > 0)}* ta\n\n"

    # Adminning testlari
    admin_tests = [code for code, test in tests_db.items()
                   if test.get('creator_id') == str(message.from_user.id)]

    if admin_tests:
        admin_stats += f"📝 **Sizning testlaringiz:** *{len(admin_tests)}* ta\n"
        for code in admin_tests[-3:]:
            test_takers = sum(1 for u in user_results.values() if code in u.get('tests', {}))
            admin_stats += f"• `{code}` (*{test_takers}* ta odam ishlagan)\n"

    await message.answer(admin_stats, parse_mode='Markdown', reply_markup=admin_keyboard())


# ➕ TEST JAVOBLARINI KIRITISH
@dp.message_handler(lambda message: message.text == "➕ Test javoblarini kiritish" and message.from_user.id in ADMINS)
async def add_test_answers_start(message: types.Message):
    """Test javoblarini kiritishni boshlash"""
    user_id = str(message.from_user.id)

    if user_id in admin_test_states:
        await message.answer("❌ **Siz allaqachon test kiritish jarayonidasiz!**")
        return

    admin_test_states[user_id] = {
        'step': 1,
        'data': {}
    }

    await message.answer(
        "➕ **Test javoblarini kiritish** 📝\n\n"
        "✨ **Bu yerda siz kanalga joylagan PDF testining javoblarini kiritasiz.**\n\n"
        "🔑 **1-bosqich: Test kodini kiriting**\n\n"
        "PDF faylda berilgan test kodini kiriting.\n"
        "Bu kod foydalanuvchilar tomonidan test topshirishda ishlatiladi.\n\n"
        "💡 **Misol:** `MATEM1`, `FIZIKA_2`, `TEST2024`\n\n"
        "Test kodini kiriting:",
        parse_mode='Markdown'
    )


# Test javoblarini kiritish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in admin_test_states)
async def process_test_answers(message: types.Message):
    """Test javoblarini qabul qilish"""
    user_id = str(message.from_user.id)

    if user_id not in admin_test_states:
        return

    state = admin_test_states[user_id]
    step = state['step']

    try:
        if step == 1:  # Test kodi
            test_code = message.text.strip().upper()

            if not test_code.replace('_', '').isalnum():
                await message.answer(
                    "❌ **Noto'g'ri format!**\n\n"
                    "Test kodi faqat harf, raqam va _ belgisidan iborat bo'lishi kerak."
                )
                return

            if test_code in tests_db:
                test_data = tests_db[test_code]
                await message.answer(
                    f"❌ **'{test_code}' kodli test allaqachon mavjud!**\n\n"
                    f"📊 **Test ma'lumotlari:**\n"
                    f"• Yaratuvchi: {test_data.get('created_by', 'Noma\'lum')}\n"
                    f"• Savollar soni: {test_data.get('questions_count', len(test_data.get('javoblar', '')))} ta\n"
                    f"• Yaratilgan sana: {test_data.get('created_at', 'Noma\'lum')}\n\n"
                    "Agar yangilamoqchi bo'lsangiz, avval o'chiring.",
                    parse_mode='Markdown'
                )
                return

            state['data']['code'] = test_code
            state['step'] = 2

            await message.answer(
                f"✅ **Kod qabul qilindi:** `{test_code}`\n\n"
                "🔢 **2-bosqich: Savollar sonini kiriting**\n\n"
                "PDF fayldagi savollar sonini raqamda kiriting.\n\n"
                "💡 **Misol:** 10, 15, 20\n\n"
                "Savollar soni (1 dan 100 gacha):",
                parse_mode='Markdown'
            )

        elif step == 2:  # Savollar soni
            try:
                questions_count = int(message.text.strip())
                if questions_count < 1 or questions_count > 100:
                    await message.answer("❌ **Savollar soni 1 dan 100 gacha bo'lishi kerak!**")
                    return

                state['data']['questions_count'] = questions_count
                state['step'] = 3

                await message.answer(
                    f"✅ **Savollar soni qabul qilindi:** *{questions_count}* ta\n\n"
                    "🔠 **3-bosqich: To'g'ri javoblarni kiriting**\n\n"
                    f"📄 **PDF fayldagi to'g'ri javoblarni ketma-ket kiriting.**\n"
                    f"Har bir savol uchun A, B, C, D harflaridan birini yozing.\n\n"
                    f"💡 **Masalan, 5 ta savol uchun:** `ABCDA`\n\n"
                    f"📝 Iltimos, *{questions_count}* ta javob kiriting:",
                    parse_mode='Markdown'
                )

            except ValueError:
                await message.answer("❌ **Faqat raqam kiriting!**")

        elif step == 3:  # To'g'ri javoblar
            answers = message.text.strip().upper()
            questions_count = state['data']['questions_count']

            if len(answers) != questions_count:
                await message.answer(
                    f"❌ **Javoblar soni noto'g'ri!**\n\n"
                    f"Kutilgan: *{questions_count}* ta javob\n"
                    f"Siz kiritdingiz: *{len(answers)}* ta\n\n"
                    f"Iltimos, *{questions_count}* ta javob kiriting."
                )
                return

            valid_answers = {'A', 'B', 'C', 'D'}
            invalid_chars = []
            for i, ans in enumerate(answers):
                if ans not in valid_answers:
                    invalid_chars.append(f"{i + 1}-javob: '{ans}'")

            if invalid_chars:
                await message.answer(
                    f"❌ **Noto'g'ri javoblar topildi!**\n\n"
                    f"Faqat A, B, C, D harflaridan foydalaning.\n"
                    f"Noto'g'ri javoblar: {', '.join(invalid_chars)}"
                )
                return

            # Testni saqlash
            test_code = state['data']['code']
            tests_db[test_code] = {
                'javoblar': answers,
                'narx': 2,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'created_by': message.from_user.username or message.from_user.full_name,
                'creator_id': user_id,
                'questions_count': questions_count,
                'test_type': 'pdf'
            }

            save_data()
            del admin_test_states[user_id]

            await message.answer(
                f"🎉 **Test javoblari muvaffaqiyatli saqlandi!** ✅\n\n"
                f"📌 **Test ma'lumotlari:**\n"
                f"• **Kod:** `{test_code}`\n"
                f"• **Savollar soni:** *{questions_count}* ta\n"
                f"• **To'g'ri javoblar:** `{answers}`\n"
                f"• **Yaratilgan sana:** *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
                "👥 **Foydalanuvchilar endi bu testni topshira oladilar:**\n"
                f"`{test_code} [javoblari]`\n\n"
                "💡 **Misol:**\n"
                f"• `{test_code} ABCDA`\n"
                f"• `{test_code} {'A' * questions_count}`\n\n"
                "✅ **PDF testi kanalga joylangan va javoblari botga kiritilgan.**",
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )

    except Exception as e:
        print(f"❌ Test kiritishda xatolik: {e}")
        await message.answer(f"❌ **Xatolik yuz berdi:** {str(e)}\n\nIltimos, qaytadan urinib ko'ring.")
        if user_id in admin_test_states:
            del admin_test_states[user_id]


# 🎯 TEST TOPSHIRISH - Yangi interaktiv usul
@dp.message_handler(lambda message: message.text == "🎯 Test topshirish")
async def take_test_interactive(message: types.Message):
    """Test topshirishni boshlash"""
    user_id = str(message.from_user.id)

    if user_id in user_test_states:
        await message.answer(
            "ℹ️ **Siz allaqachon test topshirish jarayonidasiz!**\n\n"
            "Iltimos, oldingi testni yakunlang yoki /cancel buyrug'i bilan bekor qiling."
        )
        return

    if user_id not in registrations or not registrations[user_id].get('registered', False):
        await message.answer(
            "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
            "Ro'yxatdan o'tish uchun /start buyrug'ini yuboring.",
            parse_mode='Markdown'
        )
        return

    user_test_states[user_id] = {
        'step': 1,
        'data': {}
    }

    await message.answer(
        "🎯 **Test topshirish (bosqichma-bosqich)** 📝\n\n"
        "✨ **1-bosqich: Test kodini kiriting**\n\n"
        "PDF fayldagi test kodini kiriting.\n\n"
        "💡 **Misol:** `MATEM1`, `FIZIKA_2`, `TEST2024`\n\n"
        "Test kodingizni kiriting:",
        parse_mode='Markdown'
    )


# Test topshirish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in user_test_states)
async def process_test_taking(message: types.Message):
    """Test topshirish jarayoni"""
    user_id = str(message.from_user.id)

    if user_id not in user_test_states:
        return

    state = user_test_states[user_id]
    step = state['step']

    try:
        if step == 1:  # Test kodi
            test_code = message.text.strip().upper()

            if test_code not in tests_db:
                await message.answer(
                    f"❌ **'{test_code}' testi topilmadi!**\n\n"
                    "🔍 **Sabablari:**\n"
                    "1. Test kodi noto'g'ri kiritilgan\n"
                    "2. Test hali admin tomonidan kiritilmagan\n"
                    "3. Test o'chirilgan bo'lishi mumkin\n\n"
                    "📣 **Kanaldan test kodini oling:** @testlar231\n\n"
                    "Yoki boshqa test kodini kiriting:",
                    parse_mode='Markdown'
                )
                return

            test_data = tests_db[test_code]
            questions_count = len(test_data['javoblar'])

            state['data']['test_code'] = test_code
            state['data']['questions_count'] = questions_count
            state['data']['current_question'] = 1
            state['data']['user_answers'] = []
            state['step'] = 2

            await message.answer(
                f"✅ **'{test_code}' testi topildi!** 🎉\n\n"
                f"📊 **Test ma'lumotlari:**\n"
                f"• **Savollar soni:** *{questions_count}* ta\n"
                f"• **Har bir to'g'ri javob:** *2* ball\n"
                f"• **Maksimal ball:** *{questions_count * 2}*\n"
                f"• **Yaratuvchi:** {test_data.get('created_by', 'Noma\'lum')}\n\n"
                "🔠 **Endi savollarga javob bering:**\n\n"
                f"**1-savol:** A, B, C, D harflaridan birini kiriting:",
                parse_mode='Markdown'
            )

        elif step == 2:  # Javoblarni qabul qilish
            answer = message.text.strip().upper()
            current_q = state['data']['current_question']
            total_q = state['data']['questions_count']

            if answer not in ['A', 'B', 'C', 'D']:
                await message.answer(
                    "❌ **Noto'g'ri javob formati!**\n\n"
                    "Faqat quyidagi harflardan birini kiriting:\n"
                    "• A\n• B\n• C\n• D\n\n"
                    f"**{current_q}-savolga qayta javob bering:**",
                    parse_mode='Markdown'
                )
                return

            state['data']['user_answers'].append(answer)

            if current_q < total_q:
                state['data']['current_question'] += 1
                next_q = state['data']['current_question']

                progress = f"📊 **Progress:** *{current_q}/{total_q}* ({current_q / total_q * 100:.0f}%)"

                await message.answer(
                    f"✅ **{current_q}-savol qabul qilindi:** *{answer}*\n\n"
                    f"{progress}\n\n"
                    f"**{next_q}-savol:** A, B, C, D harflaridan birini kiriting:",
                    parse_mode='Markdown'
                )
            else:
                # Barcha javoblarni olib bo'ldik
                test_code = state['data']['test_code']
                user_answers = state['data']['user_answers']
                test_data = tests_db[test_code]
                correct_answers = test_data['javoblar']

                # Natijani hisoblash
                correct_count = 0
                detailed_results = []

                for i in range(len(correct_answers)):
                    is_correct = user_answers[i] == correct_answers[i]
                    if is_correct:
                        correct_count += 1
                    detailed_results.append({
                        'question': i + 1,
                        'user_answer': user_answers[i],
                        'correct_answer': correct_answers[i],
                        'is_correct': is_correct
                    })

                wrong_count = len(correct_answers) - correct_count
                total_score = correct_count * 2
                max_score = len(correct_answers) * 2
                percentage = (correct_count / len(correct_answers)) * 100 if len(correct_answers) > 0 else 0

                # Baholash
                if percentage >= 90:
                    grade = "🎉 A'lo! Mukammal natija!"
                    emoji = "🌟"
                    comment = "Siz juda yaxshi tayyorgarlik ko'rgansiz!"
                elif percentage >= 80:
                    grade = "👍 Yaxshi! Juda yaxshi natija!"
                    emoji = "✅"
                    comment = "Yaxshi ishladingiz, lekin yana takomillashtirishingiz mumkin!"
                elif percentage >= 60:
                    grade = "😊 Qoniqarli. Yaxshi natija!"
                    emoji = "📊"
                    comment = "Yaxshi boshlang, keyingi marta yanada yaxshiroq natijaga erishasiz!"
                else:
                    grade = "📚 Yana urinib ko'ring. Omad keyingi safar!"
                    emoji = "🔄"
                    comment = "Harakatda davom eting, siz bunga qodirsiz!"

                # Ma'lumotlarni saqlash
                if user_id not in user_results:
                    user_results[user_id] = {
                        'username': message.from_user.username or message.from_user.full_name,
                        'full_name': registrations.get(user_id, {}).get('full_name', ''),
                        'region': registrations.get(user_id, {}).get('region', ''),
                        'district': registrations.get(user_id, {}).get('district', ''),
                        'first_seen': datetime.now().strftime("%Y-%m-d %H:%M:%S"),
                        'tests_taken': 0,
                        'total_score': 0,
                        'tests': {},
                        'registered': True
                    }

                # Test yangi bo'lsa
                is_new_test = test_code not in user_results[user_id]['tests']

                # Eski natijani olib tashlash
                old_score = 0
                if test_code in user_results[user_id]['tests']:
                    old_score = user_results[user_id]['tests'][test_code].get('score', 0)
                    user_results[user_id]['total_score'] = user_results[user_id].get('total_score', 0) - old_score
                    user_results[user_id]['tests_taken'] = max(0, user_results[user_id].get('tests_taken', 0) - 1)

                # Yangi natijani saqlash
                user_results[user_id]['tests'][test_code] = {
                    'correct': correct_count,
                    'wrong': wrong_count,
                    'score': total_score,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'answers': ''.join(user_answers),
                    'percentage': percentage,
                    'grade': grade
                }

                # Umumiy ko'rsatkichlarni yangilash
                if is_new_test:
                    user_results[user_id]['tests_taken'] = user_results[user_id].get('tests_taken', 0) + 1

                user_results[user_id]['total_score'] = user_results[user_id].get('total_score', 0) + total_score

                save_data()

                # Testni nechta odam ishlaganligini hisoblash
                test_takers = 0
                for u in user_results.values():
                    if test_code in u.get('tests', {}):
                        test_takers += 1

                # Natijani chiqarish
                result_message = f"{emoji} **PDF TEST NATIJALARI** {emoji}\n\n"
                result_message += f"📌 **Test kodi:** `{test_code}`\n"
                result_message += f"👤 **Ism:** *{registrations.get(user_id, {}).get('full_name', '')}*\n"
                result_message += f"📍 **Manzil:** *{registrations.get(user_id, {}).get('region', '')}, {registrations.get(user_id, {}).get('district', '')}*\n"
                result_message += f"📊 **Umumiy savollar:** *{len(correct_answers)}* ta\n\n"
                result_message += f"🏆 **SIZNING NATIJANGIZ:**\n"
                result_message += f"✅ **To'g'ri javoblar:** *{correct_count}* ta\n"
                result_message += f"❌ **Noto'g'ri javoblar:** *{wrong_count}* ta\n"
                result_message += f"🎯 **Olingan ball:** *{total_score}/{max_score}*\n"
                result_message += f"📈 **Foiz:** *{percentage:.1f}%*\n\n"
                result_message += f"**📋 Baholash:** *{grade}*\n"
                result_message += f"**💭 Sharh:** {comment}\n\n"
                result_message += f"📊 **Statistika:** Bu testda jami *{test_takers}* ta odam ishlagan\n\n"

                # Test muallifi
                creator = test_data.get('created_by', 'Noma\'lum')
                result_message += f"👨‍💻 **Test muallifi:** *{creator}*\n\n"

                # Javoblar tafsiloti (faqat 10 ta savol ko'rsatish)
                result_message += f"📋 **Javoblar tafsiloti (dastlabki 10 ta):**\n"
                for i in range(min(10, len(detailed_results))):
                    result = detailed_results[i]
                    if result['is_correct']:
                        result_message += f"{result['question']}. ✅ **{result['user_answer']}**\n"
                    else:
                        result_message += f"{result['question']}. ❌ **{result['user_answer']}** (to'g'ri: **{result['correct_answer']}**)\n"

                if len(detailed_results) > 10:
                    result_message += f"... va yana *{len(detailed_results) - 10}* ta savol\n\n"

                # Holatni tozalash
                del user_test_states[user_id]

                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(
                    InlineKeyboardButton("🔄 Yangi test", callback_data="take_another_test"),
                    InlineKeyboardButton("⭐ Reyting", callback_data="show_rating"),
                    InlineKeyboardButton("📊 Natijalarim", callback_data="show_my_results"),
                    InlineKeyboardButton("📈 Umumiy statistika", callback_data="global_stats")
                )

                await message.answer(result_message, parse_mode='Markdown', reply_markup=keyboard)

                # Test muallifiga xabar (agar admin bo'lsa)
                creator_id = test_data.get('creator_id')
                if creator_id and creator_id != user_id and int(creator_id) in ADMINS:
                    try:
                        await bot.send_message(
                            int(creator_id),
                            f"📢 **Yangi test natijasi!** 🎉\n\n"
                            f"📌 **Test:** `{test_code}`\n"
                            f"👤 **Foydalanuvchi:** *{registrations.get(user_id, {}).get('full_name', '')}*\n"
                            f"📍 **Manzil:** *{registrations.get(user_id, {}).get('region', '')}, {registrations.get(user_id, {}).get('district', '')}*\n"
                            f"✅ **To'g'ri javoblar:** *{correct_count}/{len(correct_answers)}*\n"
                            f"🎯 **Ball:** *{total_score}/{max_score}*\n"
                            f"📈 **Foiz:** *{percentage:.1f}%*\n"
                            f"📊 **Bu testni jami ishlaganlar:** *{test_takers}* ta\n\n"
                            f"✨ **Muvaffaqiyatli test topshirish!**",
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        print(f"📨 Adminga xabar yuborishda xatolik: {e}")

                print(f"✅ Test topshirildi: {test_code} | User: {user_id} | Ball: {total_score}")

    except Exception as e:
        print(f"❌ Test topshirishda xatolik: {e}")
        await message.answer(
            f"❌ **Xatolik yuz berdi!**\n\n"
            f"Sabab: *{str(e)}*\n\n"
            f"Iltimos, qaytadan urinib ko'ring yoki /start buyrug'i orqali boshlang.",
            parse_mode='Markdown'
        )
        if user_id in user_test_states:
            del user_test_states[user_id]


# 📊 MENING NATIJALARIM
@dp.message_handler(lambda message: message.text == "📊 Mening natijalarim")
async def my_results(message: types.Message):
    """Foydalanuvchi natijalarini ko'rsatish"""
    user_id = str(message.from_user.id)

    if user_id not in registrations or not registrations[user_id].get('registered', False):
        await message.answer(
            "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
            "Ro'yxatdan o'tish uchun /start buyrog'ini yuboring.",
            parse_mode='Markdown'
        )
        return

    if user_id not in user_results or not user_results[user_id].get('tests'):
        await message.answer(
            "📭 **Siz hali test topshirmagansiz!** 😊\n\n"
            "🚀 **Birinchi testni topshirish uchun:**\n"
            "1. 📥 Kanaldan PDF testni oling (@testlar231)\n"
            "2. 🔍 Test kodini toping\n"
            "3. 🎯 'Test topshirish' tugmasini bosing\n\n"
            "💡 **Yoki tezkor usul:**\n"
            "`KOD JAVOBLAR` formatida yuboring\n"
            "✨ **Misol:** `TEST123 ABCDA`",
            parse_mode='Markdown'
        )
        return

    user_data = user_results[user_id]
    reg_data = registrations.get(user_id, {})
    tests_taken = user_data.get('tests_taken', 0)
    total_score = user_data.get('total_score', 0)

    response = f"👤 **SIZNING STATISTIKANGIZ** 📊\n\n"
    response += f"**Ism:** *{reg_data.get('full_name', '')}*\n"
    response += f"**📍 Manzil:** *{reg_data.get('region', '')}, {reg_data.get('district', '')}*\n"
    response += f"**📅 Ro'yxatdan o'tilgan:** *{reg_data.get('registered_at', '')}*\n\n"
    response += f"📈 **UMUMIY KO'RSATKICHLAR:**\n"
    response += f"• 📚 **Topshirilgan testlar:** *{tests_taken}* ta\n"
    response += f"• ⭐ **Jami to'plangan ball:** *{total_score}*\n"

    if tests_taken > 0:
        avg_score = total_score / tests_taken
        response += f"• 📊 **O'rtacha ball/test:** *{avg_score:.1f}*\n"

        # Eng yaxshi test
        best_test = None
        best_score = 0
        for test_code, results in user_data['tests'].items():
            if results.get('score', 0) > best_score:
                best_score = results['score']
                best_test = test_code

        if best_test:
            response += f"• 🏆 **Eng yaxshi test:** `{best_test}` (*{best_score}* ball)\n"

    response += f"\n📋 **SO'NGI 3 TA TEST:**\n"

    # So'nggi 3 ta test natijasi
    user_tests = list(user_data.get('tests', {}).items())[-3:]
    for test_code, results in user_tests:
        test_info = tests_db.get(test_code, {})
        total_q = len(test_info.get('javoblar', ''))

        response += f"\n📌 **`{test_code}`**\n"
        response += f"   ✅ **To'g'ri:** *{results['correct']}/{total_q}*\n"
        response += f"   🎯 **Ball:** *{results['score']}*\n"
        response += f"   📈 **Foiz:** *{results.get('percentage', 0):.1f}%*\n"
        response += f"   📅 **Sana:** *{results.get('date', '')}*\n"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📊 Batafsil statistika", callback_data="detailed_stats"),
        InlineKeyboardButton("🗑️ Natijalarni tozalash", callback_data="clear_results_confirm"),
        InlineKeyboardButton("📈 Umumiy reyting", callback_data="show_rating")
    )

    await message.answer(response, parse_mode='Markdown', reply_markup=keyboard)


# ⭐ REYTING
@dp.message_handler(lambda message: message.text == "⭐ Reyting")
async def show_rating(message: types.Message):
    """Reytingni ko'rsatish"""
    # Foydalanuvchilarni ballar bo'yicha saralash
    sorted_users = []
    for uid, data in user_results.items():
        if data.get('total_score', 0) > 0 and data.get('registered', False):
            reg_data = registrations.get(uid, {})
            full_name = reg_data.get('full_name', data.get('username', 'Noma\'lum foydalanuvchi'))
            if len(full_name) > 20:
                full_name = full_name[:17] + "..."

            region = reg_data.get('region', 'Noma\'lum')
            district = reg_data.get('district', 'Noma\'lum')

            sorted_users.append((uid, data, full_name, region, district))

    if not sorted_users:
        await message.answer(
            "📭 **Hozircha reyting mavjud emas.**\n\n"
            "🚀 **Birinchi bo'ling va reytingda yuqori o'rinlarga chiqing!**\n\n"
            "🎯 Test topshirishni boshlang va o'z o'rningizni egallang!",
            parse_mode='Markdown'
        )
        return

    sorted_users.sort(key=lambda x: x[1].get('total_score', 0), reverse=True)
    sorted_users = sorted_users[:10]

    rating_text = "🏆 **TOP 10 REYTING** 🏆\n\n"

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, (user_id, user_data, full_name, region, district) in enumerate(sorted_users):
        if i < len(medals):
            medal = medals[i]
        else:
            medal = f"{i + 1}."

        total_score = user_data.get('total_score', 0)
        tests_taken = user_data.get('tests_taken', 0)

        rating_text += f"{medal} **{full_name}**\n"
        rating_text += f"   📍 *{region}, {district}*\n"
        rating_text += f"   ⭐ **Ball:** *{total_score}*\n"
        rating_text += f"   📚 **Testlar:** *{tests_taken}* ta\n"

        if tests_taken > 0:
            avg_score = total_score / tests_taken
            rating_text += f"   📊 **O'rtacha:** *{avg_score:.1f}* ball\n"

        # Agar admin bo'lsa
        try:
            if int(user_id) in ADMINS:
                admin_tests = [code for code, test in tests_db.items()
                               if test.get('creator_id') == user_id]
                if admin_tests:
                    total_takers = 0
                    for code in admin_tests:
                        for u_data in user_results.values():
                            if code in u_data.get('tests', {}):
                                total_takers += 1
                    rating_text += f"   👨‍🏫 **Test yaratgan:** *{len(admin_tests)}* ta (*{total_takers}* ishlagan)\n"
        except:
            pass

        rating_text += "\n"

    # Foydalanuvchi o'z o'rni
    current_user_id = str(message.from_user.id)
    current_user_position = None
    for i, (user_id, _, _, _, _) in enumerate(sorted_users):
        if user_id == current_user_id:
            current_user_position = i + 1
            break

    if current_user_position:
        rating_text += f"🎯 **Sizning o'rningiz:** *{current_user_position}*\n\n"
    elif str(message.from_user.id) in user_results and user_results[str(message.from_user.id)].get('tests_taken',
                                                                                                   0) > 0:
        rating_text += "📊 **Siz reytingda emassiz. Ko'proq test topshirib ball to'plang!**\n\n"

    rating_text += "✨ **O'z o'rningizni oshiring!** 🌟\n"
    rating_text += "📚 **Har bir test sizga yangi bilim va ball olib keladi!**"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 Yangilash", callback_data="refresh_rating"),
        InlineKeyboardButton("📊 Mening natijalarim", callback_data="show_my_results"),
        InlineKeyboardButton("🎯 Test topshirish", callback_data="take_another_test")
    )

    await message.answer(rating_text, parse_mode='Markdown', reply_markup=keyboard)


# ℹ️ YORDAM
@dp.message_handler(lambda message: message.text == "ℹ️ Yordam")
async def help_command(message: types.Message):
    """Yordam ma'lumotlarini ko'rsatish"""
    help_text = """
🤖 **PDF TEST BOT - YORDAM** 📚

✨ **BU BOT ORQALI SIZ NIMALAR QILA OLASIZ?**
• 🎯 PDF testlarni topshirish
• 📊 Natijalaringizni ko'rish
• ⭐ Reytingda ishtirok etish
• 👨‍🏫 Admin sifatida testlar yaratish

🎯 **TEST TOPSHIRISH USULLARI:**

1️⃣ **BOSQICHMA-BOSQICH USUL (TAVSIYA ETILADI):**
   • "🎯 Test topshirish" tugmasini bosing
   • Test kodini kiriting
   • Har bir savolga alohida javob bering

2️⃣ **TEZKOR USUL:**
   • `KOD JAVOBLAR` formatida yuboring
   • **Misol:** `MATEM1 ABCDA`

📌 **MUHIM ESLATMALAR:**
• ✅ Avval ro'yxatdan o'tishingiz kerak
• 📣 Kanalga obuna bo'lishingiz kerak (@testlar231)
• ⭐ Har bir to'g'ri javob 2 ball

📊 **NATIJALAR VA STATISTIKA:**
• "📊 Mening natijalarim" - shaxsiy statistika
• "⭐ Reyting" - eng yaxshi foydalanuvchilar
• 📈 Har bir testdan keyin batafsil natija

⚠️ **QO'LLAB-QUVVATLASH:**
Muammo bo'lsa admin bilan bog'laning 👨‍💻

📱 **KANAL:** @testlar231
"""

    if message.from_user.id in ADMINS:
        help_text += "\n\n👨‍🏫 **ADMIN QO'LLANMASI:**\n"
        help_text += "1. 📄 PDF testni kanalga joylang\n"
        help_text += "2. 🛠️ Admin panelga o'ting\n"
        help_text += "3. ➕ 'Test javoblarini kiritish' ni bosing\n"
        help_text += "4. 🔑 Test ma'lumotlarini kiriting\n\n"
        help_text += "📊 **Admin imkoniyatlari:**\n"
        help_text += "• 📋 Testlar ro'yxatini ko'rish\n"
        help_text += "• 📈 Statistikalarni ko'rish\n"
        help_text += "• 👥 Foydalanuvchilarni boshqarish"

    await message.answer(help_text, parse_mode='Markdown')


# CALLBACK HANDLERS
@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    """Callback handler"""
    data = callback_query.data
    user_id = str(callback_query.from_user.id)

    if data == "check_subscription":
        try:
            chat_member = await bot.get_chat_member(CHANNEL_ID, callback_query.from_user.id)
            if chat_member.status not in ['left', 'kicked']:
                await callback_query.answer("✅ Obuna qilingansiz!", show_alert=True)
                await send_welcome(callback_query.message)
            else:
                await callback_query.answer("❌ Hali obuna qilmagansiz!", show_alert=True)
        except Exception as e:
            await callback_query.answer("❌ Xatolik yuz berdi!", show_alert=True)

    elif data == "take_another_test":
        await callback_query.answer("Yangi test boshlanmoqda...")
        await take_test_interactive(callback_query.message)

    elif data == "show_rating":
        await callback_query.answer("Reyting yuklanmoqda...")
        await show_rating(callback_query.message)

    elif data == "show_my_results":
        await callback_query.answer("Natijalar yuklanmoqda...")
        await my_results(callback_query.message)

    elif data == "refresh_rating":
        await callback_query.answer("Reyting yangilanmoqda...")
        await show_rating(callback_query.message)

    elif data == "global_stats":
        # Umumiy statistika
        pdf_tests = {code: test for code, test in tests_db.items() if test.get('test_type') == 'pdf'}

        total_questions = sum(len(test['javoblar']) for test in pdf_tests.values())
        total_tests_taken = sum(user.get('tests_taken', 0) for user in user_results.values())
        total_score_given = sum(user.get('total_score', 0) for user in user_results.values())
        active_users = sum(1 for user in user_results.values() if user.get('tests_taken', 0) > 0)

        response = f"📊 **UMUMIY STATISTIKA** 🌍\n\n"
        response += f"📚 **Testlar:**\n"
        response += f"• PDF testlar: *{len(pdf_tests)}* ta\n"
        response += f"• Jami savollar: *{total_questions}* ta\n\n"

        response += f"👥 **Foydalanuvchilar:**\n"
        response += f"• Ro'yxatdan o'tganlar: *{len(registrations)}* ta\n"
        response += f"• Faol foydalanuvchilar: *{active_users}* ta\n"
        response += f"• Test topshirishlar: *{total_tests_taken}* ta\n\n"

        response += f"⭐ **Ballar:**\n"
        response += f"• Berilgan ballar: *{total_score_given}*\n"

        if total_tests_taken > 0:
            avg_score_per_test = total_score_given / total_tests_taken
            response += f"• O'rtacha ball/test: *{avg_score_per_test:.1f}*\n\n"

        # Eng mashhur testlar
        test_popularity = {}
        for user in user_results.values():
            for test_code in user.get('tests', {}):
                if test_code in pdf_tests:
                    test_popularity[test_code] = test_popularity.get(test_code, 0) + 1

        if test_popularity:
            response += f"🔥 **ENG MASHHUR TESTLAR:**\n"
            sorted_tests = sorted(test_popularity.items(), key=lambda x: x[1], reverse=True)[:3]
            for test_code, count in sorted_tests:
                test_data = pdf_tests.get(test_code, {})
                creator = test_data.get('created_by', 'Noma\'lum')
                questions = test_data.get('questions_count', len(test_data['javoblar']))
                response += f"• `{test_code}`: *{count}* marta ({creator})\n"

        await callback_query.message.answer(response, parse_mode='Markdown')

    elif data == "detailed_stats":
        if user_id in user_results:
            user_data = user_results[user_id]
            reg_data = registrations.get(user_id, {})

            if not user_data.get('tests'):
                await callback_query.answer("Sizda natijalar yo'q!", show_alert=True)
                return

            response = f"📊 **BATAFSIL STATISTIKA** 🔍\n\n"
            response += f"👤 **Shaxsiy ma'lumotlar:**\n"
            response += f"• Ism: *{reg_data.get('full_name', '')}*\n"
            response += f"• Manzil: *{reg_data.get('region', '')}, {reg_data.get('district', '')}*\n"
            response += f"• Ro'yxatdan o'tilgan: *{reg_data.get('registered_at', '')}*\n\n"

            total_tests = len(user_data['tests'])
            total_correct = 0
            total_questions = 0

            for code, results in user_data['tests'].items():
                total_correct += results.get('correct', 0)
                test_info = tests_db.get(code, {})
                total_questions += len(test_info.get('javoblar', ''))

            response += f"📈 **UMUMIY:**\n"
            response += f"• Testlar: *{total_tests}* ta\n"
            response += f"• Savollar: *{total_questions}* ta\n"
            response += f"• To'g'ri javoblar: *{total_correct}* ta\n"

            if total_questions > 0:
                overall_percentage = (total_correct / total_questions) * 100
                response += f"• Umumiy foiz: *{overall_percentage:.1f}%*\n\n"

            response += f"📋 **HAR BIR TEST NATIJASI:**\n"
            for test_code, results in user_data['tests'].items():
                test_info = tests_db.get(test_code, {})
                total_q = len(test_info.get('javoblar', ''))
                percentage = (results.get('correct', 0) / total_q) * 100 if total_q > 0 else 0
                grade = results.get('grade', '')

                response += f"\n📌 **`{test_code}`**\n"
                response += f"• To'g'ri: *{results.get('correct', 0)}/{total_q}*\n"
                response += f"• Foiz: *{percentage:.1f}%*\n"
                response += f"• Baho: *{grade}*\n"
                response += f"• Sana: *{results.get('date', '')}*\n"

            await callback_query.message.answer(response, parse_mode='Markdown')

    elif data == "clear_results_confirm":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton("✅ Ha, tozalash", callback_data="clear_results_yes"),
            InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data="clear_results_no")
        )

        await callback_query.message.answer(
            "⚠️ **NATIJALARNI TOZALASH**\n\n"
            "❓ **Haqiqatan ham barcha natijalaringizni o'chirmoqchimisiz?**\n\n"
            "📌 **Bu amal:**\n"
            "• Barcha test natijalaringiz o'chadi\n"
            "• Barcha to'plagan ballaringiz yo'qoladi\n"
            "• Reytingdagi o'rningiz yo'qoladi\n"
            "• Faqat shaxsiy ma'lumotlaringiz saqlanib qoladi\n\n"
            "🔒 **Bu amalni qaytarib bo'lmaydi!**",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    elif data == "clear_results_yes":
        if user_id in user_results:
            user_results[user_id]['tests'] = {}
            user_results[user_id]['total_score'] = 0
            user_results[user_id]['tests_taken'] = 0
            save_data()
            await callback_query.answer("✅ Barcha natijalar tozalandi!", show_alert=True)
            await my_results(callback_query.message)

    elif data == "clear_results_no":
        await callback_query.answer("❌ Natijalarni tozalash bekor qilindi!", show_alert=True)
        await my_results(callback_query.message)

    await callback_query.answer()


if __name__ == '__main__':
    print("🤖 PDF TEST BOT ISHGA TUSHDI! 🎉")
    print("👨‍🏫 Adminlar:", ADMINS)
    pdf_test_count = len([t for t in tests_db.values() if t.get('test_type') == 'pdf'])
    print("📊 PDF Testlar soni:", pdf_test_count)
    registered_users = len([r for r in registrations.values() if r.get('registered', False)])
    print("👥 Ro'yxatdan o'tganlar:", registered_users)
    active_users = sum(1 for u in user_results.values() if u.get('tests_taken', 0) > 0)
    print("📈 Test topshirganlar:", active_users)
    print("✨ Bot muvaffaqiyatli ishga tushdi! Bot: @testlar231")

    executor.start_polling(dp, skip_updates=True)