import pandas as pd

# Load data
df = pd.read_csv("data/stock_live_data.csv")

# Convert timestamp to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort by time (important!)
df = df.sort_values("timestamp")

# Calculate moving averages
df["MA_3"] = df["close"].rolling(window=3).mean()
df["MA_5"] = df["close"].rolling(window=5).mean()

# Price change direction
df["trend"] = df["close"].diff().apply(
    lambda x: "UP" if x > 0 else "DOWN" if x < 0 else "NO CHANGE"
)

# Detect price spikes (>1% change)
df["price_spike"] = df["change_p"].abs() > 1

# Show last few rows
print("\n📊 ANALYSIS OUTPUT (Last 5 rows):\n")
print(df.tail())
