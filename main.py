from scraper.scraping import ImmoElizaScraping
from scraper.combining_cleaning_csv import combine_csv_files, clean_csv_file

def main():

    """starts scraping , deduplicates data, makes a pandas dataframe and finally saves it to csv"""
    
    scraper = ImmoElizaScraping()

    all_data = scraper.scrape_by_provencies()
    unique_data = scraper.remove_duplicates(all_data)
    scraper.save_to_csv(unique_data)

    """Combine multiple CSVs"""

    combined_df = combine_csv_files(folder_path = "data/raw_data", output_file = "data/cleaned_data/all_scraped_data.csv")
    
    cleaned_df = clean_csv_file(input_file="data/cleaned_data/all_scraped_data.csv", output_file="data/cleaned_data/final_cleaned_data.csv"
    )
    

if __name__ == "__main__": 
    main()