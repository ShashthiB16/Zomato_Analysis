import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Data Analysis", layout="wide")

st.title("🍽️ Zomato Data Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader("Upload Zomato CSV File", type=["csv"])

if uploaded_file is not None:
    
    # Load Data
    df = pd.read_csv(uploaded_file)

    # Data Cleaning
    df = df.drop(['url','address','book_table','phone','dish_liked',
                  'reviews_list','menu_item','listed_in(type)',
                  'listed_in(city)','cuisines'], axis=1)

    df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})
    df = df.fillna(0)

    df['approx_cost'] = df['approx_cost'].replace('[,]', '', regex=True).astype('int64')

    df['rate'] = df['rate'].astype(str)
df['rate'] = df['rate'].str.replace('/5', '', regex=False)
df['rate'] = df['rate'].replace(['-', 'NEW', 'nan'], 0)
df['rate'] = pd.to_numeric(df['rate'], errors='coerce').fillna(0)
    st.success("✅ Data Loaded Successfully!")

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Options")

    locations = st.sidebar.multiselect(
        "Select Location",
        options=df['location'].unique(),
        default=df['location'].unique()[:5]
    )

    filtered_df = df[df['location'].isin(locations)]

    # Show Data
    if st.checkbox("Show Raw Data"):
        st.dataframe(filtered_df)

    # Top N Slider
    top_n = st.slider("Select Top Locations by Avg Cost", 5, 20, 10)

    top_locations = (
        filtered_df.groupby('location')['approx_cost']
        .mean()
        .nlargest(top_n)
    )

    st.subheader(f"🏆 Top {top_n} Locations by Average Cost")

    # Bar Chart
    fig, ax = plt.subplots()
    top_locations.plot(kind='bar', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Rating vs Cost Scatter
    st.subheader("⭐ Rating vs Approx Cost")

    fig2, ax2 = plt.subplots()
    sb.scatterplot(data=filtered_df, x='approx_cost', y='rate', ax=ax2)
    st.pyplot(fig2)

else:
    st.info("Please upload the Zomato dataset CSV file to begin.")
