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
        print(f"Ma'lumotlarni yuklashda xatolik: {e}")
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
        print("Ma'lumotlar saqlandi")
    except Exception as e:
        print(f"Ma'lumotlarni saqlashda xatolik: {e}")


# Dastlabki ma'lumotlarni yuklash
load_data()

# Adminlar ro'yxati
ADMINS = [6777571934]

# Ro'yxatdan o'tish bosqichlari
user_registration = {}


# Asosiy klaviatura
def main_keyboard(user_id=None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        KeyboardButton("🎯 Test topshirish"),
        KeyboardButton("📊 Mening natijalarim"),
        KeyboardButton("⭐ Reyting"),
        KeyboardButton("ℹ️ Yordam")
    ]

    # Agar user_id berilgan bo'lsa va admin bo'lsa
    if user_id and user_id in ADMINS:
        buttons.append(KeyboardButton("👨‍🏫 Admin panel"))

    keyboard.add(*buttons)
    return keyboard


# Admin klaviatura
def admin_keyboard():
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


# Test qo'shish bosqichlari
admin_test_states = {}


# Start komandasi
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
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
            # Kanallik bor, ro'yxatdan o'tishni boshlaymiz
            await start_registration(message)
        else:
            # Kanallik yo'q, obuna qilishni so'raymiz
            await request_channel_subscription(message)
    except Exception as e:
        print(f"Kanalni tekshirishda xatolik: {e}")
        await request_channel_subscription(message)


async def request_channel_subscription(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=CHANNEL_LINK),
        InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subscription")
    )

    await message.answer(
        "👋 **Botdan foydalanish uchun kanalimizga obuna bo'ling!**\n\n"
        f"Kanal: {CHANNEL_ID}\n\n"
        "Kanalda testlar joylanadi va siz ularni yuklab olishingiz mumkin.\n"
        "Obuna bo'lgach, '✅ Obunani tekshirish' tugmasini bosing.",
        parse_mode='Markdown',
        reply_markup=keyboard
    )


async def start_registration(message: types.Message):
    user_id = str(message.from_user.id)

    # Agar allaqachon ro'yxatdan o'tgan bo'lsa
    if user_id in registrations and registrations[user_id].get('registered', False):
        welcome_text = "🎉 Assalomu alaykum! TestBotga xush kelibsiz!\n\n"
        welcome_text += "📚 **Bu bot orqali siz:**\n"
        welcome_text += "• Testlarni topshirishingiz mumkin\n"
        welcome_text += "• Natijalaringizni ko'rishingiz mumkin\n"
        welcome_text += "• Reytingda o'ringa ega bo'lishingiz mumkin\n\n"

        welcome_text += "👇 **Qanday ishlatish:**\n"
        welcome_text += "1. Kanaldan (@testlar231) PDF testni oling\n"
        welcome_text += "2. PDF da test kodini toping\n"
        welcome_text += "3. Botga shu formatda yozing: `KOD JAVOBLAR`\n"
        welcome_text += "4. **MISOL:** `MATEM1 ABCDA`\n\n"
        welcome_text += "Agar test kodini bilmasangiz, kanalga qarang: @testlar231\n\n"

        if message.from_user.id in ADMINS:
            welcome_text += "👨‍🏫 **Siz adminsiz!** Test javoblarini kiritishingiz mumkin.\n\n"

        welcome_text += "Quyidagi tugmalardan foydalaning:"

        await message.answer(welcome_text, parse_mode='Markdown',
                             reply_markup=main_keyboard(message.from_user.id))
        return

    # Ro'yxatdan o'tish bosqichlarini boshlaymiz
    user_registration[user_id] = {
        'step': 1,  # 1-ism, 2-viloyat, 3-tuman
        'data': {}
    }

    await message.answer(
        "👤 **Ro'yxatdan o'tish**\n\n"
        "Botdan to'liq foydalanish uchun ro'yxatdan o'ting.\n\n"
        "1-bosqich: **Ism familiyangizni kiriting**\n\n"
        "Misol: **Alijon Valiyev**",
        parse_mode='Markdown'
    )


# Ro'yxatdan o'tish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in user_registration)
async def process_registration(message: types.Message):
    user_id = str(message.from_user.id)
    state = user_registration[user_id]
    step = state['step']

    if step == 1:  # Ism familiya
        full_name = message.text.strip()
        if len(full_name) < 3:
            await message.answer("❌ Ism familiya kamida 3 ta belgidan iborat bo'lishi kerak!")
            return

        state['data']['full_name'] = full_name
        state['step'] = 2

        # Viloyatlar klaviaturasi
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        regions_list = list(REGIONS.keys())
        for i in range(0, len(regions_list), 2):
            row = regions_list[i:i + 2]
            keyboard.add(*[KeyboardButton(region) for region in row])

        await message.answer(
            f"✅ Ism familiya qabul qilindi: **{full_name}**\n\n"
            "2-bosqich: **Viloyatingizni tanlang**\n\n"
            "Quyidagi viloyatlardan birini tanlang:",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    elif step == 2:  # Viloyat
        region = message.text.strip()
        if region not in REGIONS:
            await message.answer("❌ Iltimos, ro'yxatdagi viloyatlardan birini tanlang!")
            return

        state['data']['region'] = region
        state['step'] = 3

        # Tumanlar klaviaturasi
        districts = REGIONS[region]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        # Tumanlarni guruhlab chiqaramiz
        for i in range(0, len(districts), 3):
            row = districts[i:i + 3]
            keyboard.add(*[KeyboardButton(district) for district in row])

        keyboard.add(KeyboardButton("🔙 Orqaga"))

        await message.answer(
            f"✅ Viloyat qabul qilindi: **{region}**\n\n"
            "3-bosqich: **Tumaningizni tanlang**\n\n"
            "Quyidagi tumanlardan birini tanlang:",
            parse_mode='Markdown',
            reply_markup=keyboard
        )

    elif step == 3:  # Tuman
        if message.text == "🔙 Orqaga":
            # Orqaga qaytish
            state['step'] = 2
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            regions_list = list(REGIONS.keys())
            for i in range(0, len(regions_list), 2):
                row = regions_list[i:i + 2]
                keyboard.add(*[KeyboardButton(region) for region in row])

            await message.answer(
                "Viloyatingizni qayta tanlang:",
                reply_markup=keyboard
            )
            return

        district = message.text.strip()
        region = state['data']['region']

        if district not in REGIONS[region]:
            await message.answer("❌ Iltimos, ro'yxatdagi tumanlardan birini tanlang!")
            return

        state['data']['district'] = district

        # Ma'lumotlarni saqlash
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

        # Holatni tozalash
        del user_registration[user_id]

        await message.answer(
            f"🎉 **Tabriklaymiz! Ro'yxatdan o'tdingiz!**\n\n"
            f"👤 **Ism familiya:** {state['data']['full_name']}\n"
            f"📍 **Manzil:** {region}, {district}\n"
            f"📅 **Ro'yxatdan o'tilgan sana:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"✅ Endi siz test topshira olasiz!\n\n"
            f"Test topshirish uchun:\n"
            f"1. Kanaldan PDF testni oling (@testlar231)\n"
            f"2. Test kodini toping\n"
            f"3. Botga yuboring: `KOD JAVOBLAR`\n\n"
            f"**Misol:** `MATEM1 ABCDA`",
            parse_mode='Markdown',
            reply_markup=main_keyboard(message.from_user.id)
        )


# Admin panel
@dp.message_handler(lambda message: message.text == "👨‍🏫 Admin panel")
async def admin_panel(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Bu bo'lim faqat adminlar uchun!",
                             reply_markup=main_keyboard(message.from_user.id))
        return

    admin_stats = f"👨‍🏫 **Admin Panel**\n\n"
    admin_stats += f"📊 **Statistika:**\n"
    admin_stats += f"• Testlar soni: {len(tests_db)} ta\n"
    admin_stats += f"• Jami foydalanuvchilar: {len(registrations)} ta\n"
    admin_stats += f"• Test topshirganlar: {sum(1 for u in user_results.values() if u.get('tests_taken', 0) > 0)} ta\n\n"

    # Adminning testlari
    admin_tests = [code for code, test in tests_db.items()
                   if test.get('creator_id') == str(message.from_user.id)]

    if admin_tests:
        admin_stats += f"📝 **Sizning testlaringiz:** {len(admin_tests)} ta\n"
        for code in admin_tests[-3:]:  # So'nggi 3 ta test
            test_takers = sum(1 for u in user_results.values() if code in u.get('tests', {}))
            admin_stats += f"• {code} ({test_takers} ta odam ishlagan)\n"

    await message.answer(admin_stats, parse_mode='Markdown', reply_markup=admin_keyboard())


# ➕ TEST JAVOBLARINI KIRITISH (faqat adminlar uchun)
@dp.message_handler(lambda message: message.text == "➕ Test javoblarini kiritish" and message.from_user.id in ADMINS)
async def add_test_answers_start(message: types.Message):
    user_id = str(message.from_user.id)

    # Adminni test javoblarini kiritish holatiga o'tkazamiz
    admin_test_states[user_id] = {
        'step': 1,  # 1-kod, 2-savollar soni, 3-javoblar
        'data': {}
    }

    await message.answer(
        "➕ **Test javoblarini kiritish**\n\n"
        "Bu yerda siz kanalga joylagan PDF testining javoblarini kiritasiz.\n\n"
        "1-bosqich: **Test kodini kiriting**\n\n"
        "PDF da berilgan test kodini kiriting.\n"
        "Bu kod foydalanuvchilar tomonidan test topshirishda ishlatiladi.\n\n"
        "Misol: `MATEM1`, `FIZIKA_2`, `TEST2024`",
        parse_mode='Markdown'
    )


# Test javoblarini kiritish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in admin_test_states)
async def process_test_answers(message: types.Message):
    user_id = str(message.from_user.id)
    state = admin_test_states[user_id]
    step = state['step']

    try:
        if step == 1:  # Test kodi
            test_code = message.text.strip().upper()

            # Kodni tekshirish
            if not test_code.replace('_', '').isalnum():
                await message.answer(
                    "❌ Noto'g'ri format! Test kodi faqat harf, raqam va _ belgisidan iborat bo'lishi kerak.")
                return

            if test_code in tests_db:
                await message.answer(
                    f"❌ '{test_code}' kodli test allaqachon mavjud!\n"
                    f"Agar yangilamoqchi bo'lsangiz, avval o'chiring."
                )
                return

            state['data']['code'] = test_code
            state['step'] = 2

            await message.answer(
                f"✅ Kod qabul qilindi: `{test_code}`\n\n"
                "2-bosqich: **Savollar sonini kiriting**\n\n"
                "PDF dagi savollar sonini raqamda kiriting.\n"
                "Misol: 10, 15, 20\n\n"
                "1 dan 100 gacha bo'lishi mumkin",
                parse_mode='Markdown'
            )

        elif step == 2:  # Savollar soni
            try:
                questions_count = int(message.text.strip())
                if questions_count < 1 or questions_count > 100:
                    await message.answer("❌ Savollar soni 1 dan 100 gacha bo'lishi kerak!")
                    return

                state['data']['questions_count'] = questions_count
                state['step'] = 3

                await message.answer(
                    f"✅ Savollar soni: {questions_count}\n\n"
                    "3-bosqich: **To'g'ri javoblarni kiriting**\n\n"
                    f"**PDF dagi to'g'ri javoblarni ketma-ket kiriting.**\n"
                    f"Har bir savol uchun A, B, C, D harflaridan birini yozing.\n"
                    f"Masalan, 5 ta savol uchun: `ABCDA`\n\n"
                    f"Iltimos, {questions_count} ta javob kiriting:",
                    parse_mode='Markdown'
                )

            except ValueError:
                await message.answer("❌ Faqat raqam kiriting!")

        elif step == 3:  # To'g'ri javoblar
            answers = message.text.strip().upper()
            questions_count = state['data']['questions_count']

            if len(answers) != questions_count:
                await message.answer(f"❌ Javoblar soni noto'g'ri! {questions_count} ta javob kiriting.")
                return

            # Har bir javob A, B, C, D bo'lishini tekshirish
            valid_answers = {'A', 'B', 'C', 'D'}
            for ans in answers:
                if ans not in valid_answers:
                    await message.answer(f"❌ Noto'g'ri javob! Faqat A, B, C, D harflaridan foydalaning.")
                    return

            # Testni saqlash
            test_code = state['data']['code']
            tests_db[test_code] = {
                'javoblar': answers,
                'narx': 2,  # Har bir to'g'ri javob uchun 2 ball
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'created_by': message.from_user.username or message.from_user.full_name,
                'creator_id': user_id,
                'questions_count': questions_count,
                'test_type': 'pdf'  # PDF testi ekanligini bildiradi
            }

            save_data()

            # Holatni tozalash
            del admin_test_states[user_id]

            await message.answer(
                f"🎉 **Test javoblari muvaffaqiyatli saqlandi!**\n\n"
                f"**Test kodi:** `{test_code}`\n"
                f"**Savollar soni:** {questions_count} ta\n"
                f"**To'g'ri javoblar:** {answers}\n\n"
                f"Foydalanuvchilar endi bu testni topshira oladilar:\n"
                f"`{test_code} [o'z javoblari]`\n\n"
                f"**Misol:** `{test_code} ABCDA`\n\n"
                f"✅ PDF testi kanalga joylangan va javoblari botga kiritilgan.",
                parse_mode='Markdown',
                reply_markup=admin_keyboard()
            )

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, qaytadan urinib ko'ring.")
        if user_id in admin_test_states:
            del admin_test_states[user_id]


# Test javoblari uchun yangi interaktiv usul
user_test_states = {}


# 🎯 TEST TOPSHIRISH - Yangi interaktiv usul
@dp.message_handler(lambda message: message.text == "🎯 Test topshirish")
async def take_test_interactive(message: types.Message):
    user_id = str(message.from_user.id)

    # Ro'yxatdan o'tganligini tekshirish
    if user_id not in registrations or not registrations[user_id].get('registered', False):
        await message.answer(
            "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
            "Ro'yxatdan o'tish uchun /start buyrug'ini yuboring.",
            parse_mode='Markdown'
        )
        return

    # Test kodini kiritishni boshlaymiz
    user_test_states[user_id] = {
        'step': 1,  # 1-test kodi, 2-bosqichma-bosqich javoblar
        'data': {}
    }

    await message.answer(
        "🎯 **Test topshirish (bosqichma-bosqich)**\n\n"
        "1-bosqich: **Test kodini kiriting**\n\n"
        "PDF fayldagi test kodini kiriting.\n"
        "Misol: `MATEM1`, `FIZIKA_2`, `TEST2024`\n\n"
        "Kodingizni kiriting:",
        parse_mode='Markdown'
    )


# Test topshirish bosqichlari
@dp.message_handler(lambda message: str(message.from_user.id) in user_test_states)
async def process_test_taking(message: types.Message):
    user_id = str(message.from_user.id)
    state = user_test_states[user_id]
    step = state['step']

    try:
        if step == 1:  # Test kodi
            test_code = message.text.strip().upper()

            # Test mavjudligini tekshirish
            if test_code not in tests_db:
                await message.answer(
                    f"❌ **{test_code} testi topilmadi!**\n\n"
                    f"Test kodini to'g'ri kiritganingizni tekshiring.\n"
                    f"Kanaldan test kodini oling: @testlar231",
                    parse_mode='Markdown'
                )
                # Holatni saqlab qo'yamiz
                state['data']['test_code'] = test_code
                return

            test_data = tests_db[test_code]
            questions_count = len(test_data['javoblar'])

            state['data']['test_code'] = test_code
            state['data']['questions_count'] = questions_count
            state['data']['current_question'] = 1
            state['data']['user_answers'] = []
            state['step'] = 2

            await message.answer(
                f"✅ **{test_code} testi topildi!**\n\n"
                f"📊 **Test ma'lumotlari:**\n"
                f"• Savollar soni: {questions_count} ta\n"
                f"• Har bir to'g'ri javob: 2 ball\n\n"
                f"Endi savollarga javob bering.\n\n"
                f"**1-savol:** A, B, C, D harflaridan birini kiriting:",
                parse_mode='Markdown'
            )

        elif step == 2:  # Javoblarni qabul qilish
            answer = message.text.strip().upper()
            current_q = state['data']['current_question']
            total_q = state['data']['questions_count']

            # Javobni tekshirish
            if answer not in ['A', 'B', 'C', 'D']:
                await message.answer(
                    "❌ Noto'g'ri javob!\n"
                    "Faqat A, B, C, D harflaridan birini kiriting."
                )
                return

            # Javobni saqlash
            state['data']['user_answers'].append(answer)

            # Keyingi savolga o'tish yoki natijani hisoblash
            if current_q < total_q:
                state['data']['current_question'] += 1
                next_q = state['data']['current_question']

                await message.answer(
                    f"✅ {current_q}-savol qabul qilindi: **{answer}**\n\n"
                    f"**{next_q}-savol:** A, B, C, D harflaridan birini kiriting:",
                    parse_mode='Markdown'
                )
            else:
                # Barcha javoblarni olib bo'ldik, natijani hisoblaymiz
                test_code = state['data']['test_code']
                user_answers = state['data']['user_answers']
                test_data = tests_db[test_code]
                correct_answers = test_data['javoblar']

                # Natijani hisoblash
                correct_count = 0
                for i in range(len(correct_answers)):
                    if user_answers[i] == correct_answers[i]:
                        correct_count += 1

                wrong_count = len(correct_answers) - correct_count
                total_score = correct_count * 2
                max_score = len(correct_answers) * 2
                percentage = (correct_count / len(correct_answers)) * 100 if len(correct_answers) > 0 else 0

                # Baholash
                if percentage >= 90:
                    grade = "🎉 A'lo!"
                    emoji = "🌟"
                elif percentage >= 80:
                    grade = "👍 Yaxshi!"
                    emoji = "✅"
                elif percentage >= 60:
                    grade = "😊 Qoniqarli"
                    emoji = "📊"
                else:
                    grade = "📚 Yana urinib ko'ring"
                    emoji = "🔄"

                # Ma'lumotlarni saqlash
                if user_id not in user_results:
                    user_results[user_id] = {
                        'username': message.from_user.username or message.from_user.full_name,
                        'full_name': registrations.get(user_id, {}).get('full_name', ''),
                        'region': registrations.get(user_id, {}).get('region', ''),
                        'district': registrations.get(user_id, {}).get('district', ''),
                        'first_seen': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'tests_taken': 0,
                        'total_score': 0,
                        'tests': {},
                        'registered': True
                    }

                # Test yangi bo'lsa, tests_taken ni oshiramiz
                is_new_test = test_code not in user_results[user_id]['tests']

                # Eski natijani olib tashlash (agar mavjud bo'lsa)
                old_score = 0
                if test_code in user_results[user_id]['tests']:
                    old_score = user_results[user_id]['tests'][test_code].get('score', 0)
                    user_results[user_id]['total_score'] = user_results[user_id].get('total_score', 0) - old_score
                    user_results[user_id]['tests_taken'] = user_results[user_id].get('tests_taken', 0) - 1

                # Yangi natijani saqlash
                user_results[user_id]['tests'][test_code] = {
                    'correct': correct_count,
                    'wrong': wrong_count,
                    'score': total_score,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'answers': ''.join(user_answers)
                }

                # Umumiy ko'rsatkichlarni yangilash
                if is_new_test:
                    user_results[user_id]['tests_taken'] = user_results[user_id].get('tests_taken', 0) + 1

                user_results[user_id]['total_score'] = user_results[user_id].get('total_score', 0) + total_score

                # Saqlash
                save_data()

                # Bu testda nechta odam ishlaganligini hisoblash
                test_takers = 0
                for u in user_results.values():
                    if test_code in u.get('tests', {}):
                        test_takers += 1

                # Natijani chiqarish
                result_message = f"{emoji} **PDF TEST NATIJALARI** {emoji}\n\n"
                result_message += f"📌 **Test kodi:** `{test_code}`\n"
                result_message += f"👤 **Ism:** {registrations.get(user_id, {}).get('full_name', '')}\n"
                result_message += f"📍 **Manzil:** {registrations.get(user_id, {}).get('region', '')}, {registrations.get(user_id, {}).get('district', '')}\n"
                result_message += f"📊 **Umumiy savollar:** {len(correct_answers)} ta\n\n"
                result_message += f"🏆 **Sizning natijangiz:**\n"
                result_message += f"✅ To'g'ri javoblar: {correct_count} ta\n"
                result_message += f"❌ Noto'g'ri javoblar: {wrong_count} ta\n"
                result_message += f"🎯 Olingan ball: {total_score}/{max_score}\n"
                result_message += f"📈 Foiz: {percentage:.1f}%\n\n"
                result_message += f"**Baholash:** {grade}\n\n"
                result_message += f"📊 **Statistika:** Bu testda jami **{test_takers}** ta odam ishlagan\n\n"

                # Test muallifi
                creator = test_data.get('created_by', 'Noma\'lum')
                result_message += f"👨‍💻 **Test muallifi:** {creator}\n\n"

                # Javoblar tafsiloti
                result_message += f"📋 **Javoblar tafsiloti:**\n"
                for i in range(len(correct_answers)):
                    if user_answers[i] == correct_answers[i]:
                        result_message += f"{i + 1}. ✅ **{user_answers[i]}**\n"
                    else:
                        result_message += f"{i + 1}. ❌ **{user_answers[i]}** (to'g'ri: **{correct_answers[i]}**)\n"

                # Holatni tozalash
                del user_test_states[user_id]

                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(
                    InlineKeyboardButton("🔄 Yangi test", callback_data="take_another_test"),
                    InlineKeyboardButton("⭐ Reyting", callback_data="show_rating"),
                    InlineKeyboardButton("📊 Natijalarim", callback_data="show_my_results")
                )

                await message.answer(result_message, parse_mode='Markdown', reply_markup=keyboard)

                # Test muallifiga xabar (agar admin bo'lsa)
                creator_id = test_data.get('creator_id')
                if creator_id and creator_id != user_id:
                    try:
                        await bot.send_message(
                            int(creator_id),
                            f"📢 **Yangi test natijasi!**\n\n"
                            f"Test: `{test_code}`\n"
                            f"Foydalanuvchi: {registrations.get(user_id, {}).get('full_name', '')}\n"
                            f"Manzil: {registrations.get(user_id, {}).get('region', '')}, {registrations.get(user_id, {}).get('district', '')}\n"
                            f"To'g'ri javoblar: {correct_count}/{len(correct_answers)}\n"
                            f"Ball: {total_score}/{max_score}\n"
                            f"Bu testni jami ishlaganlar: {test_takers} ta",
                            parse_mode='Markdown'
                        )
                    except Exception as e:
                        print(f"Adminga xabar yuborishda xatolik: {e}")

                print(f"✅ Test topshirildi: {test_code} | User: {user_id} | Ball: {total_score}")

    except Exception as e:
        print(f"❌ Test topshirishda xatolik: {e}")
        await message.answer(
            f"❌ **Xatolik yuz berdi!**\n\n"
            f"Iltimos, qaytadan urinib ko'ring yoki /start buyrug'i orqali boshlang.",
            parse_mode='Markdown'
        )
        if user_id in user_test_states:
            del user_test_states[user_id]


# 📊 MENING NATIJALARIM
@dp.message_handler(lambda message: message.text == "📊 Mening natijalarim")
async def my_results(message: types.Message):
    user_id = str(message.from_user.id)

    # Ro'yxatdan o'tganligini tekshirish
    if user_id not in registrations or not registrations[user_id].get('registered', False):
        await message.answer(
            "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
            "Ro'yxatdan o'tish uchun /start buyrog'ini yuboring.",
            parse_mode='Markdown'
        )
        return

    if user_id not in user_results or not user_results[user_id].get('tests'):
        await message.answer(
            "📭 **Siz hali test topshirmagansiz!**\n\n"
            "Birinchi testni topshirish uchun:\n"
            "1. Kanaldan PDF testni oling (@testlar231)\n"
            "2. Test kodini toping\n"
            "3. '🎯 Test topshirish' tugmasini bosing\n\n"
            "Yoki qisqa usul:\n"
            "`KOD JAVOBLAR` formatida yuboring\n"
            "**Misol:** `TEST123 ABCDA`",
            parse_mode='Markdown'
        )
        return

    user_data = user_results[user_id]
    reg_data = registrations.get(user_id, {})
    tests_taken = user_data.get('tests_taken', 0)
    total_score = user_data.get('total_score', 0)

    response = f"👤 **Sizning statistikangiz:**\n\n"
    response += f"👤 **Ism:** {reg_data.get('full_name', '')}\n"
    response += f"📍 **Manzil:** {reg_data.get('region', '')}, {reg_data.get('district', '')}\n\n"
    response += f"📈 **Umumiy:**\n"
    response += f"• Topshirilgan testlar: {tests_taken} ta\n"
    response += f"• Jami ball: {total_score}\n"

    if tests_taken > 0:
        avg_score = total_score / tests_taken
        response += f"• O'rtacha ball: {avg_score:.1f}\n\n"

    response += f"📋 **So'nggi 3 ta test:**\n"

    # So'nggi 3 ta test natijasi
    user_tests = list(user_data.get('tests', {}).items())[-3:]
    for test_code, results in user_tests:
        test_info = tests_db.get(test_code, {})
        total_q = len(test_info.get('javoblar', ''))

        response += f"\n📌 **{test_code}**\n"
        response += f"   ✅ To'g'ri: {results['correct']}/{total_q}\n"
        response += f"   🎯 Ball: {results['score']}\n"
        response += f"   📅 {results.get('date', '')}\n"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("📊 Batafsil statistika", callback_data="detailed_stats"),
        InlineKeyboardButton("🗑️ Natijalarni tozalash", callback_data="clear_results")
    )

    await message.answer(response, parse_mode='Markdown', reply_markup=keyboard)


# ⭐ REYTING - yangilangan
@dp.message_handler(lambda message: message.text == "⭐ Reyting")
async def show_rating(message: types.Message):
    # Foydalanuvchilarni ballar bo'yicha saralash
    sorted_users = []
    for uid, data in user_results.items():
        if data.get('total_score', 0) > 0 and data.get('registered', False):
            # Foydalanuvchi nomini aniqlash
            reg_data = registrations.get(uid, {})
            full_name = reg_data.get('full_name', data.get('username', 'Noma\'lum'))
            if len(full_name) > 20:
                full_name = full_name[:17] + "..."

            region = reg_data.get('region', '')
            district = reg_data.get('district', '')

            sorted_users.append((uid, data, full_name, region, district))

    if not sorted_users:
        await message.answer("📭 Hozircha reyting mavjud emas. Birinchi bo'ling!")
        return

    sorted_users.sort(key=lambda x: x[1].get('total_score', 0), reverse=True)
    sorted_users = sorted_users[:10]  # Faqat top 10

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
        rating_text += f"   📍 {region}, {district}\n"
        rating_text += f"   • Ball: {total_score} ⭐\n"
        rating_text += f"   • Testlar: {tests_taken} ta\n"

        if tests_taken > 0:
            avg_score = total_score / tests_taken
            rating_text += f"   • O'rtacha: {avg_score:.1f} ball\n"

        rating_text += "\n"

    rating_text += "✨ **O'z o'rningizni oshiring!** ✨"

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔄 Yangilash", callback_data="refresh_rating"),
        InlineKeyboardButton("📈 Umumiy statistika", callback_data="global_stats")
    )

    await message.answer(rating_text, parse_mode='Markdown', reply_markup=keyboard)


# ℹ️ YORDAM
@dp.message_handler(lambda message: message.text == "ℹ️ Yordam")
async def help_command(message: types.Message):
    help_text = """
🤖 **PDF TEST BOT - YORDAM** 🤖

🎯 **TEST TOPSHIRISH (2 USUL):**

**1. Bosqichma-bosqich usul (Tavsiya etiladi):**
• "🎯 Test topshirish" tugmasini bosing
• Test kodini kiriting
• Har bir savolga alohida javob bering

**2. Tezkor usul:**
• `KOD JAVOBLAR` formatida yuboring
• Misol: `MATEM1 ABCDA`

📌 **Eslatmalar:**
• Avval ro'yxatdan o'tishingiz kerak
• Kanallikka obuna bo'lishingiz kerak
• Har bir to'g'ri javob 2 ball

📊 **NATIJALAR:**
• "📊 Mening natijalarim" - shaxsiy statistika
• "⭐ Reyting" - eng yaxshi foydalanuvchilar

⚠️ **QO'LLAB-QUVVATLASH:**
Muammo bo'lsa admin bilan bog'laning

📣 **KANAL:** @testlar231
"""

    if message.from_user.id in ADMINS:
        help_text += "\n\n👨‍🏫 **ADMIN QO'LLANMASI:**\n"
        help_text += "1. PDF testni kanalga joylang\n"
        help_text += "2. Admin panelga o'ting\n"
        help_text += "3. '➕ Test javoblarini kiritish' ni bosing\n"

    await message.answer(help_text, parse_mode='Markdown')


# Eski usul bilan test topshirish (qisqa format)
@dp.message_handler(lambda message: len(message.text.split()) >= 2)
async def check_test_old_method(message: types.Message):
    try:
        user_id = str(message.from_user.id)

        # Ro'yxatdan o'tganligini tekshirish
        if user_id not in registrations or not registrations[user_id].get('registered', False):
            await message.answer(
                "❌ **Avval ro'yxatdan o'tishingiz kerak!**\n\n"
                "Ro'yxatdan o'tish uchun /start buyrog'ini yuboring.",
                parse_mode='Markdown'
            )
            return

        # Kod va javoblarni olish
        text = message.text.strip().upper()
        parts = text.split()
        test_code = parts[0]
        user_answers = ''.join(parts[1:])

        # Test mavjudligini tekshirish
        if test_code not in tests_db:
            await message.answer(
                f"❌ **{test_code} testi topilmadi!**\n\n"
                f"Test kodini to'g'ri kiritganingizni tekshiring.\n"
                f"Yoki '🎯 Test topshirish' tugmasi orqali bosqichma-bosqich usuldan foydalaning.",
                parse_mode='Markdown'
            )
            return

        test = tests_db[test_code]
        correct_answers = test.get('javoblar', '')

        # Javoblar sonini tekshirish
        if len(user_answers) != len(correct_answers):
            await message.answer(
                f"⚠️ **Javoblar soni noto'g'ri!**\n\n"
                f"📝 Testda: {len(correct_answers)} ta savol\n"
                f"📝 Siz kiritdingiz: {len(user_answers)} ta\n\n"
                f"Yoki '🎯 Test topshirish' tugmasi orqali bosqichma-bosqich usuldan foydalaning.",
                parse_mode='Markdown'
            )
            return

        # Natijani hisoblash va saqlash (yuqoridagi kabi)
        # ... (yuqoridagi kodni qo'shing)

        await message.answer(
            "ℹ️ **Eski usul ishlatildi!**\n\n"
            "Keyingi safar '🎯 Test topshirish' tugmasini bosing va\n"
            "bosqichma-bosqich usuldan foydalaning.\n\n"
            "Bu sizga qulayroq bo'ladi!",
            parse_mode='Markdown'
        )

    except Exception as e:
        print(f"❌ Eski usulda xatolik: {e}")
        await message.answer(
            "❌ **Xatolik yuz berdi!**\n\n"
            "Iltimos, '🎯 Test topshirish' tugmasi orqali\n"
            "bosqichma-bosqich usuldan foydalaning.",
            parse_mode='Markdown'
        )


# CALLBACK HANDLERS
@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = str(callback_query.from_user.id)

    if data == "check_subscription":
        try:
            chat_member = await bot.get_chat_member(CHANNEL_ID, callback_query.from_user.id)
            if chat_member.status not in ['left', 'kicked']:
                await callback_query.answer("✅ Obuna qilingansiz!", show_alert=True)
                await start_registration(callback_query.message)
            else:
                await callback_query.answer("❌ Hali obuna qilmagansiz!", show_alert=True)
        except Exception as e:
            await callback_query.answer("❌ Xatolik yuz berdi!", show_alert=True)

    elif data == "take_another_test":
        await take_test_interactive(callback_query.message)

    elif data == "show_rating":
        await show_rating(callback_query.message)

    elif data == "show_my_results":
        await my_results(callback_query.message)

    elif data == "refresh_rating":
        await callback_query.answer("Reyting yangilandi!")
        await show_rating(callback_query.message)

    elif data == "detailed_stats":
        if user_id in user_results:
            user_data = user_results[user_id]
            reg_data = registrations.get(user_id, {})

            if not user_data.get('tests'):
                await callback_query.answer("Sizda natijalar yo'q!")
                return

            response = f"📊 **Batafsil statistika:**\n\n"
            response += f"👤 **Ism:** {reg_data.get('full_name', '')}\n"
            response += f"📍 **Manzil:** {reg_data.get('region', '')}, {reg_data.get('district', '')}\n"
            response += f"📅 **Ro'yxatdan o'tilgan:** {reg_data.get('registered_at', '')}\n\n"

            total_tests = len(user_data['tests'])
            total_correct = 0
            total_questions = 0

            for code, results in user_data['tests'].items():
                total_correct += results.get('correct', 0)
                test_info = tests_db.get(code, {})
                total_questions += len(test_info.get('javoblar', ''))

            response += f"📈 **Umumiy:**\n"
            response += f"• Testlar: {total_tests} ta\n"
            response += f"• Savollar: {total_questions} ta\n"
            response += f"• To'g'ri javoblar: {total_correct} ta\n"

            if total_questions > 0:
                overall_percentage = (total_correct / total_questions) * 100
                response += f"• Umumiy foiz: {overall_percentage:.1f}%\n\n"

            response += f"📋 **Har bir test:**\n"
            for test_code, results in user_data['tests'].items():
                test_info = tests_db.get(test_code, {})
                total_q = len(test_info.get('javoblar', ''))
                percentage = (results.get('correct', 0) / total_q) * 100 if total_q > 0 else 0

                response += f"\n**{test_code}**\n"
                response += f"• To'g'ri: {results.get('correct', 0)}/{total_q}\n"
                response += f"• Foiz: {percentage:.1f}%\n"
                response += f"• Sana: {results.get('date', '')}\n"

            await callback_query.message.answer(response, parse_mode='Markdown')

    elif data == "clear_results":
        if user_id in user_results:
            user_results[user_id]['tests'] = {}
            user_results[user_id]['total_score'] = 0
            user_results[user_id]['tests_taken'] = 0
            save_data()
            await callback_query.answer("✅ Natijalar tozalandi!", show_alert=True)
            await my_results(callback_query.message)

    await callback_query.answer()


# Qolgan admin funksiyalari (yuqoridagi kabi)
# ... (yuqoridagi admin funksiyalarini qo'shing)


if __name__ == '__main__':
    print("🤖 PDF TEST BOT ISHGA TUSHDI! 🎉")
    print("👨‍🏫 Adminlar:", ADMINS)
    pdf_test_count = 0
    for t in tests_db.values():
        if t.get('test_type') == 'pdf':
            pdf_test_count += 1
    print("📊 PDF Testlar soni:", pdf_test_count)
    print("👥 Ro'yxatdan o'tganlar:", len([r for r in registrations.values() if r.get('registered', False)]))
    print("📈 Test topshirganlar:", sum(1 for u in user_results.values() if u.get('tests_taken', 0) > 0))

    executor.start_polling(dp, skip_updates=True)