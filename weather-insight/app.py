import streamlit as st
from api.accuweather_client import search_location

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Weather Insight - AccuWeather Test",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi tema default (Mode Gelap)
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Custom CSS Styling dinamis berdasarkan tema terpilih
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] {
            background-color: #1e293b !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        .glow-title {
            font-weight: 800;
            background: linear-gradient(to right, #00ffcc, #0099ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        [data-testid="stAppViewContainer"] {
            background-color: #f8fafc !important;
            color: #0f172a !important;
        }
        [data-testid="stSidebar"] {
            background-color: #f1f5f9 !important;
            border-right: 1px solid rgba(0, 0, 0, 0.05) !important;
        }
        .glow-title {
            font-weight: 800;
            background: linear-gradient(to right, #1e3a8a, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.8rem;
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Header Aplikasi
st.markdown("<h1 class='glow-title'>☀️ Weather Insight</h1>", unsafe_allow_html=True)
st.markdown("Pengujian Pencarian Lokasi berbasis **AccuWeather API**.")
st.markdown("---")

# Sidebar untuk Tema
with st.sidebar:
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

# Konten Utama: Pencarian Lokasi
st.subheader("📍 Uji Pencarian Lokasi")
query = st.text_input("Masukkan Nama Kota / Wilayah:", placeholder="Contoh: Jakarta, Bandung, Surabaya...")

if query:
    with st.spinner(f"🔍 Mencari lokasi '{query}' di AccuWeather..."):
        try:
            location_key, full_name = search_location(query)
            
            # Tampilkan hasil pencarian yang sukses
            st.success("🎉 Pencarian Lokasi Berhasil!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Nama Lokasi (AccuWeather)", value=full_name)
            with col2:
                st.metric(label="Location Key (ID)", value=location_key)
                
            st.write("---")
            st.info(f"Detail kembalian: Key=`{location_key}` | Name=`{full_name}`")
            
        except ValueError as ve:
            st.error("⚠️ Kesalahan Validasi / Parameter")
            st.warning(str(ve))
        except ConnectionError as ce:
            st.error("⚠️ Kesalahan Koneksi")
            st.warning(str(ce))
        except Exception as e:
            st.error("⚠️ Terjadi Kesalahan Tak Terduga")
            st.code(str(e))
else:
    st.info("Silakan ketikkan nama kota di atas untuk memulai pencarian lokasi.")
