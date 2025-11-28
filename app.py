import streamlit as st
import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# =========================================================
# 1. KONFIGURASI HALAMAN (Judul Tab Browser)
# =========================================================
st.set_page_config(page_title="Agen Material Pro", page_icon="🏗️")

# =========================================================
# 2. UI (TAMPILAN WEBSITE)
# =========================================================
st.title("🏗️ Agen Pengadaan Material Bangunan")
st.markdown("---")
st.write("Masukkan kebutuhan Anda, biarkan AI yang keliling toko online.")

# Kolom Input (Biar rapi, kita bagi 2 kolom)
col1, col2 = st.columns(2)

with col1:
    barang_input = st.text_input("Nama Barang", placeholder="Contoh: Semen Gresik 40kg")

with col2:
    lokasi_input = st.text_input("Lokasi", placeholder="Contoh: Jakarta Selatan")

# Tombol Eksekusi
tombol_cari = st.button("🚀 Mulai Pencarian")

# =========================================================
# 3. LOGIKA AGEN (Hanya jalan kalau tombol ditekan)
# =========================================================
if tombol_cari:
   # ... (kode sebelumnya sama)

        with st.spinner('Sedang menghubungi Agen Hunter & Analyst...'):
            
            # --- BAGIAN INI YANG DIUBAH (AMBIL DARI BRANKAS) ---
            # Kita tidak lagi menulis kunci di sini.
            # Kita suruh dia baca dari 'st.secrets'
            
            try:
                # Mengambil kunci dari Brankas Cloud
                serper_key = st.secrets["SERPER_API_KEY"]
                gemini_key = st.secrets["GOOGLE_API_KEY"]
                
                os.environ["SERPER_API_KEY"] = serper_key
                
                otak_gemini = LLM(
                    model="gemini/gemini-1.5-flash-001",
                    api_key=gemini_key, # Pakai variabel kunci yang baru
                    temperature=0.7
                )
                
                # ... (Sisa kode ke bawah sama persis, tidak perlu diubah)

                # --- DEFINISI AGEN ---
                hunter = Agent(
                    role='Material Hunter',
                    goal='Mencari link dan harga real-time',
                    backstory="Spesialis sourcing barang bangunan.",
                    tools=[alat_search],
                    llm=otak_gemini
                )

                analyst = Agent(
                    role='Cost Analyst',
                    goal='Memilih penawaran terbaik',
                    backstory="Auditor harga yang teliti.",
                    llm=otak_gemini
                )

                # --- DEFINISI TUGAS ---
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

                # --- EKSEKUSI ---
                tim = Crew(agents=[hunter, analyst], tasks=[tugas_cari, tugas_laporan])
                hasil = tim.kickoff()

                # --- TAMPILKAN HASIL ---
                st.success("Selesai! Berikut laporannya:")
                st.markdown("---")
                st.markdown(hasil)
            
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")