import os
import glob
import pandas as pd

BASE_PATH = r'c:/Users/anilk/OneDrive/Desktop/LAST_RIDE'
month_folders = ['NOV', 'DEC', 'JAN']

print("=" * 60)
print("DASHBOARD DATA DIAGNOSTIC")
print("=" * 60)

for month in month_folders:
    print(f"\n### {month} ###")
    month_path = os.path.join(BASE_PATH, month)
    print(f"Path: {month_path}")
    print(f"Exists: {os.path.exists(month_path)}")
    
    if os.path.exists(month_path):
        # Check KPI file
        kpi_files = glob.glob(os.path.join(month_path, '*kpi*.xlsx'))
        print(f"KPI files found: {len(kpi_files)}")
        if kpi_files:
            print(f"  - {os.path.basename(kpi_files[0])}")
            try:
                kpi_df = pd.read_excel(kpi_files[0])
                print(f"  - Rows: {len(kpi_df)}, Columns: {list(kpi_df.columns)}")
            except Exception as e:
                print(f"  - Error reading: {e}")
        
        # Check other files
        for pattern in ['*orders*.xlsx', '*abv*.xlsx', '*turnover*.xlsx']:
            files = glob.glob(os.path.join(month_path, pattern))
            if files:
                print(f"{pattern}: {os.path.basename(files[0])}")

print("\n" + "=" * 60)
print("If all files show 'found', the data is accessible.")
print("If you see 'Exists: False', check the BASE_PATH.")
print("=" * 60)
