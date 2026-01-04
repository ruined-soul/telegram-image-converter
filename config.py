import os
from pathlib import Path

# Bot configuration
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

# Webhook configuration (for deployment)
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', '')
PORT = int(os.environ.get('PORT', 8080))

# File size limits (in bytes)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Supported formats
SUPPORTED_INPUT_FORMATS = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif']
SUPPORTED_OUTPUT_FORMATS = ['PNG', 'JPEG', 'JPG', 'WEBP']

# Quality presets
QUALITY_PRESETS = {
    'low': 60,
    'medium': 80,
    'high': 95,
    'original': 100
}

# Temp directory
TEMP_DIR = Path('/tmp/telegram_bot')
TEMP_DIR.mkdir(exist_ok=True)
