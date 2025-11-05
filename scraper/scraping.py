# The selenium.webdriver module provides all the implementations of WebDriver
# Currently supported are Firefox, Chrome, IE and Remote. The `Keys` class provides keys on
# the keyboard such as RETURN, F1, ALT etc.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from bs4 import BeautifulSoup


options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Edge(options=options)
driver.get("https://immovlan.be/en")
# print(driver.title)
wait = WebDriverWait(driver, 30)
cookie_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/div/div/div[2]/button[2]"))
    )
cookie_button.click()


# # collecting one website from brussels area page
# driver = webdriver.Edge(options=options)
# driver.get("https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&municipals=brussels&noindex=1")

# wait = WebDriverWait(driver, 30)
# property_url = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div[3]/div/div[2]/div[2]/section/article[1]"))
#     )
# cookie_button.click()


# print(driver.title)


# collecting price info



# price_element = wait.until(
#     EC.visibility_of_element_located(
#         (By.XPATH, "/html/body/div[2]/div[4]/div[3]/div[1]/div[1]/div/p/span[1]")
#     )
# )

# all_titles = []
# for title in property_price:
#     all_titles.append(title.text.strip())

# all_titles


""" scrapping multiple links
property_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/detail/')]")))

unique_links = set()
for link in property_links:
    href = link.get_attribute("href")
    if href not in unique_links:
        unique_links.add(href)

print(unique_links)
"""

# print(unique_links)
# all_titles = []
# for title in article_titles:
#     all_titles.append(title.text.strip())

# all_titles

# driver.close()