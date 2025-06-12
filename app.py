import streamlit as st
import requests

API_URL = "https://call-analytics-vx86.onrender.com/get-call-details"
API_KEY = st.secrets["api_key"]

st.title("📞 GMB Call Insights Viewer")

recording_url = st.text_input("Enter Recording URL:")

if recording_url:
    try:
        with st.spinner("Fetching data..."):
            response = requests.get(
                API_URL,
                params={"recording_url": recording_url},
                headers={"X-API-Key": API_KEY}
            )
        if response.status_code == 200:
            st.success("✅ Call data retrieved!")
            st.json(response.json())
        else:
            st.error(f"❌ Error {response.status_code}: {response.json().get('detail')}")
    except Exception as e:
        st.exception(f"⚠️ Something went wrong: {e}")
