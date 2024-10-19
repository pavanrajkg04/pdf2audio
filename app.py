import streamlit as st
import PyPDF3
import pyttsx3
import pdfplumber
import os

# Function to convert PDF to audio
def convert_pdf_to_audio(pdf_file):
    try:
        # Read the PDF file as bytes
        pdf_reader = PyPDF3.PdfFileReader(pdf_file)
        pages = pdf_reader.numPages
        final_text = ""

        # Extract text from each page
        with pdfplumber.open(pdf_file) as pdf:
            for i in range(pages):
                page = pdf.pages[i]
                text = page.extract_text()
                if text:
                    final_text += text

        if not final_text.strip():
            return None, "Error: No text found in the PDF."

        # Convert text to audio
        engine = pyttsx3.init()
        audio_file = 'audiobook.mp3'
        engine.save_to_file(final_text, audio_file)
        engine.runAndWait()

        return audio_file, "Success: Audio has been saved as 'audiobook.mp3'."

    except Exception as e:
        return None, f"Error: {str(e)}"

# Streamlit app
def main():
    st.title("PDF to Audio Converter")

    # File uploader
    pdf_file = st.file_uploader("Upload PDF to convert", type=["pdf"])

    if pdf_file is not None:
        # Convert PDF to audio when the button is clicked
        if st.button("Convert"):
            with st.spinner("Converting..."):
                audio_file, result = convert_pdf_to_audio(pdf_file)
            st.success(result)

            # Provide a link to download the audio file
            if audio_file:
                st.markdown("[Download Audio](audiobook.mp3)", unsafe_allow_html=True)

                # Play the audio file
                st.audio(audio_file)

if __name__ == "__main__":
    main()
