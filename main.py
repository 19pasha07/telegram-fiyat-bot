import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATA = {
    "A52": {
        "Samsung": {
            "Ekran": 79,
            "Pil": 18
        },
        "Oppo": {
            "Ekran": 65,
            "Pil": 16
        }
    }
}

def get_usd_try():
    r = requests.get("https://api.exchangerate.host/latest?base=USD&symbols=TRY")
    return r.json()["rates"]["TRY"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📱 Model yazın\nÖrnek: A52"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()

    if text in DATA:
        context.user_data["model"] = text
        brands = list(DATA[text].keys())

        msg = "Hangi marka?\n"
        for i, b in enumerate(brands, 1):
            msg += f"{i}️⃣ {b}\n"

        await update.message.reply_text(msg)
        return

    if "model" in context.user_data:
        model = context.user_data["model"]
        brands = list(DATA[model].keys())

        if text.isdigit() and 1 <= int(text) <= len(brands):
            brand = brands[int(text)-1]
            usd_try = get_usd_try()

            msg = f"📱 {brand} {model}\n\n"
            for part, price in DATA[model][brand].items():
                final_usd = price + 17
                final_try = round(final_usd * usd_try)
                msg += f"• {part}: {final_usd} $\n  💰 {final_try} ₺\n\n"

            msg += "ℹ️ Not: -17 $ çıkart"
            await update.message.reply_text(msg)
            context.user_data.clear()

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
