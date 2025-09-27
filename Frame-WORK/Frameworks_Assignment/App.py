import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from io import BytesIO

# --- Page Setup ---
st.set_page_config(page_title="CORD-19 Research Explorer", layout="wide")
st.title("CORD-19 Interactive Dashboard")
st.write("Explore COVID-19 research papers interactively")

# --- Load Cleaned Data ---
df = pd.read_csv("metadata_cleaned.csv")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
top_journals = df['journal'].value_counts().head(20).index.tolist()
selected_journal = st.sidebar.selectbox("Select a Journal", ["All"] + top_journals)

# Filter data
if selected_journal == "All":
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
else:
    filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1]) & (df['journal'] == selected_journal)]

# --- Publications by Year ---
st.subheader("Publications Over Time")
year_counts = filtered['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values, color='skyblue')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
st.pyplot(fig1)

# --- Top Journals ---
st.subheader("Top Journals")
top_journals_counts = filtered['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
top_journals_counts.plot(kind='bar', ax=ax2, color='orange')
st.pyplot(fig2)

# --- Word Cloud of Titles ---
st.subheader("Word Cloud of Paper Titles")
titles_text = " ".join(filtered['title'].dropna().astype(str).tolist())
words_counter = Counter([w.lower() for w in titles_text.split()])
wc = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(words_counter)
fig3, ax3 = plt.subplots()
ax3.imshow(wc, interpolation='bilinear')
ax3.axis('off')
st.pyplot(fig3)

# --- Download CSV ---
csv = filtered.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Filtered CSV", csv, "filtered_metadata.csv", "text/csv")
