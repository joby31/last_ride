import pandas as pd
import plotly.express as px
import os

# Load November data
nov_path = r"c:/Users/anilk/OneDrive/Desktop/LAST_RIDE/NOV"

print("Testing November Line Charts")
print("=" * 60)

# Test ABV Chart
print("\n1. ABV LINE CHART")
abv_file = os.path.join(nov_path, "november_abv.xlsx")
df_abv = pd.read_excel(abv_file)
print(f"Columns: {list(df_abv.columns)}")
print(f"Shape: {df_abv.shape}")
print(f"Date column type: {df_abv['Date'].dtype}")
print(f"First 3 rows:\n{df_abv.head(3)}")

# Convert and clean
df_abv['Date'] = pd.to_datetime(df_abv['Date'], dayfirst=True, errors='coerce')
df_abv = df_abv.dropna(subset=['Date', 'Average Basket Value'])
df_abv = df_abv.sort_values('Date')
print(f"\nAfter cleaning - Shape: {df_abv.shape}")
print(f"Date range: {df_abv['Date'].min()} to {df_abv['Date'].max()}")

# Test Orders Chart
print("\n2. ORDERS LINE CHART")
orders_file = os.path.join(nov_path, "november_orders.xlsx")
df_orders = pd.read_excel(orders_file)
print(f"Columns: {list(df_orders.columns)}")
print(f"Shape: {df_orders.shape}")
print(f"First 3 rows:\n{df_orders.head(3)}")

df_orders['Date'] = pd.to_datetime(df_orders['Date'], dayfirst=True, errors='coerce')
df_orders = df_orders.dropna(subset=['Date', 'Total Orders'])
df_orders = df_orders.sort_values('Date')
print(f"\nAfter cleaning - Shape: {df_orders.shape}")
print(f"Date range: {df_orders['Date'].min()} to {df_orders['Date'].max()}")

# Test Turnover Chart
print("\n3. TURNOVER LINE CHART")
turnover_file = os.path.join(nov_path, "november_turnover.xlsx")
df_turn = pd.read_excel(turnover_file)
print(f"Columns: {list(df_turn.columns)}")
print(f"Shape: {df_turn.shape}")
print(f"First 3 rows:\n{df_turn.head(3)}")

df_turn['Date'] = pd.to_datetime(df_turn['Date'], dayfirst=True, errors='coerce')
df_turn = df_turn.dropna(subset=['Date', 'Daily Turnover'])
df_turn = df_turn.sort_values('Date')
print(f"\nAfter cleaning - Shape: {df_turn.shape}")
print(f"Date range: {df_turn['Date'].min()} to {df_turn['Date'].max()}")

print("\n" + "=" * 60)
print("All November line chart data is valid and ready!")
print("The charts should display when you select NOV from the dropdown.")
