import fitz  # PyMuPDF
import docx
import io

def extract_text(uploaded_file):
    text = ""

    if uploaded_file.name.endswith(".pdf"):
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")

    return text