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

## 🚀 Usage

```
python rsi_futures_radar.py
```

## 📈 Alert Examples

### Overbought Alert

```
🔴 BTCUSDT OVERBOUGHT ALERT 🔴

Symbol: BTCUSDT
RSI: 75.42
Condition: RSI > 70
TimeFrame: 15 min

Consider potential ⬇️ SHORT ⬇️ opportunities
```

### Oversold Alert

```
🟢 ETHUSDT OVERSOLD ALERT 🟢

Symbol: ETHUSDT
RSI: 25.18
Condition: RSI < 30
TimeFrame: 15 min

Consider potential ⬆️ LONG ⬆️ opportunities
```

## 🔧 Customization
Adjust RSI thresholds in check_rsi_conditions() function

Modify timeframe by changing interval=15 parameter

Change scanning frequency in should_scan_now() function

Adjust symbol chunk size in shuffle_symbols_chunks()


## 📄 License
MIT License - Feel free to modify and distribute.


## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check issues page.


## Disclaimer
This project is for informational and educational purposes only. You should not use this information or any other material as legal, tax, investment, financial or other advice. Nothing contained here is a recommendation, endorsement or offer by me to buy or sell any securities or other financial instruments. If you intend to use real money, use it at your own risk. Under no circumstances will I be responsible or liable for any claims, damages, losses, expenses, costs or liabilities of any kind, including but not limited to direct or indirect damages for loss of profits.


## Contacts
I develop trading bots of any complexity, dashboards and indicators for crypto exchanges, forex and stocks.
To contact me please pm:

Telegram: https://t.me/ryu8777

Discord: https://discord.gg/zSw58e9Uvf


## Crypto Exchanges

😎 Register on BingX and get a 20% discount on fees: https://bingx.com/invite/HAJ8YQQAG/

👍 MEXC: https://promote.mexc.com/r/f3dtDLZK

🐀 Join Bybit: https://www.bybit.com/invite?ref=P11NJW


## VPS for bots and scripts
I prefer using DigitalOcean.
  
[![DigitalOcean Referral Badge](https://web-platforms.sfo2.digitaloceanspaces.com/WWW/Badge%202.svg)](https://www.digitalocean.com/?refcode=3d7f6e57bc04&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
  
To get $200 in credit over 60 days use my ref link: https://m.do.co/c/3d7f6e57bc04
