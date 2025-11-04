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

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
# To remove all the clutter in Terminal output
options.add_argument("--log-level=3") 

driver = webdriver.Edge(options=options)
driver.get("https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion&noindex=1")

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

"""
1. + Property ID 
2. + Locality name
3. + Postal code
4. + Price (<li><strong>Price</strong>: 540 000 €</li>)
5. Type of property (house or apartment)
6. + Subtype of property (bungalow, chalet, mansion, ...)
7. Type of sale (note: exclude life sales)
8. + Number of rooms
9. + Living area (area in m²)
10. Equipped kitchen (No - 0/ Yes - 1)
11. Furnished (No - 0/ Yes - 1)
data["furnished"] = 1 if "furnished" in driver.find_element(By.TAG_NAME, "body").text.lower() else 0

12. Open fire (No - 0/ Yes - 1)
13. Terrace (area in m² or None if no terrace)
14. Garden (area in m² or None if no garden)
15. Number of facades
16. Swimming pool (No - 0/ Yes - 1)
17. State of building (new, to be renovated, ...)
"""
# 1. Property ID (<span class="vlancode">VBD46859</span>)
def data_fields(element):
    return element.get_text(strip=True) if element else None
property_ID = data_fields(soup.find("span", class_="vlancode"))
print("Property ID:", property_ID)

# 2. Locality name
def data_fields(element):
    return element.get_text(strip=True) if element else None
city_and_code = data_fields(soup.find("span", class_="city-line"))
locality = city_and_code.split()[1] if city_and_code else None  # Take only the first part
print("Locality name:", locality)

# 3. Postal code (<span class="city-line">1020 Laken</span>)
def data_fields(element):
    return element.get_text(strip=True) if element else None
city_and_code = data_fields(soup.find("span", class_="city-line"))
postal_code = city_and_code.split()[0] if city_and_code else None  # Take only the first part
print("Postal code:", postal_code)

# 4. Price of the property (include strip  and split? to remove text if there is text before the price)
def data_fields(element):
    return element.get_text(strip=True) if element else None
price = data_fields(soup.find("span", class_="detail__header_price_data"))

# Use split/strip to remove unwanted text before the number
if price:
    # Split by 'from' if it exists, take the last part
    price = price.split("from")[-1].strip()
    # Remove any trailing currency symbol if needed
    price = price.replace("€", "").strip()
print(f"Price: {price} €")

# 5. Type of property
# def data_fields(element):
#     return element.get_text(strip=True) if element else None
# property_type = data_fields(soup.find("span", class_="detail__header_title_main"))
# property_type = property_type.split("for sale")[0].strip() if property_type else None
# print("Type of property:", property_type)

# 6. Subtype of property
def data_fields(element):
    return element.get_text(strip=True) if element else None
property_type = data_fields(soup.find("span", class_="detail__header_title_main"))
property_type = property_type.split("for sale")[0].strip() if property_type else None
print("Type of property:", property_type)

# 7. Type os sale
# def data_fields(element):
#     return element.get_text(strip=True) if element else None
# bedrooms = data_fields(soup.find("h4", string="Number of bedrooms").find_next("p"))
# print("Bedrooms:", bedrooms)

# 8. Bedrooms
def data_fields(element):
    return element.get_text(strip=True) if element else None
bedrooms = data_fields(soup.find("h4", string="Number of bedrooms").find_next("p"))
print("Bedrooms:", bedrooms)

# 9. Living area
def data_fields(element):
    return element.get_text(strip=True) if element else None
living_area = data_fields(soup.find_all("li", class_=["property-highlight", "margin-bottom-05", "margin-right-05"])[1].find("strong"))
print(f"Living area: {living_area} m²")

# bathrooms
def data_fields(element):
    return element.get_text(strip=True) if element else None
bathrooms = data_fields(soup.find("h4", string="Number of bathrooms").find_next("p"))
print("Bathrooms:", bathrooms)



driver.close()