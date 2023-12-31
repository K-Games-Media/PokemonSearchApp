# Copyright (c) Kayden Cormier, 2023
# Copyright (c) K-Games Media, 2023
# All rights reserved.

import sys
import time
import math
import ebaysdk
import requests
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTextBrowser
from ebaysdk.finding import Connection as Finding
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class PokemonSearchApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

        # Set the window icon
        self.setWindowIcon(QIcon('images/pikachu1.png'))

    def initUI(self):
        self.setWindowTitle('Pokemon Search')
        self.setGeometry(100, 100, 800, 600)

        # Create widgets
        self.search_bar = QLineEdit(self)
        self.search_button = QPushButton('Search', self)
        self.search_bar = QLineEdit(self)
        self.search_button = QPushButton('Search', self)
        # self.result_label = QLabel('Search Results:', self)

        # Connect the returnPressed signal of the search_bar to the search method
        self.search_bar.returnPressed.connect(self.search)

        # Create four columns with labels
        self.column1_label = QLabel('Ebay Sold Items', self)
        self.column2_label = QLabel('Ebay Active Listings', self)
        self.column3_label = QLabel('Hobbiesville', self)
        self.column4_label = QLabel('Face To Face Games', self)
        self.column5_label = QLabel('K-Games&Collectables', self)

        # Create QTextBrowser widgets for each column
        self.column1_browser = QTextBrowser(self)
        self.column2_browser = QTextBrowser(self)
        self.column3_browser = QTextBrowser(self)
        self.column4_browser = QTextBrowser(self)
        self.column5_browser = QTextBrowser(self)

        # Create layouts
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)

        # Create a vertical layout for each column
        column1_layout = QVBoxLayout()
        column2_layout = QVBoxLayout()
        column3_layout = QVBoxLayout()
        column4_layout = QVBoxLayout()
        column5_layout = QVBoxLayout()

        # Add labels and QTextBrowser widgets to the column layouts
        column1_layout.addWidget(self.column1_label)
        column1_layout.addWidget(self.column1_browser)
        column2_layout.addWidget(self.column2_label)
        column2_layout.addWidget(self.column2_browser)
        column3_layout.addWidget(self.column3_label)
        column3_layout.addWidget(self.column3_browser)
        column4_layout.addWidget(self.column4_label)
        column4_layout.addWidget(self.column4_browser)
        column5_layout.addWidget(self.column5_label)
        column5_layout.addWidget(self.column5_browser)

        # Add the column layouts to the main layout
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)
        main_layout.addLayout(column3_layout)
        main_layout.addLayout(column4_layout)
        main_layout.addLayout(column5_layout)

        self.setLayout(main_layout)

        # Use CSS to set the background color and text color
        self.setStyleSheet("""
            background-color: #0F0424;
            color: #FFFFFF;
        """)

        # Set the button color
        self.search_button.setStyleSheet("""
            background-color: #E6013D; 
        """)

        # Add the copyright label to the main layout at the bottom
        self.addCopyrightLabel(main_layout)

        # Connect the search button to the search function
        self.search_button.clicked.connect(self.search)

    def addCopyrightLabel(self, main_layout):
        copyright_label = QLabel('Copyright © K-Games Media, 2023', self)
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("""
            background-color: #0F0424;
            color: #FFFFFF;
            font-size: 10px;
        """)

        # Add the copyright label to the main layout at the bottom
        main_layout.addWidget(
            copyright_label, alignment=Qt.AlignCenter | Qt.AlignBottom)

    def display_ebay_sold_items(self, items):
        if items:
            # Display only the most recent 10 sold items in Column 1
            recent_items = items[:10]
            result_text = "\n".join(
                [f"{item.title} - ${item.sellingStatus.currentPrice.value}" for item in recent_items])
        else:
            result_text = "No sold items found."
        self.column1_browser.setPlainText(result_text)

    def display_ebay_listings(self, listings):
        if listings:
            # Display the top 10 most recent eBay listings in Column 2
            recent_listings = listings[:10]
            result_text = "\n".join(
                [f"{listing.title} - ${listing.sellingStatus.currentPrice.value}" for listing in recent_listings])
        else:
            result_text = "No active eBay listings found."
        self.column2_browser.setPlainText(result_text)

    def search(self):
        query = self.search_bar.text()

        # Call the eBay sold items search function
        sold_items = self.search_ebay_sold_items(query)

        # Call the eBay active listings search function
        active_listings = self.search_ebay_active_listings(query)

        # Display the eBay sold items in Column 1
        self.display_ebay_sold_items(sold_items)

        # Display the eBay active listings in Column 2
        self.display_ebay_listings(active_listings)

        # Call the FaceToFaceGames search function
        facetoface_results = self.search_facetofacegames(query)

        # Display the FaceToFaceGames results in the new column
        self.column4_browser.setPlainText(facetoface_results)

        # Call the Hobbiesville search function
        hobbiesville_results = self.search_hobbiesville(query)

        # Display the Hobbiesville results in the column3_browser
        self.column3_browser.setPlainText(hobbiesville_results)

        # Call the K-Games&Collectables search function
        kgamescollectables_results = self.search_kgamescollectables(query)

        # Display the K-Games&Collectables results in the column5_browser
        self.column5_browser.setPlainText(kgamescollectables_results)

    # def search_ebay_sold_items(self, query):
    #     api = Finding(
    #         appid='KaydenCo-kgamesnc-PRD-91b3fab5b-3aa8915a', config_file=None)

    #     # Define the time frame for the last 24 hours
    #     end_time_to = datetime.now()
    #     end_time_from = end_time_to - timedelta(hours=24)

    #     for retry_attempt in range(3):  # Try up to 3 times
    #         try:
    #             response = api.execute(
    #                 'findCompletedItems', {
    #                     'keywords': query,
    #                     'EndTimeFrom': end_time_from.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    #                     'EndTimeTo': end_time_to.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    #                 })

    #             if response.reply.ack == 'Success':
    #                 # Print out the searchResult to understand its structure
    #                 print(response.reply.searchResult)

    #                 # Check if 'item' attribute exists in searchResult
    #                 if hasattr(response.reply.searchResult, 'item'):
    #                     sold_items = response.reply.searchResult.item
    #                     return sold_items
    #                 else:
    #                     print('No items found in eBay API response.')
    #                     return []
    #             else:
    #                 print('eBay API request failed.')
    #                 return []
    #         except ebaysdk.exception.ConnectionError as e:
    #             print(f'Error: {e}')
    #             retry_delay = math.pow(2, retry_attempt)  # Exponential backoff
    #             print(f'Waiting for {retry_delay} seconds before retrying...')
    #             time.sleep(retry_delay)

    def search_ebay_sold_items(self, query):
        api = Finding(
            appid='KaydenCo-kgamesnc-PRD-91b3fab5b-3aa8915a', config_file=None)

        # Define the time frame for the last 24 hours
        end_time_to = datetime.now()
        end_time_from = end_time_to - timedelta(hours=24)

        # Add a unique timestamp to bypass potential caching
        unique_timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')

        for retry_attempt in range(3):  # Try up to 3 times
            try:
                response = api.execute(
                    'findCompletedItems', {
                        # append the unique timestamp to the query
                        'keywords': query + unique_timestamp,
                        'EndTimeFrom': end_time_from.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'EndTimeTo': end_time_to.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    })

                if response.reply.ack == 'Success':
                    # Print out the searchResult to understand its structure
                    print(response.reply.searchResult)

                    # Check if 'item' attribute exists in searchResult
                    if hasattr(response.reply.searchResult, 'item'):
                        sold_items = response.reply.searchResult.item
                        return sold_items
                    else:
                        print('No items found in eBay API response.')
                        return []
                else:
                    print('eBay API request failed.')
                    return []
            except ebaysdk.exception.ConnectionError as e:
                print(f'Error: {e}')
                retry_delay = math.pow(2, retry_attempt)  # Exponential backoff
                print(f'Waiting for {retry_delay} seconds before retrying...')
                time.sleep(retry_delay)

    def search_ebay_active_listings(self, query):
        api = Finding(
            appid='KaydenCo-kgamesnc-PRD-91b3fab5b-3aa8915a', config_file=None)

        # Define the time frame for the last 24 hours
        end_time_to = datetime.now()
        end_time_from = end_time_to - timedelta(hours=24)

        for retry_attempt in range(3):  # Try up to 3 times
            try:
                response = api.execute(
                    'findItemsAdvanced', {
                        'keywords': query,
                        'EndTimeFrom': end_time_from.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                        'EndTimeTo': end_time_to.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    })

                if response.reply.ack == 'Success':
                    active_listings = response.reply.searchResult.item
                    return active_listings
                else:
                    print('eBay API request failed.')
                    return []
            except ebaysdk.exception.ConnectionError as e:
                print(f'Error: {e}')
                retry_delay = math.pow(2, retry_attempt)  # Exponential backoff
                print(f'Waiting for {retry_delay} seconds before retrying...')
                time.sleep(retry_delay)

                
    def search_facetofacegames(self, query):
        return self.run_js_scrape('facetofacegames', query)

    def search_hobbiesville(self, query):
        return self.run_js_scrape('hobbiesville', query)

    def search_kgamescollectables(self, query):
        return self.run_js_scrape('kgamescollectables', query)

    def run_js_scrape(self, site, query):
        try:
            # Run the Node.js script with subprocess
            result = subprocess.run(['node', 'scrape_sites.js', site, query], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running script: {e}")
            return f"Error scraping {site}: {e}"

    # def search_facetofacegames(self, query):
    #     base_url = "https://facetofacegames.com"
    #     search_url = f"{base_url}/products/search?q={query}"
    #     response = requests.get(search_url)

    #     if response.status_code != 200:
    #         return f"Error {response.status_code}: Unable to fetch data from FaceToFaceGames."

    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     products = soup.find_all('div', class_='product-grid-item')
    #     # Assuming 'item-class' is the correct class for items
    #     items = soup.find_all('div', class_='item-class')

    #     results = []

    #     for product in products:
    #         title = product.find('h4', class_='card-title')
    #         price = product.find('span', class_='price')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     for item in items:
    #         # Update class if different for items
    #         title = item.find('h4', class_='title-class')
    #         # Update class if different for items
    #         price = item.find('span', class_='price-class')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     if not results:
    #         return "No products or items found on FaceToFaceGames for the given query."

    #     return "\n".join(results)

    # def search_hobbiesville(self, query):
    #     base_url = "https://hobbiesville.com"
    #     search_url = f"{base_url}/search?q={query}"
    #     response = requests.get(search_url)

    #     if response.status_code != 200:
    #         return f"Error {response.status_code}: Unable to fetch data from Hobbiesville."

    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     products = soup.find_all('div', class_='product-grid-item')
    #     # Assuming 'item-class' is the correct class for items
    #     items = soup.find_all('div', class_='item-class')

    #     results = []

    #     for product in products:
    #         # Update class if different for products
    #         title = product.find('h4', class_='card-title')
    #         # Update class if different for products
    #         price = product.find('span', class_='price-class')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     for item in items:
    #         # Update class if different for items
    #         title = item.find('h4', class_='title-class')
    #         # Update class if different for items
    #         price = item.find('span', class_='price-class')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     if not results:
    #         return "No products or items found on Hobbiesville for the given query."

    #     return "\n".join(results)

    # def search_kgamescollectables(self, query):
    #     base_url = "https://kgamesncollectables.com"
    #     search_url = f"{base_url}/search?q={query}"
    #     response = requests.get(search_url)

    #     if response.status_code != 200:
    #         return f"Error {response.status_code}: Unable to fetch data from K-Games&Collectables."

    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     products = soup.find_all('div', class_='product-grid-item')
    #     # Assuming 'item-class' is the correct class for items
    #     items = soup.find_all('div', class_='item-class')

    #     results = []

    #     for product in products:
    #         # Update class if different for products
    #         title = product.find('h4', class_='card-title')
    #         # Update class if different for products
    #         price = product.find('span', class_='price-class')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     for item in items:
    #         # Update class if different for items
    #         title = item.find('h4', class_='title-class')
    #         # Update class if different for items
    #         price = item.find('span', class_='price-class')
    #         if title and price:
    #             results.append(f"{title.text.strip()} - {price.text.strip()}")

    #     if not results:
    #         return "No products or items found on K-Games&Collectables for the given query."

    #     return "\n".join(results)


def main():
    app = QApplication(sys.argv)
    window = PokemonSearchApp()

    # Set the custom app icon for the taskbar
    app_icon = QtGui.QIcon('images/pikachu1.png')
    window.setWindowIcon(app_icon)

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
