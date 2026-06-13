import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = "8809300222:AAFFeU1n0zi1RKLCY32KIxQhOqVBEf-OdBI"
HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/Rodo1234/Mi-IA-Libre"

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = requests.post(API_URL, json={"inputs": user_text}, headers=headers, timeout=30)
        if response.status_code == 200:
            resultado = response.json()
            respuesta = resultado[0].get('generated_text', '...') if isinstance(resultado, list) else str(resultado)
            await update.message.reply_text(respuesta)
        else:
            await update.message.reply_text(f"Error: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Error de conexión: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    app.run_polling()
