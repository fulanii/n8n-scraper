"""Selenium imports"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

"""Other imports"""
import requests
import json
import os

class KansasBot:
    """A bot to scrape data from the Kansas Secretary of State website"""

    WEBHOOK_URL = "ENTER_YOUR_WEBHOOK_URL_HERE"
    BUSINESS_SEARCH_URL = "https://www.sos.ks.gov/eforms/BusinessEntity/Search.aspx"

    def __init__(self, business_name: str, webhook_url=WEBHOOK_URL):
        self.business_name = business_name
        self.data = {}
        self.file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{self.business_name}.json")

    def driver(self, is_detached: bool = True) -> webdriver.Chrome:
        """Set up the Selenium WebDriver."""
        options = Options()
        # options.add_argument("--headless")
        # options.add_experimental_option("detach", is_detached)
        driver = webdriver.Chrome(options=options)

        return driver

    def scrape_data(self):
        """Get data from the Kansas Secretary of State website"""
        driver = self.driver()

        # open the business search page
        driver.get(self.BUSINESS_SEARCH_URL)

        # find the search input field and enter the business name
        input_field = driver.find_element(By.ID, "MainContent_txtSearchEntityName")

        # wait 3sec
        driver.implicitly_wait(3)

        # enter the business name
        input_field.send_keys(self.business_name)

        # find search button and click it
        search_button = driver.find_element(By.ID, "MainContent_btnSearchEntity")
        search_button.click()

        # wait 3sec
        driver.implicitly_wait(3)

        # table data
        table = driver.find_element(By.ID, "MainContent_gvSearchResults")
        rows = table.find_elements(By.TAG_NAME, "tr")

        # get table headers
        headers = []
        for th in rows[0].find_elements(By.TAG_NAME, "th"):
            header_text = th.text.strip()
            if header_text != "":
                headers.append(header_text)

        # table data
        list_data = []
        for tr in rows[1:26]:
            td = tr.find_elements(By.TAG_NAME, "td")
            row_data = {}
            for i, th in enumerate(headers):
                row_data[th] = td[i + 1].text.strip()
            list_data.append(row_data)

        self.data = {
            "business_name_loccation": f"{self.business_name}_kansas",
            "data": list_data
        }

    def save_to_json(self):
        """Save data to a JSON file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print(f"Data saved to {self.file_path}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def send_json_to_webhook(self):
        """Send JSON data from a file to a Make.com webhook."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            response = requests.post(self.WEBHOOK_URL, json=data)
            
            if response.status_code == 200:
                print("Data sent successfully to the webhook.")
            else:
                print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
        
        except Exception as e:
            print(f"Error sending data: {e}")