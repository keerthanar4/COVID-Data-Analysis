import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Step 1: Fetch the HTML content
url = 'https://www.worldometers.info/coronavirus/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Locate the table
table = soup.find('table', id='main_table_countries_today')

if not table:
    print("Error: Could not find the table on the webpage.")
    exit()

# Step 3: Extract rows
rows = table.find_all('tr')[1:]  # Skip the header row

# Step 4: Extract data
data = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 8:  # Ensure the row has enough columns
        country = cells[1].text.strip()
        active_cases = cells[8].text.strip()
        date = datetime.now().strftime('%Y-%m-%d')  # Use current date
        data.append([country, active_cases, date])

# Step 5: Save to CSV
if data:
    df = pd.DataFrame(data, columns=['Country', 'Active Cases', 'Date'])
    df.to_csv('covid_data.csv', index=False)
    print("Data scraped and saved to 'covid_data.csv'")
else:
    print("Error: No data extracted from the table.")
