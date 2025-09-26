import fitz  # PyMuPDF

def pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img_path = pdf_path.replace(".pdf", ".png")
    pix.save(img_path)
    return img_path
