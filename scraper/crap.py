""" for url_item in property_urls:
           if "/projectdetail/" in url_item:
                try:
                    driver.get(url_item)
                    time.sleep(3)
                    
                    property_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/en/detail/')]")
                    
                    for link in property_links:
                        property_url = link.get_attribute("href")
                        if property_url:
                            all_property_urls.add(property_url)"""