import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import date


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="COBIT Assessment",
    page_icon="📊",
    layout="wide"
)

st.title("📊 COBIT Assessment")
st.caption(
    "Aplikasi sederhana untuk penilaian implementasi COBIT"
)


# =========================================================
# URL GOOGLE APPS SCRIPT
# =========================================================


GOOGLE_SCRIPT_URL = (
    "https://script.google.com/macros/s/AKfycbygOtdKcUvdLk47PXeySLeF4gik1eKVVQRD_FumktsShfpYdJS3LZ8DqGQ9ANKY6h_Ptw/exec"
)


# =========================================================
# DATA PERTANYAAN COBIT
# =========================================================

pertanyaan_cobit = {

    "EDM": {
        "EDM.1 Arah dan tujuan TI": [
            "Apakah tujuan layanan TI selaras dengan tujuan organisasi?",
            "Apakah arah pengembangan TI telah ditentukan dengan jelas?",
            "Apakah manfaat penggunaan TI telah ditentukan?",
            "Apakah kebutuhan organisasi menjadi pertimbangan dalam pengembangan TI?",
            "Apakah pencapaian tujuan TI dievaluasi secara berkala?"
        ],

        "EDM.2 Penyampaian manfaat": [
            "Apakah manfaat dari penggunaan TI telah ditentukan?",
            "Apakah investasi TI memberikan manfaat bagi organisasi?",
            "Apakah penggunaan sumber daya TI dilakukan secara efektif?",
            "Apakah manfaat layanan TI dipantau secara berkala?",
            "Apakah terdapat evaluasi terhadap pencapaian manfaat TI?"
        ],

        "EDM.3 Optimasi risiko": [
            "Apakah risiko yang berkaitan dengan TI telah diidentifikasi?",
            "Apakah risiko TI dipantau secara berkala?",
            "Apakah terdapat tindakan untuk mengurangi risiko TI?",
            "Apakah pihak yang bertanggung jawab terhadap risiko telah ditentukan?",
            "Apakah evaluasi risiko dilakukan secara berkala?"
        ],

        "EDM.4 Optimasi sumber daya": [
            "Apakah sumber daya TI digunakan secara efektif?",
            "Apakah kebutuhan sumber daya TI telah direncanakan?",
            "Apakah sumber daya manusia TI dikelola dengan baik?",
            "Apakah infrastruktur TI dimanfaatkan secara optimal?",
            "Apakah penggunaan sumber daya TI dievaluasi?"
        ],

        "EDM.5 Transparansi stakeholder": [
            "Apakah informasi mengenai TI tersedia bagi pihak terkait?",
            "Apakah informasi TI disampaikan secara transparan?",
            "Apakah pihak terkait mendapatkan informasi yang diperlukan?",
            "Apakah kinerja TI dilaporkan kepada pihak terkait?",
            "Apakah transparansi informasi TI dievaluasi?"
        ]
    },

    "APO": {
        "APO.1 Pengelolaan kerangka kerja TI": [
            "Apakah organisasi memiliki kerangka kerja pengelolaan TI?",
            "Apakah kebijakan TI telah ditetapkan?",
            "Apakah tanggung jawab pengelolaan TI telah ditentukan?",
            "Apakah kebijakan TI dikomunikasikan kepada pengguna?",
            "Apakah kerangka kerja TI dievaluasi secara berkala?"
        ],

        "APO.2 Pengelolaan strategi": [
            "Apakah strategi TI telah ditentukan?",
            "Apakah strategi TI mendukung tujuan organisasi?",
            "Apakah kebutuhan TI direncanakan secara sistematis?",
            "Apakah strategi TI dikomunikasikan kepada pihak terkait?",
            "Apakah strategi TI ditinjau secara berkala?"
        ],

        "APO.3 Pengelolaan arsitektur": [
            "Apakah arsitektur TI telah ditentukan?",
            "Apakah arsitektur TI mendukung kebutuhan organisasi?",
            "Apakah komponen TI didokumentasikan?",
            "Apakah perubahan arsitektur TI dikelola?",
            "Apakah arsitektur TI dievaluasi secara berkala?"
        ],

        "APO.4 Pengelolaan inovasi": [
            "Apakah organisasi mengidentifikasi peluang inovasi TI?",
            "Apakah teknologi baru dievaluasi sebelum digunakan?",
            "Apakah inovasi TI mendukung kebutuhan organisasi?",
            "Apakah risiko inovasi TI dipertimbangkan?",
            "Apakah hasil inovasi TI dievaluasi?"
        ],

        "APO.5 Pengelolaan portofolio": [
            "Apakah investasi TI dikelola dalam suatu portofolio?",
            "Apakah prioritas investasi TI telah ditentukan?",
            "Apakah biaya dan manfaat investasi TI dibandingkan?",
            "Apakah proyek TI dipantau?",
            "Apakah portofolio TI dievaluasi secara berkala?"
        ]
    },

    "BAI": {
        "BAI.1 Pengelolaan program dan proyek": [
            "Apakah proyek TI memiliki tujuan yang jelas?",
            "Apakah proyek TI memiliki perencanaan yang terdokumentasi?",
            "Apakah tanggung jawab proyek telah ditentukan?",
            "Apakah kemajuan proyek dipantau?",
            "Apakah hasil proyek dievaluasi?"
        ],

        "BAI.2 Pengelolaan definisi kebutuhan": [
            "Apakah kebutuhan pengguna telah diidentifikasi?",
            "Apakah kebutuhan sistem didokumentasikan?",
            "Apakah kebutuhan pengguna dikonfirmasi?",
            "Apakah perubahan kebutuhan dikelola?",
            "Apakah kebutuhan sistem dievaluasi?"
        ],

        "BAI.3 Pengelolaan solusi": [
            "Apakah solusi TI dirancang berdasarkan kebutuhan pengguna?",
            "Apakah solusi TI telah diuji?",
            "Apakah solusi TI memenuhi kebutuhan organisasi?",
            "Apakah dokumentasi solusi tersedia?",
            "Apakah solusi dievaluasi setelah diterapkan?"
        ],

        "BAI.4 Ketersediaan dan kapasitas": [
            "Apakah kebutuhan kapasitas TI telah direncanakan?",
            "Apakah kapasitas sistem dipantau?",
            "Apakah ketersediaan layanan TI dipantau?",
            "Apakah terdapat tindakan ketika kapasitas tidak mencukupi?",
            "Apakah kapasitas TI dievaluasi secara berkala?"
        ],

        "BAI.5 Pengelolaan perubahan": [
            "Apakah perubahan sistem dilakukan melalui prosedur?",
            "Apakah perubahan sistem didokumentasikan?",
            "Apakah perubahan diuji sebelum diterapkan?",
            "Apakah perubahan mendapatkan persetujuan?",
            "Apakah dampak perubahan dievaluasi?"
        ]
    },

    "DSS": {
        "DSS.1 Pengelolaan operasional": [
            "Apakah operasional layanan TI telah memiliki prosedur?",
            "Apakah aktivitas operasional TI dipantau?",
            "Apakah gangguan operasional dicatat?",
            "Apakah prosedur operasional diketahui oleh pengguna?",
            "Apakah kinerja operasional dievaluasi?"
        ],

        "DSS.2 Pengelolaan permintaan dan insiden": [
            "Apakah permintaan layanan dicatat?",
            "Apakah insiden TI dicatat?",
            "Apakah insiden ditangani sesuai prosedur?",
            "Apakah waktu penyelesaian insiden dipantau?",
            "Apakah penyelesaian insiden dievaluasi?"
        ],

        "DSS.3 Pengelolaan masalah": [
            "Apakah masalah TI diidentifikasi?",
            "Apakah penyebab masalah dianalisis?",
            "Apakah masalah yang berulang dicatat?",
            "Apakah tindakan perbaikan dilakukan?",
            "Apakah masalah yang telah diselesaikan dievaluasi?"
        ],

        "DSS.4 Pengelolaan kontinuitas": [
            "Apakah organisasi memiliki rencana kontinuitas TI?",
            "Apakah risiko gangguan layanan telah diidentifikasi?",
            "Apakah prosedur pemulihan telah ditentukan?",
            "Apakah prosedur pemulihan pernah diuji?",
            "Apakah hasil pengujian kontinuitas dievaluasi?"
        ],

        "DSS.5 Pengelolaan keamanan": [
            "Apakah keamanan sistem TI diterapkan?",
            "Apakah akses pengguna dikelola?",
            "Apakah aktivitas keamanan dipantau?",
            "Apakah insiden keamanan ditangani?",
            "Apakah keamanan TI dievaluasi secara berkala?"
        ]
    },

    "MEA": {
        "MEA.1 Pemantauan kinerja": [
            "Apakah kinerja TI dipantau secara berkala?",
            "Apakah indikator kinerja TI telah ditentukan?",
            "Apakah hasil kinerja TI didokumentasikan?",
            "Apakah hasil pemantauan dilaporkan?",
            "Apakah tindakan dilakukan jika kinerja tidak sesuai target?"
        ],

        "MEA.2 Pengendalian internal": [
            "Apakah pengendalian internal TI telah diterapkan?",
            "Apakah pengendalian TI didokumentasikan?",
            "Apakah efektivitas pengendalian dipantau?",
            "Apakah kelemahan pengendalian diidentifikasi?",
            "Apakah tindakan perbaikan dilakukan?"
        ],

        "MEA.3 Kepatuhan": [
            "Apakah organisasi mematuhi kebijakan TI?",
            "Apakah kepatuhan terhadap prosedur dipantau?",
            "Apakah terdapat pemeriksaan terhadap kepatuhan TI?",
            "Apakah pelanggaran kepatuhan dicatat?",
            "Apakah tindakan perbaikan dilakukan terhadap pelanggaran?"
        ],

        "MEA.4 Evaluasi tata kelola": [
            "Apakah tata kelola TI dievaluasi secara berkala?",
            "Apakah hasil evaluasi tata kelola didokumentasikan?",
            "Apakah kelemahan tata kelola diidentifikasi?",
            "Apakah rekomendasi perbaikan dibuat?",
            "Apakah rekomendasi perbaikan ditindaklanjuti?"
        ],

        "MEA.5 Pelaporan": [
            "Apakah hasil pengelolaan TI dilaporkan?",
            "Apakah laporan TI diberikan kepada pihak yang berkepentingan?",
            "Apakah laporan TI memiliki informasi yang relevan?",
            "Apakah laporan TI dibuat secara berkala?",
            "Apakah laporan digunakan untuk evaluasi?"
        ]
    }
}


# =========================================================
# SKALA PENILAIAN 1-5
# =========================================================

skala = {
    1: "1 - Belum diterapkan",
    2: "2 - Diterapkan sebagian",
    3: "3 - Diterapkan",
    4: "4 - Diterapkan dan dievaluasi",
    5: "5 - Diterapkan secara optimal"
}


# =========================================================
# DATA RESPONDEN
# =========================================================

st.header("👤 Data Responden")

col1, col2 = st.columns(2)

with col1:

    nama = st.text_input(
        "Nama Responden *",
        placeholder="Masukkan nama"
    )

    nim = st.text_input(
        "NIM *",
        placeholder="Masukkan NIM"
    )

with col2:

    kelas = st.text_input(
        "Kelas *",
        placeholder="Contoh: SI-5A"
    )

    tanggal = st.date_input(
        "Tanggal Assessment",
        value=date.today()
    )


st.divider()


# =========================================================
# FORM ASSESSMENT
# =========================================================

st.header("📝 Assessment COBIT")

st.info(
    "Silakan pilih satu nilai untuk setiap pertanyaan. "
    "Tidak ada jawaban yang dipilih secara otomatis."
)

jawaban = {}

with st.form("form_cobit"):

    for domain, proses in pertanyaan_cobit.items():

        st.subheader(f"Domain {domain}")

        for nama_proses, daftar_pertanyaan in proses.items():

            st.markdown(f"### {nama_proses}")

            for i, pertanyaan in enumerate(
                daftar_pertanyaan,
                start=1
            ):

                key = f"{domain}_{i}_{nama_proses}"

                pilihan = st.radio(
                    pertanyaan,
                    options=list(skala.keys()),
                    format_func=lambda x: skala[x],
                    index=None,
                    key=key,
                    horizontal=True
                )

                jawaban[key] = {
                    "Domain": domain,
                    "Proses": nama_proses,
                    "Pertanyaan": pertanyaan,
                    "Nilai": pilihan
                }

                st.divider()

    submitted = st.form_submit_button(
        "📊 HITUNG PENILAIAN",
        use_container_width=True
    )


# =========================================================
# PROSES SETELAH SUBMIT
# =========================================================

if submitted:

    # =====================================================
    # VALIDASI DATA RESPONDEN
    # =====================================================

    if (
        not nama.strip()
        or not nim.strip()
        or not kelas.strip()
    ):

        st.error(
            "Data responden belum lengkap."
        )

        st.warning(
            "Nama, NIM, dan Kelas wajib diisi."
        )

        st.stop()


    # =====================================================
    # VALIDASI JAWABAN
    # =====================================================

    belum_dijawab = [
        item
        for item in jawaban.values()
        if item["Nilai"] is None
    ]

    if len(belum_dijawab) > 0:

        st.error(
            f"Masih ada {len(belum_dijawab)} pertanyaan "
            f"yang belum dijawab."
        )

        st.warning(
            "Silakan kembali ke bagian pertanyaan "
            "dan isi semua jawaban."
        )

        st.stop()


    # =====================================================
    # MEMBUAT DATAFRAME
    # =====================================================

    data = []

    for item in jawaban.values():

        data.append({
            "Domain": item["Domain"],
            "Proses": item["Proses"],
            "Pertanyaan": item["Pertanyaan"],
            "Nilai": item["Nilai"]
        })

    df = pd.DataFrame(data)


    # =====================================================
    # HITUNG NILAI KESELURUHAN
    # =====================================================

    rata_rata = df["Nilai"].mean()


    # =====================================================
    # HITUNG NILAI PER DOMAIN
    # =====================================================

    rata_domain = (
        df.groupby("Domain")["Nilai"]
        .mean()
        .reset_index()
    )

    rata_domain["Nilai"] = (
        rata_domain["Nilai"].round(2)
    )


    # =====================================================
    # KATEGORI
    # =====================================================

    if rata_rata < 2:

        kategori = "Belum diterapkan"

    elif rata_rata < 3:

        kategori = "Diterapkan sebagian"

    elif rata_rata < 4:

        kategori = "Diterapkan"

    elif rata_rata < 5:

        kategori = "Diterapkan dan dievaluasi"

    else:

        kategori = "Diterapkan secara optimal"


    # =====================================================
    # PAYLOAD UNTUK GOOGLE APPS SCRIPT
    # =====================================================

    payload = {
        "nama": nama.strip(),
        "nim": nim.strip(),
        "kelas": kelas.strip(),
        "tanggal": str(tanggal),

        "data": [
            {
                "Domain": item["Domain"],
                "Proses": item["Proses"],
                "Pertanyaan": item["Pertanyaan"],
                "Nilai": item["Nilai"]
            }

            for item in jawaban.values()
        ]
    }


    # =====================================================
    # SIMPAN KE GOOGLE SHEETS
    # =====================================================

    data_tersimpan = False

    if (
        GOOGLE_SCRIPT_URL.strip()
        and GOOGLE_SCRIPT_URL
        != "MASUKKAN_URL_APPS_SCRIPT_DI_SINI"
    ):

        try:

            with st.spinner(
                "Menyimpan data ke Google Sheets..."
            ):

                response = requests.post(
                    GOOGLE_SCRIPT_URL,
                    json=payload,
                    timeout=30
                )


            # ------------------------------------------------
            # CEK HTTP RESPONSE
            # ------------------------------------------------

            if response.status_code == 200:

                try:

                    hasil = response.json()

                except ValueError:

                    hasil = {
                        "status": "error",
                        "message": (
                            "Respons Google Apps Script "
                            "bukan JSON."
                        )
                    }


                # --------------------------------------------
                # CEK STATUS DARI APPS SCRIPT
                # --------------------------------------------

                if hasil.get("status") == "success":

                    data_tersimpan = True

                else:

                    st.error(
                        "❌ Google Apps Script mengembalikan error."
                    )

                    st.code(
                        response.text,
                        language="text"
                    )

            else:

                st.error(
                    f"❌ Gagal mengirim data ke Google Sheets.\n\n"
                    f"HTTP Status: {response.status_code}"
                )

                st.code(
                    response.text,
                    language="text"
                )


        except requests.exceptions.Timeout:

            st.error(
                "⏱️ Waktu koneksi habis (timeout). "
                "Google Apps Script tidak merespons dalam 30 detik."
            )


        except requests.exceptions.RequestException as e:

            st.error(
                "❌ Tidak dapat terhubung ke Google Apps Script."
            )

            st.code(
                str(e),
                language="text"
            )


        except Exception as e:

            st.error(
                "❌ Terjadi kesalahan saat menyimpan data."
            )

            st.code(
                str(e),
                language="text"
            )

    else:

        st.warning(
            "⚠️ URL Google Apps Script belum diatur."
        )

        st.info(
            "Assessment tetap dihitung, tetapi "
            "belum dikirim ke Google Sheets."
        )


    # =====================================================
    # STATUS PENYIMPANAN
    # =====================================================

    st.divider()

    if data_tersimpan:

        st.success(
            "✅ Assessment berhasil dihitung "
            "dan disimpan ke Google Sheets."
        )

    else:

        st.success(
            "Assessment berhasil dihitung."
        )


    # =====================================================
    # HASIL ASSESSMENT
    # =====================================================

    st.header("📊 Hasil Assessment")


    # -----------------------------------------------------
    # INFORMASI RESPONDEN
    # -----------------------------------------------------

    st.write(
        f"**Nama Responden:** {nama}"
    )

    st.write(
        f"**NIM:** {nim}"
    )

    st.write(
        f"**Kelas:** {kelas}"
    )

    st.write(
        f"**Tanggal Assessment:** {tanggal}"
    )


    st.divider()


    # =====================================================
    # NILAI UTAMA
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Nilai Rata-rata",
            f"{rata_rata:.2f}"
        )

    with col2:

        st.metric(
            "Jumlah Pertanyaan",
            len(df)
        )

    with col3:

        st.metric(
            "Skor Maksimal",
            "5.00"
        )


    # =====================================================
    # INTERPRETASI
    # =====================================================

    st.info(
        f"**Kategori hasil assessment: {kategori}**"
    )


    # =====================================================
    # NILAI SETIAP DOMAIN
    # =====================================================

    st.subheader(
        "📌 Nilai Setiap Domain"
    )

    st.dataframe(
        rata_domain,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # GRAFIK
    # =====================================================

    st.subheader(
        "📈 Grafik Nilai per Domain"
    )

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )

    ax.bar(
        rata_domain["Domain"],
        rata_domain["Nilai"]
    )

    ax.set_ylim(0, 5)

    ax.set_xlabel(
        "Domain COBIT"
    )

    ax.set_ylabel(
        "Nilai Rata-rata"
    )

    ax.set_title(
        "Hasil Assessment COBIT per Domain"
    )

    for i, nilai in enumerate(
        rata_domain["Nilai"]
    ):

        ax.text(
            i,
            nilai + 0.05,
            f"{nilai:.2f}",
            ha="center"
        )

    st.pyplot(fig)


    # =====================================================
    # DETAIL JAWABAN
    # =====================================================

    st.subheader(
        "📋 Detail Jawaban"
    )

    df_tampil = df.copy()

    df_tampil["Nilai"] = (
        df_tampil["Nilai"].astype(int)
    )

    st.dataframe(
        df_tampil,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # DOWNLOAD CSV
    # =====================================================

    csv = df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Hasil Assessment (CSV)",
        data=csv,
        file_name=f"assessment_{nim}.csv",
        mime="text/csv",
        use_container_width=True
    )


    # =====================================================
    # CATATAN
    # =====================================================

    st.warning(
        "Hasil assessment merupakan hasil berdasarkan "
        "jawaban responden dan bukan temuan audit yang "
        "telah diverifikasi."
    )