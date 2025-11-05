# The selenium.webdriver module provides all the implementations of WebDriver
# Currently supported are Firefox, Chrome, IE and Remote. The `Keys` class provides keys on
# the keyboard such as RETURN, F1, ALT etc.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import requests
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
# To remove all the clutter in Terminal output
options.add_argument("--log-level=3") 

driver = webdriver.Edge(options=options)
driver.get("https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&municipals=puurs-sint-amands&noindex=1")

# remove cookie
wait = WebDriverWait(driver, 30)
cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]"))
    )
cookie_button.click()

# collecting one website from brussels area page
property_links = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/detail/')]"))
)
property_hrefs = [link.get_attribute("href") for link in property_links]
print(property_hrefs[0])
driver.get(property_hrefs[0])

html = driver.page_source
soup = BeautifulSoup(html, features= "html.parser")

# --- Helper functions ---
def data_fields(element, attr=None):
    """Safely get text or attribute from a BeautifulSoup element."""
    try:
        if not element:
            return None
        return element.get(attr) if attr else element.get_text(strip=True)
    except Exception:
        return None

def get_property_type(meta_tag):
    """Extract main property type (house/apartment) from meta content."""
    try:
        content = data_fields(meta_tag, attr="content")
        content_lower = content.lower() if content else ""
        return next((t for t in ["house", "apartment"] if t in content_lower), None)
    except Exception:
        return None

def clean_price(price_text):
    """Clean price string, remove text before number and currency symbols."""
    if not price_text:
        return None
    price_text = price_text.split("from")[-1].strip()
    return price_text.replace("€", "").strip()

def yes_no_to_int(soup, label):
    tag = soup.find("h4", string=label)
    if tag:
        text = data_fields(tag.find_next("p")).strip().lower()
        return 1 if text == "yes" else 0
    return 0

def get_area(soup, label):
    """Extract numeric area (first value) from a label."""
    tag = soup.find("h4", string=label)
    if tag:
        text = data_fields(tag.find_next("p"))
        if text:
            return text.split()[0]  # take first word (numeric value)
    return None


# --- Extract property info ---
data = {}

# 1. Property ID
data["property_ID"] = data_fields(soup.find("span", class_="vlancode"))

# 2 & 3. Locality and Postal code
city_line = data_fields(soup.find("span", class_="city-line"))
if city_line:
    parts = city_line.split()
    data["postal_code"] = parts[0]
    data["locality"] = parts[1] if len(parts) > 1 else None
else:
    data["postal_code"] = None
    data["locality"] = None

# 4. Price
raw_price = data_fields(soup.find("span", class_="detail__header_price_data"))
data["price_€"] = clean_price(raw_price)

# 5. Type of property
meta_tag = soup.find("meta", attrs={"name": "keywords"})
data["property_type"] = get_property_type(meta_tag)

# 6. Subtype of property
subtype = data_fields(soup.find("span", class_="detail__header_title_main"))
data["property_subtype"] = subtype.split("for sale")[0].strip() if subtype else None

# 7. Type of sale (exclude life sales)
sale_type = data_fields(soup.find("span", class_="sale-type"))
if sale_type and "life" in sale_type.lower():
    sale_type = None
data["sale_type"] = sale_type

# 8. Bedrooms
header = soup.find("h4", string="Number of bedrooms")
data["bedrooms"] = data_fields(header.find_next("p")) if header else None

# 9. Living area
items = soup.find_all("li", class_=["property-highlight", "margin-bottom-05", "margin-right-05"])
data["living_area_m²"] = data_fields(items[1].find("strong")) if len(items) > 1 else None

# 10. Equipped kitchen YES or NO
kitchen_tag = soup.find("h4", string="Equipped kitchen")
if kitchen_tag:
    text = data_fields(kitchen_tag.find_next("p"))
    if text:
        text = text.strip().lower()
        data["equipped_kitchen"] = 1 if any(word in text for word in ["equipped", "fully", "super"]) and "not" not in text else 0
    else:
        data["equipped_kitchen"] = 0
else:
    data["equipped_kitchen"] = 0

# 11. Furnished YES or NO
data["furnished"] = yes_no_to_int(soup, "Furnished")

# 12. Open fire YES or NO
data["open_fire"] = yes_no_to_int(soup, "Fireplace")

# 13. Terrace YES or NO & Terrace area in square meter
data["terrace"] = yes_no_to_int(soup, "Terrace")
data["terrace_area_m²"] = get_area(soup, "Surface terrace")

# 14. Find garden area in square meter
data["garden_area_m²"] = get_area(soup, "Surface garden")

# 15. Find the number of facades
facades_tag = soup.find("h4", string="Number of facades")
data["number_of_facades"] = data_fields(facades_tag.find_next("p")) if facades_tag else None

# 16. Swimming pool YES or NO
data["swimming_pool"] = yes_no_to_int(soup, "Swimming pool")

# 17. Find the state of the building
state_tag = soup.find("h4", string="State of the property")
data["state_of_building"] = data_fields(state_tag.find_next("p")) if state_tag else None

# --- Print results ---
for key, value in data.items():
    print(f"{key}: {value}")

driver.close()

# Storing the data
properties = [data]
csv_file = "properties.csv"

with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=data.keys())
    writer.writeheader()
    writer.writerow(data)

print(f"Data saved to {csv_file}")
