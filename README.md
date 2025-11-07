# 🏡 Immo Eliza Scraper - Data Collection Project

[![Immo_Eliza_Scraping](https://images.pexels.com/photos/2157404/pexels-photo-2157404.jpeg)](https://www.pexels.com/nl-nl/foto/huizen-dichtbij-weg-2157404/) 

*Image source: [PEXELS.COM](https://www.pexels.com/nl-nl/foto/huizen-dichtbij-weg-2157404/*)


## 📖 **Description**

### Introduction

Immo Eliza Scraper is a data collection project written in Python aimed at collecting high-quality real estate data across Belgium from the website Immovlan.be.

In this project we built a dataset that gathers information about ~15 000 property listings all over Belgium. This dataset will be used later to develop a machine learning model to predict property prices.

### Dataset description
Immo Elize Scraper collects data across 17 columns containing information about:

Property ID,
locality name,	
postal code,
property price,
type of property (house/apartment),
subtype of property (bungalow, chalet, mansion, ...)
number of rooms,
living area in m²,
equipped kitchen,
furnished,
open fire,
terrace (Yes/No)
terrace	area in m²,
garden	area in m²,
number of facades,
swimming pool and
state of building	(e.g., new, to be renovated).


### Quality Standards
Data quality standards that are taken into account are:  
* Minimum 10,000 unique properties
* Properties distributed across all Belgium
* No duplicates or empty rows
* Missing values are encoded as None
* Numerical values where possible
* Consistent column naming

## 📁 **Repo structure**

```
├── .venv
│   └── .gitignore
├── Data
│   ├── cleaned_data
│   └── raw_data
├── scraper
│   ├── __init__.py
│   ├── combining_cleaning_csv.py
│   └── scraping.py
├── main.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 🚀 **Getting started**

### Installation

**1. Clone the project and navigate to the project folder**

```
cmd git clone https://github.com/butkutez/immo-eliza-scraping.git
cd immo-eliza-scraping
```

**2. Install required packages**

```
pip install -r requirements.txt
```

The main Python libraries we used were Selenium for scraping dynamic sites and Pandas to structure the data and put it in a csv file. 

**3. Run the main scraper**

````
python main.py
````
### Usage

The script will:

* Scrape property data from Immovlan.be.  
* Clean and process the data.  
* Save the final dataset to data/ folder.  
* Generate a CSV file with the required columns.

## 🌐 Sources
https://immovlan.be/en - main property scraping source

## 🎯 **Learning objectives**

By the end of the project, we have:

✅ Scraped websites for structured data using Selenium to work around dynamic content.    
✅ Built datasets from scratch and managed the dataset.      
✅ Collaborated in a team using Trello.    
✅ Used Git effectively in a team setting.


## 🗓 Timeline
This project was finished in five days.  


* Planning (assign roles, Trello setup, repo strategy): 1 day. 
* Prototype: scrape 1-10 properties, test workflow:	1 days.
* Scaling:	scrape 100 → 1,000 → 10,000 properties: 1 day.
* Cleaning:	ensure consistency, remove duplicates	2 days.
* Documentation:	README, comments, docstrings: 	1 day.
* Final submission:	publish repo, dataset & presentation.
  
## 👥 Contributors
Tim De Nijs (Project Manager)  
Živilė Butkutė (Repo Manager)   
Aleksei Shashkov (Presentation)  
Faranges Mohamadi (README)  


## 📌 Personal context note
This project was done as part of the Data Science & AI course at BeCode Ghent, class of 2025-2026.
