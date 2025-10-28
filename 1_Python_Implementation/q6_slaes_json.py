import json

with open("sales.json", "r") as f:
    data = json.load(f)

items = []
for item in data:
    total = item["price"] * item["qty"]
    item = f"{item['item']} ->₹{total}"
    items.append(item)

with open("report.txt", "w") as f:
    for item in items:
        f.write(item+ "\n")

