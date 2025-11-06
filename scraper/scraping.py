from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import traceback
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd

#options = webdriver.EdgeOptions()
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/118.0.5993.118 Safari/537.36 Edg/118.0.2088.76")
#options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 30)


# Define a helper function to extract all property links for one province

def get_property_links(province_url, max_pages=3):
    """Collect property links from all pages in a given province (limit pages for now)."""
    links = []

    for page in range(1, max_pages + 1):
        url = f"{province_url}&page={page}"
        print(f"Loading page {page}: {url}")
        driver.get(url)
        time.sleep(3)  # wait for listings to load

        # Dismiss cookie popup on first page if it appears
        try:
            cookie_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]")
            ))
            cookie_button.click()
            print("Cookie banner closed")
        except:
            pass  # already closed

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # Find all property cards
        cards = soup.select("a[href*='/en/detail/']")
        page_links = ["https://immovlan.be" + card["href"] for card in cards if card.get("href")]
        print(cards)
        print(f"Found {len(page_links)} links on page {page}")
        links.extend(page_links)

        # Stop if no new results (end of pagination)
        #if not page_links:
            #break

    return links


# Use existing scraping logic per property

def scrape_property(url):
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    def data_fields(element):
        return element.get_text(strip=True) if element else None
    
    def yes_no_to_int(soup, label):
        tag = soup.find("h4", string=label)
        if tag:
            text = data_fields(tag.find_next("p")).strip().lower()
            return 1 if text == "yes" else 0
        return 0

   
    living_area = data_fields(soup.find("h4", string="Livable surface").find_next("p")).split()[0] if soup.find("h4", string="Livable surface") else None

    kitchen_tag = soup.find("h4", string="Equipped kitchen")
    if kitchen_tag:
        text = data_fields(kitchen_tag.find_next("p")).strip().lower()
        equipped_kitchen = 1 if any(word in text for word in ["equipped", "fully", "super"]) and "not" not in text else 0
    else:
        equipped_kitchen = 0

    furnished = yes_no_to_int(soup, "Furnished")
    open_fire = yes_no_to_int(soup, "Fireplace")
    terrace = yes_no_to_int(soup, "Terrace")
    terrace_area = data_fields(soup.find("h4", string="Surface terrace").find_next("p")).split()[0] if soup.find("h4", string="Surface terrace") else None
    garden_area = data_fields(soup.find("h4", string="Surface garden").find_next("p")).split()[0] if soup.find("h4", string="Surface garden") else None
    number_of_facades = data_fields(soup.find("h4", string="Number of facades").find_next("p")) if soup.find("h4", string="Number of facades") else None
    swimming_pool = yes_no_to_int(soup, "Swimming pool")
    state_of_building = data_fields(soup.find("h4", string="State of the property").find_next("p")) if soup.find("h4", string="State of the property") else None


    return {
        "Living area": living_area,
        "Equipped kitchen": equipped_kitchen,
        "Furnished": furnished,
        "Open fire": open_fire,
        "Terrace": terrace,
        "Terrace area in square meter": terrace_area,
        "Garden area in square meter": garden_area,
        "Number of facades": number_of_facades,
        "Swimming pool": swimming_pool,
        "State of building": state_of_building,
    }
#print("Living area:", living_area)
#print("Equipped kitchen:", equipped_kitchen)
#print("Furnished:", furnished)
#print("Open fire:", open_fire)
#print("Terrace:", terrace)
#print("Terrace area in square meter:", terrace_area)
#print("Garden area in square meter:", garden_area)
#print("Number of facades:", number_of_facades)
#print("Swimming pool:", swimming_pool )
#print("State of building:", state_of_building)

# Combine everything in the main loop
province = "limburg"
province_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&provinces=limburg&noindex=1&page=1"

property_links = get_property_links(province_url, max_pages=2)
print(f"Total links collected: {len(property_links)}")

results = []

for link in property_links:
    try:
        print(f"Scraping: {link}")
        data = scrape_property(link)
        results.append(data)
    except Exception:
        print(f"Error scraping {link}")
        traceback.print_exc()

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("immovlan_limburg.csv", index=False)
print("Data saved to immovlan_limburg.csv")






