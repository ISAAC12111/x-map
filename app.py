import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

# 頁面設定
st.set_page_config(page_title="X 帳號地圖標記", layout="wide")
st.title("📍 X（Twitter）帳號地圖標記工具")

st.markdown("請輸入帳號與地點（每行一筆，用逗號分隔）")
user_input = st.text_area("格式：帳號, 地點", height=200, placeholder="elonmusk, Austin, Texas\njack, New York\nbarackobama, Washington DC")

if st.button("📌 產生地圖"):
    geolocator = Nominatim(user_agent="x_map_app")
    lines = user_input.strip().split('\n')

    markers = []
    for line in lines:
        try:
            username, location_text = [x.strip() for x in line.split(',', 1)]
            location = geolocator.geocode(location_text)
            if location:
                markers.append({
                    'username': username,
                    'location': location_text,
                    'lat': location.latitude,
                    'lon': location.longitude
                })
            else:
                st.warning(f"❗ 找不到地點：{location_text}")
        except:
            st.warning(f"⚠️ 格式錯誤：{line}")

    if markers:
        # 設定地圖中心點
        m = folium.Map(location=[markers[0]['lat'], markers[0]['lon']], zoom_start=2)

        for marker in markers:
            folium.Marker(
                location=[marker['lat'], marker['lon']],
                tooltip=f"@{marker['username']}",
                popup=f"@{marker['username']}<br>{marker['location']}"
            ).add_to(m)

        st_folium(m, width=800, height=600)
    else:
        st.info("請輸入有效的帳號與地點")
