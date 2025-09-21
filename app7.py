import streamlit as st
import google.generativeai as genai
import PyPDF2
import os

# === Streamlit UI ===
st.set_page_config(page_title="Chatbot Belajar Koding & AI", page_icon="🤖")

st.title("🤖 Chatbot Belajar Koding & AI")
st.write("Halo! Chatbot ini menggunakan materi dari beberapa PDF yang sudah disiapkan 👇")

# === Input API Key di Sidebar ===
st.sidebar.header("🔑 Konfigurasi")
api_key = st.sidebar.text_input("Masukkan API Key Google AI:", type="password")

# === Setup Model Gemini jika API key tersedia ===
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    st.warning("Silakan masukkan API Key di sidebar untuk mulai menggunakan chatbot.")
    st.stop()

# === Session state ===
if "materi_full" not in st.session_state:
    st.session_state.materi_full = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# === Baca semua PDF dari folder ===
PDF_FOLDER = "materi/"   # semua file PDF disimpan di folder ini

if not st.session_state.materi_full:
    all_text = ""
    if os.path.exists(PDF_FOLDER):
        for filename in os.listdir(PDF_FOLDER):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(PDF_FOLDER, filename)
                with open(pdf_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        if text:
                            all_text += text + "\n"

    st.session_state.materi_full = all_text

# === Input User ===
user_input = st.text_input("Ketik pertanyaanmu di sini:", "")

if st.button("Kirim") and user_input:
    try:
        if st.session_state.materi_full:
            prompt = f"""
            Berikut adalah materi pembelajaran (gabungan dari beberapa PDF):

            {st.session_state.materi_full}

            Pertanyaan: {user_input}

            Jawablah pertanyaan dengan mengacu pada materi di atas jika relevan.
            """
        else:
            prompt = user_input

        response = model.generate_content(prompt)
        bot_reply = response.text

        # Simpan ke history
        st.session_state.chat_history.append(("👨‍💻 Kamu", user_input))
        st.session_state.chat_history.append(("🤖 Chatbot", bot_reply))

    except Exception as e:
        st.error(f"Terjadi error: {e}")

# === Tampilkan riwayat chat ===
for role, msg in st.session_state.chat_history:
    if role == "👨‍💻 Kamu":
        st.markdown(f"**{role}:** {msg}")
    else:
        st.markdown(
            f"<div style='background-color:#f1f1f1;padding:10px;border-radius:8px'><b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
