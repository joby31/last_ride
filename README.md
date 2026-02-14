# Pantry Monthly Performance Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=joby31/last_ride&branch=main&mainModule=app.py)

A comprehensive Streamlit dashboard for analyzing monthly pantry performance metrics across November, December, and January.

## Features

### Filter Options
- **ALL** - Combined view with comparison charts
- **NOV** - November detailed performance
- **DEC** - December detailed performance
- **JAN** - January detailed performance

### ALL View
- **Monthly Total Orders Comparison** - Bar + Line chart showing order trends across all months
- **Top 10 Best-Selling Products** - Combined product sales from all 3 months

### Individual Month View
Each month displays:
- **Dynamic KPI Cards** - Total Orders, New Orders, Old Orders, Turnover, Average Basket Value
- **Old vs New Customers** - Pie chart showing customer distribution
- **Top 10 Products** - Bar chart of best-selling products
- **Average Basket Value Trend** - Line chart showing daily ABV
- **Day-wise Orders Trend** - Line chart showing daily orders
- **Daily Turnover Trend** - Line chart showing daily revenue

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd LAST_RIDE
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Data Structure

The dashboard expects data organized in month folders (NOV, DEC, JAN) with the following Excel files:

- `*kpi*.xlsx` - KPI metrics
- `*turnover*.xlsx` - Daily turnover data
- `*orders*.xlsx` - Daily orders data
- `*abv*.xlsx` - Average basket value data
- `ITEMS.xlsx` or `product*.xlsx` - Product quantities

## Technologies

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **OpenPyXL** - Excel file reading

## License

MIT License
