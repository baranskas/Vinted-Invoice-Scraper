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

bar_width = 0.4
bar_positions_sold = range(len(dates))
bar_positions_purchased = [pos + bar_width for pos in bar_positions_sold]

plt.figure(figsize=(14, 6))
plt.bar(bar_positions_sold, sold_values, width=bar_width, label="Sold", align="center", color="blue")
plt.bar(bar_positions_purchased, purchased_values, width=bar_width, label="Purchased", align="center", color="orange")
plt.xlabel("Date")
plt.ylabel("Value")
plt.title("Daily Sold and Purchased Items Value")
plt.xticks([pos + bar_width / 2 for pos in bar_positions_sold], dates, rotation=90, fontsize=8)
plt.legend()

total_sold = sum(sold_values)
total_purchased = sum(purchased_values)
plt.text(0.5, 0.95, f"Total Sold: {total_sold:.2f} €\nTotal Purchased: {total_purchased:.2f} €", 
         horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes,
         fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

plt.grid(True)
plt.tight_layout()
plt.show()
