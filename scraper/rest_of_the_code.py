# Here, we create instance of Firefox WebDriver.
driver = webdriver.Edge()

# The driver.get method will lead to a page given by the URL. WebDriver will wait until the page is fully
# loaded (i.e. the "onload" event has been triggered) before returning the control to your script.
# It should be noted that if your page uses a lot of AJAX calls when loading, WebDriver may not know
# when it was fully loaded.
driver.get("https://immovlan.be/en/")

# The following line is a statement confirming that the title contains the word "Python".
assert "Python" in driver.title

# WebDriver offers a method `find_element` that aims to search for item based on attributes
# For example, the input text element can be located by its name attribute by
# using the attribute `name` with the value `q`
elem = driver.find_element(By.NAME, "q")

# Then we send keys. This is similar to entering keys using your keyboard.
# Special keys can be sent using the `Keys` class imported in line 7 (from selenium.webdriver.common.keys import Keys).
# For security reasons, we will delete any pre-filled text in the input field
# (for example, "Search") so that it does not affect our search results:
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)

# After submitting the page, you should get the result if there is one. To ensure that certain results
# are found, make an assertion that ensures that the source page does not contain the word "No results found".
assert "No results found." not in driver.page_source
driver.close()





# Tims code:

# try:
#     wait = WebDriverWait(driver, 10)  # wait up to 10s
#     cookie_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Agree and close') or contains(., 'Agree and close') or contains(@class,'cookie')]"))
#     )
#     cookie_button.click()
#     # now continue scraping
#     # e.g. find listings:
#     # listings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result-class")))
#     # for l in listings: ...
# except Exception:
#     print("Error while clicking cookie or scraping:")
#     traceback.print_exc()
#     # don't call driver.quit() if you want to keep browsing to debug
#     # driver.quit()
# finally:
#     # For debugging, keep this commented so the browser stays open.
#     # When finished, call driver.quit()
#     pass


# Different way to do price

# 4. Price of the property
def data_fields(element):
    return element.get_text(strip=True) if element else None
# Find all <li> tags
all_li = soup.find_all("li")
price_li = None
# Go through each <li> and find the one with <strong>Price</strong>
for li in all_li:
    strong_tag = li.find("strong")
    if strong_tag and "Price" in strong_tag.get_text():
        price_li = li
        break  # Stop as soon as we find it

# Extract the text
price = data_fields(price_li)
# Clean the text
if price:
    price = price.replace("Price", "").replace(":", "").strip()

print(f"Price: {price} €")




# # 1. Property ID (<span class="vlancode">VBD46859</span>)
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# property_ID = data_fields(soup.find("span", class_="vlancode"))
# print("Property ID:", property_ID)

# # 2. Locality name
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# city_and_code = data_fields(soup.find("span", class_="city-line"))
# locality = city_and_code.split()[1] if city_and_code else None  # Take only the first part
# print("Locality name:", locality)

# # 3. Postal code (<span class="city-line">1020 Laken</span>)
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# city_and_code = data_fields(soup.find("span", class_="city-line"))
# postal_code = city_and_code.split()[0] if city_and_code else None  # Take only the first part
# print("Postal code:", postal_code)

# # 4. Price of the property (include strip  and split? to remove text if there is text before the price)
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# price = data_fields(soup.find("span", class_="detail__header_price_data"))
# # Use split/strip to remove unwanted text before the number
# if price:
#     # Split by 'from' if it exists, take the last part
#     price = price.split("from")[-1].strip()
#     # Remove any trailing currency symbol if needed
#     price = price.replace("€", "").strip()
# print(f"Price: {price} €")

# # 5. Type of property
# def get_property_type(element):
#     try:
#         # element is expected to be the <meta> tag
#         content = element["content"] if element else None
#         content_lower = content.lower() if content else ""
#         # look for house or apartment
#         return next((t for t in ["house", "apartment"] if t in content_lower), None)
#     except Exception:
#         return None
# meta_tag = soup.find("meta", attrs={"name": "keywords"})
# property_type = get_property_type(meta_tag)
# print("Type of property:", property_type)

# # 6. Subtype of property
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# property_subtype = data_fields(soup.find("span", class_="detail__header_title_main"))
# property_subtype = property_subtype.split("for sale")[0].strip() if property_subtype else None
# print("Type of property:", property_subtype)

# # 7. Type os sale (note: exclude life sales)
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None

# sale_type = data_fields(soup.find("span", class_="sale-type"))
# if sale_type and "life" in sale_type.lower():
#     sale_type = None
# print("Type of sale:", sale_type)

# # 8. Bedrooms
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# header = soup.find("h4", string="Number of bedrooms")
# bedrooms = data_fields(header.find_next("p")) if header else None
# print("Bedrooms:", bedrooms)

# # 9. Living area
# def data_fields(element):
#     try:
#         return element.get_text(strip=True) if element else None
#     except Exception:
#         return None
# items = soup.find_all("li", class_=["property-highlight", "margin-bottom-05", "margin-right-05"])
# living_area = data_fields(items[1].find("strong")) if len(items) > 1 else None
# print(f"Living area: {living_area} m²")
    

# driver.close()



# scrapping the websites



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# ---------------------------
# Setup Selenium
# ---------------------------
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)  # keep browser open
options.add_argument("--log-level=3")  # reduce terminal noise

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 20)

# ---------------------------
# Store all unique links
# ---------------------------
property_links = set()

# ---------------------------
# Open initial page and handle cookie
# ---------------------------
driver.get("https://immovlan.be/en/real-estate?transactiontypes=for-sale&municipals=puurs-sint-amands&noindex=1")

try:
    cookie_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]")
        )
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", cookie_button)
    cookie_button.click()
    time.sleep(1)
    print("Cookie banner closed.")
except:
    print("No cookie banner detected, continuing.")

# ---------------------------
# Provinces list
# ---------------------------
provinces = [
    "Antwerpen", "Limburg", "Oost-Vlaanderen", "Vlaams-Brabant",
    "West-Vlaanderen", "Hainaut", "Liège", "Luxembourg",
    "Namur", "Walloon-Brabant", "Brussels"
]

# ---------------------------
# Loop over provinces
# ---------------------------
for province in provinces:
    print(f"\nScraping province: {province}")
    search_url = f"https://immovlan.be/en/real-estate?transactiontypes=for-sale&municipals={province}"
    driver.get(search_url)
    time.sleep(2)  # allow page to load

    while True:
        # Collect links on current page
        try:
            links_on_page = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/detail/')]"))
            )
            print(f"Found {len(links_on_page)} links on this page.")
            for link in links_on_page:
                href = link.get_attribute("href")
                property_links.add(href)
        except:
            print("No links found on this page, skipping.")
            break

        # Next page
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(@aria-label,'Next')]")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
            time.sleep(2)  # allow next page to load
        except:
            print("No next page, moving to next province.")
            break

# ---------------------------
# Save all links to CSV
# ---------------------------
csv_file = "property_links.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["link"])
    for href in property_links:
        writer.writerow([href])

print(f"\n{len(property_links)} unique property links saved to {csv_file}")
