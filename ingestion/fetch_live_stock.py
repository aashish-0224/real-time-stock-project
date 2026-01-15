import requests
import time
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("EODHD_API_KEY")

if API_KEY is None:
    raise ValueError("API key not found in .env")

# MULTI-STOCK LIST
SYMBOLS = ["AAPL.US", "MSFT.US", "GOOGL.US"]
INTERVAL = 60  # seconds

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

CSV_FILE = "data/stock_live_data.csv"
file_exists = os.path.isfile(CSV_FILE)

with open(CSV_FILE, "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow([
            "symbol",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "change",
            "change_p",
            "timestamp"
        ])

    print("📡 Fetching live stock data... (Ctrl + C to stop)\n")

    while True:
        for symbol in SYMBOLS:
            url = f"https://eodhd.com/api/real-time/{symbol}?api_token={API_KEY}&fmt=json"
            response = requests.get(url).json()

            writer.writerow([
                symbol,
                response.get("open"),
                response.get("high"),
                response.get("low"),
                response.get("close"),
                response.get("volume"),
                response.get("change"),
                response.get("change_p"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])

            print(
                symbol,
                "| Close:", response.get("close"),
                "| Volume:", response.get("volume"),
                "| Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        time.sleep(INTERVAL)
