import streamlit as st
import PyPDF2
import pyttsx3
import pdfplumber

# Function to convert PDF to audio
def convert_to_audio(pdf_file):
    final_text = ""

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                final_text += text

    if not final_text.strip():
        return None, "No text found in the PDF."

    # Convert text to audio
    engine = pyttsx3.init()
    audio_file = 'audiobook.mp3'
    engine.save_to_file(final_text, audio_file)
    engine.runAndWait()

    return audio_file, None

# Streamlit UI
st.title("PDF to Audio Converter")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("File Uploaded: ", uploaded_file.name)

    if st.button("Convert to Audio"):
        audio_file, error = convert_to_audio(uploaded_file)

        if error:
            st.error(error)
        else:
            st.success("Audio has been saved as 'audiobook.mp3'.")
            st.audio(audio_file, format='audio/mp3')

            # Allow downloading the audio file
            with open(audio_file, 'rb') as f:
                st.download_button("Download Audiobook", data=f, file_name="audiobook.mp3", mime="audio/mp3")
