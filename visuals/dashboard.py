import streamlit as st
import pandas as pd
import sqlite3
import os

# Connect to SQLite DB
conn = sqlite3.connect("data/youtube_trends.db")
query = "SELECT * FROM trending_videos"
df = pd.read_sql(query, conn)

st.set_page_config(page_title="YouTube Trends Dashboard", layout="wide")
st.title("📊 YouTube Trending Videos")

# Filters
channel_filter = st.sidebar.selectbox("Filter by Channel", ["All"] + sorted(df["channel"].unique().tolist()))
keyword_filter = st.sidebar.text_input("Search by keyword in title")

filtered_df = df.copy()
if channel_filter != "All":
    filtered_df = filtered_df[filtered_df["channel"] == channel_filter]
if keyword_filter:
    filtered_df = filtered_df[filtered_df["title"].str.contains(keyword_filter, case=False)]

st.metric("Total Videos", len(filtered_df))
st.metric("Total Views", f"{filtered_df['view_count'].sum():,}")
st.metric("Total Likes", f"{filtered_df['like_count'].sum():,}")

st.dataframe(filtered_df.sort_values("view_count", ascending=False).reset_index(drop=True))

# Charts
st.subheader("📈 Views vs Likes")
st.bar_chart(filtered_df[["view_count", "like_count"]].head(10).set_index(filtered_df["title"].head(10)))
