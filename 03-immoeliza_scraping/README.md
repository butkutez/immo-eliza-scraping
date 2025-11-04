# Immo Eliza - Data Collection

- Repository: `immo-eliza-scraping`
- Type: `Consolidation`
- Duration: `5 days`
- Deadline: `07/11/2025 4:00 PM`
- Show and Tell: 2-3 teams will present their work.
- Team: Team

## Learning Objectives

Use Python to collect as much data as possible.

At the end of this (sub)project, you will:
- Be able to scrape a website
- Be able to build a dataset from scratch
- Collaborate in a team using Trello
- Use Git in a team setting


## The Mission

The real estate company "Immo Eliza" wants to develop a machine learning model to make price predictions on real estate sales in Belgium. They hired you to help with the entire pipeline. [Immoweb](https://www.immoweb.be/nl) is a commonly used website for Belgian properties.

Your first task is to build a dataset that gathers information about at least 10000 properties all over Belgium. This dataset will be used later to train your prediction model.


The final dataset should be a `csv` file with at least the following 18 columns:
- Property ID
- Locality name
- Postal code
- Price
- Type of property (house or apartment)
- Subtype of property (bungalow, chalet, mansion, ...)
- Type of sale (_note_: exclude life sales)
- Number of rooms
- Living area (area in m²)
- Equipped kitchen (No - 0/ Yes - 1)
- Furnished (No - 0/ Yes - 1)
- Open fire (No - 0/ Yes - 1)
- Terrace (area in m² or None if no terrace)
- Garden (area in m² or None if no garden)
- Number of facades
- Swimming pool (No - 0/ Yes - 1)
- State of building (new, to be renovated, ...)

You are welcome to scrape any additional features!

## Must-have features (for the dataset)

- The data should have properties across all Belgium
- There should be at minimum unique 10000 data points
- Missing information is initially encoded with `None`
- Whenever possible, record only numerical values (for example, instead of defining whether the kitchen is equipped using `"Yes"` or `"No"`, use binary values instead)
- Use appropriate and consistent column names for your variables (those will be key to training and understanding your model later on)
- No duplicates
- No empty rows

## Start here!
- Assign roles in your teams: Project Lead (manages the workflow + Trello), Repo Manager (Handles Git), Documenter (Writes README and presentation summarizing work).
- Make a plan of attack with your team and break the project into smaller pieces. Take a moment to note it down in your Trello; and add your coach to your board (vanessa.riveraquinones@gmail.com). 
- Decide on a Repo Strategy (branches, forks, or folders) keep it as simple as possible!

## Coding tips
- Start small and test often! Start by scraping one property then figure out how to scale up. Once you've tested you code for a few properties, move on to 10, 100, 1000,... etc. 
- Python packages that will come in very handy: `requests`, `BeautifulSoup`, `Selinium` and `pandas`
  - You can use other scraping tools such as `scrapy` or `playwright`at your own risk.
  - Keep it light in terms of `pandas` tooling, we'll give you some time afterwards to dive deeper into it for the analysis and visualization part
- You can use concurrency (Python advanced, Bonus material) to increase the speed of data collection
- You might have to work around CAPTCHA and other measures that want to slow you down in the scraping process - be creative ;-)
- Commit regularly and often

## Deliverables

1. Publish your source code on a GitHub repository:
    - Make a private repository first (`immo-eliza-scraping`), share it with your team and coaches
      - Make it public at the end of the project
    - Have a `scraper` folder with your Python modules for scraping (note: you can use OOP or functions. Classes are not mandatory for this project. )
    - Have a `data` folder with the dataset - feel free to subdivide the folder (e.g. `raw`, `cleaned`)
    - Have a `README.md` file
    - Have a `main.py` file to run the scraper
    - Have a `requirements.txt` file
    - Have a `.gitignore` file

2. Write a convincing and clear README file, including following elements as you see fit:
   - Description
   - Installation
   - Usage
   - Sources
   - Visuals
   - Contributors
   - Timeline

3. Slides-deck: A short slide deck that presents your team, project approach/workflow, and final output: We will have project debrief and show and tell on Friday at 4:00 PM. Volunteers or randomly selected people will present their slides.

## Evaluation criteria

| Criteria       | Indicator                                  | Yes/No |
| -------------- | ------------------------------------------ | ------ |
| 1. Is complete | Contains a minimum of 10000 data points    |        |
|                | Contains data across whole Belgium         |        |
|                | The dataset has no empty rows              |        |
|                | There are few non-numeric values           |        |
|                | Your code is slick & clean                 |        |
|                | Repository and commit history is clear     |        |
| 2. Is great    | Used threading/multiprocessing             |        |

## Final note

_"Attempts to create thinking machines will be a great help in discovering how we think ourselves." - Alan Turing_

![You've got this!](https://i.giphy.com/media/JWuBH9rCO2uZuHBFpm/giphy.gif)