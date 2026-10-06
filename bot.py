import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]


TEXT = {
    "en": {
        "welcome": "🌍 Welcome to Kurdistan Geography!",
        "cities": "🏙️ Cities",
        "mountains": "⛰️ Mountains",
        "rivers": "🌊 Rivers & Lakes",
        "nature": "🏞️ Natural Places",
        "locations": "📍 Locations",
        "facts": "📚 Geography Facts",
        "language": "🌐 Language",
        "choose_city": "🏙️ Choose a city:",
        "back": "🔙 Back",
    },
    "ku": {
        "welcome": "🌍 بەخێربێیت بۆ جوگرافیای کوردستان!",
        "cities": "🏙️ شارەکان",
        "mountains": "⛰️ شاخەکان",
        "rivers": "🌊 ڕووبار و دەریاچەکان",
        "nature": "🏞️ شوێنە سروشتییەکان",
        "locations": "📍 شوێنەکان",
        "facts": "📚 زانیاری جوگرافی",
        "language": "🌐 زمان",
        "choose_city": "🏙️ شارێک هەڵبژێرە:",
        "back": "🔙 گەڕانەوە",
    },
}


CITIES = {
    "erbil": {
        "en": {
            "name": "🏙️ Erbil",
            "text": (
                "🏙️ Erbil\n\n"
                "Erbil is the capital of the Kurdistan Region of Iraq "
                "and one of the oldest continuously inhabited cities in the world.\n\n"
                "📍 Famous for: Erbil Citadel, Sami Abdulrahman Park, "
                "and its historic bazaars."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Erbil+Iraq",
        },
        "ku": {
            "name": "🏙️ هەولێر",
            "text": (
                "🏙️ هەولێر\n\n"
                "هەولێر پایتەختی هەرێمی کوردستانی عێراقە و "
                "یەکێکە لە کۆنترین شارە بەردەوام نیشتەجێبووەکانی جیهان.\n\n"
                "📍 بەناوبانگە بە: قەڵای هەولێر، پارکی سامی "
                "عبدالڕەحمان و بازاڕە کۆنەکەی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Erbil+Iraq",
        },
    },
    "sulaymaniyah": {
        "en": {
            "name": "🏙️ Sulaymaniyah",
            "text": (
                "🏙️ Sulaymaniyah\n\n"
                "Sulaymaniyah is a major cultural and educational city "
                "in the Kurdistan Region of Iraq.\n\n"
                "📍 Famous for: Azmar Mountain, Dukan area, museums, "
                "and its cultural life."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sulaymaniyah+Iraq",
        },
        "ku": {
            "name": "🏙️ سلێمانی",
            "text": (
                "🏙️ سلێمانی\n\n"
                "سلێمانی یەکێکە لە شارە گرنگە کەلتووری و خوێندنگەییەکانی "
                "هەرێمی کوردستانی عێراق.\n\n"
                "📍 بەناوبانگە بە: شاخی ئەزمەر، ناوچەی دوکان، "
                "مۆزەخانەکان و ژیانی کەلتووری."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sulaymaniyah+Iraq",
        },
    },
    "duhok": {
        "en": {
            "name": "🏙️ Duhok",
            "text": (
                "🏙️ Duhok\n\n"
                "Duhok is a city surrounded by mountains in the "
                "northern part of the Kurdistan Region.\n\n"
                "📍 Famous for: Duhok Dam, Zawa Mountain, "
                "and its scenic valleys."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Iraq",
        },
        "ku": {
            "name": "🏙️ دهۆک",
            "text": (
                "🏙️ دهۆک\n\n"
                "دهۆک شارێکە لە بەشی باکووری هەرێمی کوردستان "
                "کە بە شاخەکان دەورەدراوە.\n\n"
                "📍 بەناوبانگە بە: بەندی دهۆک، شاخی زاوا "
                "و دۆڵە جوانەکانی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Iraq",
        },
    },
    "halabja": {
        "en": {
            "name": "🏙️ Halabja",
            "text": (
                "🏙️ Halabja\n\n"
                "Halabja is a city in the Kurdistan Region, "
                "near the Iranian border and the Hawraman mountains.\n\n"
                "📍 The city is known for its history, culture, "
                "and surrounding mountain landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halabja+Iraq",
        },
        "ku": {
            "name": "🏙️ هەڵەبجە",
            "text": (
                "🏙️ هەڵەبجە\n\n"
                "هەڵەبجە شارێکە لە هەرێمی کوردستان، "
                "نزیک سنووری ئێران و شاخەکانی هەورامان.\n\n"
                "📍 شارەکە بە مێژوو، کەلتوور و دیمەنی شاخاویی "
                "دەوروبەرەکەی ناسراوە."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halabja+Iraq",
        },
    },
    "akre": {
        "en": {
            "name": "🏙️ Akre",
            "text": (
                "🏙️ Akre\n\n"
                "Akre is a historic mountain city in the Duhok Governorate "
                "of the Kurdistan Region.\n\n"
                "📍 Famous for: its old houses, mountains, "
                "and traditional Newroz celebrations."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Akre+Iraq",
        },
        "ku": {
            "name": "🏙️ ئاکرێ",
            "text": (
                "🏙️ ئاکرێ\n\n"
                "ئاکرێ شارێکی مێژوویی شاخاوییە لە پارێزگای دهۆک "
                "لە هەرێمی کوردستان.\n\n"
                "📍 بەناوبانگە بە: خانووە کۆنەکان، شاخەکان "
                "و جەژنی نەورۆزی نەریتی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Akre+Iraq",
        },
    },
    "rawanduz": {
        "en": {
            "name": "🏙️ Rawanduz",
            "text": (
                "🏙️ Rawanduz\n\n"
                "Rawanduz is a historic town surrounded by dramatic "
                "mountains and deep valleys in Erbil Governorate.\n\n"
                "📍 Famous for: Rawanduz Canyon and Bekhal waterfall."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+Iraq",
        },
        "ku": {
            "name": "🏙️ ڕەواندز",
            "text": (
                "🏙️ ڕەواندز\n\n"
                "ڕەواندز شارۆچکەیەکی مێژووییە کە بە شاخ و "
                "دۆڵە قووڵەکان دەورەدراوە لە پارێزگای هەولێر.\n\n"
                "📍 بەناوبانگە بە: کانی ڕەواندز و ئاوی بەخاڵ."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+Iraq",
        },
    },
    "shaqlawa": {
        "en": {
            "name": "🏙️ Shaqlawa",
            "text": (
                "🏙️ Shaqlawa\n\n"
                "Shaqlawa is a popular mountain town in Erbil Governorate, "
                "known for its pleasant climate and surrounding mountains.\n\n"
                "📍 Famous for: Safeen Mountain and its green landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shaqlawa+Iraq",
        },
        "ku": {
            "name": "🏙️ شەقڵاوە",
            "text": (
                "🏙️ شەقڵاوە\n\n"
                "شەقڵاوە شارۆچکەیەکی شاخاوییە لە پارێزگای هەولێر "
                "و بە کەش و هەوای خۆش و شاخەکانی دەوروبەر ناسراوە.\n\n"
                "📍 بەناوبانگە بە: شاخی سەفین و دیمەنی سەوز."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shaqlawa+Iraq",
        },
    },
    "zakho": {
        "en": {
            "name": "🏙️ Zakho",
            "text": (
                "🏙️ Zakho\n\n"
                "Zakho is a city in Duhok Governorate near the "
                "Iraq–Turkey border.\n\n"
                "📍 Famous for: Delal Bridge, the Khabur River, "
                "and its important location for regional trade."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zakho+Iraq",
        },
        "ku": {
            "name": "🏙️ زاخۆ",
            "text": (
                "🏙️ زاخۆ\n\n"
                "زاخۆ شارێکە لە پارێزگای دهۆک و نزیک سنووری "
                "عێراق و تورکیایە.\n\n"
                "📍 بەناوبانگە بە: پردی دڵاڵ، ڕووباری خابوور "
                "و شوێنی گرنگی بازرگانی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zakho+Iraq",
        },
    },
}


def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏔️ کوردی",
                callback_data="lang_ku"
            ),
            InlineKeyboardButton(
                "🇬🇧 English",
                callback_data="lang_en"
            ),
        ]
    ])


def main_keyboard(lang):
    t = TEXT[lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(t["cities"], callback_data="cities"),
            InlineKeyboardButton(t["mountains"], callback_data="mountains"),
        ],
        [
            InlineKeyboardButton(t["rivers"], callback_data="rivers"),
            InlineKeyboardButton(t["nature"], callback_data="nature"),
        ],
        [
            InlineKeyboardButton(t["locations"], callback_data="locations"),
            InlineKeyboardButton(t["facts"], callback_data="facts"),
        ],
        [
            InlineKeyboardButton(t["language"], callback_data="language"),
        ],
    ])


def cities_keyboard(lang):
    names = {
        "en": [
            ("Erbil", "erbil"),
            ("Sulaymaniyah", "sulaymaniyah"),
            ("Duhok", "duhok"),
            ("Halabja", "halabja"),
            ("Akre", "akre"),
            ("Rawanduz", "rawanduz"),
            ("Shaqlawa", "shaqlawa"),
            ("Zakho", "zakho"),
        ],
        "ku": [
            ("هەولێر", "erbil"),
            ("سلێمانی", "sulaymaniyah"),
            ("دهۆک", "duhok"),
            ("هەڵەبجە", "halabja"),
            ("ئاکرێ", "akre"),
            ("ڕەواندز", "rawanduz"),
            ("شەقڵاوە", "shaqlawa"),
            ("زاخۆ", "zakho"),
        ],
    }

    buttons = []

    for name, city_id in names[lang]:
        buttons.append([
            InlineKeyboardButton(
                name,
                callback_data=f"city_{city_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            TEXT[lang]["back"],
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(buttons)


def city_keyboard(city_id, lang):
    city = CITIES[city_id][lang]

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📍 Google Maps",
                url=city["map"]
            )
        ],
        [
            InlineKeyboardButton(
                TEXT[lang]["back"],
                callback_data="cities"
            )
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["language"] = "en"

    await update.message.reply_text(
        "🌍 Kurdistan Geography\n\n"
        "🌐 Choose your language / زمان هەڵبژێرە:",
        reply_markup=language_keyboard(),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("lang_"):
        lang = data.replace("lang_", "")
        context.user_data["language"] = lang

        await query.edit_message_text(
            TEXT[lang]["welcome"],
            reply_markup=main_keyboard(lang),
        )
        return

    lang = context.user_data.get("language", "en")

    if data == "cities":
        await query.edit_message_text(
            TEXT[lang]["choose_city"],
            reply_markup=cities_keyboard(lang),
        )
        return

    if data.startswith("city_"):
        city_id = data.replace("city_", "")
        city = CITIES[city_id][lang]

        await query.edit_message_text(
            city["text"],
            reply_markup=city_keyboard(city_id, lang),
        )
        return

    if data == "back_main":
        await query.edit_message_text(
            TEXT[lang]["welcome"],
            reply_markup=main_keyboard(lang),
        )
        return

    if data == "language":
        await query.edit_message_text(
            TEXT[lang]["choose"],
            reply_markup=language_keyboard(),
        )
        return

    messages = {
        "mountains": {
            "en": "⛰️ Mountains\n\nComing soon...",
            "ku": "⛰️ شاخەکان\n\nبەم زووانە...",
        },
        "rivers": {
            "en": "🌊 Rivers & Lakes\n\nComing soon...",
            "ku": "🌊 ڕووبار و دەریاچەکان\n\nبەم زووانە...",
        },
        "nature": {
            "en": "🏞️ Natural Places\n\nComing soon...",
            "ku": "🏞️ شوێنە سروشتییەکان\n\nبەم زووانە...",
        },
        "locations": {
            "en": "📍 Locations\n\nComing soon...",
            "ku": "📍 شوێنەکان\n\nبەم زووانە...",
        },
        "facts": {
            "en": "📚 Geography Facts\n\nComing soon...",
            "ku": "📚 زانیاری جوگرافیایی\n\nبەم زووانە...",
        },
    }

    if data in messages:
        await query.edit_message_text(
            messages[data][lang],
            reply_markup=main_keyboard(lang),
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("Kurdistan Geography Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
