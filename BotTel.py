import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import telegram
import os

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define the admin IDs
ADMIN_IDS = ["421372511", "1773932361"]

# Function to read a file
def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return "Error reading file."

# Function to write to a file
def write_file(file_path: str, content: str) -> str:
    try:
        with open(file_path, 'a') as file:
            file.write(content + '\n')
        return "API token saved successfully."
    except Exception as e:
        logger.error(f"Error writing to file {file_path}: {e}")
        return "Error writing to file."

# Command handler for /api to read the .env file
async def api(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) in ADMIN_IDS:
        content = read_file('.env')
        try:
            await update.message.reply_text(content)
        except telegram.error.BadRequest:
            apis = read_file('.env')
            await update.message.reply_text(apis)
    else:
        await update.message.reply_text('Access denied.')

# Command handler for /setapi to write to the .env file
async def setapi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) in ADMIN_IDS:
        # Extract the API token from the message
        api_token = '\n'.join(context.args)
        if api_token:
            result = write_file('.env', api_token)
            await update.message.reply_text(result)
        else:
            await update.message.reply_text("Please provide an API token.")
    else:
        await update.message.reply_text('Access denied.')

# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome')

# Command handler for /good
async def good(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) in ADMIN_IDS:
        content = read_file('good.txt')
        try:
            await update.message.reply_text(content)
        except telegram.error.BadRequest:
            await update.message.reply_text("Nothing..!!! Afsooooooos!")
    else:
        await update.message.reply_text('Access denied.')

# Command handler for /bad
async def bad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) in ADMIN_IDS:
        count = os.popen("wc -l bad.txt").read().replace('\n', '')
        await update.message.reply_text(count)
    else:
        await update.message.reply_text('Access denied.')

# Command handler for /invalid_count
async def invalid_count(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.from_user.id) in ADMIN_IDS:
        content = read_file('invalid_count.txt')
        await update.message.reply_text(content)
    else:
        await update.message.reply_text('Access denied.')

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token("YourApiToken").build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("api", api))
    application.add_handler(CommandHandler("setapi", setapi))
    application.add_handler(CommandHandler("good", good))
    application.add_handler(CommandHandler("bad", bad))
    application.add_handler(CommandHandler("invalid_count", invalid_count))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    application.run_polling()

if __name__ == '__main__':
    main()
