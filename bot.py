import os
import logging
import tempfile
import shutil
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from image_processor import ImageProcessor
import asyncio

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# User session storage
user_sessions = {}

class ConversionSession:
    def __init__(self):
        self.files = []
        self.output_format = None
        self.quality_mode = None
        self.quality_value = None
        self.dimensions = None
        self.temp_dir = None

    def reset(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        self.__init__()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when /start command is issued."""
    welcome_text = (
        "🎨 *Professional Image Converter Bot* 🎨\n\n"
        "Welcome! I can help you convert and compress images professionally.\n\n"
        "*Features:*\n"
        "✅ Upload ZIP files or individual images\n"
        "✅ Support multiple ZIP uploads\n"
        "✅ Convert to PNG, JPEG, JPG, WEBP\n"
        "✅ Quality control (presets, percentage, dimensions)\n"
        "✅ Batch processing with progress updates\n"
        "✅ Maintains original file structure\n\n"
        "*How to use:*\n"
        "1️⃣ Upload your image(s) or ZIP file(s)\n"
        "2️⃣ Choose output format\n"
        "3️⃣ Select quality settings\n"
        "4️⃣ Get your converted images in a ZIP file\n\n"
        "Send /help for more information.\n"
        "Send /cancel to reset current session.\n\n"
        "Ready to start? Upload your first file! 📤"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message."""
    help_text = (
        "*📖 Help & Instructions*\n\n"
        "*Supported Input Formats:*\n"
        "• Images: PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF\n"
        "• Archives: ZIP files containing images\n\n"
        "*Supported Output Formats:*\n"
        "• PNG, JPEG, JPG, WEBP\n\n"
        "*Quality Options:*\n"
        "• Presets: Low (60%), Medium (80%), High (95%), Original (100%)\n"
        "• Custom: Choose any percentage (1-100%)\n"
        "• Dimensions: Resize by width and height in pixels\n\n"
        "*Commands:*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/cancel - Cancel current session and start over\n\n"
        "*Tips:*\n"
        "• You can upload multiple ZIP files before converting\n"
        "• Original file names and folder structure are preserved\n"
        "• All converted images are returned in a single ZIP file\n"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel current session."""
    user_id = update.effective_user.id
    if user_id in user_sessions:
        user_sessions[user_id].reset()
        del user_sessions[user_id]
    await update.message.reply_text(
        "✅ Session cancelled. You can start over by uploading new files."
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle uploaded files (images or ZIP)."""
    user_id = update.effective_user.id
    
    # Initialize session if needed
    if user_id not in user_sessions:
        user_sessions[user_id] = ConversionSession()
        user_sessions[user_id].temp_dir = tempfile.mkdtemp()
    
    session = user_sessions[user_id]
    
    # Get file
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name
    file_path = os.path.join(session.temp_dir, file_name)
    
    # Download file
    await update.message.reply_text(f"⬇️ Downloading {file_name}...")
    await file.download_to_drive(file_path)
    
    session.files.append(file_path)
    
    # Create inline keyboard
    keyboard = [
        [InlineKeyboardButton("✅ Start Converting", callback_data="start_conversion")],
        [InlineKeyboardButton("➕ Upload More Files", callback_data="upload_more")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ File received: {file_name}\n\n"
        f"Total files: {len(session.files)}\n\n"
        "What would you like to do?",
        reply_markup=reply_markup
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle uploaded photos."""
    user_id = update.effective_user.id
    
    # Initialize session if needed
    if user_id not in user_sessions:
        user_sessions[user_id] = ConversionSession()
        user_sessions[user_id].temp_dir = tempfile.mkdtemp()
    
    session = user_sessions[user_id]
    
    # Get largest photo
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_name = f"image_{len(session.files) + 1}.jpg"
    file_path = os.path.join(session.temp_dir, file_name)
    
    # Download photo
    await update.message.reply_text(f"⬇️ Downloading image...")
    await file.download_to_drive(file_path)
    
    session.files.append(file_path)
    
    # Create inline keyboard
    keyboard = [
        [InlineKeyboardButton("✅ Start Converting", callback_data="start_conversion")],
        [InlineKeyboardButton("➕ Upload More Files", callback_data="upload_more")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"✅ Image received!\n\n"
        f"Total files: {len(session.files)}\n\n"
        "What would you like to do?",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await query.edit_message_text("Session expired. Please upload files again.")
        return
    
    session = user_sessions[user_id]
    data = query.data
    
    if data == "upload_more":
        await query.edit_message_text(
            "📤 Great! Upload more files (images or ZIP files).\n\n"
            "When you're done, I'll ask you to start the conversion."
        )
    
    elif data == "start_conversion":
        # Ask for output format
        keyboard = [
            [InlineKeyboardButton("PNG", callback_data="format_png")],
            [InlineKeyboardButton("JPEG", callback_data="format_jpeg")],
            [InlineKeyboardButton("JPG", callback_data="format_jpg")],
            [InlineKeyboardButton("WEBP", callback_data="format_webp")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎨 Select output format:",
            reply_markup=reply_markup
        )
    
    elif data.startswith("format_"):
        session.output_format = data.replace("format_", "").upper()
        if session.output_format == "JPG":
            session.output_format = "JPEG"  # Pillow uses JPEG
        
        # Ask for quality mode
        keyboard = [
            [InlineKeyboardButton("📊 Presets (Low/Medium/High)", callback_data="quality_presets")],
            [InlineKeyboardButton("🎯 Custom Percentage (1-100%)", callback_data="quality_custom")],
            [InlineKeyboardButton("📐 Resize by Dimensions (pixels)", callback_data="quality_dimensions")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"✅ Format: {data.replace('format_', '').upper()}\n\n"
            "Select quality/compression mode:",
            reply_markup=reply_markup
        )
    
    elif data == "quality_presets":
        session.quality_mode = "preset"
        keyboard = [
            [InlineKeyboardButton("🔴 Low (60%)", callback_data="preset_60")],
            [InlineKeyboardButton("🟡 Medium (80%)", callback_data="preset_80")],
            [InlineKeyboardButton("🟢 High (95%)", callback_data="preset_95")],
            [InlineKeyboardButton("💎 Original (100%)", callback_data="preset_100")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Select quality preset:",
            reply_markup=reply_markup
        )
    
    elif data.startswith("preset_"):
        session.quality_value = int(data.replace("preset_", ""))
        await start_processing(query, user_id)
    
    elif data == "quality_custom":
        session.quality_mode = "custom"
        await query.edit_message_text(
            "Please enter the quality percentage (1-100):\n\n"
            "Example: 75"
        )
    
    elif data == "quality_dimensions":
        session.quality_mode = "dimensions"
        await query.edit_message_text(
            "Please enter dimensions as: width height\n\n"
            "Example: 1920 1080\n"
            "Or just width to maintain aspect ratio: 1920"
        )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (for custom quality/dimensions)."""
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await update.message.reply_text(
            "No active session. Please upload files first using /start"
        )
        return
    
    session = user_sessions[user_id]
    text = update.message.text.strip()
    
    if session.quality_mode == "custom":
        try:
            quality = int(text)
            if 1 <= quality <= 100:
                session.quality_value = quality
                await start_processing(update.message, user_id)
            else:
                await update.message.reply_text(
                    "❌ Invalid quality. Please enter a number between 1 and 100."
                )
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid input. Please enter a number between 1 and 100."
            )
    
    elif session.quality_mode == "dimensions":
        try:
            parts = text.split()
            if len(parts) == 1:
                width = int(parts[0])
                session.dimensions = (width, None)  # Maintain aspect ratio
            elif len(parts) == 2:
                width, height = int(parts[0]), int(parts[1])
                session.dimensions = (width, height)
            else:
                raise ValueError()
            
            await start_processing(update.message, user_id)
        except ValueError:
            await update.message.reply_text(
                "❌ Invalid format. Please enter:\n"
                "• Width only: 1920\n"
                "• Width and height: 1920 1080"
            )

async def start_processing(message_or_query, user_id):
    """Start the image processing."""
    session = user_sessions[user_id]
    
    # Send initial message
    if hasattr(message_or_query, 'edit_message_text'):
        status_message = await message_or_query.edit_message_text(
            "🔄 Starting conversion process...\n"
            f"Files to process: {len(session.files)}"
        )
    else:
        status_message = await message_or_query.reply_text(
            "🔄 Starting conversion process...\n"
            f"Files to process: {len(session.files)}"
        )
    
    try:
        # Process images
        processor = ImageProcessor()
        output_zip = await processor.process_files(
            session.files,
            session.output_format,
            session.quality_value,
            session.dimensions,
            status_callback=lambda msg: update_status(status_message, msg)
        )
        
        # Send result
        await status_message.edit_text("📤 Uploading converted files...")
        
        with open(output_zip, 'rb') as f:
            await message_or_query.get_bot().send_document(
                chat_id=user_id,
                document=f,
                filename=f"converted_images_{session.output_format.lower()}.zip",
                caption=(
                    "✅ *Conversion Complete!*\n\n"
                    f"Format: {session.output_format}\n"
                    f"Quality: {session.quality_value if session.quality_value else 'Custom dimensions'}\n\n"
                    "Upload more files to convert again!"
                ),
                parse_mode='Markdown'
            )
        
        await status_message.delete()
        
        # Cleanup
        session.reset()
        del user_sessions[user_id]
        
    except Exception as e:
        logger.error(f"Error processing files: {e}")
        await status_message.edit_text(
            f"❌ Error during conversion: {str(e)}\n\n"
            "Please try again or use /cancel to reset."
        )

async def update_status(message, text):
    """Update status message."""
    try:
        await message.edit_text(text)
    except Exception as e:
        logger.warning(f"Could not update status: {e}")

def main():
    """Start the bot."""
    # Get token from environment
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Start bot
    logger.info("Bot started successfully!")
    application.run_polling()

if __name__ == '__main__':
    main()
