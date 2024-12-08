import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL of the website with the table data
url = 'https://www.worldometers.info/coronavirus/'  

# Send a request to fetch the HTML content from the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')  

# Find the table containing the data
table = soup.find('table', {'id': 'main_table_countries_today'})

# Extract the column names (headers) from the table
headers = [header.text.strip() for header in table.find_all('th')]

# Extract the rows of the table
rows = []
for row in table.find_all('tr')[1:]:  # Skip the header row
    columns = row.find_all('td')
    if len(columns) > 1:
        row_data = [col.text.strip() for col in columns]
        rows.append(row_data)

# Create a DataFrame using the extracted data       
df = pd.DataFrame(rows, columns=headers)

# Convert 'ActiveCases' to numeric (if needed) and handle errors
df['ActiveCases'] = pd.to_numeric(df['ActiveCases'], errors='coerce')

# Handle missing values by filling with the mean of the column or zero
df['ActiveCases'] = df['ActiveCases'].fillna(df['ActiveCases'].mean())  # Fill NaN with mean value

# User interaction prompt
user_input = input("Enter 'top10' to see the top 10 countries by active cases, 'entire' to see the full dataset, or 'save' to save to a CSV: ").strip().lower()

if user_input == 'top10':
    # Check if 'ActiveCases' column exists and sort the data by active cases
    if 'ActiveCases' in df.columns:
        # Sort by 'ActiveCases' in descending order and select the top 10
        top_countries = df[['Country,Other', 'ActiveCases']].sort_values(by='ActiveCases', ascending=False).head(10)

        # Save top 10 data to CSV
        top_countries.to_csv('top_10_active_cases.csv', index=False)
        print("\nTop 10 data saved to 'top_10_active_cases.csv'.")
        print(top_countries)

elif user_input == 'entire':
    # Display the entire dataset
    print("\nFull Dataset:")
    print(df)
    
    # Save the entire dataset to CSV
    df.to_csv('full_dataset.csv', index=False)
    print("\nFull dataset saved to 'full_dataset.csv'.")

else:
    print("\nInvalid input. Please enter 'top10' or 'entire'.")
