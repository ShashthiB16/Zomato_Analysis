import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Analysis Dashboard", layout="wide")

st.title("🍽️ Zomato Data Analysis Dashboard")

# Load Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("zomato.csv")
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.sidebar.header("🔎 Filters")

# Sidebar Location Filter
location_list = sorted(df['location'].dropna().unique())
selected_location = st.sidebar.selectbox("Select Location", location_list)

# Sidebar Rest Type Filter
rest_type_list = sorted(df['rest_type'].dropna().unique())
selected_rest_type = st.sidebar.selectbox("Select Restaurant Type", rest_type_list)

# Top N Selector
top_n = st.sidebar.slider("Select Top N", 5, 20, 10)

# ==============================
# 📊 LOCATION ANALYSIS
# ==============================

st.header("📍 Location Based Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Locations by Avg Cost")
    top_cost = df.groupby('location')['approx_cost'].mean().nlargest(top_n)
    fig1, ax1 = plt.subplots()
    sb.barplot(x=top_cost.values, y=top_cost.index, ax=ax1)
    st.pyplot(fig1)

with col2:
    st.subheader("Top Locations by Avg Rating")
    top_rate = df.groupby('location')['rate'].mean().nlargest(top_n)
    fig2, ax2 = plt.subplots()
    sb.barplot(x=top_rate.values, y=top_rate.index, ax=ax2)
    st.pyplot(fig2)

# ==============================
# 🍴 REST TYPE ANALYSIS
# ==============================

st.header("🍴 Restaurant Type Analysis")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Top Rest Types by Votes")
    top_votes = df.groupby('rest_type')['votes'].sum().nlargest(top_n)
    fig3, ax3 = plt.subplots()
    sb.barplot(x=top_votes.values, y=top_votes.index, ax=ax3)
    st.pyplot(fig3)

with col4:
    st.subheader("Top Rest Types by Avg Rating")
    top_rest_rate = df.groupby('rest_type')['rate'].mean().nlargest(top_n)
    fig4, ax4 = plt.subplots()
    sb.barplot(x=top_rest_rate.values, y=top_rest_rate.index, ax=ax4)
    st.pyplot(fig4)

# ==============================
# 🎯 LOCATION SPECIFIC ANALYSIS
# ==============================

st.header(f"🏆 Top Restaurants in {selected_location}")

filtered_df = df[df['location'] == selected_location]

top_restaurants = (
    filtered_df.groupby('name')['approx_cost']
    .mean()
    .nlargest(top_n)
)

fig5, ax5 = plt.subplots()
sb.barplot(x=top_restaurants.values, y=top_restaurants.index, ax=ax5)
st.pyplot(fig5)

# ==============================
# 📌 REST TYPE SPECIFIC
# ==============================

st.header(f"🍽️ {selected_rest_type} Restaurant Insights")

rest_filtered = df[df['rest_type'] == selected_rest_type]

col5, col6 = st.columns(2)

with col5:
    st.metric("Average Cost", round(rest_filtered['approx_cost'].mean(), 2))

with col6:
    st.metric("Average Rating", round(rest_filtered['rate'].mean(), 2))

st.dataframe(rest_filtered.head(20))
