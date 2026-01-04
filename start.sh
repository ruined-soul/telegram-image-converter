#!/bin/bash

# Quick Start Script for Local Testing
echo "🚀 Telegram Image Converter Bot - Quick Start"
echo "=============================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "✅ .env file created!"
    echo ""
    echo "📝 IMPORTANT: Edit .env file and add your Telegram Bot Token"
    echo ""
    echo "To get your token:"
    echo "1. Open Telegram and search for @BotFather"
    echo "2. Send /newbot and follow instructions"
    echo "3. Copy the token"
    echo "4. Edit .env file and paste the token"
    echo ""
    echo "Run this script again after updating .env"
    exit 1
fi

# Check if token is set
source .env
if [ "$TELEGRAM_BOT_TOKEN" = "your_bot_token_here" ] || [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set in .env file!"
    echo ""
    echo "Please edit .env file and add your bot token:"
    echo "TELEGRAM_BOT_TOKEN=your_actual_token_here"
    echo ""
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import telegram" 2>/dev/null; then
    echo "⚠️  Dependencies not installed"
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
    echo ""
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed successfully"
    else
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🤖 Starting bot..."
echo "Press Ctrl+C to stop"
echo ""
echo "=============================================="
echo ""

# Run the bot
python3 bot.py
