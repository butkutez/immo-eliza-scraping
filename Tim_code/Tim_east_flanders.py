# type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas as pd

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 30)

# ---------------------------
# Provinces & property types
# ---------------------------

def scrape_by_provencies():
    all_data = []
    property_links = []

    # DELETE PROVINCES IN THE LIST THAT ARE NOT NEAR YOUR NAME BELOW
    # zivile: antwerp, limburg
    # faranges: east-flanders, flemish-brabant, brabant-wallon
    # aleksei : west-flanders, Hainaut
    # tim: namur, luxemburg, liege


    provinces = ["vlaams-brabant"]

    base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&provinces={province}&page={page}&noindex=1"
    for province in provinces:
        print(f"Scraping {province}")


        for page in range(1, 51):
            # Accept cookies once
            driver.get(base_url.format(province=province, page=page))
            try:
                cookie_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]"))
                )
                cookie_button.click()
            except:
                pass

            url = base_url.format(province=province, page=page)
            driver.get(url)
            time.sleep(1)

            # call here the function of scrape_property
            links = driver.find_elements(By.XPATH,"//a[contains(@href, '/detail/') or contains(@href, '/projectdetail/')]")
            hrefs = [l.get_attribute("href") for l in links if l.get_attribute("href")]

            detail_links = set([link for link in hrefs if "/detail/" in link])
            project_links = set([link for link in hrefs if "/projectdetail/" in link])
            # Add all detail links directly
            for link in detail_links:
                    if link not in property_links:
                        property_links.append(link)
            # Visit each unique project only once
            for project in project_links:
                driver.get(project)
                time.sleep(3)
                listings = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/detail/')]")
                hrefs = [p.get_attribute("href") for p in listings if p.get_attribute("href")]
                for href in hrefs:
                    if href not in property_links:
                        property_links.append(href)
            print(f" Collected {len(property_links)} unique property links in total.")

        for link in property_links:
            data = scrape_property(link)
            all_data.append(data)
            print(f"Scraped property from {province}: {link}")
        # driver.close()


    return all_data

def scrape_property(property_url):
    data = {}

    driver.get(property_url)
    time.sleep(2)  # Give the page a moment to load

    try:
        data["property_ID"] = driver.find_element(By.XPATH, "//span[contains(@class, 'vlancode')]").text.strip()
    except:
        data["property_ID"] = None

    try:
        data["locality_name"] = driver.find_element(
            By.XPATH, "//div[contains(@class,'detail__header_address')]//span[not(contains(@class,'city-line'))]"
        ).text.strip()
    except:
        data["locality_name"] = None

    try:
        data["postal_code"] = int(
            driver.find_element(
                By.XPATH, "//div[contains(@class,'detail__header_address')]//span[(contains(@class,'city-line'))]"
            ).text.split()[0].strip()
        )
    except:
        data["postal_code"] = None

    try:
        data["type"] = driver.find_element(By.XPATH, "//meta[@name='keywords']").get_attribute("content").split()[0].strip(",")
    except:
        data["type"] = None

    try:
        data["subtype"] = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[1]/div[1]/div/h1/span"
        ).text.split(" for sale")[0].strip()
    except:
        data["subtype"] = None

    try:
        data["price (€)"] = int(
            driver.find_element(By.XPATH, "//span[contains(@class, 'detail__header_price_data')]")
            .text.split("from")[-1].replace("€", "")
            .replace(" ", "")
            .replace("\u202f", "").strip()
        )

    except:
        data["price (€)"] = None

    try:
        data["number_of_bedrooms"] = int(
            driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Number of bedrooms']/following-sibling::p"
            ).text.strip()
        )
    except:
        data["number_of_bedrooms"] = None

    try:
        data["living_area (m²)"] = int(
            driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Livable surface']/following-sibling::p"
            ).text.split()[0].strip()
        )
    except:
        data["living_area (m²)"] = None

    try:
        data["equiped_kitchen (yes:1, no:0)"] = 0 if driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Kitchen equipment']/following-sibling::p"
        ).text.strip() in ["", "No"] else 1
    except:
        data["equiped_kitchen (yes:1, no:0)"] = 0

    try:
        data["furnished (yes:1, no:0)"] = 1 if "Yes" == driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Furnished']/following-sibling::p"
        ).text.strip() else 0
    except:
        data["furnished (yes:1, no:0)"] = 0

    try:
        data["open_fire (yes:1, no:0)"] = 1 if "Yes" == driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Fireplace']/following-sibling::p"
        ).text.strip() else 0
    except:
        data["open_fire (yes:1, no:0)"] = 0

    try:
        data["terrace (yes:1, no:0)"] = 1 if "Yes" == driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Terrace']/following-sibling::p"
        ).text.strip() else 0
    except:
        data["terrace (yes:1, no:0)"] = 0

    try:
        data["terrace_area (m²)"] = int(
            driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Surface terrace']/following-sibling::p"
            ).text.split()[0].strip()
        )
    except:
        data["terrace_area (m²)"] = None

    try:
        data["garden (yes:1, no:0)"] = 1 if "Yes" == driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Garden']/following-sibling::p"
        ).text.strip() else 0
    except:
        data["garden (yes:1, no:0)"] = 0

    try:
        data["number_facades"] = int(
            driver.find_element(
                By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Number of facades']/following-sibling::p"
            ).text.strip()
        )
    except:
        data["number_facades"] = None

    try:
        data["swimming_pool (yes:1, no:0)"] = 1 if "Yes" == driver.find_element(
            By.XPATH, "//div[contains(@class, 'data-row-wrapper')]//h4[text()='Swimming pool']/following-sibling::p"
        ).text.strip() else 0
    except:
        data["swimming_pool (yes:1, no:0)"] = 0

    try:
        data["state_of_building"] = driver.find_element(
            By.XPATH, "//div[contains(@class,'general-info-wrapper')]//h4[text()='State of the property']/following-sibling::p"
        ).text.strip()
    except:
        data["state_of_building"] = None

    return data

def remove_duplicates(all_data):
    seen = set()
    unique_data = []
    for item in all_data:
        locality = item["locality_name"]
        postal = item["postal_code"]
        price = item["price (€)"]
        type = item["type"]
        subtype = item["subtype"]
        bedrooms = item["number_of_bedrooms"]
        living = item["living_area (m²)"]
        kitchen = item["equiped_kitchen (yes:1, no:0)"]
        furnished = item["furnished (yes:1, no:0)"]
        fire = item["open_fire (yes:1, no:0)"]
        terrace = item["terrace (yes:1, no:0)"]
        terrace_area = item["terrace_area (m²)"]
        garden = item["garden (yes:1, no:0)"]
        facades = item["number_facades"]
        pool = item["swimming_pool (yes:1, no:0)"]
        state = item["state_of_building"]
        # only continue if locality_name is not empty or None
        combo = (locality, postal, price, type, subtype, price, bedrooms, living, kitchen, furnished, fire, terrace, terrace_area, garden, facades, pool, state)
        if combo not in seen:
            seen.add(combo)
            unique_data.append(item)
    return unique_data

# -------------------------------
# Save to CSV
# -------------------------------

def save_to_csv():
    all_data= scrape_by_provencies()
    unique_data = remove_duplicates(all_data)

    df = pd.DataFrame(unique_data)

    #EVERYONE!!! EVERY TIME YOU RUN A NEW SCRAPING, CHANGE CSV FILE NAME using this syntax 'province_yourname_1_number_of_scrapped_data.csv'

    #ALEKSEI name your output file '_aleksei_1_number_of_scrapped_data.csv'
    #FARANGES name your output file 'east_flanders_faranges_1_number_of_scrapped_data.csv'
    #TIM name your output file 'namur_tim_1_number_of_scrapped_data.csv'
    #ZIVILE name your output file 'antwerp_zivile_1_number_of_scrapped_data.csv'

    df.to_csv('vlaams_brabant_faranges_1.csv', index=False)
    print(f"Saved {len(unique_data)} unique records to vlaams_brabant_faranges_1.csv")


if __name__ == "__main__": # Added now
    save_to_csv()