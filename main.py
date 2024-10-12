import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

url = 'https://alfa.mzuri.pl/ogloszenia/all?prov=mazowieckie&cityId=Warszawa&page={}'

all_result = []

for page in range(1, 9):
    resp = requests.get(url.format(page))
    soup = BeautifulSoup(resp.text, 'html.parser')

    # Extract address and links
    adresses = soup.find_all('div', attrs={'class': 'item-address'})
    prices = soup.find_all('div', attrs={'class': 'item-numbers'})
    
    # Make sure the number of addresses and prices match
    for adress, price in zip(adresses, prices):
        address_text = adress.text.strip('\n')  # Adres
        district_text=address_text.split('-')[-1].strip() #for trim whitespace
        address_link = adress.find('a')['href']  # Bağlantı
        price_text = price.find('span').text.split(' ')[0].split(',')[0] # Price
        price_zl=price_text
        price_Є=round(int(price_text)/4.2,0)
        price_tl=int(price_text)*8.9

        # Append address, link, and price together as a row
        all_result.append([address_text, district_text,address_link, price_zl,price_Є,price_tl])

# Convert list to DataFrame with 3 columns
df = pd.DataFrame(all_result, columns=['Address','District', 'Link', 'Price (zł)','Price (Є)','Price (₺)'])

# Print DataFrame
print(df)

# Optionally save the DataFrame to CSV
df.to_excel('rent_tracking.xlsx', index=False)