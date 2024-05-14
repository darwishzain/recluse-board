import requests
import time

# Luno API base URL
base_url = 'https://api.luno.com/api/1/ticker?pair=XRPMYR'

def get_luno_price():
    try:
        response = requests.get(base_url)
        data = response.json()
        if 'last_trade' in data:
            price = data['last_trade']
            return price
        else:
            return None
    except Exception as e:
        print(f"Error fetching Luno price: {e}")
        return None

def track_luno_price(interval_seconds):
    while True:
        price = get_luno_price()
        if price is not None:
            print(f"Luno XRP/MYR Price: {price}")
        else:
            print("Unable to fetch Luno price.")
        time.sleep(interval_seconds)

# Track Luno price every 60 seconds
track_luno_price(60)
