import requests
from bs4 import BeautifulSoup
import pandas as pd

first_names = []
last_names = []
gender_list = []
plz_list = []
ort_list = []
email_list = []

def get_email(details_url):
    try:
        response = requests.get(details_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during request to details page: {e}")
        return ''

    soup = BeautifulSoup(response.content, 'html.parser')
    email_element = soup.find('a', href=lambda href: href and 'mailto' in href)
    if email_element:
        return email_element['href'].split(':')[-1]
    return ''

def get_gender(name):
    main_name = name.split(' ')[0]

    try:
        url = f'https://api.genderize.io?name={main_name}'
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        gender = data.get('gender')
        
        if gender == 'male':
            return 'm'
        elif gender == 'female':
            return 'f'
        else:
            return ''
    except requests.exceptions.RequestException as e:
        print(f"Error during gender prediction for name '{name}': {e}")
        return ''

def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error during request to page {url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select('table.table tr')[1:]

    for row in rows:
        cells = row.select('td')

        full_name = cells[0].get_text(strip=True)
        last_name, first_name = map(str.strip, full_name.split(','))
        gender = get_gender(first_name)

        plz = cells[2].get_text(strip=True)
        ort = cells[3].get_text(strip=True)

        details_url = cells[5].find('a')['href']
        email = get_email(details_url)

        first_names.append(first_name)
        last_names.append(last_name)
        gender_list.append(gender)
        plz_list.append(plz)
        ort_list.append(ort)
        email_list.append(email)

base_url = "https://www.bdh-online.de/patienten/therapeutensuche/"
page_urls = [f"{base_url}?seite={page}" for page in range(1, 3)]

for page_url in page_urls:
    page_df = scrape_page(page_url)

data = {
'First Name': first_names,
'Last Name': last_names,
'Gender': gender_list,
'PLZ (ZIP)': plz_list,
'Ort (city)': ort_list,
'Email': email_list
}

df = pd.DataFrame(data)

df.to_excel('output.xlsx', index=False)
df.to_csv('output.csv', index=False)
