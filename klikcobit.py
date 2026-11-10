import streamlit as st
import pandas as pd
import requests
from datetime import date


# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(
    page_title="COBIT Testing",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 COBIT Assessment - Testing")
st.caption("File testing untuk menguji pengisian otomatis dan penyimpanan ke Google Sheets.")


# =========================================================
# GOOGLE APPS SCRIPT
# =========================================================

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbygOtdKcUvdLk47PXeySLeF4gik1eKVVQRD_FumktsShfpYdJS3LZ8DqGQ9ANKY6h_Ptw/exec"


# =========================================================
# DATA PERTANYAAN COBIT
# =========================================================

pertanyaan_cobit = {
    "APO": {
        "APO01": [
            "Apakah organisasi memiliki kerangka kerja manajemen TI yang terdokumentasi?",
            "Apakah peran dan tanggung jawab terkait TI telah ditetapkan dengan jelas?",
            "Apakah kebijakan dan prosedur TI dikomunikasikan kepada pihak terkait?",
            "Apakah pelaksanaan tata kelola TI dievaluasi secara berkala?",
            "Apakah terdapat mekanisme untuk melakukan perbaikan terhadap tata kelola TI?"
        ],
        "APO02": [
            "Apakah organisasi memiliki strategi TI yang selaras dengan tujuan bisnis?",
            "Apakah kebutuhan bisnis menjadi dasar dalam penyusunan strategi TI?",
            "Apakah strategi TI dikomunikasikan kepada pihak yang berkepentingan?",
            "Apakah pencapaian strategi TI dipantau secara berkala?",
            "Apakah strategi TI diperbarui ketika terjadi perubahan kebutuhan bisnis?"
        ],
        "APO03": [
            "Apakah organisasi memiliki arsitektur enterprise yang terdokumentasi?",
            "Apakah arsitektur TI mendukung kebutuhan bisnis organisasi?",
            "Apakah standar arsitektur TI telah ditetapkan?",
            "Apakah perubahan arsitektur TI dikendalikan?",
            "Apakah arsitektur TI dievaluasi secara berkala?"
        ],
        "APO04": [
            "Apakah organisasi mengidentifikasi peluang inovasi teknologi?",
            "Apakah perkembangan teknologi dipantau secara berkala?",
            "Apakah dampak teknologi baru terhadap bisnis dianalisis?",
            "Apakah inovasi TI diprioritaskan berdasarkan kebutuhan organisasi?",
            "Apakah hasil penerapan inovasi TI dievaluasi?"
        ],
        "APO05": [
            "Apakah organisasi memiliki proses pengelolaan portofolio TI?",
            "Apakah investasi TI diprioritaskan berdasarkan kebutuhan bisnis?",
            "Apakah manfaat dari investasi TI dipantau?",
            "Apakah risiko investasi TI dipertimbangkan?",
            "Apakah portofolio investasi TI dievaluasi secara berkala?"
        ]
    },

    "BAI": {
        "BAI01": [
            "Apakah program dan proyek TI dikelola secara terstruktur?",
            "Apakah tujuan proyek TI telah ditetapkan dengan jelas?",
            "Apakah sumber daya proyek TI direncanakan dengan baik?",
            "Apakah kemajuan proyek dipantau secara berkala?",
            "Apakah hasil proyek dievaluasi setelah selesai?"
        ],
        "BAI02": [
            "Apakah kebutuhan bisnis untuk solusi TI telah diidentifikasi?",
            "Apakah kebutuhan pengguna didokumentasikan?",
            "Apakah kebutuhan tersebut divalidasi oleh pihak terkait?",
            "Apakah perubahan kebutuhan dikendalikan?",
            "Apakah solusi yang dikembangkan sesuai dengan kebutuhan yang telah ditentukan?"
        ],
        "BAI03": [
            "Apakah solusi TI dikembangkan menggunakan proses yang terstruktur?",
            "Apakah desain solusi didokumentasikan?",
            "Apakah pengujian solusi dilakukan sebelum implementasi?",
            "Apakah hasil pengujian didokumentasikan?",
            "Apakah solusi ditinjau sebelum digunakan?"
        ],
        "BAI04": [
            "Apakah kapasitas sistem TI dipantau secara berkala?",
            "Apakah kebutuhan kapasitas di masa depan diperkirakan?",
            "Apakah kinerja sistem dievaluasi?",
            "Apakah masalah kapasitas ditangani sebelum mengganggu layanan?",
            "Apakah perencanaan kapasitas diperbarui secara berkala?"
        ],
        "BAI05": [
            "Apakah perubahan organisasi akibat implementasi TI dikelola?",
            "Apakah dampak perubahan terhadap pengguna dianalisis?",
            "Apakah pengguna mendapatkan sosialisasi terkait perubahan?",
            "Apakah pelatihan diberikan ketika diperlukan?",
            "Apakah efektivitas perubahan dievaluasi?"
        ]
    },

    "DSS": {
        "DSS01": [
            "Apakah operasional layanan TI dilakukan berdasarkan prosedur yang terdokumentasi?",
            "Apakah aktivitas operasional TI dipantau secara berkala?",
            "Apakah kejadian operasional dicatat?",
            "Apakah prosedur operasional diperbarui ketika diperlukan?",
            "Apakah kinerja operasional TI dievaluasi?"
        ],
        "DSS02": [
            "Apakah insiden TI dicatat dan diklasifikasikan?",
            "Apakah terdapat prosedur penanganan insiden?",
            "Apakah insiden diprioritaskan berdasarkan tingkat dampaknya?",
            "Apakah penyelesaian insiden dipantau?",
            "Apakah riwayat insiden digunakan untuk perbaikan layanan?"
        ],
        "DSS03": [
            "Apakah masalah TI diidentifikasi secara sistematis?",
            "Apakah akar penyebab masalah dianalisis?",
            "Apakah tindakan penyelesaian masalah didokumentasikan?",
            "Apakah masalah berulang dipantau?",
            "Apakah solusi permanen diterapkan untuk masalah yang telah diketahui?"
        ],
        "DSS04": [
            "Apakah organisasi memiliki rencana keberlangsungan layanan TI?",
            "Apakah risiko gangguan layanan telah diidentifikasi?",
            "Apakah prosedur pemulihan layanan telah ditetapkan?",
            "Apakah rencana keberlangsungan diuji secara berkala?",
            "Apakah hasil pengujian digunakan untuk memperbaiki rencana?"
        ],
        "DSS05": [
            "Apakah keamanan layanan TI dipantau?",
            "Apakah akses terhadap sistem TI dikendalikan?",
            "Apakah aktivitas keamanan dicatat dan dipantau?",
            "Apakah insiden keamanan ditangani?",
            "Apakah kontrol keamanan dievaluasi secara berkala?"
        ]
    },

    "MEA": {
        "MEA01": [
            "Apakah kinerja TI dipantau berdasarkan indikator yang telah ditetapkan?",
            "Apakah hasil pengukuran kinerja TI didokumentasikan?",
            "Apakah pencapaian target TI dievaluasi?",
            "Apakah penyimpangan dari target ditindaklanjuti?",
            "Apakah hasil monitoring digunakan untuk perbaikan?"
        ],
        "MEA02": [
            "Apakah pengendalian internal TI dievaluasi?",
            "Apakah kelemahan pengendalian internal diidentifikasi?",
            "Apakah hasil evaluasi pengendalian didokumentasikan?",
            "Apakah tindakan perbaikan dilakukan terhadap kelemahan kontrol?",
            "Apakah efektivitas pengendalian dievaluasi secara berkala?"
        ],
        "MEA03": [
            "Apakah organisasi memantau kepatuhan terhadap peraturan?",
            "Apakah persyaratan hukum dan regulasi diidentifikasi?",
            "Apakah kepatuhan TI dievaluasi secara berkala?",
            "Apakah pelanggaran kepatuhan ditindaklanjuti?",
            "Apakah perubahan regulasi dipantau?"
        ],
        "MEA04": [
            "Apakah organisasi melakukan assurance terhadap tata kelola TI?",
            "Apakah proses assurance memiliki tujuan dan ruang lingkup yang jelas?",
            "Apakah hasil assurance didokumentasikan?",
            "Apakah temuan assurance ditindaklanjuti?",
            "Apakah hasil assurance digunakan untuk meningkatkan tata kelola TI?"
        ],
        "MEA05": [
            "Apakah evaluasi tata kelola TI dilakukan secara berkala?",
            "Apakah hasil evaluasi dibandingkan dengan target yang ditetapkan?",
            "Apakah kelemahan tata kelola diidentifikasi?",
            "Apakah rekomendasi perbaikan dibuat berdasarkan hasil evaluasi?",
            "Apakah implementasi rekomendasi dipantau?"
        ]
    },

    "EDM": {
        "EDM01": [
            "Apakah organisasi memastikan kerangka tata kelola TI telah ditetapkan?",
            "Apakah prinsip tata kelola TI dikomunikasikan kepada pihak terkait?",
            "Apakah pelaksanaan tata kelola TI dipantau?",
            "Apakah efektivitas tata kelola TI dievaluasi?",
            "Apakah perbaikan tata kelola dilakukan berdasarkan hasil evaluasi?"
        ],
        "EDM02": [
            "Apakah manfaat dari penggunaan TI dievaluasi?",
            "Apakah manfaat TI dibandingkan dengan tujuan bisnis?",
            "Apakah pencapaian manfaat TI dipantau?",
            "Apakah penyimpangan manfaat ditindaklanjuti?",
            "Apakah keputusan investasi TI mempertimbangkan manfaat yang dihasilkan?"
        ],
        "EDM03": [
            "Apakah risiko TI diidentifikasi?",
            "Apakah organisasi memiliki batas toleransi risiko TI?",
            "Apakah risiko TI dipantau secara berkala?",
            "Apakah risiko TI dilaporkan kepada pihak yang berwenang?",
            "Apakah tindakan mitigasi dilakukan terhadap risiko TI?"
        ],
        "EDM04": [
            "Apakah sumber daya TI dikelola secara efektif?",
            "Apakah kebutuhan sumber daya TI direncanakan?",
            "Apakah penggunaan sumber daya TI dipantau?",
            "Apakah sumber daya TI disesuaikan dengan kebutuhan organisasi?",
            "Apakah efektivitas penggunaan sumber daya TI dievaluasi?"
        ],
        "EDM05": [
            "Apakah komunikasi antara pihak manajemen dan pemangku kepentingan dilakukan?",
            "Apakah informasi kinerja TI dilaporkan kepada pihak terkait?",
            "Apakah risiko TI dikomunikasikan kepada pemangku kepentingan?",
            "Apakah laporan TI disampaikan secara berkala?",
            "Apakah kebutuhan informasi pemangku kepentingan dievaluasi?"
        ]
    }
}


# =========================================================
# SKALA NILAI
# =========================================================

skala_nilai = {
    1: "Belum diterapkan",
    2: "Diterapkan sebagian",
    3: "Diterapkan",
    4: "Diterapkan dan dievaluasi",
    5: "Diterapkan secara optimal"
}


# =========================================================
# SESSION STATE
# =========================================================

if "fill_value" not in st.session_state:
    st.session_state.fill_value = 1

if "version" not in st.session_state:
    st.session_state.version = 0


# =========================================================
# FUNGSI ISI SEMUA
# =========================================================

def isi_semua(nilai):
    st.session_state.fill_value = nilai
    st.session_state.version += 1


# =========================================================
# DATA RESPONDEN
# =========================================================

st.header("1. Data Responden")

col1, col2 = st.columns(2)

with col1:
    nama = st.text_input("Nama")

    nim = st.text_input("NIM")

with col2:
    kelas = st.text_input("Kelas")

    tanggal = st.date_input(
        "Tanggal",
        value=date.today()
    )


# =========================================================
# TOMBOL TESTING
# =========================================================

st.header("2. Testing Pengisian Nilai")

st.write(
    "Klik salah satu tombol untuk mengisi seluruh pertanyaan "
    "dengan nilai yang sama."
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.button(
        "ISI SEMUA 1",
        on_click=isi_semua,
        args=(1,),
        use_container_width=True
    )

with col2:
    st.button(
        "ISI SEMUA 2",
        on_click=isi_semua,
        args=(2,),
        use_container_width=True
    )

with col3:
    st.button(
        "ISI SEMUA 3",
        on_click=isi_semua,
        args=(3,),
        use_container_width=True
    )

with col4:
    st.button(
        "ISI SEMUA 4",
        on_click=isi_semua,
        args=(4,),
        use_container_width=True
    )

with col5:
    st.button(
        "ISI SEMUA 5",
        on_click=isi_semua,
        args=(5,),
        use_container_width=True
    )


st.success(
    f"Nilai testing saat ini: {st.session_state.fill_value} — "
    f"{skala_nilai[st.session_state.fill_value]}"
)


# =========================================================
# PERTANYAAN
# =========================================================

st.header("3. Pertanyaan COBIT")

jawaban = []

nomor = 1

for domain, proses_list in pertanyaan_cobit.items():

    st.subheader(f"Domain {domain}")

    for proses, pertanyaan_list in proses_list.items():

        st.markdown(f"### {proses}")

        for pertanyaan in pertanyaan_list:

            key = f"q_{nomor}_v_{st.session_state.version}"

            pilihan = st.radio(
                f"{nomor}. {pertanyaan}",
                options=[1, 2, 3, 4, 5],
                index=st.session_state.fill_value - 1,
                format_func=lambda x: f"{x} - {skala_nilai[x]}",
                key=key,
                horizontal=True
            )

            jawaban.append({
                "Domain": domain,
                "Proses": proses,
                "Pertanyaan": pertanyaan,
                "Nilai": pilihan
            })

            nomor += 1


# =========================================================
# RINGKASAN
# =========================================================

df = pd.DataFrame(jawaban)

st.header("4. Ringkasan Testing")

if not df.empty:

    rata_rata = df["Nilai"].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jumlah Pertanyaan",
            len(df)
        )

    with col2:
        st.metric(
            "Nilai Rata-rata",
            f"{rata_rata:.2f}"
        )

    with col3:
        st.metric(
            "Nilai Maksimal",
            "5"
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# SUBMIT KE GOOGLE SHEETS
# =========================================================

st.header("5. Simpan ke Google Sheets")

if st.button(
    "💾 SIMPAN HASIL TESTING",
    type="primary",
    use_container_width=True
):

    if not nama.strip():
        st.error("Nama belum diisi.")
        st.stop()

    if not nim.strip():
        st.error("NIM belum diisi.")
        st.stop()

    if not kelas.strip():
        st.error("Kelas belum diisi.")
        st.stop()

    if GOOGLE_SCRIPT_URL == "MASUKKAN_URL_GOOGLE_APPS_SCRIPT_ANDA_DI_SINI":
        st.error(
            "URL Google Apps Script belum dimasukkan ke klikcobit.py."
        )
        st.stop()

    payload = {
        "nama": nama,
        "nim": nim,
        "kelas": kelas,
        "tanggal": tanggal.strftime("%Y-%m-%d"),
        "data": df.to_dict(orient="records")
    }

    try:

        with st.spinner("Mengirim data ke Google Sheets..."):

            response = requests.post(
                GOOGLE_SCRIPT_URL,
                json=payload,
                timeout=30
            )

        st.write("HTTP Status:", response.status_code)
        st.write("Response:", response.text)

        try:
            hasil = response.json()
        except Exception:
            hasil = None

        if (
            response.status_code == 200
            and hasil
            and hasil.get("status") == "success"
        ):

            st.success(
                "✅ Data berhasil dikirim dan disimpan ke Google Sheets."
            )

        else:

            st.error(
                "❌ Data gagal disimpan. Cek response di atas."
            )

    except Exception as e:

        st.error(
            f"❌ Terjadi error saat mengirim data: {e}"
        )