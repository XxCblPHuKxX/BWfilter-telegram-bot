from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image
import io

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне фото, и я сделаю его черно-белым.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        image = Image.open(io.BytesIO(photo_bytes))
        
        bw_image = image.convert("L")
        
        output_buffer = io.BytesIO()
        bw_image.save(output_buffer, format="JPEG")
        output_buffer.seek(0)
        
        await update.message.reply_photo(photo=output_buffer, caption="Черно-белое фото готово!")
        output_buffer.close()
        
    except Exception as e:
        print(f"Error processing photo: {e}")
        await update.message.reply_text("Ошибка при обработке фото. Попробуй снова!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, отправь фото.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text("Произошла ошибка. Попробуй снова!")

app = ApplicationBuilder().token("here is a bot token from the @BotFather in telegram").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_error_handler(error)
