import streamlit as st
import base64
import os
import requests
import tempfile

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

def download_external_pdf(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Create server's uploaded_docs directory if it doesn't exist
        sample_pdfs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                      "server", "uploaded_docs")
        os.makedirs(sample_pdfs_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(sample_pdfs_dir, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return file_path
    except Exception as e:
        st.sidebar.error(f"Failed to download PDF: {str(e)}")
        return None

def render_sample_pdf_download():
    st.sidebar.markdown("### 📄 Sample PDFs for Testing")
    st.sidebar.markdown("Download sample medical PDFs to test the system:")
    
    # External PDF from NCERT
    ncert_url = "https://ncert.nic.in/vocational/pdf/kevt103.pdf"
    ncert_filename = "kevt103.pdf"
    
    # Check if the NCERT PDF already exists
    sample_pdfs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                  "server", "uploaded_docs")
    ncert_file_path = os.path.join(sample_pdfs_dir, ncert_filename)
    
    if not os.path.exists(ncert_file_path):
        if st.sidebar.button("Download NCERT Vocational PDF"):
            with st.sidebar.spinner("Downloading NCERT PDF..."):
                file_path = download_external_pdf(ncert_url, ncert_filename)
                if file_path:
                    st.sidebar.success(f"Downloaded {ncert_filename}")
    else:
        st.sidebar.markdown(
            get_binary_file_downloader_html(ncert_file_path, "NCERT Vocational PDF"),
            unsafe_allow_html=True
        )
    
    # Get paths to other sample PDFs in the server's uploaded_docs folder
    if os.path.exists(sample_pdfs_dir):
        pdf_files = [f for f in os.listdir(sample_pdfs_dir) if f.endswith('.pdf') and f != ncert_filename]
        
        if pdf_files:
            st.sidebar.markdown("### Other Available PDFs:")
            for pdf_file in pdf_files:
                pdf_path = os.path.join(sample_pdfs_dir, pdf_file)
                st.sidebar.markdown(
                    get_binary_file_downloader_html(pdf_path, pdf_file),
                    unsafe_allow_html=True
                )
        else:
            st.sidebar.info("No other sample PDFs available.")
    else:
        st.sidebar.warning("Sample PDFs directory not found.")