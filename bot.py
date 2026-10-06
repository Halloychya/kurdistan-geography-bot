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
        "choose": "Please choose a language:",
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
        "choose": "تکایە زمانەکەت هەڵبژێرە:",
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

MOUNTAINS = {
    "safine": {
        "en": {
            "name": "⛰️ Mount Safeen",
            "text": (
                "⛰️ Mount Safeen\n\n"
                "Mount Safeen is one of the famous mountains in the "
                "Erbil Governorate and rises near Shaqlawa.\n\n"
                "📍 Famous for: beautiful mountain landscapes, "
                "hiking areas, and views over the surrounding region."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Mount+Safeen+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی سەفین",
            "text": (
                "⛰️ شاخی سەفین\n\n"
                "شاخی سەفین یەکێکە لە شاخە ناسراوەکانی "
                "پارێزگای هەولێر و لە نزیکی شەقڵاوەیە.\n\n"
                "📍 بەناوبانگە بە: دیمەنی جوانی شاخستانی، "
                " شوێنی گەشت و ڕووانینە جوانەکانی ناوچەکە ، پێگه‌ی مێژویی ، به‌رهه‌مه‌سروشتیه‌كان."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Mount+Safeen+Iraq",
        },
    },

    "azmar": {
        "en": {
            "name": "⛰️ Azmar Mountain",
            "text": (
                "⛰️ Azmar Mountain\n\n"
                "Azmar Mountain overlooks Sulaymaniyah and is one of "
                "the best-known mountains around the city.\n\n"
                "📍 Famous for: panoramic views of Sulaymaniyah "
                "and the surrounding valleys."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Azmar+Mountain+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی ئەزمەر",
            "text": (
                "⛰️ شاخی ئەزمەر\n\n"
                "شاخی ئەزمەر بەسەر شاری سلێمانییەوە دەڕوانێت "
                "و یەکێکە لە شاخە ناسراوەکانی دەوروبەری شار.\n\n"
                "📍 بەناوبانگە بە: دیمەنی پانۆرامایی سلێمانی "
                "و دۆڵەکانی دەوروبەر."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Azmar+Mountain+Iraq",
        },
    },

    "zawa": {
        "en": {
            "name": "⛰️ Zawa Mountain",
            "text": (
                "⛰️ Zawa Mountain\n\n"
                "Zawa Mountain is located near Duhok and is an "
                "important natural landmark of the area.\n\n"
                "📍 Famous for: mountain views and outdoor landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zawa+Mountain+Duhok+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی زاوا",
            "text": (
                "⛰️ شاخی زاوا\n\n"
                "شاخی زاوا لە نزیکی دهۆکە و یەکێکە لە "
                "نیشانە سروشتییە گرنگەکانی ناوچەکە.\n\n"
                "📍 بەناوبانگە بە: دیمەنی شاخستانی ، ته‌له‌فریك ، دیمه‌نی پانۆرامای دڵ رفێن ، گرنگی شوێنه‌وار ناسی و سروشتی دەوروبەر."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zawa+Mountain+Duhok+Iraq",
        },
    },

    "korak": {
        "en": {
            "name": "⛰️ Korek Mountain",
            "text": (
                "⛰️ Korek Mountain\n\n"
                "Korek Mountain is a major mountain destination "
                "in Erbil Governorate.\n\n"
                "📍 Famous for: Korek Resort, cable car, "
                "and spectacular mountain scenery."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Korek+Mountain+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی کۆڕەک",
            "text": (
                "⛰️ شاخی کۆڕەک\n\n"
                "شاخی کۆڕەک یەکێکە لە ناوچە شاخاوییە گرنگەکانی "
                "پارێزگای هەولێر.\n\n"
                "📍 بەناوبانگە بە: رێزۆرتی کۆڕەک، تەلەفەریک "
                "و دیمەنی شاخستانی سەرسوڕهێنەر."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Korek+Mountain+Iraq",
        },
    },

    "gara": {
        "en": {
            "name": "⛰️ Gara Mountain",
            "text": (
                "⛰️ Gara Mountain\n\n"
                "Gara Mountain is a prominent mountain range "
                "in Duhok Governorate.\n\n"
                "📍 Famous for: rugged landscapes, valleys, "
                "and diverse natural scenery."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gara+Mountain+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی گارە",
            "text": (
                "⛰️ شاخی گارە\n\n"
                "شاخی گارە یەکێکە لە زنجیرە شاخە دیارەکانی "
                "پارێزگای دهۆک.\n\n"
                "📍 بەناوبانگە بە: دیمەنی بەردەوامی شاخستانی، "
                "دۆڵەکان و سروشتی جۆراوجۆر."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gara+Mountain+Iraq",
        },
    },

    "halgurd": {
        "en": {
            "name": "⛰️ Halgurd Mountain",
            "text": (
                "⛰️ Halgurd Mountain\n\n"
                "Halgurd is one of the highest mountains in Iraq "
                "and is located in the Erbil Governorate.\n\n"
                "📍 Famous for: high-altitude landscapes, "
                "snow in winter, and dramatic valleys."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halgurd+Mountain+Iraq",
        },
        "ku": {
            "name": "⛰️ شاخی هەڵگورد",
            "text": (
                "⛰️ شاخی هەڵگورد\n\n"
                "هەڵگورد یەکێکە لە بەرزترین شاخەکانی عێراق "
                "و لە پارێزگای هەولێرە.\n\n"
                "📍 بەناوبانگە بە: دیمەنی بەرزی شاخستانی، "
                "بەفر لە زستان و دۆڵە قووڵەکان."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halgurd+Mountain+Iraq",
        },
    },
}
CITIES = {
    "erbil": {
        "en": {
            "name": "🏙️ Erbil",
            "text": (
                "🏙️ Erbil\n\n"
                "Erbil is the capital of the Kurdistan Region of Iraq "
                "and one of the world's oldest continuously inhabited cities.\n\n"
                "📍 Famous for: Erbil Citadel, Sami Abdulrahman Park, "
                "and its historic bazaar."
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
                "عه‌بدولرەحمان و بازاڕە کۆنەکەی."
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
                "سلێمانی یەکێکە لە شارە گرنگەكان له‌ بواری کلتووری و فێربوون "
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
                " بە شاخەکان دەورەدراوە.\n\n"
                "📍 بەناوبانگە بە: بەنداوی دهۆک، شاخی زاوا "
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
                "Halabja is a city in the Kurdistan Region near "
                "the Iranian border and the Hawraman mountains.\n\n"
                "📍 Known for its history, culture, and surrounding "
                "mountain landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halabja+Iraq",
        },
        "ku": {
            "name": "🏙️ هەڵەبجە",
            "text": (
                "🏙️ هەڵەبجە\n\n"
                "هەڵەبجە شارێکە لە هەرێمی کوردستان، "
                "نزیکه‌ له‌ سنووری ئێران و شاخەکانی هەورامان.\n\n"
                "📍 بە مێژوو و کەلتوور و دیمەنی شاخاویی دەوروبەرەکەی ناسراوە."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Halabja+Iraq",
        },
    },

    "akre": {
        "en": {
            "name": "🏙️ Akre",
            "text": (
                "🏙️ Akre\n\n"
                "Akre is a historic mountain city in Duhok Governorate.\n\n"
                "📍 Famous for its old houses, mountains, "
                "and traditional Newroz celebrations."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Akre+Iraq",
        },
        "ku": {
            "name": "🏙️ ئاکرێ",
            "text": (
                "🏙️ ئاکرێ\n\n"
                "ئاکرێ شارێکی مێژوویی شاخاوییە لە پارێزگای دهۆک.\n\n"
                "📍 بەناوبانگە بە خانووە کۆنەکان، شاخەکان "
                "و ڕێوڕه‌سمی جەژنی نەورۆز."
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
                "دۆڵە قووڵەکان دەورەدراوە.\n\n"
                "📍 بەناوبانگە بە کانی ڕەواندز و خه‌ره‌ند و ئاوی بێخاڵ."
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
                "📍 Famous for: Safeen Mountain and green landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shaqlawa+Iraq",
        },
        "ku": {
            "name": "🏙️ شەقڵاوە",
            "text": (
                "🏙️ شەقڵاوە\n\n"
                "شەقڵاوە شارۆچکەیەکی شاخاوییە لە پارێزگای هەولێر.\n\n"
                "📍 بەناوبانگە بە شاخی سەفین و ناوچه‌ی گه‌شتیاری هیران و به‌نداوی ئاقوبان و دیمەنی سەوز."
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
                "and regional trade."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zakho+Iraq",
        },
        "ku": {
            "name": "🏙️ زاخۆ",
            "text": (
                "🏙️ زاخۆ\n\n"
                "زاخۆ شارێکە لە پارێزگای دهۆک و نزیک سنووری "
                "عێراق و تورکیایە.\n\n"
                "📍 بەناوبانگە بە پردی ده‌لال، ڕووباری خابوور "
                "و شوێنی گرنگی بازرگانی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zakho+Iraq",
        },
    },
}


def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏔️ کوردی", callback_data="lang_ku"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
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

def mountains_keyboard(lang):
    mountains = {
        "en": [
            ("Mount Safeen", "safine"),
            ("Azmar Mountain", "azmar"),
            ("Zawa Mountain", "zawa"),
            ("Korek Mountain", "korak"),
            ("Gara Mountain", "gara"),
            ("Halgurd Mountain", "halgurd"),
        ],
        "ku": [
            ("شاخی سەفین", "safine"),
            ("شاخی ئەزمەر", "azmar"),
            ("شاخی زاوا", "zawa"),
            ("شاخی کۆڕەک", "korak"),
            ("شاخی گارە", "gara"),
            ("شاخی هەڵگورد", "halgurd"),
        ],
    }

    buttons = []

    for name, mountain_id in mountains[lang]:
        buttons.append([
            InlineKeyboardButton(
                name,
                callback_data=f"mountain_{mountain_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            TEXT[lang]["back"],
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(buttons)
def cities_keyboard(lang):
    cities = {
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

    for name, city_id in cities[lang]:
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
    lang = context.user_data.get("language", "en")

    if data.startswith("lang_"):
        new_lang = data.replace("lang_", "")
        context.user_data["language"] = new_lang

        await query.edit_message_text(
            TEXT[new_lang]["welcome"],
            reply_markup=main_keyboard(new_lang),
        )
        return
        
    if data == "mountains":
        await query.edit_message_text(
            "⛰️ Choose a mountain:" if lang == "en" else "⛰️ شاخێک هەڵبژێرە:",
            reply_markup=mountains_keyboard(lang),
        )
        return

    if data.startswith("mountain_"):
        mountain_id = data.replace("mountain_", "")
        mountain = MOUNTAINS[mountain_id][lang]

        await query.edit_message_text(
            mountain["text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📍 Google Maps",
                        url=mountain["map"]
                    )
                ],
                [
                    InlineKeyboardButton(
                        TEXT[lang]["back"],
                        callback_data="mountains"
                    )
                ],
            ]),
        )
        return
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

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Kurdistan Geography Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
