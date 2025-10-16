# RSI Futures Radar
A real-time RSI (Relative Strength Index) monitoring bot for Bybit futures markets that sends Telegram alerts for overbought and oversold conditions.


## 📊 Overview

This Python script continuously monitors Bybit linear futures markets (15-minute timeframe) and sends automated Telegram notifications when symbols reach extreme RSI levels:
- **🔴 Overbought Alert**: RSI > 70 (Potential short opportunities)
- **🟢 Oversold Alert**: RSI < 30 (Potential long opportunities)

## ✨ Features

- **Real-time Monitoring**: Scans all available USDT linear futures pairs on Bybit
- **Smart Scanning**: Optimized to run at the beginning of each 15-minute candle
- **Randomized Processing**: Shuffles symbol processing order each run for fair distribution
- **Duplicate Prevention**: Avoids sending repeated alerts for the same condition
- **Delisting Detection**: Automatically filters out soon-to-be-delisted symbols
- **Robust Error Handling**: Retry mechanisms and comprehensive error management
- **Rate Limit Aware**: Respects API limits with intelligent delays

## 🛠️ Technical Details

### Indicators Used
- **RSI Period**: 14
- **Timeframe**: 15 minutes
- **Data Points**: 50 candles for accurate RSI calculation

### Technologies
- `pybit` - Bybit API integration
- `python-telegram-bot` - Telegram notifications
- `TA-Lib` - Technical analysis (RSI calculation)
- `pandas` - Data manipulation
- `numpy` - Numerical computations

## 📋 Requirements

```bash
pip install pybit python-telegram-bot pandas numpy talib
```

## ⚙️ Configuration
Telegram Bot Setup:

1. Create a bot via @BotFather

- Get your BOT_TOKEN

- Set your CHAT_ID (group or personal)

2. Bybit API:

- No API keys required for public market data

- Uses Bybit's public endpoints

3. Script Configuration:

- Update BOT_TOKEN and CHAT_ID in the script

- Adjust scanning intervals if needed

