import streamlit as st
import requests

API_URL = "https://your-fastapi-service.onrender.com/get-call-details"
API_KEY = st.secrets["api_key"]

st.title("📞 GMB Call Insight UI")

recording_url = st.text_input("Enter Recording URL:")

if recording_url:
    try:
        response = requests.get(
            API_URL,
            params={"recording_url": recording_url},
            headers={"X-API-Key": API_KEY}
        )
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Call data found!")
            st.json(data)
        else:
            st.error(f"❌ {response.status_code}: {response.json().get('detail')}")
    except Exception as e:
        st.exception(e)
