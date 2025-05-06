import schedule
import time
from bot.Kansas_bot import KansasBot

def run_scraper():
    business_type = "Housing"
    ks_bot = KansasBot(business_name=business_type)
    KansasBot.WEBHOOK_URL = "ENTER_YOUR_WEBHOOK_URL_HERE"  # Replace with your actual webhook URL
    ks_bot.scrape_data()
    ks_bot.save_to_json()
    ks_bot.send_json_to_webhook()

schedule.every().day.at("09:00").do(run_scraper)  # Every day at 9:00 AM

while True:
    schedule.run_pending()
    time.sleep(1)
