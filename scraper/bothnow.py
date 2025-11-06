# type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = webdriver.EdgeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 30)

#base_url: the webpage-url where we work from
#input houses or apartments (or both) after propertytypes
#input name of province after province in the url

provinces = ["antwerp", "limburg", "east-flanders", "flemish-brabant", "west-flanders", "hainaut", "namur", "liege", "luxembourg", "walloon-brabant", "brussels"]
i = 1
for province in provinces:
    print(i, province)
    i += 1
print("what province would you like to scrape?")
k = int(input())
province = provinces[k-1]

base_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale&propertytypes=house,apartment&provinces={province}&page={page}&noindex=1"

# Accept cookies
driver.get(base_url.format(province=province, page=1))
try:
    cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]"))
    )
    cookie_button.click()
except:
    pass

all_data = []
property_links = []


def scrape_property(property_url):
    driver.get(property_url)
    time.sleep(2)  # Give the page a moment to load
    data = {}

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


# -------------------------------
# Get property links from first x pages
# -------------------------------
for page in range(1, 2):  # Pages 1 to x-1
    url = base_url.format(province=province, page=page)
    driver.get(url)
    try:
        wait.until(lambda d: len(d.find_elements(By.XPATH,"//a[contains(@href, '/detail/') or contains(@href, '/projectdetail/')]")) > 0)
    except:
        continue  # skip if page fails to load

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
        print(f" Found {len(hrefs)} property links in this project.")
    print(f" Collected {len(property_links)} unique property links in total.")            

# -------------------------------
# Scrape each property
# -------------------------------
for url in property_links:
    property_data = scrape_property(url)
    all_data.append(property_data)

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
    combo = (locality, postal, price, type, subtype, price, bedrooms, living, kitchen, furnished, fire, terrace, terrace_area, garden, facades, pool, state)
    if combo not in seen:
        seen.add(combo)
        unique_data.append(item)

# -------------------------------
# Save to CSV
# -------------------------------
keys = all_data[0].keys() if all_data else []
with open("immo_eliza_old_data_not_unique.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(all_data)

print(f"Scraped {len(all_data)} properties and saved to immo_eliza_old_data_not_unique.csv")

keys = unique_data[0].keys() if unique_data else []
with open("immo_eliza_unique_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    writer.writerows(unique_data)

print(f"Scraped {len(unique_data)} properties and saved to immo_eliza_unique_data.csv")


driver.quit()