import pandas as pd
import re

def combine_csv_files():

    """Combine multiple CSV files into a single DataFrame."""

    csv_files = ["antwerp_zivile_51.csv", "brabant_wallon_faranges_1_1532.csv", 
                "east-flanders _zivile_51.csv", "hainaut_Aleksei_1_51.csv", "liege_tim_1_51.csv", 
                "limburg_zivile_51.csv", "luxemburg_tim_1_51.csv", "namur_tim_1_51.csv",
                "vlaams_brabant_faranges_1._1218.csv", "west-flanders_Aleksei_1_51.csv"]
    df_csv_concat = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
    return df_csv_concat

# combine and save    
df = combine_csv_files()
df.to_csv('all_scraped_data.csv', index=False)


def clean_csv_file():

    """Remove rows containing the backspace character."""

    df = pd.read_csv("all_scraped_data.csv")
    pattern = r'\x08'

    # Filter rows that do not match the pattern
    # axis=1 means “operate horizontally”
    # ~ (tilde operator): this is a logical NOT in pandas.
    filtered_df = df[~df.apply(lambda row: row.astype(str).str.contains(pattern, regex=True).any(), axis=1)]
    filtered_df.to_csv("final_cleaned_data.csv", index=False)
    return filtered_df
cleaned_df = clean_csv_file()