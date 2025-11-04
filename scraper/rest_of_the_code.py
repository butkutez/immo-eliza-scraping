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