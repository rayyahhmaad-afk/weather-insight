import streamlit as st
import pandas as pd
import plotly.express as px
from api.location_client import fetch_provinces, fetch_regencies, fetch_districts, fetch_villages
from api.bmkg_client import fetch_weather
from services.weather_service import parse_weather_forecast, get_location_info, get_current_forecast, get_activity_recommendations

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Weather Insight",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi tema default (Mode Gelap)
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Custom CSS Styling dinamis berdasarkan tema terpilih (Mendukung Responsivitas Ponsel, Efek Premium & Custom Global Theme)
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        /* 1. Reset Font Global & Warna Latar Belakang Seluruh Halaman */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important; /* Latar belakang halaman abu mendung gelap */
            color: #f8fafc !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #1e293b !important; /* Latar belakang sidebar */
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        /* 2. Judul Efek Gradien Premium */
        .glow-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            background: linear-gradient(to right, #00ffcc, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            font-size: 2.8rem;
        }
        
        /* 3. Card utama cuaca saat ini */
        .main-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.7) 100%);
            color: white;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .main-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px 0 rgba(0, 255, 204, 0.12);
            border-color: rgba(0, 255, 204, 0.3);
        }
        
        /* Grid metrik detail cuaca */
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        /* Card detail */
        .detail-card {
            background: rgba(30, 41, 59, 0.4);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        }
        .detail-card:hover {
            transform: translateY(-2px);
            background: rgba(30, 41, 59, 0.6);
            border-color: rgba(255, 255, 255, 0.1);
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: #cbd5e0;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #00ffcc;
            margin-top: 5px;
        }
        
        .metric-subvalue {
            font-size: 1.2rem;
            color: #f7fafc;
            font-weight: 600;
            margin-top: 5px;
        }
        
        /* Styling rekomendasi aktivitas */
        .recs-container {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            margin-top: 25px;
            margin-bottom: 25px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
        }
        .recs-title {
            font-size: 1rem;
            font-weight: 600;
            color: #cbd5e0;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .recs-list {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        .recs-item {
            border-radius: 30px;
            padding: 8px 18px;
            font-size: 0.95rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: white;
            background: rgba(255, 255, 255, 0.03);
            transition: all 0.2s ease;
        }
        .recs-item:hover {
            transform: scale(1.03);
        }
        .recs-item.warn {
            color: #ffcc00;
            border-color: rgba(255, 204, 0, 0.3);
            background: rgba(255, 204, 0, 0.05);
            box-shadow: 0 0 10px rgba(255, 204, 0, 0.1);
        }
        .recs-item.success {
            color: #00ffcc;
            border-color: rgba(0, 255, 204, 0.3);
            background: rgba(0, 255, 204, 0.05);
            box-shadow: 0 0 10px rgba(0, 255, 204, 0.1);
        }
    
        /* Styling horizontal scroll untuk card prakiraan */
        .forecast-card-container {
            display: flex;
            overflow-x: auto;
            gap: 15px;
            padding: 15px 5px;
            scroll-behavior: smooth;
            scrollbar-width: thin;
            scrollbar-color: rgba(255,255,255,0.2) transparent;
        }
        .forecast-card-container::-webkit-scrollbar {
            height: 6px;
        }
        .forecast-card-container::-webkit-scrollbar-thumb {
            background-color: rgba(255,255,255,0.2);
            border-radius: 10px;
        }
        
        .forecast-card {
            background: rgba(30, 41, 59, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 15px;
            min-width: 125px;
            text-align: center;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            flex-shrink: 0;
            transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        .forecast-card:hover {
            transform: translateY(-4px);
            background: rgba(30, 41, 59, 0.5);
            border-color: rgba(0, 255, 204, 0.2);
            box-shadow: 0 8px 25px rgba(0, 255, 204, 0.1);
        }
        
        .forecast-time {
            font-size: 0.9rem;
            font-weight: 600;
            color: #cbd5e0;
        }
        .forecast-temp {
            font-size: 1.6rem;
            font-weight: 700;
            color: #00ffcc;
            margin: 8px 0;
        }
        .forecast-desc {
            font-size: 0.8rem;
            color: #cbd5e0;
            font-weight: 500;
            height: 2.4em;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.2;
        }
        
        /* Animasi mengambang untuk ikon cuaca */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        .weather-icon-float {
            animation: float 4s ease-in-out infinite;
        }
        
        /* Styling Streamlit Tabs */
        button[data-baseweb="tab"] {
            color: #cbd5e0 !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #00ffcc !important;
            border-bottom-color: #00ffcc !important;
            font-weight: 700 !important;
        }
        
        /* Styling Expander Header */
        [data-testid="stExpander"] {
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            background-color: rgba(30, 41, 59, 0.2) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }
        
        /* Styling Button Micro-interaction */
        div.stButton > button {
            border-radius: 12px !important;
            background-color: #1e293b !important;
            color: #f8fafc !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
        }
        div.stButton > button:hover {
            transform: translateY(-1px) !important;
            border-color: #00ffcc !important;
            color: #00ffcc !important;
            box-shadow: 0 4px 12px rgba(0, 255, 204, 0.15) !important;
        }
        
        /* Media Queries untuk Responsivitas Ponsel */
        @media (max-width: 768px) {
            .detail-grid {
                grid-template-columns: 1fr !important;
                gap: 15px;
            }
            .main-card {
                padding: 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        /* 1. Reset Font Global & Warna Latar Belakang Seluruh Halaman */
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc !important; /* Latar belakang halaman langit terang/bersih */
            color: #0f172a !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #f1f5f9 !important; /* Latar belakang sidebar mode terang */
            border-right: 1px solid rgba(0, 0, 0, 0.05) !important;
        }
        
        /* 2. Judul Efek Gradien Terang */
        .glow-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            background: linear-gradient(to right, #1e3a8a, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            font-size: 2.8rem;
        }
        
        /* 3. Card utama cuaca saat ini */
        .main-card {
            background: linear-gradient(135deg, rgba(241, 245, 249, 0.9) 0%, rgba(226, 232, 240, 0.9) 100%);
            color: #1e293b;
            padding: 30px;
            border-radius: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.06);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .main-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.3);
        }
        
        /* Grid metrik detail cuaca */
        .detail-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }
        
        /* Card detail */
        .detail-card {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(0, 0, 0, 0.04);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
            color: #1e293b;
        }
        .detail-card:hover {
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 1);
            border-color: rgba(0, 0, 0, 0.08);
        }
        
        .metric-label {
            font-size: 0.85rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #2b6cb0;
            margin-top: 5px;
        }
        
        .metric-subvalue {
            font-size: 1.2rem;
            color: #1e293b;
            font-weight: 600;
            margin-top: 5px;
        }
        
        /* Styling rekomendasi aktivitas */
        .recs-container {
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(0, 0, 0, 0.04);
            border-radius: 20px;
            padding: 20px;
            margin-top: 25px;
            margin-bottom: 25px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.03);
        }
        .recs-title {
            font-size: 1rem;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .recs-list {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
        }
        .recs-item {
            border-radius: 30px;
            padding: 8px 18px;
            font-size: 0.95rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            border: 1px solid rgba(0, 0, 0, 0.05);
            color: #1e293b;
            background: rgba(255, 255, 255, 0.8);
            transition: all 0.2s ease;
        }
        .recs-item:hover {
            transform: scale(1.03);
        }
        .recs-item.warn {
            color: #d97706;
            border-color: rgba(217, 119, 6, 0.3);
            background: rgba(217, 119, 6, 0.05);
            box-shadow: 0 0 10px rgba(217, 119, 6, 0.05);
        }
        .recs-item.success {
            color: #16a34a;
            border-color: rgba(22, 163, 74, 0.3);
            background: rgba(22, 163, 74, 0.05);
            box-shadow: 0 0 10px rgba(22, 163, 74, 0.05);
        }
    
        /* Styling horizontal scroll untuk card prakiraan */
        .forecast-card-container {
            display: flex;
            overflow-x: auto;
            gap: 15px;
            padding: 15px 5px;
            scroll-behavior: smooth;
            scrollbar-width: thin;
            scrollbar-color: rgba(0,0,0,0.1) transparent;
        }
        .forecast-card-container::-webkit-scrollbar {
            height: 6px;
        }
        .forecast-card-container::-webkit-scrollbar-thumb {
            background-color: rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        
        .forecast-card {
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(0, 0, 0, 0.04);
            border-radius: 16px;
            padding: 15px;
            min-width: 125px;
            text-align: center;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            flex-shrink: 0;
            transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: #1e293b;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        }
        .forecast-card:hover {
            transform: translateY(-4px);
            background: rgba(255, 255, 255, 0.9);
            border-color: rgba(59, 130, 246, 0.2);
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.08);
        }
        
        .forecast-time {
            font-size: 0.9rem;
            font-weight: 600;
            color: #64748b;
        }
        .forecast-temp {
            font-size: 1.6rem;
            font-weight: 700;
            color: #2b6cb0;
            margin: 8px 0;
        }
        .forecast-desc {
            font-size: 0.8rem;
            color: #64748b;
            font-weight: 500;
            height: 2.4em;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.2;
        }
        
        /* Animasi mengambang untuk ikon cuaca */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        .weather-icon-float {
            animation: float 4s ease-in-out infinite;
        }
        
        /* Styling Streamlit Tabs */
        button[data-baseweb="tab"] {
            color: #64748b !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #2b6cb0 !important;
            border-bottom-color: #2b6cb0 !important;
            font-weight: 700 !important;
        }
        
        /* Styling Expander Header */
        [data-testid="stExpander"] {
            border-radius: 16px !important;
            border: 1px solid rgba(0, 0, 0, 0.06) !important;
            background-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
        }
        
        /* Styling Button Micro-interaction */
        div.stButton > button {
            border-radius: 12px !important;
            background-color: #ffffff !important;
            color: #1e293b !important;
            border: 1px solid rgba(0,0,0,0.1) !important;
            transition: all 0.2s ease !important;
            font-weight: 600 !important;
        }
        div.stButton > button:hover {
            transform: translateY(-1px) !important;
            border-color: #2b6cb0 !important;
            color: #2b6cb0 !important;
            box-shadow: 0 4px 12px rgba(43, 108, 176, 0.15) !important;
        }
        
        /* Media Queries untuk Responsivitas Ponsel */
        @media (max-width: 768px) {
            .detail-grid {
                grid-template-columns: 1fr !important;
                gap: 15px;
            }
            .main-card {
                padding: 20px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Helper untuk lokalisasi nama hari dan bulan ke Bahasa Indonesia
def format_indonesian_date(date_obj) -> str:
    day_names = {
        "Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu",
        "Thursday": "Kamis", "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"
    }
    month_names = {
        "January": "Januari", "February": "Februari", "March": "Maret", "April": "April",
        "May": "Mei", "June": "Juni", "July": "Juli", "August": "Agustus",
        "September": "September", "October": "Oktober", "November": "November", "December": "Desember"
    }
    formatted = date_obj.strftime("%A, %d %B %Y")
    for eng, ind in day_names.items():
        formatted = formatted.replace(eng, ind)
    for eng, ind in month_names.items():
        formatted = formatted.replace(eng, ind)
    return formatted

# Helper untuk merender list forecast card secara horizontal
def render_forecast_cards(df_day) -> str:
    cards_html = []
    for _, row in df_day.iterrows():
        time_str = pd.to_datetime(row["datetime_local"]).strftime("%H:%M")
        icon_url = row["icon_url"]
        icon_html = f'<img src="{icon_url}" class="weather-icon-float" width="42" style="margin: 5px 0; filter: drop-shadow(0px 0px 4px rgba(255,255,255,0.3));">' if icon_url else ""
        card = (
            f'<div class="forecast-card">'
            f'<div class="forecast-time">{time_str}</div>'
            f'{icon_html}'
            f'<div class="forecast-temp">{row["temp"]}°C</div>'
            f'<div class="forecast-desc">{row["weather_desc"]}</div>'
            f'<div style="font-size: 0.72rem; color: #a0aec0; margin-top: 8px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 5px;">'
            f'💧 {row["humidity"]}%<br>💨 {row["wind_speed"]} km/h'
            f'</div>'
            f'</div>'
        )
        cards_html.append(card)
        
    return f'<div class="forecast-card-container">{"".join(cards_html)}</div>'

# Helper untuk membuat visualisasi grafik tren suhu (Plotly dengan spline dan area fill)
def render_temperature_chart(df_forecast):
    fig = px.line(
        df_forecast,
        x="datetime_local",
        y="temp",
        labels={"datetime_local": "Waktu Prakiraan", "temp": "Suhu (°C)"},
        title="Tren Suhu Udara 3 Hari ke Depan",
        template="plotly_dark" if st.session_state.theme == "dark" else "plotly_white"
    )
    line_color = "#00ffcc" if st.session_state.theme == "dark" else "#2b6cb0"
    fill_color = "rgba(0, 255, 204, 0.06)" if st.session_state.theme == "dark" else "rgba(43, 108, 176, 0.06)"
    
    fig.update_traces(
        line=dict(color=line_color, width=3, shape="spline"),
        mode="lines+markers",
        fill="tozeroy",
        fillcolor=fill_color,
        marker=dict(size=6, color=line_color, symbol="circle")
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Outfit", size=12),
        hovermode="x unified"
    )
    return fig

# Header Aplikasi dengan Title Premium Glow
st.markdown("<h1 class='glow-title'>☀️ Weather Insight</h1>", unsafe_allow_html=True)
st.markdown("Aplikasi prakiraan cuaca real-time dengan data resmi dari BMKG.")
st.markdown("---")

# Inisialisasi session state untuk Favorit dan Dropdown lokasi
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "prov_val" not in st.session_state:
    st.session_state.prov_val = "DKI JAKARTA"
if "reg_val" not in st.session_state:
    st.session_state.reg_val = None
if "dist_val" not in st.session_state:
    st.session_state.dist_val = None
if "vill_val" not in st.session_state:
    st.session_state.vill_val = None

# Inisialisasi variabel lokasi
target_code = None
location_label = ""

# Sidebar untuk Pencarian / Dropdown Lokasi Bertingkat, Tema, & Lokasi Favorit
with st.sidebar:
    # 1. TOGGLE TEMA (Gelap / Terang)
    st.markdown("### 🎨 Tema Aplikasi")
    theme_choice = st.radio(
        "Pilih Tema", 
        ["Mode Gelap 🌙", "Mode Terang ☀️"], 
        index=0 if st.session_state.theme == "dark" else 1,
        label_visibility="collapsed"
    )
    new_theme = "dark" if "Mode Gelap" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("---")
    
    # 2. FITUR FAVORIT
    st.markdown("### ⭐ Lokasi Favorit")
    if st.session_state.favorites:
        fav_names = list(st.session_state.favorites.keys())
        selected_fav = st.selectbox("Pilih Kota Favorit", ["-- Pilih Favorit --"] + fav_names)
        if selected_fav != "-- Pilih Favorit --":
            fav_data = st.session_state.favorites[selected_fav]
            st.session_state.prov_val = fav_data["prov"]
            st.session_state.reg_val = fav_data["reg"]
            st.session_state.dist_val = fav_data["dist"]
            st.session_state.vill_val = fav_data["vill"]
            st.rerun()
    else:
        st.info("Belum ada kota favorit yang disimpan.")
        
    st.markdown("---")
    
    # 3. DROPDOWN LOKASI
    st.markdown("### 📍 Pilih Wilayah")
    
    try:
        provinces = fetch_provinces()
        
        if not provinces:
            st.warning("🔍 Provinsi Tidak Ditemukan")
            st.info("Daftar wilayah kosong. Coba muat ulang halaman.")
        else:
            prov_names = [p["nama_wilayah"] for p in provinces]
            
            default_prov_idx = 0
            if st.session_state.prov_val in prov_names:
                default_prov_idx = prov_names.index(st.session_state.prov_val)
            elif "DKI JAKARTA" in prov_names:
                default_prov_idx = prov_names.index("DKI JAKARTA")
                
            selected_prov_name = st.selectbox("Provinsi", prov_names, index=default_prov_idx)
            
            if selected_prov_name != st.session_state.prov_val:
                st.session_state.prov_val = selected_prov_name
                st.session_state.reg_val = None
                st.session_state.dist_val = None
                st.session_state.vill_val = None
                st.rerun()
                
            selected_prov = [p for p in provinces if p["nama_wilayah"] == selected_prov_name][0]
            
            # Fetch Kabupaten
            regencies = fetch_regencies(selected_prov["kode_wilayah"])
            
            if not regencies:
                st.warning("🔍 Kabupaten/Kota Tidak Ditemukan")
            else:
                reg_names = [r["nama_wilayah"] for r in regencies]
                
                default_reg_idx = 0
                if st.session_state.reg_val in reg_names:
                    default_reg_idx = reg_names.index(st.session_state.reg_val)
                    
                selected_reg_name = st.selectbox("Kabupaten / Kota", reg_names, index=default_reg_idx)
                
                if selected_reg_name != st.session_state.reg_val:
                    st.session_state.reg_val = selected_reg_name
                    st.session_state.dist_val = None
                    st.session_state.vill_val = None
                    st.rerun()
                    
                selected_reg = [r for r in regencies if r["nama_wilayah"] == selected_reg_name][0]
                
                # Fetch Kecamatan
                districts = fetch_districts(selected_reg["kode_wilayah"])
                
                if not districts:
                    st.warning("🔍 Kecamatan Tidak Ditemukan")
                else:
                    dist_names = [d["nama_wilayah"] for d in districts]
                    
                    default_dist_idx = 0
                    if st.session_state.dist_val in dist_names:
                        default_dist_idx = dist_names.index(st.session_state.dist_val)
                        
                    selected_dist_name = st.selectbox("Kecamatan", dist_names, index=default_dist_idx)
                    
                    if selected_dist_name != st.session_state.dist_val:
                        st.session_state.dist_val = selected_dist_name
                        st.session_state.vill_val = None
                        st.rerun()
                        
                    selected_dist = [d for d in districts if d["nama_wilayah"] == selected_dist_name][0]
                    
                    # Fetch Kelurahan/Desa
                    villages = fetch_villages(selected_dist["kode_wilayah"])
                    
                    if not villages:
                        st.warning("🔍 Kelurahan/Desa Tidak Ditemukan")
                    else:
                        village_names = [v["nama_wilayah"] for v in villages]
                        
                        default_vill_idx = 0
                        if st.session_state.vill_val in village_names:
                            default_vill_idx = village_names.index(st.session_state.vill_val)
                            
                        selected_village_name = st.selectbox("Kelurahan / Desa", village_names, index=default_vill_idx)
                        st.session_state.vill_val = selected_village_name
                        
                        selected_village = [v for v in villages if v["nama_wilayah"] == selected_village_name][0]
                        
                        target_code = selected_village["kode_wilayah"]
                        location_label = f"{selected_village_name}, Kec. {selected_dist_name}, {selected_reg_name}, {selected_prov_name}"
                        
                        # Kelola Tambah/Hapus Favorit
                        st.markdown("---")
                        fav_label = f"⭐ {selected_village_name}, {selected_reg_name}"
                        
                        if fav_label in st.session_state.favorites:
                            if st.button("❌ Hapus dari Favorit", use_container_width=True):
                                del st.session_state.favorites[fav_label]
                                st.success("Lokasi dihapus dari favorit!")
                                st.rerun()
                        else:
                            if st.button("⭐ Simpan ke Favorit", use_container_width=True):
                                st.session_state.favorites[fav_label] = {
                                    "code": target_code,
                                    "prov": selected_prov_name,
                                    "reg": selected_reg_name,
                                    "dist": selected_dist_name,
                                    "vill": selected_village_name
                                }
                                st.success("Lokasi disimpan ke favorit!")
                                st.rerun()
        
    except Exception as e:
        # Error state yang jelas pada muat daftar wilayah di sidebar
        st.sidebar.error("⚠️ Gagal memuat daftar wilayah.")
        st.sidebar.warning(f"Koneksi terganggu: {str(e)}")
        st.sidebar.info("Sistem beralih otomatis ke Kemayoran, Jakarta Pusat.")
        target_code = "31.71.03.1001"
        location_label = "Kemayoran, Kec. Kemayoran, Kota Adm. Jakarta Pusat, DKI Jakarta"

# Konten Utama Dashboard dengan indikator loading spinner
if target_code:
    with st.spinner("⏳ Menghubungi BMKG dan mengunduh prakiraan cuaca terbaru..."):
        try:
            # Panggil API BMKG
            raw_weather = fetch_weather(target_code)
            
            if not raw_weather:
                st.warning("🔍 Data Prakiraan Cuaca Kosong")
                st.info("BMKG tidak mengirim data cuaca untuk wilayah ini. Silakan coba wilayah lain.")
            else:
                loc_info = get_location_info(raw_weather)
                df_forecast = parse_weather_forecast(raw_weather)
                
                if df_forecast.empty:
                    st.warning("🔍 Data Prakiraan Cuaca Tidak Ditemukan")
                    st.info("Prakiraan cuaca kelurahan/desa ini belum diterbitkan oleh BMKG. Silakan pilih wilayah di sekitarnya.")
                else:
                    # Cari ramalan terdekat dengan waktu saat ini
                    current = get_current_forecast(df_forecast)
                    
                    if not current:
                        st.warning("🔍 Tidak ada data cuaca yang cocok dengan waktu saat ini.")
                    else:
                        # Format waktu lokal prakiraan
                        time_local = pd.to_datetime(current.get("datetime_local"))
                        time_str = time_local.strftime("%d %b %Y, %H:%M")
                        
                        # Tampilkan Lokasi yang sedang aktif di Header
                        st.subheader(f"📍 Kondisi Cuaca untuk: {location_label}")
                        
                        # Layout Kolom (Kiri: Info Utama & Suhu, Kanan: Metrik Pendukung)
                        col_left, col_right = st.columns([2, 3])
                        
                        with col_left:
                            icon_url = current.get("icon_url")
                            icon_html = f'<img src="{icon_url}" class="weather-icon-float" width="100" style="filter: drop-shadow(0px 0px 8px rgba(255,255,255,0.4));">' if icon_url else ""
                            
                            st.markdown(f"""
                            <div class="main-card">
                                <div style="font-size: 1.1rem; opacity: 0.8; font-weight: 500;">CUACA SAAT INI</div>
                                <h2 style="margin: 5px 0 15px 0; font-weight: 700;">📍 {loc_info.get('desa', selected_village_name)}</h2>
                                <div style="display: flex; align-items: center; gap: 20px;">
                                    {icon_html}
                                    <div>
                                        <div style="font-size: 3.8rem; font-weight: 700; line-height: 1;">{current.get('temp')}°C</div>
                                        <div style="font-size: 1.4rem; font-weight: 600; margin-top: 5px;">{current.get('weather_desc')}</div>
                                    </div>
                                </div>
                                <div style="font-size: 0.85rem; margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; opacity: 0.8;">
                                    Wilayah: {location_label}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with col_right:
                            st.markdown("### 📊 Detail Kondisi")
                            
                            # Tampilkan metrik cuaca pendukung dalam grid detail
                            st.markdown(f"""
                            <div class="detail-grid">
                                <div class="detail-card">
                                    <div class="metric-label">💧 Kelembapan</div>
                                    <div class="metric-value">{current.get('humidity')}%</div>
                                </div>
                                <div class="detail-card">
                                    <div class="metric-label">💨 Kecepatan Angin</div>
                                    <div class="metric-value">{current.get('wind_speed')} <span style="font-size: 1.2rem; opacity: 0.8;">km/h</span></div>
                                    <div style="font-size: 0.85rem; margin-top: 5px; opacity: 0.8;">Arah: {current.get('wind_dir')} ({current.get('wind_deg')}°)</div>
                                </div>
                                <div class="detail-card">
                                    <div class="metric-label">🌧️ Curah Hujan</div>
                                    <div class="metric-value">{current.get('precipitation')} <span style="font-size: 1.2rem; opacity: 0.8;">mm</span></div>
                                </div>
                                <div class="detail-card">
                                    <div class="metric-label">🕒 Waktu Prakiraan</div>
                                    <div class="metric-subvalue">{time_str}</div>
                                    <div style="font-size: 0.85rem; margin-top: 5px; opacity: 0.8;">Terdekat dari waktu sekarang</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Rekomendasi Aktivitas
                        recs = get_activity_recommendations(current)
                        if recs:
                            recs_html = []
                            for r in recs:
                                if r.startswith("⚠"):
                                    recs_html.append(f'<div class="recs-item warn">{r}</div>')
                                else:
                                    recs_html.append(f'<div class="recs-item success">{r}</div>')
                            
                            st.markdown(f"""
                            <div class="recs-container">
                                <div class="recs-title">💡 Rekomendasi Aktivitas</div>
                                <div class="recs-list">
                                    {"".join(recs_html)}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Prakiraan Cuaca (3 Tab)
                        st.markdown("---")
                        st.markdown("### 📅 Prakiraan Cuaca Berkala")
                        
                        tab_today, tab_tomorrow, tab_three_days = st.tabs([
                            "☀️ Hari Ini", 
                            "⛅ Besok", 
                            "📅 3 Hari ke Depan"
                        ])
                        
                        # Tab 1: Hari Ini
                        with tab_today:
                            df_today = df_forecast[df_forecast["day_index"] == 0]
                            if df_today.empty:
                                st.info("Prakiraan cuaca untuk hari ini tidak tersedia.")
                            else:
                                st.markdown(render_forecast_cards(df_today), unsafe_allow_html=True)
                                
                        # Tab 2: Besok
                        with tab_tomorrow:
                            df_tomorrow = df_forecast[df_forecast["day_index"] == 1]
                            if df_tomorrow.empty:
                                st.info("Prakiraan cuaca untuk besok tidak tersedia.")
                            else:
                                st.markdown(render_forecast_cards(df_tomorrow), unsafe_allow_html=True)
                                
                        # Tab 3: 3 Hari ke Depan
                        with tab_three_days:
                            for day in range(3):
                                df_day = df_forecast[df_forecast["day_index"] == day]
                                if not df_day.empty:
                                    day_date = pd.to_datetime(df_day.iloc[0]["datetime_local"])
                                    formatted_date = format_indonesian_date(day_date)
                                    st.markdown(f"<h5 style='margin-top:15px; opacity: 0.9;'>📆 {formatted_date}</h5>", unsafe_allow_html=True)
                                    st.markdown(render_forecast_cards(df_day), unsafe_allow_html=True)
                        
                        # Visualisasi Grafik Tren Suhu (Plotly)
                        st.markdown("---")
                        with st.expander("📈 Grafik Tren Suhu 3 Hari ke Depan", expanded=True):
                            fig = render_temperature_chart(df_forecast)
                            st.plotly_chart(fig, use_container_width=True)
                        
                        # Atribusi Wajib dari BMKG
                        st.markdown("---")
                        st.caption("Sumber Data: **Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)**. Data diperbarui secara berkala.")
                        
        except Exception as e:
            # Error state yang ramah pengguna saat koneksi BMKG gagal (tanpa traceback)
            st.error("⚠️ Gagal Menghubungi Layanan BMKG")
            st.warning(f"Keterangan kendala: {str(e)}")
            st.info("Saran tindakan: Pastikan koneksi internet Anda aktif, atau coba pilih kelurahan/desa lainnya di sidebar beberapa saat lagi.")
else:
    st.info("Pilihlah lokasi di sidebar terlebih dahulu.")
