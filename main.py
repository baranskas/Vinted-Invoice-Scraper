from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

# SET YOUR VINTED USERNAME HERE
BUYER_NAME = ""

with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

cells = soup.find_all("div", class_="cell")

daily_values = defaultdict(lambda: {"sold": 0, "purchased": 0})

for cell in cells:
    buyer_span = cell.find("span", itemprop="buyer")
    order_value_span = cell.find("span", itemprop="order_value")
    order_purchased_span = cell.find("span", itemprop="order_purchased")
    
    if buyer_span and order_value_span and order_purchased_span:
        buyer = buyer_span.get_text(strip=True)
        order_value = float(order_value_span.get_text(strip=True))
        order_purchased = datetime.strptime(order_purchased_span.get_text(strip=True), "%Y-%m-%d %H:%M:%S %z")
        
        day_key = order_purchased.strftime("%Y-%m-%d")
        daily_values[day_key]["purchased" if buyer == BUYER_NAME else "sold"] += order_value

dates = sorted(daily_values.keys())
sold_values = [daily_values[date]["sold"] for date in dates]
purchased_values = [daily_values[date]["purchased"] for date in dates]

plt.figure(figsize=(14, 6))
plt.bar(dates, sold_values, width=0.4, label="Sold", align="center", color="blue")
plt.bar(dates, purchased_values, width=0.4, label="Purchased", align="edge", color="orange")
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Daily Sold and Purchased Items Value")
plt.xticks(rotation=90, fontsize=8)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
