# 🎨 Professional Telegram Image Converter Bot

A powerful Telegram bot for converting and compressing images with professional quality control. Upload ZIP files or individual images, choose your output format and quality settings, and get perfectly processed images back!

## ✨ Features

- 📤 **Multiple Upload Methods**: Upload ZIP files or individual images
- 🔄 **Batch Processing**: Upload multiple ZIP files and process them all at once
- 🎨 **Format Support**: Convert to PNG, JPEG, JPG, or WEBP
- 🎯 **Quality Control**:
  - Presets: Low (60%), Medium (80%), High (95%), Original (100%)
  - Custom percentage (1-100%)
  - Resize by pixel dimensions
- 📊 **Progress Updates**: Real-time status updates during conversion
- 📁 **Structure Preservation**: Maintains original file names and folder structure
- ⚡ **Professional Grade**: Optimized compression algorithms

## 🚀 Quick Start

### Prerequisites

1. **Get Telegram Bot Token**:
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` and follow instructions
   - Copy your bot token

### Local Testing

1. **Clone/Download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_actual_token_here
   ```

4. **Run the bot**:
   ```bash
   python bot.py
   ```

5. **Test it**: Open Telegram, find your bot, and send `/start`

## 🌐 Deploy to Koyeb (Free Tier)

### Method 1: GitHub Deployment (Recommended)

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your_repo_url
   git push -u origin main
   ```

2. **Deploy on Koyeb**:
   - Go to [Koyeb Dashboard](https://app.koyeb.com/)
   - Click **Create App**
   - Select **GitHub** as source
   - Choose your repository
   - Configure:
     - **Build Command**: Leave empty (no build needed)
     - **Run Command**: `python bot.py`
     - **Instance Type**: Free (Eco)
   - Add **Environment Variables**:
     - `TELEGRAM_BOT_TOKEN`: Your bot token
   - Click **Deploy**

3. **Wait for deployment**: Your bot will be live in 1-2 minutes!

### Method 2: Docker Deployment

1. **Create Dockerfile**:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["python", "bot.py"]
   ```

2. **Deploy on Koyeb**:
   - Choose **Docker** as source
   - Follow similar steps as GitHub method

## 📖 How to Use

1. **Start the bot**: Send `/start` to your bot in Telegram

2. **Upload files**:
   - Send image files directly (PNG, JPG, WEBP, etc.)
   - Or send ZIP files containing images
   - Upload multiple files if needed

3. **Choose format**: Select output format (PNG/JPEG/JPG/WEBP)

4. **Select quality**:
   - **Presets**: Quick options (Low/Medium/High/Original)
   - **Custom %**: Enter exact percentage (e.g., 75)
   - **Dimensions**: Resize by pixels (e.g., "1920 1080" or just "1920")

5. **Get results**: Receive converted images in a ZIP file!

## 🎯 Use Cases

- **Web Optimization**: Convert images to WEBP for faster loading
- **Batch Processing**: Process entire photo collections at once
- **Quality Control**: Fine-tune compression for perfect balance
- **Format Conversion**: Convert between image formats easily
- **Resize Images**: Bulk resize for social media or web use

## 🛠️ Commands

- `/start` - Start the bot and see welcome message
- `/help` - Display help information
- `/cancel` - Cancel current session and start over

## 📊 Technical Details

- **Language**: Python 3.11
- **Framework**: python-telegram-bot 20.7
- **Image Processing**: Pillow (PIL)
- **Deployment**: Optimized for Koyeb free tier
- **Mode**: Polling (works on free tier)

## 🔧 Configuration

### Environment Variables

- `TELEGRAM_BOT_TOKEN` (required): Your bot token from BotFather
- `PORT` (optional): Port for webhook mode (default: 8080)
- `WEBHOOK_URL` (optional): Webhook URL for production deployment

### Supported Input Formats

- PNG, JPG, JPEG, WEBP, GIF, BMP, TIFF

### Supported Output Formats

- PNG, JPEG, JPG, WEBP

## 🐛 Troubleshooting

### Bot not responding?

1. Check if bot token is correct in `.env`
2. Ensure dependencies are installed: `pip install -r requirements.txt`
3. Check logs for errors

### Deployment issues on Koyeb?

1. Verify `TELEGRAM_BOT_TOKEN` environment variable is set
2. Check **Logs** tab in Koyeb dashboard
3. Ensure `Procfile` and `runtime.txt` are present
4. Make sure instance type is set to **Free (Eco)**

### Images not converting?

1. Check file format is supported
2. Ensure images are not corrupted
3. Try with smaller file sizes first

## 📝 Notes

- **Free Tier Limits**: Koyeb free tier has resource limits. The bot will sleep after inactivity and wake up when needed.
- **File Size**: Telegram has a 50MB file limit for bots
- **Processing Time**: Large batches may take time depending on file sizes
- **Temporary Files**: All temporary files are cleaned up automatically

## 🔐 Security

- Never commit your `.env` file with real tokens
- Keep your bot token secret
- Use environment variables for sensitive data

## 📄 License

Free to use for personal and commercial projects.

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review logs in Koyeb dashboard
3. Ensure all dependencies are correctly installed

## 🎉 Enjoy!

Your professional image converter bot is ready to use! Upload files and start converting! 🚀

---

**Made with ❤️ for image processing enthusiasts**
