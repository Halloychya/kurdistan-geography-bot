import os
from telegram.error import BadRequest
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
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
        "search": "🔎 Search for a Place",
        "language": "🌐 Language",
        "choose_city": "🏙️ Choose a city:",
        "back": "🔙 Back",
    },
    "ku": {
        "welcome": "🌍 بەخێربێیت بۆ جوگرافیای کوردستان!",
        "choose": "تکایە زمانەکەت هەڵبژێرە:",
        "cities": "🏙️ شارەکان",
        "mountains": "⛰️ چیاکان",
        "rivers": "🌊 ڕووبار و دەریاچەکان",
        "nature": "🏞️ شوێنە سروشتییەکان",
        "locations": "📍 شوێنەکان",
        "facts": "📚 زانیاری جوگرافی",
        "search": "🔎 گەڕان بۆ شوێنێک",
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
            "name": "⛰️ چیای سەفین",
            "text": (
                "⛰️ شاخی سەفین\n\n"
                "چیای سەفین یەکێکە لە شاخە ناسراوەکانی "
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
            "name": "⛰️ چیای ئەزمەر",
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
            "name": "⛰️ چیای زاوا",
            "text": (
                "⛰️ شاخی زاوا\n\n"
                "چیای زاوا لە نزیکی دهۆکە و یەکێکە لە "
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
            "name": "⛰️ چیای کۆڕەک",
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
            "name": "⛰️ چیای گارە",
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
            "name": "⛰️ چیای هەڵگورد",
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

# Coordinates used by the Nearby Places Finder
NEARBY_PLACES = [
    {
        "name_en": "Erbil",
        "name_ku": "هەولێر",
        "lat": 36.1911,
        "lon": 44.0092,
        "map": "https://www.google.com/maps/search/?api=1&query=Erbil+Iraq",
    },
    {
        "name_en": "Sulaymaniyah",
        "name_ku": "سلێمانی",
        "lat": 35.5613,
        "lon": 45.4309,
        "map": "https://www.google.com/maps/search/?api=1&query=Sulaymaniyah+Iraq",
    },
]

LOCATIONS = {

    "erbil_citadel": {
        "category": "🏛️ Ancient & History",
        "en": {
            "name": "🏰 Erbil Citadel",
            "text": (
                "🏰 ERBIL CITADEL\n\n"
                "📍 Destination: Erbil Citadel\n"
                "🏛️ Type: Ancient heritage site\n"
                "🚗 From Erbil center: 0 km\n"
                "⏱️ Drive: 0 min\n"
                "🕐 Visit: about 2 hours\n"
                "📅 Best months: March–May, October–November\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Any car\n"
                "💰 Entrance: Main grounds are free\n\n"
                "📖 HISTORY\n"
                "The Erbil Citadel is a huge archaeological mound in "
                "the center of Erbil. It has been occupied for thousands "
                "of years and became a UNESCO World Heritage Site in 2014.\n\n"
                "🤯 DID YOU KNOW?\n"
                "The citadel stands directly above the modern city center "
                "and contains archaeological layers from different periods.\n\n"
                "🎒 BRING\n"
                "• Comfortable shoes\n"
                "• Water\n"
                "• Phone/camera\n"
                "• Sun protection\n"
                "• Some cash for nearby places\n\n"
                "⭐ WHY VISIT?\n"
                "History + architecture + city views + Qaysari Bazaar."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Erbil+Citadel"
        },
        "ku": {
            "name": "🏰 کۆشکی هەولێر",
            "text": (
                "🏰 کۆشکی هەولێر\n\n"
                "📍 شوێن: کۆشکی هەولێر\n"
                "🏛️ جۆر: شوێنی مێژوویی\n"
                "🚗 لە ناوەندی هەولێر: ٠ کیلۆمەتر\n"
                "⏱️ گەشت: ٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٢ کاتژمێر\n"
                "📅 باشترین وەرز: بەهار و پاییز\n"
                "🥾 ئاست: 🟢 ئاسان\n"
                "🚙 ئۆتۆمبێل: هەر ئۆتۆمبێلێک\n\n"
                "📖 مێژوو\n"
                "کۆشکی هەولێر کۆمەڵێک چینە مێژووییە لەسەر گردێکی "
                "گەورە لە ناوەندی هەولێر. شوێنەکە هەزاران ساڵە "
                "شوێنی ژیان و نیشتەجێبوون بووە.\n\n"
                "🤯 دەزانی؟\n"
                "کۆشکەکە لە دڵی شاری نوێی هەولێرە و لەسەر گردێکی "
                "مێژوویی دانراوە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی ئاسوودە\n"
                "• ئاو\n"
                "• مۆبایل/کامێرا\n"
                "• پارێزەری خۆر\n\n"
                "⭐ بۆچی سەردانی بکەیت؟\n"
                "مێژوو + تەلارسازی + دیمەنی شار + بازاڕی قەیسەری."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Erbil+Citadel"
        }
    },

    "qaysari_bazaar": {
        "category": "🏛️ Ancient & History",
        "en": {
            "name": "🛍️ Qaysari Bazaar",
            "text": (
                "🛍️ QAYSARI BAZAAR\n\n"
                "📍 Destination: Qaysari Bazaar\n"
                "🏛️ Type: Historic covered market\n"
                "🚗 From Erbil center: 0 km\n"
                "🕐 Visit: about 1–2 hours\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Any car; walking is better\n\n"
                "📖 HISTORY\n"
                "Qaysari Bazaar is a traditional covered market "
                "located beside Erbil Citadel.\n\n"
                "🤯 DID YOU KNOW?\n"
                "The market dates back to the early 13th century.\n\n"
                "🎒 BRING\n"
                "• Comfortable shoes\n"
                "• Small cash\n"
                "• Phone/camera\n\n"
                "⭐ BEST COMBINATION\n"
                "Erbil Citadel → Qaysari Bazaar → Mudhafaria Minaret."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Qaysari+Bazaar+Erbil"
        },
        "ku": {
            "name": "🛍️ بازاڕی قەیسەری",
            "text": (
                "🛍️ بازاڕی قەیسەری\n\n"
                "📍 شوێن: بازاڕی قەیسەری\n"
                "🏛️ جۆر: بازاڕی مێژوویی\n"
                "🚗 لە ناوەندی هەولێر: ٠ کیلۆمەتر\n"
                "🕐 ماوەی سەردان: ١–٢ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "📖 مێژوو\n"
                "بازاڕی قەیسەری بازاڕێکی نەریتی و مێژووییە "
                "لە تەنیشت کۆشکی هەولێر.\n\n"
                "🤯 دەزانی؟\n"
                "بنەمای بازاڕەکە بۆ سەدەی ١٣ دەگەڕێتەوە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی ئاسوودە\n"
                "• پارەی کاش\n"
                "• مۆبایل/کامێرا\n\n"
                "⭐ پێشنیاری گەشت\n"
                "کۆشکی هەولێر → بازاڕی قەیسەری → منارەی مظەفەری."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Qaysari+Bazaar+Erbil"
        }
    },

    "mudhafaria": {
        "category": "🏛️ Ancient & History",
        "en": {
            "name": "🕌 Mudhafaria Minaret",
            "text": (
                "🕌 MUDHAFARIA MINARET\n\n"
                "📍 Destination: Mudhafaria Minaret\n"
                "🏛️ Type: Historic minaret\n"
                "🚗 From Erbil center: about 10 min\n"
                "🕐 Visit: about 30 minutes\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🤯 DID YOU KNOW?\n"
                "The minaret is approximately 36 metres tall "
                "and dates from the 13th century.\n\n"
                "🎒 BRING\n"
                "• Comfortable shoes\n"
                "• Phone/camera\n"
                "• Water in hot weather\n\n"
                "⭐ GOOD FOR\n"
                "History, architecture and photography."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Mudhafaria+Minaret+Erbil"
        },
        "ku": {
            "name": "🕌 منارەی مظەفەری",
            "text": (
                "🕌 منارەی مظەفەری\n\n"
                "📍 شوێن: منارەی مظەفەری\n"
                "🏛️ جۆر: منارەی مێژوویی\n"
                "🚗 لە ناوەندی هەولێر: نزیکەی ١٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٣٠ خولەک\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🤯 دەزانی؟\n"
                "بەرزی منارەکە نزیکەی ٣٦ مەترە و مێژووەکەی "
                "دەگەڕێتەوە بۆ سەدەی ١٣.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی ئاسوودە\n"
                "• مۆبایل/کامێرا\n"
                "• ئاو لە هاوین\n\n"
                "⭐ باشە بۆ\n"
                "مێژوو، تەلارسازی و وێنەگرتن."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Mudhafaria+Minaret+Erbil"
        }
    },

    "sami_abdulrahman": {
        "category": "🌳 Nature & Parks",
        "en": {
            "name": "🌳 Sami Abdulrahman Park",
            "text": (
                "🌳 SAMI ABDULRAHMAN PARK\n\n"
                "📍 Destination: Sami Abdulrahman Park\n"
                "🚗 From Erbil center: about 15 min\n"
                "🕐 Visit: 2–3 hours\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Any car\n\n"
                "🌿 WHAT YOU'LL FIND\n"
                "• Large green spaces\n"
                "• Two lakes\n"
                "• Walking areas\n"
                "• Relaxation areas\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Comfortable shoes\n"
                "• Sun protection\n"
                "• Picnic items if desired\n\n"
                "⭐ BEST FOR\n"
                "Families, walking, relaxing and sunset."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sami+Abdulrahman+Park+Erbil"
        },
        "ku": {
            "name": "🌳 پارکی سامی عەبدولڕەحمان",
            "text": (
                "🌳 پارکی سامی عەبدولڕەحمان\n\n"
                "📍 شوێن: پارکی سامی عەبدولڕەحمان\n"
                "🚗 لە ناوەندی هەولێر: نزیکەی ١٥ خولەک\n"
                "🕐 ماوەی سەردان: ٢–٣ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🌿 لەوێ چی هەیە؟\n"
                "• بۆشایی سەوز\n"
                "• دوو دەریاچە\n"
                "• شوێنی پیاسە\n"
                "• شوێنی پشوودان\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• پارێزەری خۆر\n\n"
                "⭐ باشە بۆ\n"
                "خێزان، پیاسە، پشوودان و خۆرئاوابوون."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sami+Abdulrahman+Park+Erbil"
        }
    },

    "shanidar_park": {
        "category": "🌳 Nature & Parks",
        "en": {
            "name": "🌳 Shanidar Park",
            "text": (
                "🌳 SHANIDAR PARK\n\n"
                "📍 Destination: Shanidar Park, Erbil\n"
                "🚗 From Erbil center: about 10 min\n"
                "🕐 Visit: 1–2 hours\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Comfortable shoes\n"
                "• Camera\n\n"
                "⭐ GOOD FOR\n"
                "Relaxing, walking and family activities."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shanidar+Park+Erbil"
        },
        "ku": {
            "name": "🌳 پارکی شانەدەر",
            "text": (
                "🌳 پارکی شانەدەر\n\n"
                "📍 شوێن: پارکی شانەدەر، هەولێر\n"
                "🚗 لە ناوەندی هەولێر: نزیکەی ١٠ خولەک\n"
                "🕐 ماوەی سەردان: ١–٢ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• کامێرا\n\n"
                "⭐ باشە بۆ\n"
                "پشوودان، پیاسە و چاالکی خێزانی."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shanidar+Park+Erbil"
        }
    },

    "shaqlawa": {
        "category": "🏘️ Towns & Culture",
        "en": {
            "name": "🏘️ Shaqlawa",
            "text": (
                "🏘️ SHAQLAWA\n\n"
                "📍 Destination: Shaqlawa\n"
                "🏔️ Elevation: about 1,066 m\n"
                "🚗 From Erbil: about 50 km\n"
                "⏱️ Drive: about 60 min\n"
                "🕐 Visit: about 3 hours\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🌿 WHY GO?\n"
                "A famous mountain resort below Safeen Mountain, "
                "known for its cooler climate, valleys and mountain scenery.\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Comfortable shoes\n"
                "• Light jacket for cooler weather\n"
                "• Camera\n\n"
                "⭐ BEST FOR\n"
                "A relaxed day trip from Erbil."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shaqlawa+Iraq"
        },
        "ku": {
            "name": "🏘️ شەقڵاوە",
            "text": (
                "🏘️ شەقڵاوە\n\n"
                "📍 شوێن: شەقڵاوە\n"
                "🏔️ بەرزی: نزیکەی ١٠٦٦ مەتر\n"
                "🚗 لە هەولێرەوە: نزیکەی ٥٠ کیلۆمەتر\n"
                "⏱️ گەشت: نزیکەی ٦٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٣ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🌿 بۆچی بچیت؟\n"
                "شەقڵاوە شوێنێکی گەشتیاریی شاخاوییە لە ژێر "
                "شاخی سەفین، بە کەشوهەوای خۆش و دیمەنی شاخەکان.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• جلوبەرگی سووک\n"
                "• کامێرا"
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Shaqlawa+Iraq"
        }
    },

    "rawanduz": {
        "category": "🏔️ Mountains & Canyons",
        "en": {
            "name": "🏞️ Rawanduz",
            "text": (
                "🏞️ RAWANDUZ\n\n"
                "📍 Destination: Rawanduz\n"
                "🚗 From Erbil: about 116 km\n"
                "⏱️ Drive: about 105 min\n"
                "🕐 Visit: about 2 hours\n"
                "📅 Best months: April–October\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "📖 HISTORY\n"
                "Rawanduz sits on a rocky ridge between deep river gorges "
                "and was the capital of the Soran Emirate from 1816 to 1836.\n\n"
                "🤯 DID YOU KNOW?\n"
                "The town is surrounded by dramatic mountain peaks "
                "and is a natural gateway toward Gali Ali Beg and Hamilton Road.\n\n"
                "🎒 BRING\n"
                "• Drinking water\n"
                "• Comfortable shoes\n"
                "• Camera\n"
                "• Power bank\n"
                "• Offline map\n\n"
                "⚠️ NOTE\n"
                "Mountain weather can change quickly. Check road conditions "
                "before travelling in winter."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+Iraq"
        },
        "ku": {
            "name": "🏞️ ڕەواندز",
            "text": (
                "🏞️ ڕەواندز\n\n"
                "📍 شوێن: ڕەواندز\n"
                "🚗 لە هەولێرەوە: نزیکەی ١١٦ کیلۆمەتر\n"
                "⏱️ گەشت: نزیکەی ١٠٥ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٢ کاتژمێر\n"
                "📅 باشترین وەرز: نیسان تا تشرینی یەکەم\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "📖 مێژوو\n"
                "ڕەواندز لەسەر پشتی بەردینێک لەنێوان دوو کانیۆنی "
                "قووڵ دانراوە و لە ساڵانی ١٨١٦ تا ١٨٣٦ پایتەختی "
                "میرنشینی سۆران بووە.\n\n"
                "🤯 دەزانی؟\n"
                "شاخە گەورەکان لە هەموو لایەکەوە دەوری شارەکەیان داوە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• کامێرا\n"
                "• پاوەربانک\n"
                "• نەخشەی ئۆفلاین\n\n"
                "⚠️ تێبینی\n"
                "کەشوهەوای شاخاویی دەتوانێت بەخێرایی بگۆڕێت."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Rawanduz+Iraq"
        }
    },

    "gali_ali_beg": {
        "category": "💦 Waterfalls & Nature",
        "en": {
            "name": "💦 Gali Ali Beg Waterfall",
            "text": (
                "💦 GALI ALI BEG WATERFALL\n\n"
                "📍 Destination: Gali Ali Beg Waterfall\n"
                "🚗 From Erbil: about 130 km\n"
                "⏱️ Drive: about 150 min\n"
                "🕐 Visit: about 1 hour\n"
                "🥾 Difficulty: 🟢 Easy–Moderate\n"
                "🚙 Vehicle: Normal car on the main route\n\n"
                "🏞️ LOCATION\n"
                "The waterfall is in Rawanduz Gorge along the historic "
                "Hamilton Road.\n\n"
                "💧 WATERFALL\n"
                "The main waterfall is about 12 metres high.\n\n"
                "🎒 BRING\n"
                "• Drinking water\n"
                "• Walking shoes\n"
                "• Extra clothes if you go near the water\n"
                "• Sun protection\n"
                "• Camera\n\n"
                "⭐ BEST COMBINATION\n"
                "Rawanduz → Hamilton Road → Gali Ali Beg."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gali+Ali+Beg+Waterfall"
        },
        "ku": {
            "name": "💦 ئاوی گەلی عەلی بەگ",
            "text": (
                "💦 ئاوی گەلی عەلی بەگ\n\n"
                "📍 شوێن: ئاوی گەلی عەلی بەگ\n"
                "🚗 لە هەولێرەوە: نزیکەی ١٣٠ کیلۆمەتر\n"
                "⏱️ گەشت: نزیکەی ١٥٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ١ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان–مامناوەند\n"
                "🚙 ئۆتۆمبێل: ئۆتۆمبێلی ئاسایی بۆ ڕێگای سەرەکی\n\n"
                "🏞️ شوێن\n"
                "لە کانیۆنی ڕەواندز و لەسەر ڕێگای مێژوویی هامیلتۆنە.\n\n"
                "💧 ئاوشار\n"
                "بەرزی ئاوشارە سەرەکییەکە نزیکەی ١٢ مەترە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی گەشت\n"
                "• جلوبەرگی زیادە ئەگەر نزیک ئاو دەچیت\n"
                "• پارێزەری خۆر\n"
                "• کامێرا\n\n"
                "⭐ گەشتی پێشنیارکراو\n"
                "ڕەواندز → ڕێگای هامیلتۆن → گەلی عەلی بەگ."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gali+Ali+Beg+Waterfall"
        }
    },

    "amadiya": {
        "category": "🏛️ Ancient & History",
        "en": {
            "name": "🏘️ Amedi (Amadiya)",
            "text": (
                "🏘️ AMEDI\n\n"
                "📍 Destination: Amedi\n"
                "🏔️ Elevation: about 1,400 m\n"
                "🚗 From Duhok: about 90 min\n"
                "🕐 Visit: about 3 hours\n"
                "📅 Best months: April–June, September–October\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Normal car\n"
                "💰 Admission: Free\n\n"
                "📖 HISTORY\n"
                "Amedi is an ancient hilltop settlement built on a "
                "flat-topped limestone plateau.\n\n"
                "🤯 SEE\n"
                "• Historic Ottoman gate\n"
                "• Old mosque minaret\n"
                "• Mountain panoramas\n"
                "• Ancient rock inscriptions\n\n"
                "🎒 BRING\n"
                "• Walking shoes\n"
                "• Water\n"
                "• Camera\n"
                "• Light jacket\n"
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Amedi+Iraq"
        },
        "ku": {
            "name": "🏘️ ئەمێدی",
            "text": (
                "🏘️ ئەمێدی\n\n"
                "📍 شوێن: ئەمێدی\n"
                "🏔️ بەرزی: نزیکەی ١٤٠٠ مەتر\n"
                "🚗 لە دهۆکەوە: نزیکەی ٩٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٣ کاتژمێر\n"
                "📅 باشترین وەرز: نیسان–حوزەیران و ئەیلول–تشرینی یەکەم\n"
                "🥾 ئاست: 🟢 ئاسان\n"
                "🚙 ئۆتۆمبێل: ئاسایی\n"
                "💰 چوونەژوورەوە: بەلاش\n\n"
                "📖 مێژوو\n"
                "ئەمێدی شارێکی کۆنی سەر تەختە بەردینێکی بەرزە.\n\n"
                "🤯 چی ببینیت؟\n"
                "• دەروازەی مێژوویی\n"
                "• منارەی مزگەوتی کۆن\n"
                "• دیمەنی شاخەکان\n"
                "• نوسینە بەردینە کۆنەکان\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی گەشت\n"
                "• ئاو\n"
                "• کامێرا\n"
                "• جلوبەرگی سووک"
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Amedi+Iraq"
        }
    },

    "sulav": {
        "category": "💦 Waterfalls & Nature",
        "en": {
            "name": "💦 Sulav Springs",
            "text": (
                "💦 SULAV SPRINGS\n\n"
                "📍 Destination: Sulav Springs Resort\n"
                "🚗 From Duhok: about 90 min\n"
                "🕐 Visit: about 3 hours\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Normal car\n\n"
                "🌿 WHAT YOU GET\n"
                "Cold mountain springs, green surroundings, "
                "pine-shaded areas and a relaxing mountain atmosphere.\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Comfortable shoes\n"
                "• Camera\n"
                "• Light jacket\n\n"
                "⭐ BEST FOR\n"
                "Summer trips and relaxing with family."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sulav+Springs+Resort+Iraq"
        },
        "ku": {
            "name": "💦 سولاڤ",
            "text": (
                "💦 سولاڤ\n\n"
                "📍 شوێن: سولاڤ\n"
                "🚗 لە دهۆکەوە: نزیکەی ٩٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٣ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n"
                "🚙 ئۆتۆمبێل: ئاسایی\n\n"
                "🌿 چی هەیە؟\n"
                "سەرچاوەی ساردی شاخاویی، دارستان و دیمەنی سروشتی جوان.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• کامێرا\n"
                "• جلوبەرگی سووک\n\n"
                "⭐ باشە بۆ\n"
                "گەشتی هاوین و پشوودان لەگەڵ خێزان."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Sulav+Springs+Resort+Iraq"
        }
    },

    "gara": {
        "category": "🏔️ Mountains & Canyons",
        "en": {
            "name": "🏔️ Gara Mountain",
            "text": (
                "🏔️ GARA MOUNTAIN\n\n"
                "📍 Destination: Gara Mountain\n"
                "🚗 From Duhok: about 105 min\n"
                "🕐 Suggested visit: about 5 hours\n"
                "🥾 Difficulty: 🟠 Difficult\n"
                "🚙 Vehicle: Check road conditions before remote trips\n\n"
                "🌲 WHAT TO EXPECT\n"
                "A remote highland massif with oak forests, "
                "seasonal waterfalls and mountain trails.\n\n"
                "🎒 BRING\n"
                "• Plenty of water\n"
                "• Food/snacks\n"
                "• Proper hiking shoes\n"
                "• First-aid kit\n"
                "• Power bank\n"
                "• Offline map\n"
                "• Extra layer\n\n"
                "🧭 GUIDE\n"
                "For remote hiking routes, a knowledgeable local guide "
                "is strongly recommended.\n\n"
                "⚠️ IMPORTANT\n"
                "Do not treat unknown spring water as automatically safe."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gara+Mountain+Iraq"
        },
        "ku": {
            "name": "🏔️ شاخی گەرا",
            "text": (
                "🏔️ شاخی گەرا\n\n"
                "📍 شوێن: شاخی گەرا\n"
                "🚗 لە دهۆکەوە: نزیکەی ١٠٥ خولەک\n"
                "🕐 ماوەی پێشنیارکراو: نزیکەی ٥ کاتژمێر\n"
                "🥾 ئاست: 🟠 سەخت\n"
                "🚙 ئۆتۆمبێل: پێش گەشت دۆخی ڕێگا بپشکنە\n\n"
                "🌲 چی دەبینیت؟\n"
                "شاخێکی دوورەدەست بە دارستانی بلوط، "
                "ئاوشاری وەرزی و ڕێگای شاخاویی.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاوێکی زۆر\n"
                "• خواردن\n"
                "• پێڵاوی گەشت\n"
                "• کۆمەکی یەکەم\n"
                "• پاوەربانک\n"
                "• نەخشەی ئۆفلاین\n"
                "• جلوبەرگی زیادە\n\n"
                "🧭 ڕێبەر\n"
                "بۆ ڕێگاکانی دوور، ڕێبەری ناوخۆی شارەزا پێشنیار دەکرێت."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Gara+Mountain+Iraq"
        }
    },

    "zawa": {
        "category": "🏔️ Mountains & Viewpoints",
        "en": {
            "name": "🏔️ Zawa Mountain Viewpoint",
            "text": (
                "🏔️ ZAWA MOUNTAIN\n\n"
                "📍 Destination: Zawa Mountain viewpoint\n"
                "🚗 From Duhok: about 18 min\n"
                "🕐 Visit: about 1.5 hours\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Normal car\n\n"
                "🌆 HIGHLIGHT\n"
                "A mountain ridge overlooking Duhok and the reservoir.\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Camera\n"
                "• Light jacket\n\n"
                "⭐ BEST TIME\n"
                "Late afternoon for mountain and city views."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zawa+Mountain+Duhok"
        },
        "ku": {
            "name": "🏔️ شاخی زاوا",
            "text": (
                "🏔️ شاخی زاوا\n\n"
                "📍 شوێن: خاڵی دیمەنی شاخی زاوا\n"
                "🚗 لە دهۆکەوە: نزیکەی ١٨ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ١.٥ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n"
                "🚙 ئۆتۆمبێل: ئاسایی\n\n"
                "🌆 تایبەتمەندی\n"
                "دیمەنێکی فراوانی شاری دهۆک و دەریاچەکە دەدات.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• کامێرا\n"
                "• جلوبەرگی سووک\n\n"
                "⭐ باشترین کات\n"
                "دوای نیوەڕۆ بۆ دیمەنی شار و شاخ."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Zawa+Mountain+Duhok"
        }
    },

    "duhok_dam": {
        "category": "🌊 Lakes & Water",
        "en": {
            "name": "🌊 Duhok Dam & Reservoir",
            "text": (
                "🌊 DUHOK DAM\n\n"
                "📍 Destination: Duhok Dam & Reservoir\n"
                "🚗 From Duhok center: about 12 min\n"
                "🕐 Visit: about 1.5 hours\n"
                "🥾 Difficulty: 🟢 Easy\n"
                "🚙 Vehicle: Normal car\n\n"
                "🌿 WHAT TO SEE\n"
                "A mountain reservoir surrounded by hills and pine-covered slopes.\n\n"
                "🎒 BRING\n"
                "• Water\n"
                "• Comfortable shoes\n"
                "• Camera\n\n"
                "⭐ BEST FOR\n"
                "Evening walks and mountain scenery."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Dam"
        },
        "ku": {
            "name": "🌊 بەندی ئاوی دهۆک",
            "text": (
                "🌊 بەندی ئاوی دهۆک\n\n"
                "📍 شوێن: بەندی ئاوی دهۆک\n"
                "🚗 لە ناوەندی دهۆکەوە: نزیکەی ١٢ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ١.٥ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n"
                "🚙 ئۆتۆمبێل: ئاسایی\n\n"
                "🌿 چی دەبینیت؟\n"
                "دەریاچەیەکی شاخاویی کە بە دۆڵ و شاخەکان دەورەدراوە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• ئاو\n"
                "• پێڵاوی ئاسوودە\n"
                "• کامێرا\n\n"
                "⭐ باشە بۆ\n"
                "پیاسەی ئێوارە و دیمەنی شاخ."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Dam"
        }
    },

    "duhok_bazaar": {
        "category": "🏘️ Towns & Culture",
        "en": {
            "name": "🛍️ Duhok Old Bazaar",
            "text": (
                "🛍️ DUHOK OLD BAZAAR\n\n"
                "📍 Destination: Duhok Old Bazaar\n"
                "🚗 From Duhok center: 0 min\n"
                "🕐 Visit: about 2 hours\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🌿 EXPERIENCE\n"
                "Explore traditional covered trading lanes, "
                "local shops, spices, fabrics and traditional food.\n\n"
                "🎒 BRING\n"
                "• Comfortable shoes\n"
                "• Small cash\n"
                "• Phone/camera\n\n"
                "⭐ BEST FOR\n"
                "Local culture, food and photography."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Old+Bazaar"
        },
        "ku": {
            "name": "🛍️ بازاڕی کۆنی دهۆک",
            "text": (
                "🛍️ بازاڕی کۆنی دهۆک\n\n"
                "📍 شوێن: بازاڕی کۆنی دهۆک\n"
                "🚗 لە ناوەندی دهۆکەوە: ٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٢ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🌿 ئەزموون\n"
                "لە کۆڵانەکانی بازاڕی کۆن بگەڕێ، "
                "دوکانە ناوخۆییەکان و خواردنی نەریتی ببینە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی ئاسوودە\n"
                "• پارەی کاش\n"
                "• مۆبایل/کامێرا\n\n"
                "⭐ باشە بۆ\n"
                "کەلتوور، خواردن و وێنەگرتن."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Duhok+Old+Bazaar"
        }
    },

    "delal_bridge": {
        "category": "🏛️ Ancient & History",
        "en": {
            "name": "🌉 Delal Bridge – Zakho",
            "text": (
                "🌉 DELAL BRIDGE\n\n"
                "📍 Destination: Delal Bridge, Zakho\n"
                "🚗 From Duhok: about 55 min\n"
                "🕐 Visit: about 1 hour\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🏛️ HISTORY\n"
                "A historic stone arch bridge crossing the Little Khabur River.\n\n"
                "🎒 BRING\n"
                "• Comfortable shoes\n"
                "• Water\n"
                "• Camera\n\n"
                "⭐ BEST FOR\n"
                "History, architecture and photography."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Delal+Bridge+Zakho"
        },
        "ku": {
            "name": "🌉 پردی دلال – زاخۆ",
            "text": (
                "🌉 پردی دلال\n\n"
                "📍 شوێن: پردی دلال، زاخۆ\n"
                "🚗 لە دهۆکەوە: نزیکەی ٥٥ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ١ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🏛️ مێژوو\n"
                "پردێکی بەردینی مێژووییە کە بەسەر ڕووباری خابووری بچووکدا تێدەپەڕێت.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی ئاسوودە\n"
                "• ئاو\n"
                "• کامێرا\n\n"
                "⭐ باشە بۆ\n"
                "مێژوو، تەلارسازی و وێنەگرتن."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Delal+Bridge+Zakho"
        }
    },

    "akre": {
        "category": "🏘️ Towns & Culture",
        "en": {
            "name": "🏘️ Akre Old Town",
            "text": (
                "🏘️ AKRE\n\n"
                "📍 Destination: Akre\n"
                "🚗 From Duhok: about 90 min\n"
                "🕐 Visit: about 3 hours\n"
                "🥾 Difficulty: 🟡 Moderate\n\n"
                "🏛️ WHY IT'S SPECIAL\n"
                "An ancient mountain town built along a dramatic rocky valley, "
                "with traditional houses and historic character.\n\n"
                "🎒 BRING\n"
                "• Walking shoes\n"
                "• Water\n"
                "• Camera\n"
                "• Sun protection\n\n"
                "⭐ BEST FOR\n"
                "Historic streets, mountain views and photography."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Akre+Iraq"
        },
        "ku": {
            "name": "🏘️ ئاکرێ",
            "text": (
                "🏘️ ئاکرێ\n\n"
                "📍 شوێن: ئاکرێ\n"
                "🚗 لە دهۆکەوە: نزیکەی ٩٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٣ کاتژمێر\n"
                "🥾 ئاست: 🟡 مامناوەند\n\n"
                "🏛️ بۆچی تایبەتە؟\n"
                "شارۆچکەیەکی کۆنی شاخاوییە کە بەسەر دۆڵێکی "
                "بەردین و دیمەنی شاخەکاندا دروست بووە.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• پێڵاوی گەشت\n"
                "• ئاو\n"
                "• کامێرا\n"
                "• پارێزەری خۆر\n\n"
                "⭐ باشە بۆ\n"
                "کۆڵانە کۆنەکان، دیمەنی شاخ و وێنەگرتن."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Akre+Iraq"
        }
    },

    "lalish": {
        "category": "🕍 Cultural & Sacred",
        "en": {
            "name": "🕍 Lalish",
            "text": (
                "🕍 LALISH\n\n"
                "📍 Destination: Lalish\n"
                "🚗 From Duhok: about 60 min\n"
                "🕐 Visit: about 2 hours\n"
                "🥾 Difficulty: 🟢 Easy\n\n"
                "🌿 ABOUT\n"
                "Lalish is a sacred valley and an important religious "
                "and cultural site of the Yazidi community.\n\n"
                "🎒 BRING\n"
                "• Modest and respectful clothing\n"
                "• Comfortable shoes\n"
                "• Water\n\n"
                "⚠️ RESPECT\n"
                "Follow local customs and instructions when visiting "
                "religious areas.\n\n"
                "⭐ BEST FOR\n"
                "Culture, architecture, history and photography."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Lalish+Iraq"
        },
        "ku": {
            "name": "🕍 لالش",
            "text": (
                "🕍 لالش\n\n"
                "📍 شوێن: لالش\n"
                "🚗 لە دهۆکەوە: نزیکەی ٦٠ خولەک\n"
                "🕐 ماوەی سەردان: نزیکەی ٢ کاتژمێر\n"
                "🥾 ئاست: 🟢 ئاسان\n\n"
                "🌿 دەربارەی شوێنەکە\n"
                "لالش دۆڵێکی پیرۆز و شوێنێکی گرنگی ئایینی و "
                "کەلتوورییە بۆ کۆمەڵگەی ئێزیدی.\n\n"
                "🎒 پێویستە بهێنیت\n"
                "• جلوبەرگی گونجاو و ڕێزدار\n"
                "• پێڵاوی ئاسوودە\n"
                "• ئاو\n\n"
                "⚠️ ڕێز\n"
                "لە کاتی سەرداندا ڕێزی نەریت و ڕێنماییە ناوخۆییەکان بگرە.\n\n"
                "⭐ باشە بۆ\n"
                "کەلتوور، تەلارسازی، مێژوو و وێنەگرتن."
            ),
            "map": "https://www.google.com/maps/search/?api=1&query=Lalish+Iraq"
        }
    }
}

FACTS = {
    "mountain_belt": {
        "en": {
            "title": "🏔️ The Taurus–Zagros Mountain Belt",
            "text": (
                "The mountains of Kurdistan form part of the huge "
                "Taurus–Zagros mountain system. This mountain belt was "
                "created by the collision of the Arabian and Eurasian "
                "tectonic plates."
            ),
        },
        "ku": {
            "title": "🏔️ زنجیرە شاخەکانی تاورۆس–زاگرۆس",
            "text": (
                "شاخەکانی کوردستان بەشێکن لە سیستەمی گەورەی "
                "شاخەکانی تاورۆس–زاگرۆس. ئەم شاخانە بەهۆی "
                "پێکدادانی پلێتەکانی عەرەبی و ئەورو-ئاسیایی دروست بوون."
            ),
        },
    },

    "water_source": {
        "en": {
            "title": "💧 Kurdistan: A Water Source for Mesopotamia",
            "text": (
                "Snow and rainfall in the Kurdistan highlands feed major "
                "rivers such as the Tigris, Great Zab and Little Zab, "
                "providing water for the plains of Mesopotamia."
            ),
        },
        "ku": {
            "title": "💧 کوردستان: سەرچاوەی ئاوه‌ بۆ میسۆپۆتامیا",
            "text": (
                "بەفر و بارانەکانی ناوچە شاخاوییەکانی کوردستان "
                "سەرچاوەی ئاوی ڕووبارە گەورەکانن وەک دیجلە، زێی گەورە "
                "و زێی بچووک، کە ئاو بۆ دشتەکانی میسۆپۆتامیا دابین دەکەن."
            ),
        },
    },

    "elevation": {
        "en": {
            "title": "🏞️ Huge Changes in Elevation",
            "text": (
                "Kurdistan contains both low plains and mountains rising "
                "thousands of metres. This creates major differences in "
                "climate, vegetation and agriculture within relatively "
                "short distances."
            ),
        },
        "ku": {
            "title": "🏞️ جیاوازی زۆری بەرزی",
            "text": (
               " کوردستان پێكهاتووه‌ له‌ ده‌شتە نزمەکان و شاخە بەرزەکانی "
                "هەزاران مەتر لەخۆدەگرێت. ئەمەش جیاوازی گەورە لە "
                "کەشوهەوا، ڕووەک و کشتوکاڵ دروست دەکات."
            ),
        },
    },

    "ancient_glaciers": {
        "en": {
            "title": "🧊 Ancient Glaciers",
            "text": (
                "During past ice ages, glaciers affected some of the "
                "highest mountains of Kurdistan. Ancient ice helped shape "
                "some of the valleys and mountain landscapes we see today."
            ),
        },
        "ku": {
            "title": "🧊 بەستەڵەکی کۆن",
            "text": (
                "لە سەردەمە ساردەکانی ڕابردوودا، بەستەڵەک کاریگەری "
                "لەسەر هەندێک لە شاخە بەرزەکانی کوردستان هەبووە. "
                "ئەو بەستەڵەکە کۆنانە بەشێک لە دۆڵ و دیمەنی شاخەکانی "
                "ئەمڕۆیان دروست کردووە."
            ),
        },
    },

    "lake_van": {
        "en": {
            "title": "🌊 Lake Van Is an Alkaline Lake",
            "text": (
                "Lake Van is one of the world's largest alkaline lakes. "
                "Its water contains a high concentration of carbonate "
                "and is very different from ordinary freshwater lakes."
            ),
        },
        "ku": {
            "title": "🌊 دەریاچەی وان ئاوی كبریتی هەیە",
            "text": (
                "دەریاچەی وان یەکێکە لە گەورەترین دەریاچە كبریتیه‌كانی "
                "جیهان. ئاوی ئەم دەریاچەیە ڕێژەیەکی بەرزی کاربۆناتی "
                "هەیە و لە ئاوی دەریاچە ئاساییە شیرینەکان جیاوازە."
            ),
        },
    },

    "volcanoes": {
        "en": {
            "title": "🌋 Volcanic Mountains",
            "text": (
                "The wider Kurdish highlands around Lake Van contain "
                "important volcanic landscapes, including Mount Süphan "
                "and Mount Nemrut."
            ),
        },
        "ku": {
            "title": "🌋 شاخە ئاگرکانییەکان",
            "text": (
                "ناوچە شاخاوییەکانی دەوری دەریاچەی وان دیمەنی "
                "گركانی گرنگی تێدایە، لەوانە شاخی سوفان و شاخی نەمرود."
            ),
        },
    },

    "halgurd_rocks": {
        "en": {
            "title": "🪨 Strange Rocks on Halgurd",
            "text": (
                "Geological studies around Halgurd have identified unusual "
                "rocks, including pillow basalts. These rocks help scientists "
                "understand the complicated geological history of the Zagros."
            ),
        },
        "ku": {
            "title": "🪨 بەردە سەیرەکانی هەڵگورد",
            "text": (
                "توێژینەوە جیۆلۆجییەکان لە دەوری هەڵگورد بەردی "
                "نامۆیان دۆزیوەتەوە، لەوانە pillow basalt. ئەم بەردانە "
                "یارمەتی زاناکان دەدەن بۆ تێگەیشتن لە مێژووی جیۆلۆجی "
                "ئاڵۆزی زاگرۆس."
            ),
        },
    },

    "zagros_length": {
        "en": {
            "title": "🏔️ The Zagros Is Enormous",
            "text": (
                "The Zagros mountain system stretches for roughly "
                "1,500–1,600 kilometres, forming one of the great mountain "
                "belts of the Middle East."
            ),
        },
        "ku": {
            "title": "🏔️ زاگرۆس زۆر گەورەیە",
            "text": (
                "سیستەمی شاخەکانی زاگرۆس نزیکەی ١٥٠٠–١٦٠٠ کیلۆمەتر "
                "درێژ دەبێتەوە و یەکێکە لە گەورەترین زنجیرە شاخەکانی "
                "ڕۆژهەڵاتی ناوەڕاست."
            ),
        },
    },

    "ancient_ocean": {
        "en": {
            "title": "🌊 Rocks That Remember an Ancient Ocean",
            "text": (
                "Some rocks in the Zagros are connected to ancient oceanic "
                "environments that existed millions of years ago. Their "
                "presence gives geologists clues about the ancient oceans "
                "that disappeared as the Arabian and Eurasian plates collided."
            ),
        },
        "ku": {
            "title": "🌊 بەردی بیرەوەری و دەریای کۆن",
            "text": (
                "هەندێک بەرد لە زاگرۆس پەیوەندییان بە ژینگە "
                "دەریاییە کۆنەکانەوە هەیە کە ملیۆنان ساڵ لەمەوبەر "
                "بوونیان هەبووە. ئەم بەردانە نیشانەیەکن بۆ زاناکان "
                "بۆ ناسینەوەی دەریایی کۆن کە لە کاتی پێکدادانی "
                "پلێتە عەرەبی و ئەورو-ئاسیاییەکاندا لەناوچوون."
            ),
        },
    },

    "early_farming": {
        "en": {
            "title": "🌾 One of the Birthplaces of Farming",
            "text": (
                "The Zagros and surrounding Fertile Crescent contain "
                "archaeological evidence of very early plant cultivation "
                "and animal domestication. The region played an important "
                "role in humanity's transition toward farming communities."
            ),
        },
        "ku": {
            "title": "🌾 یەکێک لە شوێنە سەرەتاییەکانی کشتوکاڵ",
            "text": (
                "لە زاگرۆس و ناوچەکانی دەوری هەلالی پڕبەرەکەت، "
                "بەڵگەی شوێنەواری بۆ چاندنی ڕووەک و ماڵیکردنی ئاژەڵ "
                "لە سەردەمە زۆر کۆنەکاندا دۆزراوەتەوە. ئەم ناوچەیە "
                "ڕۆڵێکی گرنگی هەبووە لە گواستنەوەی مرۆڤ بۆ ژیانی "
                "کشتوکاڵی."
            ),
        },
    },
}
# =========================
# GEOGRAPHY QUIZ
# =========================

QUIZ_QUESTIONS = [
    {
        "en": {
            "question": "Which city is the capital of the Kurdistan Region of Iraq?",
            "options": ["Erbil", "Duhok", "Halabja", "Zakho"],
            "answer": "Erbil",
        },
        "ku": {
            "question": "پایتەختی هەرێمی کوردستانی عێراق کام شارە؟",
            "options": ["هەولێر", "دهۆک", "هەڵەبجە", "زاخۆ"],
            "answer": "هەولێر",
        },
    },
    {
        "en": {
            "question": "Which major river is one of the main tributaries of the Tigris in Kurdistan?",
            "options": ["Great Zab", "Nile", "Jordan", "Euphrates"],
            "answer": "Great Zab",
        },
        "ku": {
            "question": "کام ڕووبارێک یەکێکە لە ڕووبارە سەرەکییەکانی پەیوەندیدار بە دیجلە لە کوردستان؟",
            "options": ["زێی گەورە", "نیل", "ئوردن", "فورات"],
            "answer": "زێی گەورە",
        },
    },
    {
        "en": {
            "question": "Which mountain is one of the highest peaks in Iraq?",
            "options": ["Halgurd", "Zawa", "Azmar", "Gara"],
            "answer": "Halgurd",
        },
        "ku": {
            "question": "کام شاخێک یەکێکە لە بەرزترین لووتکەکانی عێراق؟",
            "options": ["هەڵگورد", "زاوا", "ئەزمەر", "گارە"],
            "answer": "هەڵگورد",
        },
    },
    {
        "en": {
            "question": "Where is the historic Erbil Citadel located?",
            "options": ["Erbil", "Duhok", "Zakho", "Akre"],
            "answer": "Erbil",
        },
        "ku": {
            "question": "قەڵای مێژوویی هەولێر لە کوێیە؟",
            "options": ["هەولێر", "دهۆک", "زاخۆ", "ئاکرێ"],
            "answer": "هەولێر",
        },
    },
    {
        "en": {
            "question": "Which city is the capital of Duhok Governorate?",
            "options": ["Duhok", "Akre", "Zakho", "Shaqlawa"],
            "answer": "Duhok",
        },
        "ku": {
            "question": "کام شار پایتەختی پارێزگای دهۆکە؟",
            "options": ["دهۆک", "ئاکرێ", "زاخۆ", "شەقڵاوە"],
            "answer": "دهۆک",
        },
    },
    {
        "en": {
            "question": "Which mountain is located near Sulaymaniyah?",
            "options": ["Azmar", "Halgurd", "Gara", "Korek"],
            "answer": "Azmar",
        },
        "ku": {
            "question": "کام شاخ لە نزیکی سلێمانییە؟",
            "options": ["ئەزمەر", "هەڵگورد", "گارە", "کۆڕەک"],
            "answer": "ئەزمەر",
        },
    },
    {
        "en": {
            "question": "Which famous waterfall is near Rawanduz?",
            "options": ["Gali Ali Beg", "Bekhal", "Sulav", "Akre Falls"],
            "answer": "Gali Ali Beg",
        },
        "ku": {
            "question": "کام ئاوشارە بەناوبانگە لە نزیکی ڕەواندزە؟",
            "options": ["گەلی عەلی بەگ", "بێخاڵ", "سولاڤ", "ئاوشاری ئاکرێ"],
            "answer": "گەلی عەلی بەگ",
        },
    },
    {
        "en": {
            "question": "Which city is famous for Delal Bridge?",
            "options": ["Zakho", "Erbil", "Halabja", "Duhok"],
            "answer": "Zakho",
        },
        "ku": {
            "question": "کام شار بە پردی دلال بەناوبانگە؟",
            "options": ["زاخۆ", "هەولێر", "هەڵەبجە", "دهۆک"],
            "answer": "زاخۆ",
        },
    },
    {
        "en": {
            "question": "Lalish is an important religious and cultural site of which community?",
            "options": ["Yazidi", "Assyrian", "Armenian", "Turkmen"],
            "answer": "Yazidi",
        },
        "ku": {
            "question": "لالش شوێنێکی گرنگی ئایینی و کەلتووریی کام کۆمەڵگەیە؟",
            "options": ["ئێزیدی", "ئاشووری", "ئەرمەنی", "تورکمانی"],
            "answer": "ئێزیدی",
        },
    },
    {
        "en": {
            "question": "Which river is also known as the Diyala?",
            "options": ["Sirwan", "Khabur", "Tanjero", "Great Zab"],
            "answer": "Sirwan",
        },
        "ku": {
            "question": "کام ڕووبار بە ناوی دیالەش ناسراوە؟",
            "options": ["سیروان", "خابور", "تانجەڕۆ", "زێی گەورە"],
            "answer": "سیروان",
        },
    },
    {
        "en": {
            "question": "Which city is located in the east of the Kurdistan Region and is famous for its history?",
            "options": ["Halabja", "Zakho", "Duhok", "Akre"],
            "answer": "Halabja",
        },
        "ku": {
            "question": "کام شار لە ڕۆژهەڵاتی هەرێمی کوردستانە و بە مێژووی خۆی بەناوبانگە؟",
            "options": ["هەڵەبجە", "زاخۆ", "دهۆک", "ئاکرێ"],
            "answer": "هەڵەبجە",
        },
    },
    {
        "en": {
            "question": "Which large reservoir is located near Sulaymaniyah?",
            "options": ["Dukan Lake", "Duhok Dam", "Van Lake", "Urmia Lake"],
            "answer": "Dukan Lake",
        },
        "ku": {
            "question": "کام دەریاچەی دەستکردی گەورە لە نزیکی سلێمانییە؟",
            "options": ["دەریاچەی دوکان", "بەندی ئاوی دهۆک", "دەریاچەی وان", "دەریاچەی ورمێ"],
            "answer": "دەریاچەی دوکان",
        },
    },
    {
        "en": {
            "question": "Which mountain is famous near Shaqlawa?",
            "options": ["Safeen", "Azmar", "Halgurd", "Gara"],
            "answer": "Safeen",
        },
        "ku": {
            "question": "کام شاخ لە نزیکی شەقڵاوە بەناوبانگە؟",
            "options": ["سەفین", "ئەزمەر", "هەڵگورد", "گارە"],
            "answer": "سەفین",
        },
    },
    {
        "en": {
            "question": "Which city is famous for its old mountain-town character?",
            "options": ["Akre", "Erbil", "Halabja", "Duhok"],
            "answer": "Akre",
        },
        "ku": {
            "question": "کام شار بە کۆڵان و کەسایەتی شارە شاخاوییە کۆنەکەی بەناوبانگە؟",
            "options": ["ئاکرێ", "هەولێر", "هەڵەبجە", "دهۆک"],
            "answer": "ئاکرێ",
        },
    },
    {
        "en": {
            "question": "Which river flows through the Duhok area?",
            "options": ["Khabur", "Nile", "Jordan", "Euphrates"],
            "answer": "Khabur",
        },
        "ku": {
            "question": "کام ڕووبار بە ناوچەی دهۆکدا تێدەپەڕێت؟",
            "options": ["خابور", "نیل", "ئوردن", "فورات"],
            "answer": "خابور",
        },
    },
    {
        "en": {
            "question": "Which mountain is associated with Rawanduz?",
            "options": ["Korek", "Azmar", "Zawa", "Safeen"],
            "answer": "Korek",
        },
        "ku": {
            "question": "کام شاخ پەیوەندی بە ڕەواندزەوە هەیە؟",
            "options": ["کۆڕەک", "ئەزمەر", "زاوا", "سەفین"],
            "answer": "کۆڕەک",
        },
    },
    {
        "en": {
            "question": "What type of landscape dominates much of Kurdistan?",
            "options": ["Mountains and valleys", "Desert only", "Flat coastline", "Tropical rainforest"],
            "answer": "Mountains and valleys",
        },
        "ku": {
            "question": "کام جۆری دیمەن لە زۆربەی کوردستاندا زاڵە؟",
            "options": ["شاخ و دۆڵ", "تەنها بیابان", "کەناری تەخت", "دارستانی گەرمسیری"],
            "answer": "شاخ و دۆڵ",
        },
    },
    {
        "en": {
            "question": "Which major river is known as the Tigris in English?",
            "options": ["Dicle", "Firat", "Sirwan", "Khabur"],
            "answer": "Dicle",
        },
        "ku": {
            "question": "کام ڕووبار بە ناوی دیجلە ناسراوە؟",
            "options": ["دیجلە", "فورات", "سیروان", "خابور"],
            "answer": "دیجلە",
        },
    },
    {
        "en": {
            "question": "Which mountain is near Duhok city?",
            "options": ["Zawa", "Azmar", "Halgurd", "Süphan"],
            "answer": "Zawa",
        },
        "ku": {
            "question": "کام شاخ لە نزیکی شاری دهۆکە؟",
            "options": ["زاوا", "ئەزمەر", "هەڵگورد", "سوفان"],
            "answer": "زاوا",
        },
    },
    {
        "en": {
            "question": "Which city is known as an important historic city in northern Kurdistan?",
            "options": ["Akre", "Halabja", "Erbil", "Sulaymaniyah"],
            "answer": "Akre",
        },
        "ku": {
            "question": "کام شار بە شارێکی مێژوویی گرنگ لە باکووری کوردستان ناسراوە؟",
            "options": ["ئاکرێ", "هەڵەبجە", "هەولێر", "سلێمانی"],
            "answer": "ئاکرێ",
        },
    },
    {
        "en": {
            "question": "Which river is called the Little Zab?",
            "options": ["Little Zab", "Great Zab", "Sirwan", "Tanjero"],
            "answer": "Little Zab",
        },
        "ku": {
            "question": "کام ڕووبار بە زێی بچووک ناسراوە؟",
            "options": ["زێی بچووک", "زێی گەورە", "سیروان", "تانجەڕۆ"],
            "answer": "زێی بچووک",
        },
    },
    {
        "en": {
            "question": "Which lake is famous in the Sulaymaniyah region?",
            "options": ["Dukan Lake", "Lake Van", "Lake Urmia", "Lake Tuz"],
            "answer": "Dukan Lake",
        },
        "ku": {
            "question": "کام دەریاچە لە ناوچەی سلێمانی بەناوبانگە؟",
            "options": ["دەریاچەی دوکان", "دەریاچەی وان", "دەریاچەی ورمێ", "دەریاچەی توز"],
            "answer": "دەریاچەی دوکان",
        },
    },
    {
        "en": {
            "question": "Which city is famous for the Erbil Citadel?",
            "options": ["Erbil", "Zakho", "Akre", "Duhok"],
            "answer": "Erbil",
        },
        "ku": {
            "question": "کام شار بە قەڵای هەولێر بەناوبانگە؟",
            "options": ["هەولێر", "زاخۆ", "ئاکرێ", "دهۆک"],
            "answer": "هەولێر",
        },
    },
    {
        "en": {
            "question": "Which mountain range is strongly associated with Kurdistan?",
            "options": ["Zagros", "Alps", "Andes", "Himalayas"],
            "answer": "Zagros",
        },
        "ku": {
            "question": "کام زنجیرە شاخە بە شێوەیەکی زۆر پەیوەندی بە کوردستانەوە هەیە؟",
            "options": ["زاگرۆس", "ئەڵپ", "ئەندیز", "هیمالایا"],
            "answer": "زاگرۆس",
        },
    },
    {
        "en": {
            "question": "Which waterfall is located near Shaqlawa?",
            "options": ["Bekhal", "Gali Ali Beg", "Niagara", "Victoria"],
            "answer": "Bekhal",
        },
        "ku": {
            "question": "کام ئاوشار لە نزیکی شەقڵاوەیە؟",
            "options": ["بێخاڵ", "گەلی عەلی بەگ", "نیاگارا", "ڤیکتۆریا"],
            "answer": "بێخاڵ",
        },
    },
    {
        "en": {
            "question": "Which city is located near the Turkish border?",
            "options": ["Zakho", "Halabja", "Sulaymaniyah", "Shaqlawa"],
            "answer": "Zakho",
        },
        "ku": {
            "question": "کام شار لە نزیکی سنووری تورکیایە؟",
            "options": ["زاخۆ", "هەڵەبجە", "سلێمانی", "شەقڵاوە"],
            "answer": "زاخۆ",
        },
    },
    {
        "en": {
            "question": "What feeds many rivers in the Kurdistan highlands?",
            "options": ["Snow and rainfall", "Ocean tides", "Desert sand", "Volcanic lava"],
            "answer": "Snow and rainfall",
        },
        "ku": {
            "question": "چی سەرچاوەی ئاو بۆ زۆرێک لە ڕووبارەکانی ناوچە شاخاوییەکانی کوردستانە؟",
            "options": ["بەفر و باران", "شەپۆلی دەریا", "خۆڵی بیابان", "لاوەی گڕکان"],
            "answer": "بەفر و باران",
        },
    },
    {
        "en": {
            "question": "Which city is the capital of Sulaymaniyah Governorate?",
            "options": ["Sulaymaniyah", "Erbil", "Duhok", "Zakho"],
            "answer": "Sulaymaniyah",
        },
        "ku": {
            "question": "پایتەختی پارێزگای سلێمانی کام شارە؟",
            "options": ["سلێمانی", "هەولێر", "دهۆک", "زاخۆ"],
            "answer": "سلێمانی",
        },
    },
    {
        "en": {
            "question": "Which mountain is famous for its location near Erbil?",
            "options": ["Safeen", "Azmar", "Halgurd", "Gara"],
            "answer": "Safeen",
        },
        "ku": {
            "question": "کام شاخ بە نزیکی هەولێر بەناوبانگە؟",
            "options": ["سەفین", "ئەزمەر", "هەڵگورد", "گارە"],
            "answer": "سەفین",
        },
    },
    {
        "en": {
            "question": "Which ancient town is located in a dramatic mountain setting?",
            "options": ["Akre", "Erbil", "Halabja", "Duhok"],
            "answer": "Akre",
        },
        "ku": {
            "question": "کام شارۆچکەیەکی کۆن لە ناو دیمەنێکی شاخاویی سەرنجڕاکێشە؟",
            "options": ["ئاکرێ", "هەولێر", "هەڵەبجە", "دهۆک"],
            "answer": "ئاکرێ",
        },
    },
    {
        "en": {
            "question": "Which river is one of the famous rivers of Kurdistan?",
            "options": ["Tanjero", "Amazon", "Danube", "Rhine"],
            "answer": "Tanjero",
        },
        "ku": {
            "question": "کام ڕووبار یەکێکە لە ڕووبارە بەناوبانگەکانی کوردستان؟",
            "options": ["تانجەڕۆ", "ئامازۆن", "دانوب", "ڕاین"],
            "answer": "تانجەڕۆ",
        },
    },
    {
        "en": {
            "question": "Which place is a sacred valley associated with the Yazidi religion?",
            "options": ["Lalish", "Akre", "Shaqlawa", "Zakho"],
            "answer": "Lalish",
        },
        "ku": {
            "question": "کام شوێن دۆڵێکی پیرۆزە و پەیوەندی بە ئایینی ئێزیدییەوە هەیە؟",
            "options": ["لالش", "ئاکرێ", "شەقڵاوە", "زاخۆ"],
            "answer": "لالش",
        },
    },
    {
        "en": {
            "question": "Which river is known as the Great Zab?",
            "options": ["Great Zab", "Little Zab", "Sirwan", "Murat"],
            "answer": "Great Zab",
        },
        "ku": {
            "question": "کام ڕووبار بە زێی گەورە ناسراوە؟",
            "options": ["زێی گەورە", "زێی بچووک", "سیروان", "مورات"],
            "answer": "زێی گەورە",
        },
    },
    {
        "en": {
            "question": "Which city is known for its traditional old bazaar in this bot?",
            "options": ["Duhok", "Erbil", "Halabja", "Rawanduz"],
            "answer": "Duhok",
        },
        "ku": {
            "question": "کام شار لە ئەم بۆتەدا بە بازاڕی کۆنی خۆی ناسراوە؟",
            "options": ["دهۆک", "هەولێر", "هەڵەبجە", "ڕەواندز"],
            "answer": "دهۆک",
        },
    },
    {
        "en": {
            "question": "What is a major geographical feature of Kurdistan?",
            "options": ["Mountain ranges", "Coral reefs", "Polar ice sheets", "Savanna only"],
            "answer": "Mountain ranges",
        },
        "ku": {
            "question": "تایبەتمەندییەکی سەرەکی جوگرافیای کوردستان چییە؟",
            "options": ["زنجیرە شاخەکان", "ریفە مرجانییەکان", "بەستەڵەخی قەڵەمەری", "تەنها ساڤانا"],
            "answer": "زنجیرە شاخەکان",
        },
    },
    {
        "en": {
            "question": "Which city is famous for its historic citadel in the center?",
            "options": ["Erbil", "Zakho", "Duhok", "Halabja"],
            "answer": "Erbil",
        },
        "ku": {
            "question": "کام شار بە قەڵای مێژوویی لە ناوەڕاستی شارەکەی بەناوبانگە؟",
            "options": ["هەولێر", "زاخۆ", "دهۆک", "هەڵەبجە"],
            "answer": "هەولێر",
        },
    },
    {
        "en": {
            "question": "Which river is associated with Darbandikhan?",
            "options": ["Sirwan", "Great Zab", "Khabur", "Tigris"],
            "answer": "Sirwan",
        },
        "ku": {
            "question": "کام ڕووبار پەیوەندی بە دەربەندیخانەوە هەیە؟",
            "options": ["سیروان", "زێی گەورە", "خابور", "دیجلە"],
            "answer": "سیروان",
        },
    },
    {
        "en": {
            "question": "Which location is famous for its historic stone bridge near Zakho?",
            "options": ["Delal Bridge", "Golden Gate", "Brooklyn Bridge", "Tower Bridge"],
            "answer": "Delal Bridge",
        },
        "ku": {
            "question": "کام شوێن بە پردی بەردینی مێژوویی لە نزیکی زاخۆ بەناوبانگە؟",
            "options": ["پردی دلال", "گۆڵدن گەیت", "پردی برۆکلین", "تاوەر بریج"],
            "answer": "پردی دلال",
        },
    },
    {
        "en": {
            "question": "Which mountain is located in the Erbil area?",
            "options": ["Safeen", "Azmar", "Zawa", "Halgurd"],
            "answer": "Safeen",
        },
        "ku": {
            "question": "کام شاخ لە ناوچەی هەولێرە؟",
            "options": ["سەفین", "ئەزمەر", "زاوا", "هەڵگورد"],
            "answer": "سەفین",
        },
    },
    {
        "en": {
            "question": "Which city is famous for its mountain scenery and old streets?",
            "options": ["Akre", "Halabja", "Erbil", "Zakho"],
            "answer": "Akre",
        },
        "ku": {
            "question": "کام شار بە دیمەنی شاخ و کۆڵانە کۆنەکانی بەناوبانگە؟",
            "options": ["ئاکرێ", "هەڵەبجە", "هەولێر", "زاخۆ"],
            "answer": "ئاکرێ",
        },
    },
    {
        "en": {
            "question": "Which water body is located near Duhok city?",
            "options": ["Duhok Dam", "Dukan Lake", "Lake Van", "Lake Urmia"],
            "answer": "Duhok Dam",
        },
        "ku": {
            "question": "کام شوێنی ئاوی لە نزیکی شاری دهۆکە؟",
            "options": ["بەندی ئاوی دهۆک", "دەریاچەی دوکان", "دەریاچەی وان", "دەریاچەی ورمێ"],
            "answer": "بەندی ئاوی دهۆک",
        },
    },
    {
        "en": {
            "question": "Which city is famous for the Rawanduz area?",
            "options": ["Rawanduz", "Halabja", "Duhok", "Zakho"],
            "answer": "Rawanduz",
        },
        "ku": {
            "question": "ناوچەی ڕەواندز بە کام شارەوە ناسراوە؟",
            "options": ["ڕەواندز", "هەڵەبجە", "دهۆک", "زاخۆ"],
            "answer": "ڕەواندز",
        },
    },
]


def quiz_keyboard(question, lang):
    options = list(question[lang]["options"])
    random.shuffle(options)

    buttons = []

    for index, option in enumerate(options):
        buttons.append([
            InlineKeyboardButton(
                option,
                callback_data=f"quiz_answer_{index}"
            )
        ])

    # End Quiz button
    if lang == "en":
        buttons.append([
            InlineKeyboardButton(
                "❌ End Quiz",
                callback_data="quiz_end"
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                "❌ کۆتایی هێنان بە تاقیکردنەوە",
                callback_data="quiz_end"
            )
        ])

    return options, InlineKeyboardMarkup(buttons)


def quiz_menu_keyboard(lang):
    if lang == "en":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🎯 Start Quiz",
                    callback_data="quiz_start"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Main Menu",
                    callback_data="back_main"
                )
            ],
        ])

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎯 دەستپێکردنی تاقیکردنەوە",
                callback_data="quiz_start"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 سەرەکی",
                callback_data="back_main"
            )
        ],
    ])


def quiz_result_keyboard(lang):
    if lang == "en":
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔄 Play Again",
                    callback_data="quiz_start"
                )
            ],
            [
                InlineKeyboardButton(
                    "🏠 Main Menu",
                    callback_data="back_main"
                )
            ],
        ])

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 دووبارە یاری بکە",
                callback_data="quiz_start"
            )
        ],
        [
            InlineKeyboardButton(
                "🏠 سەرەکی",
                callback_data="back_main"
            )
        ],
    ])


async def show_quiz_question(query, context):
    quiz = context.user_data["quiz"]
    lang = quiz["language"]

    question_number = quiz["current"] + 1
    question = quiz["questions"][quiz["current"]]

    options, keyboard = quiz_keyboard(question, lang)

    # Save THIS question's randomized button order.
    quiz["current_options"] = options

    if lang == "en":
        text = (
            f"🎯 KURDISTAN GEOGRAPHY QUIZ\n\n"
            f"Question {question_number}/15\n\n"
            f"{question['en']['question']}"
        )
    else:
        text = (
            f"🎯 تاقیکردنەوەی جوگرافیای کوردستان\n\n"
            f"پرسیاری {question_number}/15\n\n"
            f"{question['ku']['question']}"
        )

    await query.edit_message_text(
        text,
        reply_markup=keyboard
    )


async def start_quiz(query, context, lang):
    # Choose 15 DIFFERENT questions randomly from the full bank.
    selected_questions = random.sample(QUIZ_QUESTIONS, 15)

    context.user_data["quiz"] = {
        "questions": selected_questions,
        "current": 0,
        "score": 0,
        "language": lang,
        "current_options": [],
    }

    await show_quiz_question(query, context)
def language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏔️ کوردی", callback_data="lang_ku"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ])


def main_keyboard(lang):
    t = TEXT[lang]

    quiz_name = "🎯 Geography Quiz" if lang == "en" else "🎯 تاقیکردنەوەی جوگرافیا"

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
            InlineKeyboardButton(
                quiz_name,
                callback_data="quiz_menu"
            )
        ],
        
        [
            InlineKeyboardButton(
                t["search"],
                callback_data="search_place"
            )
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
            ("🌊 ئاوه‌سپی", "adhaim"),
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

def rivers_keyboard(lang):
    rivers = {
        "en": [
            ("Tigris River", "tigris"),
            ("Euphrates River", "euphrates"),
            ("Great Zab", "great_zab"),
            ("Little Zab", "little_zab"),
            ("Sirwan River", "sirwan"),
            ("Khabur River", "khabur"),
            ("Adhaim River", "adhaim"),
            ("Khazir River", "khazir"),
            ("Tanjero River", "tanjero"),
            ("Rawanduz River", "rwandz"),
            ("Gali Ali Beg", "gali_ali_bag"),
            ("Shamdinan River", "shamdinan"),
            ("Murat River", "murat"),
            ("Karasu River", "karasu"),
            ("Botan River", "botan"),
            ("Aras River", "aras"),
            ("Zarrineh River", "zarrinarud"),
            ("Simineh River", "siminarud"),
            ("Qezel Ozan", "ghezel_ozan"),
        ],
        "ku": [
            ("ڕووباری دیجلە", "tigris"),
            ("ڕووباری فورات", "euphrates"),
            ("زێی گەورە", "great_zab"),
            ("زێی بچووک", "little_zab"),
            ("ڕووباری سیروان", "sirwan"),
            ("ڕووباری خابوور", "khabur"),
            ("ڕووباری عەدهایم", "adhaim"),
            ("ڕووباری خازر", "khazir"),
            ("ڕووباری تەنژەرۆ", "tanjero"),
            ("ڕووباری ڕەواندز", "rwandz"),
            ("گالی عەلی بەگ", "gali_ali_bag"),
            ("ڕووباری شەمەدینان", "shamdinan"),
            ("ڕووباری مورات", "murat"),
            ("ڕووباری کاراسو", "karasu"),
            ("ڕووباری بۆتان", "botan"),
            ("ڕووباری ئاراس", "aras"),
            ("ڕووباری زەڕینە", "zarrinarud"),
            ("ڕووباری سیمینە", "siminarud"),
            ("قەزەل ئۆزان", "ghezel_ozan"),
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
            ("Safeen Mountain", "safine"),
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


def locations_keyboard(lang):
    categories = {}

    category_names = {
        "🏛️ Ancient & History": {
            "en": "🏛️ Ancient & History",
            "ku": "🏛️ شوێنە مێژووییەکان",
        },
        "🌳 Nature & Parks": {
            "en": "🌳 Nature & Parks",
            "ku": "🌳 سروشت و پارکەکان",
        },
        "🏘️ Towns & Culture": {
            "en": "🏘️ Towns & Culture",
            "ku": "🏘️ شارۆچکە و کەلتوور",
        },
        "🏔️ Mountains & Canyons": {
            "en": "🏔️ Mountains & Canyons",
            "ku": "🏔️ شاخەکان و کانیۆنەکان",
        },
        "💦 Waterfalls & Nature": {
            "en": "💦 Waterfalls & Nature",
            "ku": "💦 ئاوشار و سروشت",
        },
        "🏔️ Mountains & Viewpoints": {
            "en": "🏔️ Mountains & Viewpoints",
            "ku": "🏔️ شاخ و خاڵەکانی دیمەن",
        },
        "🌊 Lakes & Water": {
            "en": "🌊 Lakes & Water",
            "ku": "🌊 دەریاچە و ئاو",
        },
        "🕍 Cultural & Sacred": {
            "en": "🕍 Cultural & Sacred",
            "ku": "🕍 کەلتووری و پیرۆز",
        },
    }

    for location_id, location in LOCATIONS.items():
        category = location["category"]

        if category not in categories:
            categories[category] = []

        categories[category].append(location_id)

    buttons = []

    for category in categories:
        button_text = category_names.get(
            category,
            {}
        ).get(lang, category)

        buttons.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"loccat_{category}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            TEXT[lang]["back"],
            callback_data="back_main"
        )
    ])

    return InlineKeyboardMarkup(buttons)


def location_category_keyboard(category, lang):
    buttons = []

    for location_id, location in LOCATIONS.items():
        if location["category"] == category:
            buttons.append([
                InlineKeyboardButton(
                    location[lang]["name"],
                    callback_data=f"location_{location_id}"
                )
            ])

    buttons.append([
        InlineKeyboardButton(
            TEXT[lang]["back"],
            callback_data="locations"
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



async def safe_query_answer(query, *args, **kwargs):
    try:
        await query.answer(*args, **kwargs)
    except BadRequest as error:
        error_text = str(error).lower()
        if (
            "query is too old" in error_text
            or "query id is invalid" in error_text
            or "response timeout expired" in error_text
        ):
            return
        raise



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    data = query.data
    lang = context.user_data.get("language", "en")
    
    # =========================
    # SEARCH FOR A PLACE
    # =========================

 
    if data == "nearby_places":
        await safe_query_answer(query)

        location_text = (
            "📍 Share your location to find the nearest places in Kurdistan."
            if lang == "en"
            else
            "📍 بۆ دۆزینەوەی شوێنە نزیکەکان لە کوردستان، شوێنی خۆت هاوبەش بکە."
        )

        location_button = (
            "📍 Share my location"
            if lang == "en"
            else
            "📍 شوێنی خۆم هاوبەش بکەم"
        )

        location_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton(location_button, request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        await query.message.reply_text(
            location_text,
            reply_markup=location_keyboard,
        )
        return

    if data == "search_place":
        await safe_query_answer(query)

        context.user_data["searching_place"] = True

        search_text = (
            "🔎 Enter the name of a place in Kurdistan.\n\n"
            "Examples: Erbil Citadel, Mount Safeen, Dukan Lake"
            if lang == "en"
            else
            "🔎 ناوی شوێنێک لە کوردستان بنووسە.\n\n"
            "نموونە: قەڵای هەولێر، چیای سەفین، دەریاچەی دووکان"
        )

        await query.message.reply_text(search_text)
        return

    # =========================
    # QUIZ MENU
    # =========================

    if data == "quiz_menu":
        await safe_query_answer(query)

        quiz_text = (
            "🎯 KURDISTAN GEOGRAPHY QUIZ\n\n"
            "Test your knowledge of Kurdistan geography!\n\n"
            "• 15 questions\n"
            "• Random questions every game\n"
            "• Random answer order\n"
            "• Score at the end"
            if lang == "en"
            else
            "🎯 تاقیکردنەوەی جوگرافیای کوردستان\n\n"
            "زانیاریت لە جوگرافیای کوردستان تاقی بکەرەوە!\n\n"
            "• ١٥ پرسیار\n"
            "• پرسیاری جیاواز لە هەر یارییەکدا\n"
            "• ڕیزبەندی وەڵامەکان بە شێوەی هەڕەمەکی\n"
            "• نمرە لە کۆتاییدا"
        )

        await query.edit_message_text(
            quiz_text,
            reply_markup=quiz_menu_keyboard(lang)
        )
        return

    # =========================
    # START / RESTART QUIZ
    # =========================

    if data == "quiz_start":
        await safe_query_answer(query)
        await start_quiz(query, context, lang)
        return

    # =========================
    # END QUIZ
    # =========================

    if data == "quiz_end":
        quiz = context.user_data.get("quiz")

        if not quiz:
            await safe_query_answer(
                query,
                "No active quiz.",
                show_alert=True
            )
            return

        await safe_query_answer(query)

        score = quiz["score"]
        current = quiz["current"]

        if quiz["language"] == "en":
            result_text = (
                "🎯 KURDISTAN GEOGRAPHY QUIZ\n\n"
                "🛑 QUIZ ENDED\n\n"
                f"⭐ Your score: {score}/{current}\n"
                f"📚 Questions completed: {current}/15\n\n"
                "You can start a new quiz anytime!"
            )
        else:
            result_text = (
                "🎯 تاقیکردنەوەی جوگرافیای کوردستان\n\n"
                "🛑 تاقیکردنەوەکە کۆتایی پێهات\n\n"
                f"⭐ نمرەکەت: {score}/{current}\n"
                f"📚 پرسیارە تەواوکراوەکان: {current}/15\n\n"
                "دەتوانیت هەر کاتێک تاقیکردنەوەیەکی نوێ دەست پێ بکەیت!"
            )

        await query.edit_message_text(
            result_text,
            reply_markup=quiz_result_keyboard(
                quiz["language"]
            )
        )

        return

    # =========================
    # QUIZ ANSWER
    # =========================

    if data.startswith("quiz_answer_"):
        quiz = context.user_data.get("quiz")

        if not quiz:
            await safe_query_answer(
                query,
                "Quiz session expired. Please start again.",
                show_alert=True
            )
            return

        answer_index = int(
            data.replace("quiz_answer_", "")
        )

        options = quiz["current_options"]

        if answer_index >= len(options):
            await safe_query_answer(
                query,
                "Invalid answer.",
                show_alert=True
            )
            return

        selected_answer = options[answer_index]

        current_question = quiz["questions"][quiz["current"]]

        correct_answer = current_question[
            quiz["language"]
        ]["answer"]

        if selected_answer == correct_answer:
            quiz["score"] += 1
            answer_message = (
                "✅ Correct!"
                if quiz["language"] == "en"
                else "✅ ڕاستە!"
            )
        else:
            answer_message = (
                "❌ Wrong!"
                if quiz["language"] == "en"
                else "❌ هەڵەیە!"
            )

        await safe_query_answer(query, answer_message)

        quiz["current"] += 1

        if quiz["current"] < 15:
            await show_quiz_question(
                query,
                context
            )
            return

        # =========================
        # QUIZ FINISHED
        # =========================

        score = quiz["score"]

        if quiz["language"] == "en":

            if score >= 13:
                message = "🏆 Excellent!"
            elif score >= 10:
                message = "👏 Great job!"
            elif score >= 7:
                message = "👍 Good job!"
            else:
                message = "💪 Keep learning!"

            result_text = (
                "🎯 KURDISTAN GEOGRAPHY QUIZ\n\n"
                "🏁 QUIZ COMPLETE!\n\n"
                f"⭐ Your score: {score}/15\n\n"
                f"{message}"
            )

        else:

            if score >= 13:
                message = "🏆 زۆر نایاب!"
            elif score >= 10:
                message = "👏 زۆر باشە!"
            elif score >= 7:
                message = "👍 باشە!"
            else:
                message = "💪 بەردەوام بە لە فێربوون!"

            result_text = (
                "🎯 تاقیکردنەوەی جوگرافیای کوردستان\n\n"
                "🏁 تاقیکردنەوەکە تەواو بوو!\n\n"
                f"⭐ نمرەکەت: {score}/15\n\n"
                f"{message}"
            )

        await query.edit_message_text(
            result_text,
            reply_markup=quiz_result_keyboard(
                quiz["language"]
            )
        )

        return

    # =========================
    # LANGUAGE
    # =========================

    if data.startswith("lang_"):
        await safe_query_answer(query)

        new_lang = data.replace("lang_", "")

        if new_lang not in ["en", "ku"]:
            new_lang = "en"

        context.user_data["language"] = new_lang

        await query.edit_message_text(
            TEXT[new_lang]["welcome"],
            reply_markup=main_keyboard(new_lang),
        )
        return

    # =========================
    # 
    # =========================
    # =========================
    # FOUR SEASONS GUIDE
    # =========================

    if data == "nature":
        await safe_query_answer(query)

        seasons_text = (
            "🌍 KURDISTAN: FOUR SEASONS\n\n"
            "Discover unusual natural and historical places.\n"
            "Choose a season to explore:\n\n"
            "🌸 Spring — green valleys and ancient sites\n"
            "☀️ Summer — highlands and forest escapes\n"
            "🍂 Autumn — heritage and scenic landscapes\n"
            "❄️ Winter — mountain scenery and cultural trips"
            if lang == "en"
            else
            "🌍 کوردستان: چوار وەرز\n\n"
            "شوێنە سروشتی و مێژووییە تایبەتەکان بدۆزەرەوە.\n"
            "وەرزێک هەڵبژێرە:\n\n"
            "🌸 بەهار — دۆڵی سەوز و شوێنی مێژوویی\n"
            "☀️ هاوین — ناوچە بەرزەکان و دارستان\n"
            "🍂 پاییز — مێژوو و دیمەنی جوان\n"
            "❄️ زستان — دیمەنی چیا و شوێنی کولتووری"
        )

        seasons_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🌸 Spring" if lang == "en" else "🌸 بەهار",
                    callback_data="season_spring"
                )
            ],
            [
                InlineKeyboardButton(
                    "☀️ Summer" if lang == "en" else "☀️ هاوین",
                    callback_data="season_summer"
                )
            ],
            [
                InlineKeyboardButton(
                    "🍂 Autumn" if lang == "en" else "🍂 پاییز",
                    callback_data="season_autumn"
                )
            ],
            [
                InlineKeyboardButton(
                    "❄️ Winter" if lang == "en" else "❄️ زستان",
                    callback_data="season_winter"
                )
            ],
            [
                InlineKeyboardButton(
                    TEXT[lang]["back"],
                    callback_data="back_main"
                )
            ]
        ])

        await query.edit_message_text(
            seasons_text,
            reply_markup=seasons_keyboard
        )
        return
        
    # =========================
    # FOUR SEASONS DESTINATIONS
    # =========================

    SEASON_PLACES = {
        "spring": [
            ("🌿 Barzan Valley", "Barzan Valley, Kurdistan Region, Iraq"),
            ("🏞️ Zawita Forest", "Zawita, Duhok, Iraq"),
            ("🌊 Ahmed Awa", "Ahmed Awa Waterfall, Halabja, Iraq"),
            ("⛰️ Gali Ali Beg", "Gali Ali Beg Waterfall, Kurdistan Region, Iraq"),
            ("🏛️ Shanidar Cave", "Shanidar Cave, Bradost, Iraq"),
        ],
        "summer": [
            ("🌲 Sarsink", "Sarsink, Duhok, Iraq"),
            ("⛰️ Gara Mountain", "Mount Gara, Duhok, Iraq"),
            ("🌄 Amedi Cliffs", "Amedi, Duhok, Iraq"),
            ("🌳 Zawa Mountain", "Zawa Mountain, Duhok, Iraq"),
            ("🏞️ Rawanduz Gorge", "Rawanduz Gorge, Erbil, Iraq"),
        ],
        "autumn": [
            ("🍂 Akre", "Akre, Duhok, Iraq"),
            ("🏛️ Khanzad Castle", "Khanzad Castle, Erbil, Iraq"),
            ("🏰 Sherwana Castle", "Sherwana Castle, Kalar, Iraq"),
            ("🪨 Qizqapan Cave", "Qizqapan Cave, Sulaymaniyah, Iraq"),
            ("🌄 Barzan Valley", "Barzan Valley, Kurdistan Region, Iraq"),
        ],
        "winter": [
            ("🏙️ Erbil Citadel", "Erbil Citadel, Erbil, Iraq"),
            ("🏛️ Shanidar Cave area", "Shanidar Cave, Bradost, Iraq"),
            ("🌊 Dukan Lake", "Dukan Lake, Sulaymaniyah, Iraq"),
            ("🏞️ Duhok Dam", "Duhok Dam, Duhok, Iraq"),
            ("🏰 Amedi", "Amedi, Duhok, Iraq"),
        ],
    }

    if data.startswith("season_"):
        await safe_query_answer(query)

        season = data.replace("season_", "", 1)
        places = SEASON_PLACES.get(season, [])

        season_names = {
            "spring": ("🌸 Spring", "🌸 بەهار"),
            "summer": ("☀️ Summer", "☀️ هاوین"),
            "autumn": ("🍂 Autumn", "🍂 پاییز"),
            "winter": ("❄️ Winter", "❄️ زستان"),
        }

        season_title = season_names.get(
            season, ("Natural Places", "شوێنە سروشتییەکان")
        )[0 if lang == "en" else 1]

        buttons = []

        for place_name, map_query in places:
            map_url = (
                "https://www.google.com/maps/search/?api=1&query="
                + map_query.replace(" ", "+")
            )

            buttons.append([
                InlineKeyboardButton(
                    place_name,
                    url=map_url
                )
            ])

        buttons.append([
            InlineKeyboardButton(
                "⬅️ Back to Seasons" if lang == "en"
                else "⬅️ گەڕانەوە بۆ وەرزەکان",
                callback_data="nature"
            )
        ])

        buttons.append([
            InlineKeyboardButton(
                TEXT[lang]["back"],
                callback_data="back_main"
            )
        ])

        await query.edit_message_text(
            (
                f"{season_title}\n\n"
                + (
                    "Explore these destinations. Tap a place to open Google Maps."
                    if lang == "en"
                    else
                    "ئەم شوێنانە بدۆزەرەوە. لەسەر ناوی شوێنێک دابگرە بۆ کردنەوەی Google Maps."
                )
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return
    if data == "locations":
        await safe_query_answer(query)

        title = (
            "📍 EXPLORE KURDISTAN\n\n"
            "Choose a type of destination:"
            if lang == "en"
            else
            "📍 کوردستان بگەڕێ\n\n"
            "جۆری شوێنێک هەڵبژێرە:"
        )

        await query.edit_message_text(
            title,
            reply_markup=locations_keyboard(lang)
        )
        return

    # =========================
    # LOCATION CATEGORY
    # =========================

    if data.startswith("loccat_"):
        await safe_query_answer(query)

        category = data.replace("loccat_", "")

        await query.edit_message_text(
            category,
            reply_markup=location_category_keyboard(
                category,
                lang
            )
        )
        return

    # =========================
    # INDIVIDUAL LOCATION
    # =========================

    if data.startswith("location_"):
        await safe_query_answer(query)

        location_id = data.replace("location_", "")

        if location_id not in LOCATIONS:
            await safe_query_answer(
                query,
                "Location not found.",
                show_alert=True
            )
            return

        location = LOCATIONS[location_id][lang]

        await query.edit_message_text(
            location["text"],
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🗺️ Google Maps",
                        url=location["map"]
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📍 Back to Locations",
                        callback_data="locations"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🏠 Main Menu",
                        callback_data="back_main"
                    )
                ]
            ])
        )
        return

    # =========================
    # MOUNTAINS MENU
    # =========================

    if data == "mountains":
        await safe_query_answer(query)

        await query.edit_message_text(
            "⛰️ Choose a mountain:"
            if lang == "en"
            else
            "⛰️ چیاێک هەڵبژێرە:",
            reply_markup=mountains_keyboard(lang),
        )
        return

    # =========================
    # INDIVIDUAL MOUNTAIN
    # =========================

    if data.startswith("mountain_"):
        await safe_query_answer(query)

        mountain_id = data.replace(
            "mountain_",
            ""
        )

        if mountain_id not in MOUNTAINS:
            await safe_query_answer(
                query,
                "Mountain not found.",
                show_alert=True
            )
            return

        mountain = MOUNTAINS[mountain_id][lang]

        if "photo" in mountain:
            with open(
                mountain["photo"],
                "rb"
            ) as photo:

                await query.message.reply_photo(
                    photo=photo,
                    caption=mountain["text"],
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
                        ]
                    ])
                )
        else:
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
                    ]
                ])
            )

        return

    # =========================
    # RIVERS
    # =========================

    if data == "rivers":
        await safe_query_answer(query)

        await query.edit_message_text(
            "🌊 Choose a river or water place:"
            if lang == "en"
            else
            "🌊 ڕووبار یان شوێنی ئاوی هەڵبژێرە:",
            reply_markup=rivers_keyboard(lang),
        )
        return

    # =========================
    # INDIVIDUAL RIVER
    # =========================

    if data.startswith("river_"):
        await safe_query_answer(query)

        river_id = data.replace(
            "river_",
            ""
        )

        if river_id not in RIVERS:
            await safe_query_answer(
                query,
                "River not found.",
                show_alert=True
            )
            return

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
                ]
            ]),
        )
        return

    # =========================
    # CITIES
    # =========================

    if data == "cities":
        await safe_query_answer(query)

        await query.edit_message_text(
            TEXT[lang]["choose_city"],
            reply_markup=cities_keyboard(lang),
        )
        return

    # =========================
    # INDIVIDUAL CITY
    # =========================

    if data.startswith("city_"):
        await safe_query_answer(query)

        city_id = data.replace(
            "city_",
            ""
        )

        if city_id not in CITIES:
            await safe_query_answer(
                query,
                "City not found.",
                show_alert=True
            )
            return

        city = CITIES[city_id][lang]

        await query.edit_message_text(
            city["text"],
            reply_markup=city_keyboard(
                city_id,
                lang
            ),
        )
        return

    # =========================
    # FACTS
    # =========================

    if data == "facts":
        await safe_query_answer(query)
        keyboard = []

        for fact_id, fact in FACTS.items():
            keyboard.append([
                InlineKeyboardButton(
                    fact[lang]["title"],
                    callback_data=f"fact_{fact_id}"
                )
            ])

        keyboard.append([
            InlineKeyboardButton(
                TEXT[lang]["back"],
                callback_data="back_main"
            )
        ])

        await query.edit_message_text(
            "📚 Choose a geography fact:"
            if lang == "en"
            else
            "📚 زانیارییەکی جوگرافی هەڵبژێرە:",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
        )
        return

    # =========================
    # INDIVIDUAL FACT
    # =========================

    if data.startswith("fact_"):
        await safe_query_answer(query)

        fact_id = data.replace(
            "fact_",
            ""
        )

        if fact_id not in FACTS:
            await safe_query_answer(
                query,
                "Fact not found.",
                show_alert=True
            )
            return

        fact = FACTS[fact_id][lang]

        await query.edit_message_text(
            f"{fact['title']}\n\n{fact['text']}",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        TEXT[lang]["back"],
                        callback_data="facts"
                    )
                ]
            ]),
        )
        return

    # =========================
    # BACK TO MAIN MENU
    # =========================

    if data == "back_main":
        await safe_query_answer(query)

        await query.edit_message_text(
            TEXT[lang]["welcome"],
            reply_markup=main_keyboard(lang),
        )
        return

    # =========================
    # LANGUAGE MENU
    # =========================

    if data == "language":
        await safe_query_answer(query)

        await query.edit_message_text(
            TEXT[lang]["choose"],
            reply_markup=language_keyboard(),
        )
        return

# =========================
# SEARCH PLACE MESSAGE HANDLER
# =========================

async def search_place_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not context.user_data.get("searching_place"):
        return

    if not update.message or not update.message.text:
        return

    place_name = update.message.text.strip()
    lang = context.user_data.get("language", "en")

    if not place_name:
        await update.message.reply_text(
            "Please enter a place name."
            if lang == "en"
            else "تکایە ناوی شوێنێک بنووسە."
        )
        return

    context.user_data["searching_place"] = False

    from urllib.parse import quote_plus

    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        + quote_plus(place_name + ", Kurdistan Region, Iraq")
    )

    if lang == "en":
        result_text = (
            f"🔎 Your search: {place_name}\n\n"
            "Open Google Maps to explore this place."
        )
        maps_label = "🗺️ Open Google Maps"
        again_label = "🔎 Search Again"
    else:
        result_text = (
            f"🔎 گەڕانت: {place_name}\n\n"
            "بۆ بینینی شوێنەکە لە نەخشەی گووگڵ بکەرەوە."
        )
        maps_label = "🗺️ کردنەوەی نەخشەی گووگڵ"
        again_label = "🔎 گەڕانەوە"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                maps_label,
                url=maps_url
            )
        ],
        [
            InlineKeyboardButton(
                t["search"],
                callback_data="search_place"
            )
        ],
        [
            InlineKeyboardButton(
                "📍 Nearby Places" if lang == "en" else "📍 شوێنە نزیکەکان",
                callback_data="nearby_places"
            )
        ],
        [
            InlineKeyboardButton(
                TEXT[lang]["back"],
                callback_data="back_main"
            )
        ]
    ])

    await update.message.reply_text(
        result_text,
        reply_markup=keyboard
    )

# =========================
# RENDER HEALTH SERVER
# =========================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(
            b"Kurdistan Geography Bot is running!"
        )

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    server.serve_forever()


# =========================
# MAIN
# =========================

import math


def calculate_distance(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return earth_radius_km * 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

async def handle_shared_location(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not update.message or not update.message.location:
        return

    user_location = update.message.location
    lang = context.user_data.get("language", "en")

    nearest_places = []

    for place in NEARBY_PLACES:
        distance = calculate_distance(
            user_location.latitude,
            user_location.longitude,
            place["lat"],
            place["lon"],
        )

        nearest_places.append((distance, place))

    nearest_places.sort(key=lambda item: item[0])

    if lang == "ku":
        response = "📍 شوێنە نزیکەکان بەپێی دووری:\n\n"
    else:
        response = "📍 Nearest cities by distance:\n\n"

    for distance, place in nearest_places:
        name = place["name_ku"] if lang == "ku" else place["name_en"]

        response += (
            f"📌 {name}\n"
            f"📏 {distance:.1f} km\n"
            f"🗺️ {place['map']}\n\n"
        )

    response += (
        "تێبینی: دوورییەکان نزیکەیین."
        if lang == "ku"
        else "Note: Distances are approximate straight-line distances."
    )

    await update.message.reply_text(
        response,
        reply_markup=ReplyKeyboardRemove(),
        disable_web_page_preview=True,
    )

def main():

    health_thread = threading.Thread(
        target=run_health_server,
        daemon=True
    )

    health_thread.start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            search_place_message
        )
    )
    
    app.add_handler(
        MessageHandler(
            filters.LOCATION,
            handle_shared_location
        )
    )

    print(
        "Kurdistan Geography Bot is running..."
    )

    app.run_polling()


if __name__ == "__main__":
    main()
