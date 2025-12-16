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
        KeyboardButton("➕ Test qo'shish"),
        KeyboardButton("📋 Testlar ro'yxati"),
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


# ➕ TEST QO'SHISH - YANGI VA SODDA USUL
@dp.message_handler(lambda message: message.text == "➕ Test qo'shish" and message.from_user.id in ADMINS)
async def add_test_simple(message: types.Message):
    """Test qo'shishni boshlash - sodda usul"""
    user_id = str(message.from_user.id)

    if user_id in admin_test_states:
        await message.answer("❌ **Siz allaqachon test kiritish jarayonidasiz!**")
        return

    admin_test_states[user_id] = {
        'step': 1,
        'data': {}
    }

    await message.answer(
        "➕ **YANGI TEST QO'SHISH** 📝\n\n"
        "✨ **Test ma'lumotlarini bir qatorda kiriting:**\n\n"
        "📋 **FORMAT:** `KOD SAVOLLAR_SONI JAVOBLAR`\n\n"
        "📝 **MISOL:** `MATEM1 10 ABCDAEDCBA`\n"
        "📝 **MISOL:** `FIZIKA2 15 ABCDABCDABCDABC`\n\n"
        "📍 **TAVSIYALAR:**\n"
        "• Kod: Harflar va raqamlardan iborat bo'lsin\n"
        "• Javoblar: Faqat A, B, C, D harflari\n"
        "• Masofa: Bo'sh joy bilan ajrating\n\n"
        "📝 **Test ma'lumotlarini kiriting:**",
        parse_mode='Markdown'
    )


# Test qo'shish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in admin_test_states)
async def process_test_addition(message: types.Message):
    """Test qo'shish jarayoni"""
    user_id = str(message.from_user.id)

    if user_id not in admin_test_states:
        return

    state = admin_test_states[user_id]
    step = state['step']

    try:
        if step == 1:
            text = message.text.strip()

            # Formatni tekshirish
            parts = text.split()
            if len(parts) != 3:
                await message.answer(
                    "❌ **Noto'g'ri format!**\n\n"
                    "📋 **To'g'ri format:** `KOD SAVOLLAR_SONI JAVOBLAR`\n\n"
                    "📝 **Misol:** `MATEM1 10 ABCDAEDCBA`\n\n"
                    "Iltimos, qaytadan kiriting:"
                )
                return

            test_code, questions_str, answers = parts
            test_code = test_code.upper()
            answers = answers.upper()

            # Kodni tekshirish
            if not test_code.replace('_', '').isalnum():
                await message.answer(
                    "❌ **Noto'g'ri test kodi!**\n\n"
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
                    "Agar yangilamoqchi bo'lsangiz, avval eski testni o'chiring.",
                    parse_mode='Markdown'
                )
                return

            # Savollar sonini tekshirish
            try:
                questions_count = int(questions_str)
                if questions_count < 1 or questions_count > 100:
                    await message.answer(
                        "❌ **Savollar soni noto'g'ri!**\n\n"
                        "Savollar soni 1 dan 100 gacha bo'lishi kerak.\n\n"
                        "Iltimos, qaytadan kiriting:"
                    )
                    return
            except ValueError:
                await message.answer(
                    "❌ **Savollar soni raqam bo'lishi kerak!**\n\n"
                    "Iltimos, qaytadan kiriting:"
                )
                return

            # Javoblarni tekshirish
            if len(answers) != questions_count:
                await message.answer(
                    f"❌ **Javoblar soni noto'g'ri!**\n\n"
                    f"Kiritilgan savollar soni: *{questions_count}*\n"
                    f"Kiritilgan javoblar soni: *{len(answers)}*\n\n"
                    f"Javoblar soni savollar soniga teng bo'lishi kerak!\n\n"
                    "Iltimos, qaytadan kiriting:",
                    parse_mode='Markdown'
                )
                return

            # Javoblarni tekshirish
            valid_answers = {'A', 'B', 'C', 'D'}
            invalid_chars = []
            for i, ans in enumerate(answers):
                if ans not in valid_answers:
                    invalid_chars.append(f"{i + 1}-javob: '{ans}'")

            if invalid_chars:
                await message.answer(
                    f"❌ **Noto'g'ri javoblar topildi!**\n\n"
                    f"Faqat A, B, C, D harflaridan foydalaning.\n"
                    f"Noto'g'ri javoblar: {', '.join(invalid_chars)}\n\n"
                    "Iltimos, qaytadan kiriting:"
                )
                return

            # Tasdiqlash
            state['data'] = {
                'code': test_code,
                'questions_count': questions_count,
                'answers': answers
            }
            state['step'] = 2

            # Tasdiqlash klaviaturasi
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("✅ Saqlash", callback_data="save_test"),
                InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_test")
            )

            await message.answer(
                f"📋 **TEST MA'LUMOTLARI:**\n\n"
                f"🔑 **Kod:** `{test_code}`\n"
                f"🔢 **Savollar soni:** *{questions_count}* ta\n"
                f"📄 **Javoblar:** `{answers}`\n\n"
                f"📊 **Tekshirish natijalari:**\n"
                f"✅ Format to'g'ri\n"
                f"✅ Javoblar soni to'g'ri\n"
                f"✅ Har bir javob A-D oralig'ida\n\n"
                f"**Testni saqlashni tasdiqlaysizmi?**",
                parse_mode='Markdown',
                reply_markup=keyboard
            )

    except Exception as e:
        print(f"❌ Test qo'shishda xatolik: {e}")
        await message.answer(f"❌ **Xatolik yuz berdi:** {str(e)}\n\nIltimos, qaytadan urinib ko'ring.")
        if user_id in admin_test_states:
            del admin_test_states[user_id]


# Testni saqlash callback
@dp.callback_query_handler(lambda c: c.data in ['save_test', 'cancel_test'])
async def confirm_test_addition(callback_query: types.CallbackQuery):
    """Testni saqlashni tasdiqlash"""
    user_id = str(callback_query.from_user.id)

    if user_id not in admin_test_states:
        await callback_query.answer("Siz test qo'shish jarayonida emassiz!", show_alert=True)
        return

    if callback_query.data == 'save_test':
        data = admin_test_states[user_id]['data']

        # Testni saqlash
        tests_db[data['code']] = {
            'javoblar': data['answers'],
            'narx': 2,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'created_by': callback_query.from_user.username or callback_query.from_user.full_name,
            'creator_id': user_id,
            'questions_count': data['questions_count'],
            'test_type': 'pdf'
        }

        save_data()
        del admin_test_states[user_id]

        await callback_query.answer("✅ Test muvaffaqiyatli saqlandi!", show_alert=True)
        await callback_query.message.edit_text(
            f"🎉 **TEST MUVAFFAQIYATLI SAQLANDI!** ✅\n\n"
            f"📌 **Test ma'lumotlari:**\n"
            f"• **Kod:** `{data['code']}`\n"
            f"• **Savollar soni:** *{data['questions_count']}* ta\n"
            f"• **To'g'ri javoblar:** `{data['answers']}`\n"
            f"• **Yaratilgan sana:** *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            "👥 **Foydalanuvchilar endi bu testni topshira oladilar:**\n"
            f"1. `{data['code']} [javoblari]`\n"
            f"2. '🎯 Test topshirish' tugmasi orqali\n\n"
            "✅ **PDF testi kanalga joylashni unutmang!** 📣",
            parse_mode='Markdown'
        )

    elif callback_query.data == 'cancel_test':
        del admin_test_states[user_id]
        await callback_query.answer("❌ Test qo'shish bekor qilindi!", show_alert=True)
        await callback_query.message.edit_text(
            "❌ **Test qo'shish bekor qilindi!**\n\n"
            "Agar xohlasangiz, qaytadan /start buyrug'i yordamida boshlashingiz mumkin.",
            parse_mode='Markdown'
        )


# 📋 TESTLAR RO'YXATI
@dp.message_handler(lambda message: message.text == "📋 Testlar ro'yxati" and message.from_user.id in ADMINS)
async def list_tests(message: types.Message):
    """Testlar ro'yxatini ko'rsatish"""
    if not tests_db:
        await message.answer("📭 **Hozircha testlar mavjud emas.**")
        return

    response = "📚 **TESTLAR RO'YXATI**\n\n"

    # Adminning testlarini ajratib ko'rsatish
    admin_tests = []
    other_tests = []

    for code, test in tests_db.items():
        if test.get('creator_id') == str(message.from_user.id):
            admin_tests.append((code, test))
        else:
            other_tests.append((code, test))

    if admin_tests:
        response += f"👨‍🏫 **SIZNING TESTLARINGIZ ({len(admin_tests)} ta):**\n"
        for code, test in admin_tests:
            questions = test.get('questions_count', len(test.get('javoblar', '')))
            test_takers = sum(1 for u in user_results.values() if code in u.get('tests', {}))
            response += f"• `{code}` - *{questions}* ta savol (*{test_takers}* ishlagan)\n"
        response += "\n"

    if other_tests:
        response += f"👥 **BOSHQA TESTLAR ({len(other_tests)} ta):**\n"
        for code, test in other_tests:
            questions = test.get('questions_count', len(test.get('javoblar', '')))
            creator = test.get('created_by', 'Noma\'lum')
            response += f"• `{code}` - *{questions}* ta savol ({creator})\n"

    await message.answer(response, parse_mode='Markdown')


# 🗑️ TEST O'CHIRISH
@dp.message_handler(lambda message: message.text == "🗑️ Test o'chirish" and message.from_user.id in ADMINS)
async def delete_test_menu(message: types.Message):
    """Test o'chirish menyusi"""
    # Faqat adminning o'z testlari
    admin_tests = [code for code, test in tests_db.items()
                   if test.get('creator_id') == str(message.from_user.id)]

    if not admin_tests:
        await message.answer(
            "📭 **Sizning testlaringiz yo'q.**\n\n"
            "Avval test qo'shing va keyin o'chirishingiz mumkin.",
            parse_mode='Markdown'
        )
        return

    keyboard = InlineKeyboardMarkup(row_width=2)
    for code in admin_tests:
        keyboard.add(InlineKeyboardButton(f"🗑️ {code}", callback_data=f"delete_{code}"))

    keyboard.add(InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_delete"))

    await message.answer(
        "🗑️ **TEST O'CHIRISH**\n\n"
        "⚠️ **Ogohlantirish:** Testni o'chirish uni butunlay yo'q qiladi va "
        "barcha foydalanuvchi natijalari ham o'chib ketadi!\n\n"
        "👇 O'chirmoqchi bo'lgan testingizni tanlang:",
        parse_mode='Markdown',
        reply_markup=keyboard
    )


# Test o'chirish callback
@dp.callback_query_handler(lambda c: c.data.startswith('delete_'))
async def delete_test_confirmation(callback_query: types.CallbackQuery):
    """Testni o'chirishni tasdiqlash"""
    test_code = callback_query.data.replace('delete_', '')

    if test_code not in tests_db:
        await callback_query.answer("Test topilmadi!", show_alert=True)
        return

    test_data = tests_db[test_code]

    # Faqat o'zining testini o'chira olish
    if test_data.get('creator_id') != str(callback_query.from_user.id):
        await callback_query.answer("Siz faqat o'z testingizni o'chira olasiz!", show_alert=True)
        return

    # Tasdiqlash klaviaturasi
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Ha, o'chirish", callback_data=f"confirm_delete_{test_code}"),
        InlineKeyboardButton("❌ Yo'q, bekor", callback_data="cancel_delete")
    )

    # Test statistikasi
    test_takers = sum(1 for u in user_results.values() if test_code in u.get('tests', {}))
    questions = len(test_data['javoblar'])

    await callback_query.message.edit_text(
        f"⚠️ **TESTNI O'CHIRISHNI TASDIQLASH**\n\n"
        f"📌 **Test kodi:** `{test_code}`\n"
        f"📊 **Test ma'lumotlari:**\n"
        f"• Savollar soni: *{questions}* ta\n"
        f"• Ishlagan odamlar: *{test_takers}* ta\n"
        f"• Yaratuvchi: {test_data.get('created_by', 'Noma\'lum')}\n"
        f"• Yaratilgan sana: {test_data.get('created_at', 'Noma\'lum')}\n\n"
        f"🔴 **O'chirilganda:**\n"
        f"• Test butunlay yo'q bo'ladi\n"
        f"• *{test_takers}* ta foydalanuvchi natijasi o'chadi\n"
        f"• Reytinglar yangilanadi\n\n"
        f"**Testni o'chirishni tasdiqlaysizmi?**",
        parse_mode='Markdown',
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda c: c.data.startswith('confirm_delete_'))
async def delete_test_execute(callback_query: types.CallbackQuery):
    """Testni o'chirishni amalga oshirish"""
    test_code = callback_query.data.replace('confirm_delete_', '')

    if test_code not in tests_db:
        await callback_query.answer("Test topilmadi!", show_alert=True)
        return

    test_data = tests_db[test_code]

    # Faqat o'zining testini o'chira olish
    if test_data.get('creator_id') != str(callback_query.from_user.id):
        await callback_query.answer("Siz faqat o'z testingizni o'chira olasiz!", show_alert=True)
        return

    # Testni o'chirish
    deleted_test = tests_db.pop(test_code)

    # Foydalanuvchi natijalaridan testni o'chirish
    for user_id, user_data in user_results.items():
        if 'tests' in user_data and test_code in user_data['tests']:
            # Ballarni qaytarib olish
            old_score = user_data['tests'][test_code].get('score', 0)
            user_data['total_score'] = max(0, user_data.get('total_score', 0) - old_score)
            user_data['tests_taken'] = max(0, user_data.get('tests_taken', 0) - 1)

            # Testni o'chirish
            del user_data['tests'][test_code]

    save_data()

    await callback_query.answer(f"✅ '{test_code}' testi o'chirildi!", show_alert=True)
    await callback_query.message.edit_text(
        f"✅ **TEST O'CHIRILDI!**\n\n"
        f"📌 **Test kodi:** `{test_code}`\n"
        f"📊 **O'chirilgan test ma'lumotlari:**\n"
        f"• Savollar soni: *{len(deleted_test['javoblar'])}* ta\n"
        f"• Yaratuvchi: {deleted_test.get('created_by', 'Noma\'lum')}\n\n"
        f"🔄 **Ma'lumotlar bazasi yangilandi.**",
        parse_mode='Markdown'
    )


@dp.callback_query_handler(lambda c: c.data == 'cancel_delete')
async def cancel_delete(callback_query: types.CallbackQuery):
    """Test o'chirishni bekor qilish"""
    await callback_query.answer("❌ Test o'chirish bekor qilindi!", show_alert=True)
    await callback_query.message.edit_text(
        "❌ **Test o'chirish bekor qilindi!**\n\n"
        "Test saqlanib qoldi.",
        parse_mode='Markdown'
    )


# 📊 STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika" and message.from_user.id in ADMINS)
async def admin_statistics(message: types.Message):
    """Admin uchun statistikalar"""
    total_tests = len(tests_db)
    total_users = len(registrations)
    active_users = sum(1 for u in user_results.values() if u.get('tests_taken', 0) > 0)
    total_tests_taken = sum(u.get('tests_taken', 0) for u in user_results.values())
    total_score_given = sum(u.get('total_score', 0) for u in user_results.values())

    # Adminning testlari
    admin_tests = [code for code, test in tests_db.items()
                   if test.get('creator_id') == str(message.from_user.id)]

    response = f"📊 **ADMIN STATISTIKASI** 👨‍🏫\n\n"
    response += f"📈 **Umumiy ko'rsatkichlar:**\n"
    response += f"• 📚 Jami testlar: *{total_tests}* ta\n"
    response += f"• 👥 Ro'yxatdan o'tganlar: *{total_users}* ta\n"
    response += f"• ✅ Faol foydalanuvchilar: *{active_users}* ta\n"
    response += f"• 🎯 Jami test topshirishlar: *{total_tests_taken}* ta\n"
    response += f"• ⭐ Berilgan ballar: *{total_score_given}*\n\n"

    if admin_tests:
        response += f"📝 **SIZNING TESTLARINGIZ ({len(admin_tests)} ta):**\n"

        test_stats = []
        for code in admin_tests:
            test_data = tests_db[code]
            questions = len(test_data['javoblar'])
            test_takers = sum(1 for u in user_results.values() if code in u.get('tests', {}))
            total_score = sum(u.get('tests', {}).get(code, {}).get('score', 0) for u in user_results.values())

            test_stats.append((code, test_takers, questions, total_score))

        # Testlarni ishlagan odamlar soni bo'yicha saralash
        test_stats.sort(key=lambda x: x[1], reverse=True)

        for code, takers, questions, score in test_stats[:5]:  # Faqat 5 ta eng mashhuri
            avg_score = score / takers if takers > 0 else 0
            response += f"• `{code}`: *{takers}* ishlagan, o'rtacha *{avg_score:.1f}* ball\n"

    # Eng mashhur testlar
    all_test_stats = []
    for code, test_data in tests_db.items():
        test_takers = sum(1 for u in user_results.values() if code in u.get('tests', {}))
        if test_takers > 0:
            all_test_stats.append((code, test_takers, test_data.get('created_by', 'Noma\'lum')))

    if all_test_stats:
        all_test_stats.sort(key=lambda x: x[1], reverse=True)
        response += f"\n🔥 **ENG MASHHUR 5 TA TEST:**\n"
        for i, (code, takers, creator) in enumerate(all_test_stats[:5], 1):
            response += f"{i}. `{code}`: *{takers}* ishlagan ({creator})\n"

    await message.answer(response, parse_mode='Markdown')


# 👥 FOYDALANUVCHILAR
@dp.message_handler(lambda message: message.text == "👥 Foydalanuvchilar" and message.from_user.id in ADMINS)
async def list_users(message: types.Message):
    """Foydalanuvchilar ro'yxati"""
    if not registrations:
        await message.answer("📭 **Hozircha ro'yxatdan o'tgan foydalanuvchilar yo'q.**")
        return

    response = f"👥 **FOYDALANUVCHILAR RO'YXATI** ({len(registrations)} ta)\n\n"

    # Faol foydalanuvchilar
    active_users = []
    inactive_users = []

    for user_id, reg_data in registrations.items():
        if reg_data.get('registered', False):
            user_data = user_results.get(user_id, {})
            tests_taken = user_data.get('tests_taken', 0)

            if tests_taken > 0:
                active_users.append((user_id, reg_data, user_data))
            else:
                inactive_users.append((user_id, reg_data, user_data))

    if active_users:
        response += f"✅ **FAOL FOYDALANUVCHILAR ({len(active_users)} ta):**\n"
        for user_id, reg_data, user_data in active_users[:10]:  # Faqat 10 tasi
            full_name = reg_data.get('full_name', 'Noma\'lum')
            if len(full_name) > 20:
                full_name = full_name[:17] + "..."

            tests_taken = user_data.get('tests_taken', 0)
            total_score = user_data.get('total_score', 0)

            response += f"• *{full_name}* - {tests_taken} test, {total_score} ball\n"

        if len(active_users) > 10:
            response += f"... va yana {len(active_users) - 10} ta\n"
        response += "\n"

    if inactive_users:
        response += f"📭 **FAOL EMAS FOYDALANUVCHILAR ({len(inactive_users)} ta):**\n"
        for user_id, reg_data, user_data in inactive_users[:5]:  # Faqat 5 tasi
            full_name = reg_data.get('full_name', 'Noma\'lum')
            if len(full_name) > 20:
                full_name = full_name[:17] + "..."

            reg_date = reg_data.get('registered_at', 'Noma\'lum')
            response += f"• *{full_name}* - {reg_date}\n"

        if len(inactive_users) > 5:
            response += f"... va yana {len(inactive_users) - 5} ta\n"

    await message.answer(response, parse_mode='Markdown')


# TEZKOR USULDA TEST TOPSHIRISH
@dp.message_handler(lambda message: ' ' in message.text and len(message.text.split()) == 2)
async def quick_test_submission(message: types.Message):
    """Tezkor test topshirish usuli: KOD JAVOBLAR"""
    user_id = str(message.from_user.id)

    # Ro'yxatdan o'tganligini tekshirish
    if user_id not in registrations or not registrations[user_id].get('registered', False):
        await message.answer(
            "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
            "Ro'yxatdan o'tish uchun /start buyrog'ini yuboring.",
            parse_mode='Markdown'
        )
        return

    # Kanallikni tekshirish
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, message.from_user.id)
        if chat_member.status in ['left', 'kicked']:
            await message.answer(
                "❌ **Kanalga obuna bo'lmagansiz!**\n\n"
                f"Test topshirish uchun kanalga obuna bo'ling: {CHANNEL_ID}",
                parse_mode='Markdown'
            )
            return
    except Exception as e:
        print(f"Kanalni tekshirishda xatolik: {e}")

    # Ma'lumotlarni ajratish
    try:
        test_code, answers = message.text.strip().upper().split()
        answers = answers.upper()

        # Test mavjudligini tekshirish
        if test_code not in tests_db:
            await message.answer(
                f"❌ **'{test_code}' testi topilmadi!**\n\n"
                f"📣 **Kanaldan test kodini tekshiring:** @testlar231\n\n"
                "🔍 **Ehtimoliy sabablar:**\n"
                "1. Test kodi noto'g'ri kiritilgan\n"
                "2. Test hali admin tomonidan kiritilmagan\n"
                "3. Test o'chirilgan bo'lishi mumkin",
                parse_mode='Markdown'
            )
            return

        test_data = tests_db[test_code]
        correct_answers = test_data['javoblar']
        questions_count = len(correct_answers)

        # Javoblarni tekshirish
        if len(answers) != questions_count:
            await message.answer(
                f"❌ **Javoblar soni noto'g'ri!**\n\n"
                f"Testda *{questions_count}* ta savol bor.\n"
                f"Siz *{len(answers)}* ta javob kiritdingiz.\n\n"
                f"💡 **To'g'ri format:** `{test_code} {'A' * questions_count}`",
                parse_mode='Markdown'
            )
            return

        # Javoblarni tekshirish
        valid_answers = {'A', 'B', 'C', 'D'}
        invalid_chars = []
        for i, ans in enumerate(answers):
            if ans not in valid_answers:
                invalid_chars.append(f"{i + 1}-javob: '{ans}'")

        if invalid_chars:
            await message.answer(
                f"❌ **Noto'g'ri javoblar topildi!**\n\n"
                f"Faqat A, B, C, D harflaridan foydalaning.\n"
                f"Noto'g'ri javoblar: {', '.join(invalid_chars[:3])}\n\n"
                f"💡 **Misol:** `{test_code} {'A' * questions_count}`",
                parse_mode='Markdown'
            )
            return

        # Natijani hisoblash
        correct_count = 0
        detailed_results = []

        for i in range(questions_count):
            is_correct = answers[i] == correct_answers[i]
            if is_correct:
                correct_count += 1
            detailed_results.append({
                'question': i + 1,
                'user_answer': answers[i],
                'correct_answer': correct_answers[i],
                'is_correct': is_correct
            })

        wrong_count = questions_count - correct_count
        total_score = correct_count * 2
        max_score = questions_count * 2
        percentage = (correct_count / questions_count) * 100 if questions_count > 0 else 0

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

        # Eski natijani olib tashlash (agar mavjud bo'lsa)
        old_score = 0
        if test_code in user_results[user_id]['tests']:
            old_score = user_results[user_id]['tests'][test_code].get('score', 0)
            user_results[user_id]['total_score'] = max(0, user_results[user_id].get('total_score', 0) - old_score)
            user_results[user_id]['tests_taken'] = max(0, user_results[user_id].get('tests_taken', 0) - 1)

        # Yangi natijani saqlash
        user_results[user_id]['tests'][test_code] = {
            'correct': correct_count,
            'wrong': wrong_count,
            'score': total_score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'answers': answers,
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
        result_message = f"{emoji} **TEST NATIJALARI (TEZKOR USUL)** {emoji}\n\n"
        result_message += f"📌 **Test kodi:** `{test_code}`\n"
        result_message += f"👤 **Ism:** *{registrations.get(user_id, {}).get('full_name', '')}*\n"
        result_message += f"📍 **Manzil:** *{registrations.get(user_id, {}).get('region', '')}, {registrations.get(user_id, {}).get('district', '')}*\n"
        result_message += f"📊 **Umumiy savollar:** *{questions_count}* ta\n\n"
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
                    f"✅ **To'g'ri javoblar:** *{correct_count}/{questions_count}*\n"
                    f"🎯 **Ball:** *{total_score}/{max_score}*\n"
                    f"📈 **Foiz:** *{percentage:.1f}%*\n"
                    f"📊 **Bu testni jami ishlaganlar:** *{test_takers}* ta\n\n"
                    f"✨ **Muvaffaqiyatli test topshirish!**",
                    parse_mode='Markdown'
                )
            except Exception as e:
                print(f"📨 Adminga xabar yuborishda xatolik: {e}")

        print(f"✅ Test topshirildi (tezkor): {test_code} | User: {user_id} | Ball: {total_score}")

    except Exception as e:
        print(f"❌ Tezkor test topshirishda xatolik: {e}")
        await message.answer(
            f"❌ **Noto'g'ri format!**\n\n"
            f"📋 **To'g'ri format:** `KOD JAVOBLAR`\n\n"
            f"📝 **Misol:** `MATEM1 ABCDA`\n"
            f"📝 **Misol:** `FIZIKA2 ABCDABCDABCDABC`\n\n"
            f"Iltimos, qaytadan urinib ko'ring.",
            parse_mode='Markdown'
        )


# 🔙 ASOSIY MENYU
@dp.message_handler(lambda message: message.text == "🏠 Bosh menyu" and message.from_user.id in ADMINS)
async def back_to_main(message: types.Message):
    """Asosiy menyuga qaytish"""
    await message.answer(
        "🏠 **Bosh menyuga qaytingiz!**\n\n"
        "Quyidagi tugmalardan foydalaning:",
        parse_mode='Markdown',
        reply_markup=main_keyboard(message.from_user.id)
    )


# QOLGAN HANDLERLAR (oldingi kod bilan bir xil)
@dp.message_handler(lambda message: message.text == "🎯 Test topshirish")
async def take_test_interactive(message: types.Message):
    """Test topshirishni boshlash (oldingi kod bilan bir xil)"""
    # ... oldingi kodni bu yerga qo'ying ...


@dp.message_handler(lambda message: str(message.from_user.id) in user_test_states)
async def process_test_taking(message: types.Message):
    """Test topshirish jarayoni (oldingi kod bilan bir xil)"""
    # ... oldingi kodni bu yerga qo'ying ...


@dp.message_handler(lambda message: message.text == "📊 Mening natijalarim")
async def my_results(message: types.Message):
    """Foydalanuvchi natijalarini ko'rsatish (oldingi kod bilan bir xil)"""
    # ... oldingi kodni bu yerga qo'ying ...


@dp.message_handler(lambda message: message.text == "⭐ Reyting")
async def show_rating(message: types.Message):
    """Reytingni ko'rsatish (oldingi kod bilan bir xil)"""
    # ... oldingi kodni bu yerga qo'ying ...


@dp.message_handler(lambda message: message.text == "ℹ️ Yordam")
async def help_command(message: types.Message):
    """Yordam ma'lumotlarini ko'rsatish (oldingi kod bilan bir xil)"""
    # ... oldingi kodni bu yerga qo'ying ...


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
        # ... oldingi global_stats kodini bu yerga qo'ying ...
        pass

    elif data == "detailed_stats":
        # ... oldingi detailed_stats kodini bu yerga qo'ying ...
        pass

    elif data == "clear_results_confirm":
        # ... oldingi clear_results_confirm kodini bu yerga qo'ying ...
        pass

    elif data == "clear_results_yes":
        # ... oldingi clear_results_yes kodini bu yerga qo'ying ...
        pass

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