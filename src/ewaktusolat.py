import requests
from bs4 import BeautifulSoup

url = "https://www.e-solat.gov.my/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the prayer time elements (adjust based on website structure)
prayer_times = soup.find_all("span", class_="prayer-time")

for time in prayer_times:
    print(time.text)
