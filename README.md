# Therapist Data Crawling Project

## Task Description

This is a test project to crawl data from the [BDH Therapist Search Website](https://www.bdh-online.de/patienten/therapeutensuche/). The goal is to retrieve information from the first two pages, including the following data for each therapist:

- First name
- Last name
- PLZ (ZIP)
- Ort (city)
- Email

Additionally, a bonus field is required: automatically detect the gender of the person. The output should be "m" for male or "f" for female. The final data should be saved as an Excel or CSV file.

## Implementation

The task is implemented using Python 3 and various libraries, including BeautifulSoup for web scraping and requests for making HTTP requests.

## How to Run

1. Ensure you have Python 3 installed on your system.
2. Install the required dependencies by running: `pip3 install -r requirements.txt`
3. Execute the script: `python3 crawl_data.py`

## Output

The script will generate an Excel file (`output.xlsx`) and a CSV file (`output.csv`) containing the extracted therapist data.
