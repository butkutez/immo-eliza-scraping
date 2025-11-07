# type: ignore
import pandas as pd
from scraper.scraping import ImmoElizaScraping

def main():
    # starts scraping , deduplicates data, makes a pandas dataframe and finally saves it to csv
    
    scraper = ImmoElizaScraping()

    all_data = scraper.scrape_by_provencies()
    unique_data = scraper.remove_duplicates(all_data)
    scraper.save_to_csv()
  
    # Combine multiple CSVs
    combined_df = scraper.combine_csv_files()

    # Clean the combined CSV
    cleaned_df = scraper.clean_csv_file()

if __name__ == "__main__": 
    main()