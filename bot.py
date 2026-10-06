
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
            InlineKeyboardButton(
                t["cities"],
                callback_data="cities"
            ),
            InlineKeyboardButton(
                t["mountains"],
                callback_data="mountains"
            ),
        ],
        [
            InlineKeyboardButton(
                t["rivers"],
                callback_data="rivers"
            ),
            InlineKeyboardButton(
                t["nature"],
                callback_data="nature"
            ),
        ],
        [
            InlineKeyboardButton(
                t["locations"],
                callback_data="locations"
            ),
            InlineKeyboardButton(
                t["facts"],
                callback_data="facts"
            ),
        ],
        [
            InlineKeyboardButton(
                t["language"],
                callback_data="language"
            ),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌍 Kurdistan Geography\n\n"
        "🌐 Choose your language / زمان هەڵبژێرە:",
        reply_markup=language_keyboard(),
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    if query.data.startswith("lang_"):
        lang = query.data.replace("lang_", "")

        context.user_data["language"] = lang

        await query.edit_message_text(
            TEXT[lang]["welcome"],
            reply_markup=main_keyboard(lang),
        )

        return

    lang = context.user_data.get("language", "en")

    messages = {
        "cities": {
            "en": "🏙️ Cities\n\nComing soon...",
            "ku": "🏙️ شارەکان\n\nبەم زووانە...",
        },
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
        "language": {
            "en": "🌐 Choose your language:",
            "ku": "🌐 زمان هەڵبژێرە:",
        },
    }

    if query.data == "language":
        await query.edit_message_text(
            messages["language"][lang],
            reply_markup=language_keyboard(),
        )
    else:
        await query.edit_message_text(
            messages[query.data][lang],
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
