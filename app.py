import streamlit as st
import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# =========================================================
# 1. KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(page_title="Agen Material Pro", page_icon="🏗️")

# =========================================================
# 2. UI (TAMPILAN WEBSITE)
# =========================================================
st.title("🏗️ Agen Pengadaan Material Bangunan")
st.markdown("---")
st.write("Masukkan kebutuhan Anda, biarkan AI yang keliling toko online.")

col1, col2 = st.columns(2)
with col1:
    barang_input = st.text_input("Nama Barang", placeholder="Contoh: Semen Gresik 40kg")
with col2:
    lokasi_input = st.text_input("Lokasi", placeholder="Contoh: Jakarta Selatan")

tombol_cari = st.button("🚀 Mulai Pencarian")

# =========================================================
# 3. LOGIKA AGEN
# =========================================================
if tombol_cari:
    if not barang_input or not lokasi_input:
        st.warning("Mohon isi nama barang dan lokasi dulu ya, Bos!")
    else:
        with st.spinner('Sedang menghubungi Agen Hunter & Analyst... Mohon tunggu sebentar...'):
            try:
                # --- A. AMBIL KUNCI DARI BRANKAS CLOUD (SECRETS) ---
                # Pastikan Anda sudah setting Secrets di Streamlit Cloud
                os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]
                MY_GEMINI_KEY = st.secrets["GOOGLE_API_KEY"]
                
                # --- B. DEFINISI ALAT (INI YANG TADI HILANG!) ---
                # Kita wajib definisikan ini sebelum dipakai oleh Agent
                alat_search = SerperDevTool()

                # --- C. SETUP OTAK ---
                otak_gemini = LLM(
                    model="gemini/gemini-2.0-flash-001",
                    api_key=MY_GEMINI_KEY,
                    temperature=0.7
                )

                # --- D. DEFINISI AGEN ---
                hunter = Agent(
                    role='Material Hunter',
                    goal='Mencari link dan harga real-time',
                    backstory="Spesialis sourcing barang bangunan.",
                    tools=[alat_search], # Di sini alat_search dipanggil
                    llm=otak_gemini
                )

                analyst = Agent(
                    role='Cost Analyst',
                    goal='Memilih penawaran terbaik',
                    backstory="Auditor harga yang teliti.",
                    llm=otak_gemini
                )

                # --- E. DEFINISI TUGAS ---
                tugas_cari = Task(
                    description=f"Cari harga real-time '{barang_input}' di area '{lokasi_input}' via Tokopedia/Shopee.",
                    expected_output="List harga dan link.",
                    agent=hunter
                )

                tugas_laporan = Task(
                    description="Buat tabel perbandingan dan rekomendasi termurah.",
                    expected_output="Laporan Markdown lengkap.",
                    agent=analyst
                )

                # --- F. EKSEKUSI ---
                tim = Crew(agents=[hunter, analyst], tasks=[tugas_cari, tugas_laporan])
                hasil = tim.kickoff()

                # --- G. TAMPILKAN HASIL ---
                st.success("Selesai! Berikut laporannya:")
                st.markdown("---")
                st.markdown(hasil)
            # ... (kode sebelumnya) ...
                st.markdown(hasil)

                # --- FITUR DOWNLOAD ---
                st.download_button(
                    label="📥 Download Laporan (.md)",
                    data=str(hasil),
                    file_name="laporan_belanja.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")


