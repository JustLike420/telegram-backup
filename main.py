import os
import subprocess
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')

DUMP_FILE = 'dump.sql'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{current_time}_{DUMP_FILE}"
    command = [
        "pg_dump",
        f"--dbname=postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}",
        f"--file={filename}"
    ]
    subprocess.run(
        command,
        check=True
    )
    with open(filename, 'rb') as file:
        await update.message.reply_document(file)

    os.remove(filename)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()
