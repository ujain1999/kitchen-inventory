import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Kitchen Inventory").sheet1

def add_place(place_name):
    places = sheet.col_values(3)[1:]  # skip header
    if place_name not in places:
        sheet.append_row(["", "", place_name, ""])
        return True
    return False

def add_item(item_name, quantity, place):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([item_name, quantity, place, timestamp])

def get_places():
    # Get all unique places
    places = sheet.col_values(3)[1:]  # skip header
    return sorted(list(set(filter(None, places))))

def list_inventory(place_name=None):
    records = sheet.get_all_records()
    if place_name:
        return [r for r in records if r["Place"].lower() == place_name.lower()]
    # group by place
    grouped = {}
    for r in records:
        p = r["Place"] or "Unassigned"
        grouped.setdefault(p, []).append(r)
    return grouped
