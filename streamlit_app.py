import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Lebanon Inflation Dashboard", layout="wide")

# Load the CSV file (correct file path)
file_path = 'consumer price indices.csv'
data = pd.read_csv(file_path)

# Drop the first row as it contains metadata
data_cleaned = data.drop(index=0)

# Convert relevant columns to proper formats
data_cleaned['EndDate'] = pd.to_datetime(data_cleaned['EndDate'], errors='coerce')
data_cleaned['Year'] = pd.to_datetime(data_cleaned['EndDate']).dt.year
data_cleaned['Month'] = pd.to_datetime(data_cleaned['EndDate']).dt.month
data_cleaned['Value'] = pd.to_numeric(data_cleaned['Value'], errors='coerce')

# Filter by variables
food_price_inflation = data_cleaned[data_cleaned['Item'] == 'Food price inflation']
general_cpi = data_cleaned[data_cleaned['Item'] == 'Consumer Prices, General Indices (2015 = 100)']
food_cpi = data_cleaned[data_cleaned['Item'] == 'Consumer Prices, Food Indices (2015 = 100)']

# Sidebar panel for overview
st.sidebar.title("Overview")
st.sidebar.markdown("""
This dashboard provides insights into **Lebanon's inflation trends**, focusing on **consumer prices** and **food prices** relative to 2015, as well as monthly **food price inflation**.
The data covers the period from **2000 to 2023**, with a special focus on the **post-2019 economic collapse** and its effects on food prices due to Lebanon's high dependency on imports.
""")

# Sidebar interactive features
st.sidebar.title("Filters")
year_range = st.sidebar.slider("Select Year Range", int(data_cleaned['Year'].min()), int(data_cleaned['Year'].max()), (2000, 2023))
selected_month = st.sidebar.selectbox("Select Month", list(range(1, 13)), format_func=lambda x: pd.to_datetime(f'2023-{x}-01').strftime('%B'))

# Filter data by year range and month
food_inflation_filtered = food_price_inflation[(food_price_inflation['Year'] >= year_range[0]) & (food_price_inflation['Year'] <= year_range[1])]
general_cpi_filtered = general_cpi[general_cpi['Month'] == selected_month]
food_cpi_filtered = food_cpi[food_cpi['Month'] == selected_month]

# New Approach 1: Aggregating Monthly Inflation to Yearly Averages
food_inflation_yearly = food_price_inflation.groupby('Year').agg({'Value': 'mean'}).reset_index()

# Visualization 1: Yearly Food Price Inflation Over Time
st.title("Lebanon Inflation Dashboard")
st.subheader("Yearly Average Food Price Inflation Over Time")
fig1 = px.line(food_inflation_yearly, x='Year', y='Value', title="Yearly Average Food Price Inflation Over Time",
               labels={'Value': 'Average Inflation (%)', 'Year': 'Year'})
st.plotly_chart(fig1, use_container_width=True)

# Insight: Food Price Inflation Over Time
st.markdown("""
### Food Price Inflation Over Time
Lebanon has experienced **significant inflation in food prices**, especially post-2019. This period marks the **economic collapse**, triggered by mismanagement of public debt, currency depreciation, and political instability. **Food price inflation** reflects Lebanon's heavy reliance on imports and its inability to stabilize the local currency. 
- **Pre-2019**: Inflation remained relatively controlled, though rising slowly.
- **Post-2019**: Hyperinflation set in as the Lebanese pound depreciated significantly. By 2020, the situation worsened due to the **COVID-19 pandemic**, which exacerbated supply chain disruptions globally.
""")


# O Comparison of General CPI vs Food CPI for a specific month across years
st.subheader(f"Comparison of General vs. Food CPI in {pd.to_datetime(f'2023-{selected_month}-01').strftime('%B')} Across Years")
combined_cpi = pd.concat([general_cpi_filtered, food_cpi_filtered])

fig3 = px.bar(combined_cpi, x='Year', y='Value', color='Item', barmode='group',
              labels={'Value': 'CPI (2015 = 100)', 'Year': 'Year', 'Item': 'Index Type'},
              title=f"General vs. Food CPI in {pd.to_datetime(f'2023-{selected_month}-01').strftime('%B')} Across Years")

st.plotly_chart(fig3, use_container_width=True)

# Insight: General vs. Food CPI
st.markdown(f"""
### General vs. Food CPI
Food prices have increased at a disproportionately higher rate compared to general consumer prices, particularly post-2019. This divergence underscores the critical role that food imports play in Lebanon’s economy. **Currency devaluation**, **increased import costs**, and **supply chain disruptions** have disproportionately affected food prices, making inflation felt much more severely in basic goods compared to general services.
""")
