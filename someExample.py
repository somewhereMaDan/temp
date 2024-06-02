import os
import subprocess
import streamlit as st

# Function to convert Word file to PDF using LibreOffice
def convert_to_pdf(uploaded_file):
    # Save uploaded file
    temp_docx_path = os.path.join("/tmp", uploaded_file.name)
    with open(temp_docx_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    # Convert Word to PDF using LibreOffice
    temp_pdf_path = temp_docx_path.replace('.docx', '.pdf')
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', os.path.dirname(temp_docx_path), temp_docx_path])
    
    return temp_pdf_path

# Streamlit app
def main():
    st.title("Word to PDF Converter")

    uploaded_file = st.file_uploader("Choose a Word file", type=["docx"])

    if uploaded_file:
        converted_pdf_path = convert_to_pdf(uploaded_file)
        st.success("Conversion successful!")

        with open(converted_pdf_path, 'rb') as f:
            pdf_bytes = f.read()

        # Provide a download link for the PDF file
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="converted.pdf",
            mime="application/pdf"
        )

        # Optionally, clean up temporary files
        os.remove(temp_docx_path)
        os.remove(converted_pdf_path)

if __name__ == "__main__":
    main()
