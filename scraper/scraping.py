# type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import re

# ---------------------------
# Provinces & Initialization
# ---------------------------
"""initalizes attributes
all_data: a list of dictionaries with data for each property
property_links: a list of urls for each property
provinces: a list of all the provinces found in Belgium"""


class ImmoElizaScraping():

    def __init__(self):
        self.provinces = ["antwerp","brabant-wallon","east-flanders","vlaams-brabant","hainaut","liege","limburg","luxembourg","namur","west-flanders"]
        self.all_data = []
        self.property_links = []

        self.options = webdriver.EdgeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_experimental_option("detach", True)

        self.driver = webdriver.Edge(options=self.options)
        self.wait = WebDriverWait(self.driver, 30)


    def scrape_by_provencies(self) -> list:
        """scrapes all the properties from a specified list of provinces, saves and returns a list all_data
        different steps taken in chronological order (with indents):
        1) base url that containts lists of properties of specified provinces
        2) "province" for-loop: cycles through each of specified province
        3)      "page" for-loop: cycles through a specified number of pages
        4)      loading base url into webdriver
        5)      automated cookie acceptance
        6)      collect each link of each looped page url into a set property_links:
                    property for-loop: collecting property links
                    project for-loop: collecting project links
                        propery for-loop: collecting all the propeties associated with a project
        7) "scrape" for-loop: scraping each link from list property_links and appending results to list all_data
        8) returns all_data as list of property dictionaries with datapoints
        """
        # base url that containts lists of properties of specified provinces
        self.base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&provinces={province}&page={page}&noindex=1"
        # cycle through each of specified province
        for province in self.provinces:
            print(f"Scraping {province}")

            # cycle through a specified number of pages (default 51)
            for page in range(1, 2):

                # loading base url into webdriver
                self.driver.get(self.base_url.format(province=province, page=page))

                # automated cookie acceptance
                try:
                    cookie_button = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]"))
                    )
                    cookie_button.click()
                except:
                    pass

                time.sleep(1)

                # initalizing attributes to store links and collect each link of each looped page url into a set property_links
                self.links = self.driver.find_elements(By.XPATH,"//a[contains(@href, '/detail/') or contains(@href, '/projectdetail/')]")
                self.hrefs = [l.get_attribute("href") for l in self.links if l.get_attribute("href")]
                self.detail_links = set([link for link in self.hrefs if "/detail/" in link])
                self.project_links = set([link for link in self.hrefs if "/projectdetail/" in link])

                # collecting property links
                for link in self.detail_links:
                        if link not in self.property_links:
                            self.property_links.append(link)

                # collecting project links
                for project in self.project_links:

                    self.driver.get(project)
                    time.sleep(3)
                    self.listings = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/en/detail/')]")
                    self.hrefs = [p.get_attribute("href") for p in self.listings if p.get_attribute("href")]

                    # collecting all the propeties associated with a project
                    for href in self.hrefs:
                        if href not in self.property_links:
                            self.property_links.append(href)
                print(f" Collected {len(self.property_links)} unique property links in total")

            # scraping each link from set property_links and adding the result to list all_data
            for link in self.property_links:
                data = self.scrape_property(link)
                self.all_data.append(data)
                print(f"Scraped property from {province}: {link}:")
                print(f"done: {round(len(self.all_data)/len(self.property_links)*100)} %")

        self.driver.close()

        # returns all_data as list of property dictionaries with datapoints
        return self.all_data

    def scrape_property(self, property_url) -> dict:
        """extracts and stores 17 different datapoints in a dictionary data"""
        data = {}

        self.driver.get(property_url)
        time.sleep(2)  # Give the page a moment to load

        try:
            data["property_ID"] = self.driver.find_element(By.XPATH, "//span[contains(@class, 'vlancode')]").text.strip()
        except:
            data["property_ID"] = None

        try:
            data["locality_name"] = self.driver.find_element(
                By.XPATH, "//div[contains(@class,'detail__header_address')]//span[not(contains(@class,'city-line'))]"
            ).text.strip()
        except:
            data["locality_name"] = None

        try:
            data["postal_code"] = int(
                self.driver.find_element(
                    By.XPATH, "//div[contains(@class,'detail__header_address')]//span[(contains(@class,'city-line'))]"
                ).text.split()[0].strip()
            )
        except:
            data["postal_code"] = None

        try:
            data["type"] = self.driver.find_element(By.XPATH, "//meta[@name='keywords']").get_attribute("content").split()[0].strip(",")
        except:
            data["type"] = None

        try:
            data["subtype"] = self.driver.find_element(
                By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[1]/div[1]/div/h1/span"
            ).text.split(" for sale")[0].strip()
        except:
            data["subtype"] = None

        try:
            data["price (€)"] = int(
                self.driver.find_element(By.XPATH, "//span[contains(@class, 'detail__header_price_data')]")
                .text.split("from")[-1].replace("€", "")
                .replace(" ", "")
                .replace("\u202f", "").strip()
            )

        except:
            data["price (€)"] = None

        try:
            data["number_of_bedrooms"] = int(
                self.driver.find_element(
                    By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Number of bedrooms']/following-sibling::p"
                ).text.strip()
            )
        except:
            data["number_of_bedrooms"] = None

        try:
            data["living_area (m²)"] = int(
                self.driver.find_element(
                    By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Livable surface']/following-sibling::p"
                ).text.split()[0].strip()
            )
        except:
            data["living_area (m²)"] = None

        try:
            data["equiped_kitchen (yes:1, no:0)"] = 0 if self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Kitchen equipment']/following-sibling::p"
            ).text.strip() in ["", "No"] else 1
        except:
            data["equiped_kitchen (yes:1, no:0)"] = 0

        try:
            data["furnished (yes:1, no:0)"] = 1 if "Yes" == self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Furnished']/following-sibling::p"
            ).text.strip() else 0
        except:
            data["furnished (yes:1, no:0)"] = 0

        try:
            data["open_fire (yes:1, no:0)"] = 1 if "Yes" == self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Fireplace']/following-sibling::p"
            ).text.strip() else 0
        except:
            data["open_fire (yes:1, no:0)"] = 0

        try:
            data["terrace (yes:1, no:0)"] = 1 if "Yes" == self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Terrace']/following-sibling::p"
            ).text.strip() else 0
        except:
            data["terrace (yes:1, no:0)"] = 0

        try:
            data["terrace_area (m²)"] = int(
                self.driver.find_element(
                    By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Surface terrace']/following-sibling::p"
                ).text.split()[0].strip()
            )
        except:
            data["terrace_area (m²)"] = None

        try:
            data["garden (yes:1, no:0)"] = 1 if "Yes" == self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Garden']/following-sibling::p"
            ).text.strip() else 0
        except:
            data["garden (yes:1, no:0)"] = 0

        try:
            data["number_facades"] = int(
                self.driver.find_element(
                    By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Number of facades']/following-sibling::p"
                ).text.strip()
            )
        except:
            data["number_facades"] = None

        try:
            data["swimming_pool (yes:1, no:0)"] = 1 if "Yes" == self.driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Swimming pool']/following-sibling::p"
            ).text.strip() else 0
        except:
            data["swimming_pool (yes:1, no:0)"] = 0

        try:
            data["state_of_building"] = self.driver.find_element(
                By.XPATH, "//div[contains(@class,'general-info-wrapper')]//h4[text()='State of the property']/following-sibling::p"
            ).text.strip()
        except:
            data["state_of_building"] = None

        return data

    def remove_duplicates(self, all_data):
        """deduplicates all_data and stores/returns the result in unique_data"""
        self.seen = set()
        self.unique_data = []
        for item in self.all_data:
            self.locality = item["locality_name"]
            self.postal = item["postal_code"]
            self.price = item["price (€)"]
            self.type = item["type"]
            self.subtype = item["subtype"]
            self.bedrooms = item["number_of_bedrooms"]
            self.living = item["living_area (m²)"]
            self.kitchen = item["equiped_kitchen (yes:1, no:0)"]
            self.furnished = item["furnished (yes:1, no:0)"]
            self.fire = item["open_fire (yes:1, no:0)"]
            self.terrace = item["terrace (yes:1, no:0)"]
            self.terrace_area = item["terrace_area (m²)"]
            self.garden = item["garden (yes:1, no:0)"]
            self.facades = item["number_facades"]
            self.pool = item["swimming_pool (yes:1, no:0)"]
            self.state = item["state_of_building"]
            # only continue if locality_name is not empty or None
            combo = (self.locality, self.postal, self.price, self.type, self.subtype, self.bedrooms, self.living, self.kitchen, self.furnished, self.fire, self.terrace, self.terrace_area, self.garden, self.facades, self.pool, self.state)
            if combo not in self.seen:
                self.seen.add(combo)
                self.unique_data.append(item)
        return self.unique_data

    # -------------------------------
    # Save to CSV
    # -------------------------------
    def create_dataframe(self):
        "creates a pandas dataframe for later analysis"
        self.df = pd.DataFrame(self.unique_data)
        return self.df

    def save_to_csv(self):
        "save unique_data to a csv file"
        self.df = self.create_dataframe()
        self.df.to_csv('scraped_data_properties.csv', index=False)
        print(f"Saved {len(self.unique_data)} unique records to liege_tim_1_51.csv")
    