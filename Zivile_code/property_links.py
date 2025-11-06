from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from urllib.parse import quote

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
# Provinces & property types
# ---------------------------

provinces = [
    "Antwerpen", "Limburg", "Oost-Vlaanderen", "Vlaams-Brabant",
    "West-Vlaanderen", "Hainaut", "Liège", "Luxembourg",
    "Namur", "Walloon Brabant"
]

property_types = ["house", "apartment"]

property_links = set()
# ---------------------------
# Handle cookie banner
# ---------------------------
driver.get("https://immovlan.be/en/real-estate")
try:
    cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body//button[contains(text(),'Accept') or contains(text(),'OK')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", cookie_button)
    cookie_button.click()
    time.sleep(1)
    print("Cookie banner closed.")
except:
    print("No cookie banner detected, continuing.")

# ---------------------------
# Collect property links
# ---------------------------
for province in provinces:
    province_encoded = quote(province)
    for property_type in property_types:
        search_url = f"https://immovlan.be/en/real-estate?transactiontypes=for-sale&municipals={province_encoded}&propertytypes={property_type}"
        driver.get(search_url)
        time.sleep(2)
        print(f"\nScraping province: {province} | Type: {property_type}")

        while True:  # pagination loop
            # Scroll to bottom once to load all lazy listings
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Collect links on current page
            links_on_page = driver.find_elements(By.XPATH, "//a[contains(@href,'/detail/')]")
            if links_on_page:
                print(f"Found {len(links_on_page)} links on this page.")
                for link in links_on_page:
                    property_links.add(link.get_attribute("href"))
            else:
                print("No links found on this page.")
                break

            # Go to next page if it exists and is enabled
            next_buttons = driver.find_elements(By.XPATH, "//a[contains(@aria-label,'Next') and not(contains(@class,'disabled'))]")
            if next_buttons:
                driver.execute_script("arguments[0].scrollIntoView(true);", next_buttons[0])
                next_buttons[0].click()
                time.sleep(2)
            else:
                print("No next page, moving to next province/type.")
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

