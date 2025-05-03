from bot.Kansas_bot import KansasBot


if __name__ == "__main__":
    business_type = "Trucking"
    ks_bot = KansasBot(business_name=business_type)

    # n8n webhook url
    KansasBot.WEBHOOK_URL = "ENTER_YOUR_WEBHOOK_URL_HERE"

    ks_bot.scrape_data()
    ks_bot.save_to_json()
    ks_bot.send_json_to_webhook()

