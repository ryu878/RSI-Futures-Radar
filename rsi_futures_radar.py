import telebot
import pandas as pd
import numpy as np
import time
import requests
import re
from pybit.unified_trading import WebSocket, HTTP
import talib
import pandas as pd
from datetime import datetime
import random



NAME = "rsi_futures_radar"
VER = '16102025'

# Bot configuration
BOT_TOKEN = ""
CHAT_ID = -100 # Replace with your chat ID

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)
session = HTTP(testnet=False)

# Global variables
symbols_list = []
sent_alerts = set()  # Track already sent alerts to avoid duplicates


def safe_api_call(func, *args, retries=3, delay=5, **kwargs):
    """Retry wrapper for Bybit API calls."""
    for attempt in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"⚠️ API call failed (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("❌ Giving up after retries.")
                return None

def get_symbols_list():
    """Fetch all available symbols from Bybit."""
    global symbols_list
    
    try:
        # Step 1: Check delistings
        news = safe_api_call(session.get_announcement, category="listing", locale='en-US', limit=500)
        skip_set = set()
        
        if news and "result" in news:
            df = pd.DataFrame(news['result']['list'])
            filtered_df = df[df['title'].str.contains('Delisting', case=False, na=False)]
            usdt_words = filtered_df['title'].str.findall(r'\w*USDT\w*', flags=re.IGNORECASE)
            usdt_words_list = [word for sublist in usdt_words for word in sublist]
            delisted_usdt = [word for word in usdt_words_list if len(word) >= 5]
            skip_set = {c.upper() for c in delisted_usdt}
            print(f'Will be Delisted Soon: {delisted_usdt}')

        # Step 2: Fetch all linear futures instruments
        all_data, cursor = [], None
        while True:
            params = {'category': 'linear', 'limit': 1000}
            if cursor:
                params['cursor'] = cursor
                
            get_data = safe_api_call(session.get_instruments_info, **params)
            if not get_data or "result" not in get_data:
                break
                
            response_data = get_data['result']['list']
            all_data.extend(response_data)
            cursor = get_data['result'].get('nextPageCursor')
            if not cursor:
                break

        df_instr = pd.DataFrame(all_data)
        if 'symbol' in df_instr.columns:
            df_instr = df_instr.set_index("symbol")

        # Filter symbols
        symbols_list = [
            s for s in df_instr.index
            if (
                s.upper() not in skip_set
                and "-" not in s
                and "PERP" not in s.upper()
                and s.endswith('USDT')
            )
        ]

        print(f"Total tradable symbols: {len(symbols_list)}")
        return symbols_list

    except Exception as e:
        print(f"💥 Error fetching instruments: {e}")
        return []


def shuffle_symbols_chunks(symbols_list, chunk_size=50):
    """Shuffle symbols and split into chunks for better distribution"""
    shuffled = symbols_list.copy()
    random.shuffle(shuffled)
    
    # Split into chunks to avoid overwhelming the API
    chunks = [shuffled[i:i + chunk_size] for i in range(0, len(shuffled), chunk_size)]
    return chunks


def send_telegram_alert(symbol, rsi_value, condition):
    """Send alert to Telegram."""
    try:
        if condition == "OVERBOUGHT":
            message = f"🔴 {symbol} *OVERBOUGHT ALERT* 🔴\n\n" \
                     f"*Symbol:* {symbol}\n" \
                     f"*RSI:* {rsi_value:.2f}\n" \
                     f"*Condition:* RSI > 70\n" \
                     f"*TimeFrame:* 15 min\n\n" \
                     f"Consider potential ⬇️ SHORT ⬇️ opportunities"
        else:  # OVERSOLD
            message = f"🟢 {symbol} *OVERSOLD ALERT* 🟢\n\n" \
                     f"*Symbol:* {symbol}\n" \
                     f"*RSI:* {rsi_value:.2f}\n" \
                     f"*Condition:* RSI < 30\n" \
                     f"*TimeFrame:* 15 min\n\n" \
                     f"Consider potential ⬆️ LONG ⬆️ opportunities"
        
        bot.send_message(CHAT_ID, message, parse_mode='Markdown')
        print(f"✅ Telegram alert sent for {symbol} - RSI: {rsi_value:.2f} ({condition})")
        
        # Add to sent alerts to avoid duplicates
        alert_key = f"{symbol}_{condition}"
        sent_alerts.add(alert_key)
        
    except Exception as e:
        print(f"❌ Failed to send Telegram alert for {symbol}: {e}")


def should_scan_now():
    """Check if we're at the beginning of a new 15m candle"""
    now = datetime.now()
    current_minute = now.minute
    
    # Scan during first 2 minutes of each 15m candle (0, 15, 30, 45 minutes)
    return current_minute % 15 in [0, 1]


def check_rsi_conditions():
    """Check RSI conditions for all symbols and send alerts."""
    print(f"🔍 Scanning {len(symbols_list)} symbols for RSI conditions...")
    
    overbought_count = 0
    oversold_count = 0
    
    for symbol in symbols_list:
        try:
            # Fetch kline data
            data = safe_api_call(session.get_kline, category='linear', symbol=symbol, interval=15, limit=50)
            time.sleep(0.05)  # Reduced sleep time to avoid rate limiting
            
            if data and "result" in data and data["result"]["list"]:
                # Extract close prices
                kline_data = data["result"]["list"]
                close_prices = [float(candle[4]) for candle in kline_data]
                
                # Reverse the list to have oldest first
                close_prices.reverse()
                
                # Calculate RSI using talib
                close_array = np.array(close_prices, dtype=float)
                rsi_values = talib.RSI(close_array, timeperiod=14)
                
                # Get the latest RSI value
                latest_rsi = rsi_values[-1] if not np.isnan(rsi_values[-1]) else None
                
                if latest_rsi is not None:
                    # Check RSI conditions
                    if latest_rsi > 70:
                        overbought_count += 1
                        alert_key = f"{symbol}_OVERBOUGHT"
                        if alert_key not in sent_alerts:
                            send_telegram_alert(symbol, latest_rsi, "OVERBOUGHT")
                        else:
                            print(f"⚠️ Overbought alert already sent for {symbol} - RSI: {latest_rsi:.2f}")
                    
                    elif latest_rsi < 30:
                        oversold_count += 1
                        alert_key = f"{symbol}_OVERSOLD"
                        if alert_key not in sent_alerts:
                            send_telegram_alert(symbol, latest_rsi, "OVERSOLD")
                        else:
                            print(f"⚠️ Oversold alert already sent for {symbol} - RSI: {latest_rsi:.2f}")
                    
                    else:
                        print(f"✅ {symbol}: RSI = {latest_rsi:.2f} (Normal)")
                        
                else:
                    print(f"⚠️ {symbol}: Not enough data for RSI calculation")
                    
            else:
                print(f"❌ Failed to fetch data for {symbol}")
                
        except Exception as e:
            print(f"💥 Error processing {symbol}: {e}")
    
    print(f"\n📊 Scan completed:")
    print(f"   Overbought symbols (RSI > 70): {overbought_count}")
    print(f"   Oversold symbols (RSI < 30): {oversold_count}")
    print(f"   Total alerts sent: {len(sent_alerts)}")


# Main execution
if __name__ == "__main__":
    # Get symbols list
    get_symbols_list()
    print(f"Starting RSI monitoring for {len(symbols_list)} symbols...")
    
    # Run continuously
    while True:
        try:
            if should_scan_now():
                print(f"\n{'='*60}")
                print(f"🔄 Starting new scan at {time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*60}")

                # Shuffle symbols for this run
                shuffled_symbols = symbols_list.copy()
                random.shuffle(shuffled_symbols)

                print(f"🔀 Symbols randomized for this scan run")

                # Temporarily use shuffled symbols
                original_symbols = symbols_list.copy()
                symbols_list.clear()
                symbols_list.extend(shuffled_symbols)
                
                check_rsi_conditions()

                # Restore original symbols list
                symbols_list.clear()
                symbols_list.extend(original_symbols)

                print(f"\n💤 Waiting 60 seconds before checking if it's scan time...")
            else:
                current_minute = datetime.now().minute
                minutes_until_scan = 15 - (current_minute % 15)
                print(f"⏰ Next scan in {minutes_until_scan} minutes...")
                
            time.sleep(60)  # Check every minute if we should scan
            
        except KeyboardInterrupt:
            print("\n🛑 Script stopped by user")
            break
