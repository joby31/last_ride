import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import glob

st.set_page_config(page_title='Pantry Monthly Performance Dashboard', layout='wide')
st.title('Pantry Monthly Performance Dashboard')

# Define base path - use current directory for compatibility with Streamlit Cloud
BASE_PATH = os.getcwd()
month_folders = ['NOV', 'DEC', 'JAN']

st.sidebar.header('Filter Options')
month_options = ['ALL'] + month_folders
selected_month = st.sidebar.selectbox('Select Month', month_options)

if selected_month == 'ALL':
    st.header(' Combined Performance - All Months')
    
    all_months_data = {}
    for month in month_folders:
        month_path = os.path.join(BASE_PATH, month)
        all_months_data[month] = {}
        
        kpi_file = glob.glob(os.path.join(month_path, '*kpi*.xlsx'))
        if kpi_file:
            all_months_data[month]['kpi'] = pd.read_excel(kpi_file[0])
        
        items_file = None
        for pattern in ['ITEMS.xlsx', 'All_Product*.xlsx', 'product*.xlsx']:
            files = glob.glob(os.path.join(month_path, pattern))
            if files:
                items_file = files[0]
                break
        if items_file:
            all_months_data[month]['items_file'] = items_file
    
    st.subheader('Monthly Total Orders Comparison')
    monthly_orders = []
    for month in month_folders:
        if 'kpi' in all_months_data[month]:
            kpi_df = all_months_data[month]['kpi']
            kpi_df['KPI'] = kpi_df['KPI'].astype(str).str.lower().str.strip()
            try:
                total_orders = kpi_df.loc[kpi_df['KPI'] == 'total orders', 'Value'].values[0]
                monthly_orders.append({'Month': month, 'Total Orders': total_orders})
            except:
                pass
    
    if monthly_orders:
        orders_df = pd.DataFrame(monthly_orders)
        fig = make_subplots(specs=[[{'secondary_y': False}]])
        fig.add_trace(go.Bar(x=orders_df['Month'], y=orders_df['Total Orders'], name='Total Orders',
                            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1'], text=orders_df['Total Orders'],
                            textposition='outside', texttemplate='%{text:.0f}'))
        fig.add_trace(go.Scatter(x=orders_df['Month'], y=orders_df['Total Orders'], name='Trend',
                                mode='lines+markers', line=dict(color='#2C3E50', width=3),
                                marker=dict(size=10, color='#E74C3C')))
        fig.update_layout(xaxis_title='Month', yaxis_title='Total Orders', showlegend=True, height=500, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('---')
    st.subheader('Top 10 Best-Selling Products (DEC + JAN + NOV Combined)')
    all_items = []
    
    for month in month_folders:
        if 'items_file' in all_months_data[month]:
            try:
                items_file = all_months_data[month]['items_file']
                items_df = pd.read_excel(items_file, header=None, nrows=10)
                header_row = 0
                for index, row in items_df.iterrows():
                    if row.astype(str).str.lower().str.contains('row labels|product|item').any():
                        header_row = index
                        break
                items_df = pd.read_excel(items_file, header=header_row)
                new_columns = {}
                for col in items_df.columns:
                    col_lower = str(col).lower()
                    if 'row labels' in col_lower or 'product' in col_lower or 'item' in col_lower:
                        new_columns[col] = 'Product'
                    elif 'quantity' in col_lower or 'qty' in col_lower:
                        new_columns[col] = 'Quantity'
                items_df.rename(columns=new_columns, inplace=True)
                if 'Product' in items_df.columns and 'Quantity' in items_df.columns:
                    items_df = items_df[items_df['Product'].notna()]
                    items_df = items_df[~items_df['Product'].astype(str).str.lower().str.contains('grand total', na=False)]
                    all_items.append(items_df[['Product', 'Quantity']])
            except:
                pass
    
    if all_items:
        combined_items = pd.concat(all_items, ignore_index=True)
        items_grouped = combined_items.groupby('Product', as_index=False)['Quantity'].sum()
        top_10_all = items_grouped.sort_values(by='Quantity', ascending=False).head(10)
        fig_top10 = px.bar(top_10_all, x='Quantity', y='Product', orientation='h',
                          labels={'Quantity': 'Total Quantity', 'Product': 'Product'},
                          color_discrete_sequence=['#9B59B6'])
        fig_top10.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top10, use_container_width=True)
    
    st.markdown('---')
    st.subheader('Customer Purchasing Gap (%)')
    all_gap_data = []
    for month in month_folders:
        month_path = os.path.join(BASE_PATH, month)
        gap_file = glob.glob(os.path.join(month_path, '*purchasing_gap*.xlsx'))
        if gap_file:
            try:
                gap_df = pd.read_excel(gap_file[0])
                if 'Purchasing Gap' in gap_df.columns and 'Percentage' in gap_df.columns:
                    all_gap_data.append(gap_df)
            except:
                pass
    
    if all_gap_data:
        combined_gap = pd.concat(all_gap_data, ignore_index=True)
        gap_grouped = combined_gap.groupby('Purchasing Gap', as_index=False)['Percentage'].mean()
        gap_grouped = gap_grouped.sort_values('Percentage', ascending=True)
        fig_gap = px.bar(gap_grouped, x='Percentage', y='Purchasing Gap', orientation='h',
                        text=gap_grouped['Percentage'].apply(lambda x: f'{x:.1f}%'),
                        color_discrete_sequence=['#1f77b4'])
        fig_gap.update_traces(textposition='outside')
        fig_gap.update_layout(
            xaxis_title='Percentage (%)',
            yaxis_title='Purchasing Gap',
            showlegend=False,
            height=400,
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_gap, use_container_width=True)
    
    st.info('Select a specific month from the sidebar to view detailed performance.')

else:
    month_path = os.path.join(BASE_PATH, selected_month)
    st.header(f' {selected_month} Performance')
    
    kpi_file = glob.glob(os.path.join(month_path, '*kpi*.xlsx'))
    if kpi_file:
        kpi_df = pd.read_excel(kpi_file[0])
        kpi_df['KPI'] = kpi_df['KPI'].astype(str).str.strip()
        kpi_df['Value'] = pd.to_numeric(kpi_df['Value'], errors='coerce')
        
        # Calculate or Set Retention Rate
        if not kpi_df['KPI'].str.contains('Retention', case=False).any():
            retention_value = None
            
            # Use hardcoded values if available
            if selected_month == 'DEC':
                retention_value = 12.2
            elif selected_month == 'JAN':
                retention_value = 16.0
            else:
                # Calculate for other months (like NOV)
                try:
                    total_orders = kpi_df.loc[kpi_df['KPI'].str.contains('Total Orders', case=False), 'Value'].values[0]
                    old_orders = kpi_df.loc[kpi_df['KPI'].str.contains('Old Orders', case=False), 'Value'].values[0]
                    if total_orders > 0:
                        retention_value = (old_orders / total_orders) * 100
                except:
                    pass
            
            if retention_value is not None:
                new_row = pd.DataFrame({'KPI': ['Retention Rate'], 'Value': [retention_value]})
                kpi_df = pd.concat([kpi_df, new_row], ignore_index=True)
        
        kpi_df = kpi_df.dropna(subset=['Value'])
        num_kpis = len(kpi_df)
        if num_kpis > 0:
            cols = st.columns(num_kpis)
            for idx, row in kpi_df.iterrows():
                kpi_name = row['KPI']
                kpi_value = row['Value']
                if 'turnover' in kpi_name.lower() or 'basket' in kpi_name.lower():
                    formatted_value = f'₹{kpi_value:,.2f}'
                elif 'rate' in kpi_name.lower() or 'retention' in kpi_name.lower():
                    formatted_value = f'{kpi_value:.2f}%'
                else:
                    formatted_value = f'{kpi_value:,.0f}'
                cols[idx % num_kpis].metric(kpi_name, formatted_value)
    
    st.markdown('---')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Old vs New Customers')
        if kpi_file:
            kpi_lower = kpi_df.copy()
            kpi_lower['KPI'] = kpi_lower['KPI'].str.lower()
            new_orders = 0
            old_orders = 0
            try:
                new_orders = kpi_lower.loc[kpi_lower['KPI'] == 'new orders', 'Value'].values[0]
            except:
                pass
            try:
                old_orders = kpi_lower.loc[kpi_lower['KPI'] == 'old orders', 'Value'].values[0]
            except:
                pass
            if new_orders > 0 or old_orders > 0:
                pie_data = pd.DataFrame({'Customer Type': ['New Orders', 'Old Orders'], 'Count': [new_orders, old_orders]})
                fig_pie = px.pie(pie_data, values='Count', names='Customer Type', hole=0.4,
                               color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader('Top 10 Products')
        items_file = None
        for pattern in ['ITEMS.xlsx', 'All_Product*.xlsx', 'product*.xlsx']:
            files = glob.glob(os.path.join(month_path, pattern))
            if files:
                items_file = files[0]
                break
        if items_file:
            try:
                items_df = pd.read_excel(items_file, header=None, nrows=10)
                header_row = 0
                for index, row in items_df.iterrows():
                    if row.astype(str).str.lower().str.contains('row labels|product|item').any():
                        header_row = index
                        break
                items_df = pd.read_excel(items_file, header=header_row)
                new_columns = {}
                for col in items_df.columns:
                    col_lower = str(col).lower()
                    if 'row labels' in col_lower or 'product' in col_lower or 'item' in col_lower:
                        new_columns[col] = 'Product'
                    elif 'quantity' in col_lower or 'qty' in col_lower:
                        new_columns[col] = 'Quantity'
                items_df.rename(columns=new_columns, inplace=True)
                if 'Product' in items_df.columns and 'Quantity' in items_df.columns:
                    items_df = items_df[items_df['Product'].notna()]
                    items_df = items_df[~items_df['Product'].astype(str).str.lower().str.contains('grand total', na=False)]
                    items_grouped = items_df.groupby('Product', as_index=False)['Quantity'].sum()
                    top_10 = items_grouped.sort_values(by='Quantity', ascending=False).head(10)
                    fig_bar = px.bar(top_10, x='Quantity', y='Product', orientation='h',
                                   labels={'Quantity': 'Quantity', 'Product': 'Product'},
                                   color_discrete_sequence=['#3366CC'])
                    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_bar, use_container_width=True)
            except Exception as e:
                st.error(f'Error loading products: {e}')
    
    st.markdown('---')
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Average Basket Value Trend')
        abv_file = glob.glob(os.path.join(month_path, '*abv*.xlsx'))
        if abv_file:
            try:
                df_abv = pd.read_excel(abv_file[0])
                if 'Date' in df_abv.columns and 'Average Basket Value' in df_abv.columns:
                    df_abv = df_abv.dropna(subset=['Date', 'Average Basket Value'])
                    df_abv['Date'] = pd.to_datetime(df_abv['Date'], dayfirst=True, errors='coerce')
                    df_abv = df_abv.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='first')
                    if not df_abv.empty:
                        fig_abv = px.line(df_abv, x='Date', y='Average Basket Value')
                        fig_abv.update_layout(showlegend=False, xaxis_title=None, yaxis_title='ABV (₹)')
                        first_date = df_abv['Date'].min()
                        month_start = first_date.replace(day=1)
                        if first_date.month == 12:
                            month_end = first_date.replace(day=31)
                        else:
                            next_month = first_date.replace(day=28) + pd.Timedelta(days=4)
                            month_end = next_month.replace(day=1) - pd.Timedelta(days=1)
                        fig_abv.update_xaxes(tickformat='%d-%b', range=[month_start, month_end])
                        st.plotly_chart(fig_abv, use_container_width=True)
                        st.success(f' {selected_month} ABV Chart Loaded!')
            except Exception as e:
                st.error(f'Error loading ABV: {e}')
    
    with col2:
        st.subheader('Day-wise Orders Trend')
        orders_file = glob.glob(os.path.join(month_path, '*orders*.xlsx'))
        if orders_file:
            try:
                df_orders = pd.read_excel(orders_file[0])
                if 'Date' in df_orders.columns and 'Total Orders' in df_orders.columns:
                    df_orders = df_orders.dropna(subset=['Date', 'Total Orders'])
                    df_orders['Date'] = pd.to_datetime(df_orders['Date'], dayfirst=True, errors='coerce')
                    df_orders = df_orders.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='first')
                    if not df_orders.empty:
                        fig_orders = px.line(df_orders, x='Date', y='Total Orders', color_discrete_sequence=['green'])
                        fig_orders.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Orders')
                        first_date = df_orders['Date'].min()
                        month_start = first_date.replace(day=1)
                        if first_date.month == 12:
                            month_end = first_date.replace(day=31)
                        else:
                            next_month = first_date.replace(day=28) + pd.Timedelta(days=4)
                            month_end = next_month.replace(day=1) - pd.Timedelta(days=1)
                        fig_orders.update_xaxes(tickformat='%d-%b', range=[month_start, month_end])
                        st.plotly_chart(fig_orders, use_container_width=True)
                        st.success(f' {selected_month} Orders Chart Loaded!')
            except Exception as e:
                st.error(f'Error loading orders: {e}')
    
    st.markdown('---')
    st.subheader('Daily Turnover Trend')
    turnover_file = glob.glob(os.path.join(month_path, '*turnover*.xlsx'))
    if turnover_file:
        try:
            df_turn = pd.read_excel(turnover_file[0])
            if 'Date' in df_turn.columns and 'Daily Turnover' in df_turn.columns:
                df_turn = df_turn.dropna(subset=['Date', 'Daily Turnover'])
                df_turn['Date'] = pd.to_datetime(df_turn['Date'], dayfirst=True, errors='coerce')
                df_turn = df_turn.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='first')
                if not df_turn.empty:
                    fig_turnover = px.line(df_turn, x='Date', y='Daily Turnover', color_discrete_sequence=['orange'])
                    fig_turnover.update_layout(showlegend=False, xaxis_title=None, yaxis_title='Turnover (₹)')
                    first_date = df_turn['Date'].min()
                    month_start = first_date.replace(day=1)
                    if first_date.month == 12:
                        month_end = first_date.replace(day=31)
                    else:
                        next_month = first_date.replace(day=28) + pd.Timedelta(days=4)
                        month_end = next_month.replace(day=1) - pd.Timedelta(days=1)
                    fig_turnover.update_xaxes(tickformat='%d-%b', range=[month_start, month_end])
                    fig_turnover.update_yaxes(tickformat='.2s')
                    st.plotly_chart(fig_turnover, use_container_width=True)
                    st.success(f' {selected_month} Turnover Chart Loaded!')
        except Exception as e:
            st.error(f'Error loading turnover: {e}')
    
    st.markdown('---')
    st.subheader('Customer Purchasing Gap (%)')
    gap_file = glob.glob(os.path.join(month_path, '*purchasing_gap*.xlsx'))
    if gap_file:
        try:
            gap_df = pd.read_excel(gap_file[0])
            if 'Purchasing Gap' in gap_df.columns and 'Percentage' in gap_df.columns:
                gap_df = gap_df.sort_values('Percentage', ascending=True)
                fig_gap = px.bar(gap_df, x='Percentage', y='Purchasing Gap', orientation='h',
                                text=gap_df['Percentage'].apply(lambda x: f'{x:.1f}%'),
                                color_discrete_sequence=['#1f77b4'])
                fig_gap.update_traces(textposition='outside')
                fig_gap.update_layout(
                    xaxis_title='Percentage (%)',
                    yaxis_title='Purchasing Gap',
                    showlegend=False,
                    height=400,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig_gap, use_container_width=True)
        except Exception as e:
            st.error(f'Error loading purchasing gap: {e}')
