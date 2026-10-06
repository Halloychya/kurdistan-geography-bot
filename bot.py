import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
app = Flask(__name__)


@app.route("/")
def home():
    return "Kurdistan Geography Bot is running!"


def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


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
RIVERS = {
    "tigris": {
        "en": {
            "name": "🌊 Tigris (Dîcle)",
            "text": (
                "🌊 Tigris River (Dîcle)\n\n"
                "The Tigris is one of the great rivers of Mesopotamia "
                "and one of the most important rivers of Iraq.\n\n"
                "📍 Known for: ancient civilizations, agriculture, "
                "water resources, and major cities along its course."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Tigris+River+Iraq",
        },
        "ku": {
            "name": "🌊 دیجلە (Dîcle)",
            "text": (
                "🌊 ڕووباری دیجلە\n\n"
                "دیجلە یەکێکە لە ڕووبارە گەورەکانی مەیسۆپۆتامیا "
                "و یەکێکە لە گرنگترین ڕووبارەکانی عێراق.\n\n"
                "📍 بەناوبانگە بە: شارستانییە کۆنەکان، کشتوکاڵ، "
                "سەرچاوەکانی ئاو و شارە گرنگەکان."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Tigris+River+Iraq",
        },
    },

    "euphrates": {
        "en": {
            "name": "🌊 Euphrates (Firat)",
            "text": (
                "🌊 Euphrates River (Firat)\n\n"
                "The Euphrates is one of the two great rivers "
                "of ancient Mesopotamia.\n\n"
                "📍 Known for: ancient civilizations, agriculture, "
                "and its importance to the history of the region."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Euphrates+River+Iraq",
        },
        "ku": {
            "name": "🌊 فورات (Firat)",
            "text": (
                "🌊 ڕووباری فورات\n\n"
                "فورات یەکێکە لە دوو ڕووبارە گەورەکانی "
                "مەیسۆپۆتامیا و گرنگییەکی مێژوویی زۆری هەیە.\n\n"
                "📍 بەناوبانگە بە: شارستانییە کۆنەکان، "
                "کشتوکاڵ و مێژووی ناوچەکە."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Euphrates+River+Iraq",
        },
    },

    "great_zab": {
        "en": {
            "name": "🌊 Great Zab (Zêyê Mezin)",
            "text": (
                "🌊 Great Zab River\n\n"
                "The Great Zab is one of the major tributaries "
                "of the Tigris River.\n\n"
                "📍 Known for: mountain valleys, water resources, "
                "and beautiful landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Great+Zab+River+Iraq",
        },
        "ku": {
            "name": "🌊 زێی گەورە (Zêyê Mezin)",
            "text": (
                "🌊 ڕووباری زێی گەورە\n\n"
                "زێی گەورە یەکێکە لە لقە گرنگەکانی "
                "ڕووباری دیجلە.\n\n"
                "📍 بەناوبانگە بە: دۆڵە شاخاوییەکان، "
                "سەرچاوەکانی ئاو و دیمەنی سروشتی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Great+Zab+River+Iraq",
        },
    },

    "little_zab": {
        "en": {
            "name": "🌊 Little Zab (Zêyê Biçûk)",
            "text": (
                "🌊 Little Zab River\n\n"
                "The Little Zab is an important tributary "
                "of the Tigris River.\n\n"
                "📍 Known for: fertile valleys, agriculture, "
                "and water resources."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Little+Zab+River+Iraq",
        },
        "ku": {
            "name": "🌊 زێی بچووک (Zêyê Biçûk)",
            "text": (
                "🌊 ڕووباری زێی بچووک\n\n"
                "زێی بچووک یەکێکە لە لقە گرنگەکانی "
                "ڕووباری دیجلە.\n\n"
                "📍 بەناوبانگە بە: دۆڵە بەرهەمدارەکان، "
                "کشتوکاڵ و سەرچاوەکانی ئاو."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Little+Zab+River+Iraq",
        },
    },

    "sirwan": {
        "en": {
            "name": "🌊 Sirwan (Diyala)",
            "text": (
                "🌊 Sirwan River\n\n"
                "The Sirwan River, also known as the Darbandixan River "
                "in Kurdistan, is an important river of the region.\n\n"
                "📍 Known for: mountain valleys, reservoirs, "
                "and natural scenery."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sirwan+River+Iraq",
        },
        "ku": {
            "name": "🌊 سیروان (Diyala)",
            "text": (
                "🌊 ڕووباری سیروان\n\n"
                "سیروان، کە لە كوردستان بە ناوی ده‌ربه‌ندیخان ناسراوە، "
                "ڕووبارێکی گرنگی ناوچەکەیە.\n\n"
                "📍 بەناوبانگە بە: دۆڵە شاخاوییەکان، "
                "بەنداوەکان و دیمەنی سروشتی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sirwan+River+Iraq",
        },
    },

    "khabur": {
        "en": {
            "name": "🌊 Khabur (Little Khabur)",
            "text": (
                "🌊 Khabur River\n\n"
                "The Little Khabur is a river associated with "
                "the northern Mesopotamian river system.\n\n"
                "📍 Known for: valleys, water resources, "
                "and its connection to the regional river network."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Little+Khabur+River+Iraq",
        },
        "ku": {
            "name": "🌊 خابور (Khabur)",
            "text": (
                "🌊 ڕووباری خابور\n\n"
                "خابور ڕووبارێکە لە سیستەمی ڕووبارەکانی "
                "باکووری مەیسۆپۆتامیا.\n\n"
                "📍 بەناوبانگە بە: دۆڵەکان، سەرچاوەکانی ئاو "
                "و پەیوەندی بە تۆڕی ڕووبارەکانی ناوچەکە."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Little+Khabur+River+Iraq",
        },
    },

    "adhaim": {
        "en": {
            "name": "🌊 Adhaim (Awaspee)",
            "text": (
                "🌊 Adhaim River\n\n"
                "The Adhaim is an important tributary "
                "of the Tigris River.\n\n"
                "📍 Known for: its role in the water system "
                "of northern and central Iraq."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Adhaim+River+Iraq",
        },
        "ku": {
            "name": "🌊 ئاوه‌سپی (Awaspee)",
            "text": (
                "🌊 ڕووباری ئاوه‌سپی\n\n"
                "عەدهایم یەکێکە لە لقە گرنگەکانی "
                "ڕووباری دیجلە.\n\n"
                "📍 گرنگە بۆ سیستەمی ئاوی باکوور و ناوەڕاستی عێراق."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Adhaim+River+Iraq",
        },
    },

    "khazir": {
        "en": {
            "name": "🌊 Khazir River",
            "text": (
                "🌊 Khazir River\n\n"
                "The Khazir is an important river in the "
                "Erbil–Nineveh region.\n\n"
                "📍 Known for: fertile areas, water resources, "
                "and its connection to the Great Zab system."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Khazir+River+Iraq",
        },
        "ku": {
            "name": "🌊 ڕووباری خازر",
            "text": (
                "🌊 ڕووباری خازر\n\n"
                "خازر ڕووبارێکی گرنگە لە ناوچەی "
                "هەولێر و نینەوا.\n\n"
                "📍 بەناوبانگە بە: ناوچە بەرهەمدارەکان، "
                "سەرچاوەکانی ئاو و پەیوەنده‌ بە سیستەمی زێی گەورە."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Khazir+River+Iraq",
        },
    },

    "tanjero": {
        "en": {
            "name": "🌊 Tanjero River",
            "text": (
                "🌊 Tanjero River\n\n"
                "Tanjero is an important river around Sulaymaniyah "
                "and is part of the regional river system.\n\n"
                "📍 Known for: the valleys and landscapes around Sulaymaniyah."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Tanjero+River+Iraq",
        },
        "ku": {
            "name": "🌊 ڕووباری تانجەڕۆ",
            "text": (
                "🌊 ڕووباری تانجەڕۆ\n\n"
                "تانجەڕۆ ڕووبارێکی گرنگە لە دەوروبەری سلێمانی "
                "و بەشێکە لە سیستەمی ئاوی ناوچەکە.\n\n"
                "📍 بەناوبانگە بە: دۆڵ و دیمەنی سروشتی دەوروبەری سلێمانی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Tanjero+River+Iraq",
        },
    },

    "rwandz": {
        "en": {
            "name": "🌊 Rwandz River",
            "text": (
                "🌊 Rwandz River\n\n"
                "The Rwandz River flows through the mountainous "
                "Rawanduz area of Erbil Governorate.\n\n"
                "📍 Known for: dramatic mountain valleys and "
                "the natural scenery of Rawanduz."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+River+Iraq",
        },
        "ku": {
            "name": "🌊 ڕووباری ڕەواندز",
            "text": (
                "🌊 ڕووباری ڕەواندز\n\n"
                "ڕووباری ڕەواندز لە ناوچە شاخاوییەکانی "
                "ڕەواندز لە پارێزگای هەولێرە.\n\n"
                "📍 بەناوبانگە بە: دۆڵە شاخاوییە سەرسوڕهێنەرەکان "
                "و دیمەنی سروشتی ڕەواندز."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+River+Iraq",
        },
    },

    "gali_ali_bag": {
        "en": {
            "name": "💧 Gali Ali Beg",
            "text": (
                "💧 Gali Ali Beg Waterfall\n\n"
                "Gali Ali Beg is one of the famous waterfalls "
                "in the Kurdistan Region, near Korek and Rawanduz.\n\n"
                "📍 Known for: waterfalls, mountain scenery, "
                "and tourism."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gali+Ali+Bag+Waterfall+Iraq",
        },
        "ku": {
            "name": "💧 گەلی عەلی بەگ",
            "text": (
                "💧 ئاویشارەکەی گەلی عەلی بەگ\n\n"
                "گەلی عەلی بەگ یەکێکە لە ئاویشارە بەناوبانگەکانی "
                "هەرێمی کوردستان، لە نزیکی کۆڕەک و ڕەواندز.\n\n"
                "📍 بەناوبانگە بە: ئاویشار، دیمەنی شاخستانی "
                "و گەشتوگوزار."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gali+Ali+Bag+Waterfall+Iraq",
        },
    },

    "shamdinan": {
        "en": {
            "name": "🌊 Shamdinan River",
            "text": (
                "🌊 Shamdinan River\n\n"
                "The Shamdinan River is associated with the "
                "mountainous areas of northern Kurdistan.\n\n"
                "📍 Known for: mountain landscapes and valleys."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shamdinan+River",
        },
        "ku": {
            "name": "🌊 ڕووباری شەمزینان",
            "text": (
                "🌊 ڕووباری شەمزینان\n\n"
                "ڕووباری شەمزینان پەیوەندی بە ناوچە شاخاوییەکانی "
                "باکووری کوردستانەوە هەیە.\n\n"
                "📍 بەناوبانگە بە: دیمەنی شاخستانی و دۆڵەکان."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shamdinan+River",
        },
    },

    "murat": {
        "en": {
            "name": "🌊 Murat River",
            "text": (
                "🌊 Murat River\n\n"
                "The Murat is one of the important headwaters "
                "of the Euphrates system in eastern Turkey.\n\n"
                "📍 Known for: mountain landscapes and its role "
                "in the Euphrates river system."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Murat+River+Turkey",
        },
        "ku": {
            "name": "🌊 ڕووباری مورات",
            "text": (
                "🌊 ڕووباری مورات\n\n"
                "مورات یەکێکە لە سەرچاوە گرنگەکانی "
                "سیستەمی ڕووباری فورات لە ڕۆژهەڵاتی تورکیا.\n\n"
                "📍 بەناوبانگە بە: دیمەنی شاخستانی و ڕۆڵی لە سیستەمی فورات."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Murat+River+Turkey",
        },
    },

    "karasu": {
        "en": {
            "name": "🌊 Karasu River",
            "text": (
                "🌊 Karasu River\n\n"
                "Karasu is an important headwater stream "
                "of the Euphrates system.\n\n"
                "📍 Known for: mountainous landscapes and "
                "its connection to the Euphrates."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Karasu+River+Turkey",
        },
        "ku": {
            "name": "🌊 ڕووباری کاراسو",
            "text": (
                "🌊 ڕووباری کاراسو\n\n"
                "کاراسو یەکێکە لە سەرچاوە گرنگەکانی "
                "سیستەمی ڕووباری فوراتە.\n\n"
                "📍 بەناوبانگە بە: دیمەنی شاخستانی و پەیوەندی بە فورات."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Karasu+River+Turkey",
        },
    },

    "botan": {
        "en": {
            "name": "🌊 Botan (Buhtân)",
            "text": (
                "🌊 Botan River\n\n"
                "The Botan River is an important river in "
                "the mountainous region of southeastern Turkey.\n\n"
                "📍 Known for: deep valleys, mountains, "
                "and dramatic landscapes."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Botan+River+Turkey",
        },
        "ku": {
            "name": "🌊 بۆتان (Buhtân)",
            "text": (
                "🌊 ڕووباری بۆتان\n\n"
                "بۆتان ڕووبارێکی گرنگە لە ناوچە شاخاوییەکانی "
                "باشووری ڕۆژهەڵاتی تورکیا.\n\n"
                "📍 بەناوبانگە بە: دۆڵە قووڵەکان، شاخەکان "
                "و دیمەنی سەرسوڕهێنەر."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Botan+River+Turkey",
        },
    },

    "aras": {
        "en": {
            "name": "🌊 Aras River",
            "text": (
                "🌊 Aras River\n\n"
                "The Aras is a major river of the Caucasus "
                "and forms parts of international borders.\n\n"
                "📍 Known for: its long historical and "
                "geographical importance in the region."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Aras+River",
        },
        "ku": {
            "name": "🌊 ڕووباری ئاراس",
            "text": (
                "🌊 ڕووباری ئاراس\n\n"
                "ئاراس یەکێکە لە ڕووبارە گرنگەکانی ناوچەی "
                "قەفقاز و بەشێک لە سنوورە نێودەوڵەتییەکان پێکدەهێنێت.\n\n"
                "📍 بەناوبانگە بە: گرنگییە مێژوویی و جوگرافییەکەی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Aras+River",
        },
    },

    "zarrinarud": {
        "en": {
            "name": "🌊 Zarrinarud (Jaghatu)",
            "text": (
                "🌊 Zarrinarud River (Jaghatu)\n\n"
                "Zarrinarud is an important river in northwestern Iran "
                "and is connected to the Lake Urmia basin.\n\n"
                "📍 Known for: agriculture and water resources."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zarrinarud+River+Iran",
        },
        "ku": {
            "name": "🌊 زەڕینەڕوود (Jaghatu)",
            "text": (
                "🌊 ڕووباری زەڕینەڕوود\n\n"
                "زەڕینەڕوود ڕووبارێکی گرنگە لە باکووری ڕۆژئاوای "
                "ئێران و پەیوەندی بە حەوزەی دەریاچەی ورمێ هەیە.\n\n"
                "📍 بەناوبانگە بە: کشتوکاڵ و سەرچاوەکانی ئاو."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zarrinarud+River+Iran",
        },
    },

    "siminarud": {
        "en": {
            "name": "🌊 Siminarud (Tâtâ’u)",
            "text": (
                "🌊 Siminarud River\n\n"
                "Siminarud is a river in northwestern Iran "
                "associated with the Lake Urmia basin.\n\n"
                "📍 Known for: valleys, agriculture, and water resources."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Siminarud+River+Iran",
        },
        "ku": {
            "name": "🌊 سیمینەڕوود (Tâtâ’u)",
            "text": (
                "🌊 ڕووباری سیمینەڕوود\n\n"
                "سیمینەڕوود ڕووبارێکە لە باکووری ڕۆژئاوای "
                "ئێران و پەیوەندی بە حەوزەی دەریاچەی ورمێ هەیە.\n\n"
                "📍 بەناوبانگە بە: دۆڵەکان، کشتوکاڵ و سەرچاوەکانی ئاو."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Siminarud+River+Iran",
        },
    },

    "ghezel_ozan": {
        "en": {
            "name": "🌊 Ghezel Ozan River",
            "text": (
                "🌊 Ghezel Ozan River\n\n"
                "Ghezel Ozan is a major river in northwestern Iran "
                "and one of the important rivers of the region.\n\n"
                "📍 Known for: large valleys, agriculture, "
                "and water resources."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Ghezel+Ozan+River+Iran",
        },
        "ku": {
            "name": "🌊 ڕووباری غەزەل ئۆزەن",
            "text": (
                "🌊 ڕووباری غەزەل ئۆزەن\n\n"
                "غەزەل ئۆزەن ڕووبارێکی گەورەی باکووری ڕۆژئاوای "
                "ئێرانە و لە ڕووبارە گرنگەکانی ناوچەکەیە.\n\n"
                "📍 بەناوبانگە بە: دۆڵە گەورەکان، کشتوکاڵ "
                "و سەرچاوەکانی ئاو."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Ghezel+Ozan+River+Iran",
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
def rivers_keyboard(lang):
    rivers = {
        "en": [
            ("🌊 Tigris (Dîcle)", "tigris"),
            ("🌊 Euphrates (Firat)", "euphrates"),
            ("🌊 Great Zab (Zêyê Mezin)", "great_zab"),
            ("🌊 Little Zab (Zêyê Biçûk)", "little_zab"),
            ("🌊 Sirwan (Diyala)", "sirwan"),
            ("🌊 Khabur", "khabur"),
            ("🌊 Adhaim (Awaspee)", "adhaim"),
            ("🌊 Khazir", "khazir"),
            ("🌊 Tanjero", "tanjero"),
            ("🌊 Rwandz", "rwandz"),
            ("💧 Gali Ali Beg", "gali_ali_bag"),
            ("🌊 Shamdinan", "shamdinan"),
            ("🌊 Murat", "murat"),
            ("🌊 Karasu", "karasu"),
            ("🌊 Botan (Buhtân)", "botan"),
            ("🌊 Aras", "aras"),
            ("🌊 Zarrinarud (Jaghatu)", "zarrinarud"),
            ("🌊 Siminarud (Tâtâ’u)", "siminarud"),
            ("🌊 Ghezel Ozan", "ghezel_ozan"),
        ],
        "ku": [
            ("🌊 دیجلە (Dîcle)", "tigris"),
            ("🌊 فورات (Firat)", "euphrates"),
            ("🌊 زێی گەورە", "great_zab"),
            ("🌊 زێی بچووک", "little_zab"),
            ("🌊 سیروان (Darbandixan)", "sirwan"),
            ("🌊 خابور", "khabur"),
            ("🌊 ئاوه‌سپی", "Awaspi"),
            ("🌊 خازر", "khazir"),
            ("🌊 تانجەڕۆ", "tanjero"),
            ("🌊 ڕووباری ڕەواندز", "rwandz"),
            ("💧 گەلی عەلی بەگ", "gali_ali_bag"),
            ("🌊 شەمزینان", "shamdinan"),
            ("🌊 مورات", "murat"),
            ("🌊 کاراسو", "karasu"),
            ("🌊 بۆتان", "botan"),
            ("🌊 ئاراس", "aras"),
            ("🌊 زەڕینەڕوود", "zarrinarud"),
            ("🌊 سیمینەڕوود", "siminarud"),
            ("🌊 غەزەل ئۆزەن", "ghezel_ozan"),
        ],
    }

    buttons = []

    for name, river_id in rivers[lang]:
        buttons.append([
            InlineKeyboardButton(
                name,
                callback_data=f"river_{river_id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            TEXT[lang]["back"],
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(buttons)
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
            if data == "rivers":
        await query.edit_message_text(
            "🌊 Choose a river or water place:"
            if lang == "en"
            else "🌊 ڕووبار یان شوێنی ئاوی هەڵبژێرە:",
            reply_markup=rivers_keyboard(lang),
        )
        return

    if data.startswith("river_"):
        river_id = data.replace("river_", "")
        river = RIVERS[river_id][lang]

        await query.edit_message_text(
            river["text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "📍 Google Maps",
                        url=river["map"]
                    )
                ],
                [
                    InlineKeyboardButton(
                        TEXT[lang]["back"],
                        callback_data="rivers"
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
    threading.Thread(target=run_web_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Kurdistan Geography Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
