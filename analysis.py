import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the scraped data
df = pd.read_csv('covid_data.csv')

# Step 2: Clean and Prepare Data
# Convert 'Active Cases' to numeric (remove commas)
df['Active Cases'] = df['Active Cases'].str.replace(',', '').astype(float)

# Step 3: Filter Top 10 Countries by Active Cases
top_countries = df.nlargest(10, 'Active Cases')

# Step 4: Visualize the Data
plt.figure(figsize=(10, 6))
plt.bar(top_countries['Country'], top_countries['Active Cases'], color='skyblue')
plt.title('Top 10 Countries with the Most Active Cases', fontsize=16)
plt.xlabel('Country', fontsize=12)
plt.ylabel('Active Cases', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()

# Step 5: Save the Plot
plt.savefig('top_10_active_cases.png')
plt.show()

print("Analysis complete. Bar chart saved as 'top_10_active_cases.png'")

