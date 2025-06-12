import streamlit as st
import requests
import pandas as pd
from collections import Counter

API_URL = "https://call-analytics-vx86.onrender.com/get-call-details"
API_KEY = st.secrets["api_key"]

st.title("📞 GMB Call Analysis")

user_input = st.text_area("Enter one or more Recording URLs (comma-separated):")

# Store results in list
results = []

if st.button("Fetch Call Data"):
    if user_input:
        urls = [u.strip() for u in user_input.split(",") if u.strip()]
        with st.spinner("Fetching data..."):
            for url in urls:
                try:
                    resp = requests.get(
                        API_URL,
                        params={"recording_url": url},
                        headers={"X-API-Key": API_KEY}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        data["Recording URL"] = url
                        results.append(data)
                    else:
                        st.warning(f"❌ {url} → {resp.status_code}: {resp.json().get('detail')}")
                except Exception as e:
                    st.error(f"Error fetching {url}: {e}")

    # Display table
    if results:
        df = pd.DataFrame(results)
        st.success(f"✅ Retrieved {len(df)} records.")
        st.dataframe(df)

        # Save to session
        st.session_state["last_df"] = df

# Summary
if st.button("🔍 Summarize") and "last_df" in st.session_state:
    df = st.session_state["last_df"]
    st.subheader("📊 Summary")

    if "AudioDurationMinutes" in df:
        avg_duration = round(df["AudioDurationMinutes"].dropna().mean(), 2)
        st.markdown(f"**Average Call Duration:** {avg_duration} mins")

    if "CallSentiment" in df:
        st.markdown("**Sentiment Distribution:**")
        st.bar_chart(df["CallSentiment"].value_counts())

    if "Top3Themes" in df:
        all_themes = []
        for t in df["Top3Themes"].dropna():
            if isinstance(t, list):
                all_themes.extend(t)
        top_themes = Counter(all_themes).most_common(5)
        st.markdown("**Top Themes:**")
        for theme, count in top_themes:
            st.write(f"- {theme}: {count} mentions")
