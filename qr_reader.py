import fitz  # PyMuPDF
from PIL import Image
from pyzbar.pyzbar import decode
import os
import shutil

def pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    img_path = pdf_path.replace(".pdf", ".png")
    pix.save(img_path)
    return img_path

def read_qr(image_path):
    img = Image.open(image_path)
    qr_data = decode(img)
    if qr_data:
        return qr_data[0].data.decode("utf-8")  # 例: "JUKU001-0001"
    return None

def organize_file(pdf_path, qr_text, output_dir):
    if not qr_text or "-" not in qr_text:
        return False
    venue, number = qr_text.split("-")
    folder = os.path.join(output_dir, venue)
    os.makedirs(folder, exist_ok=True)
    new_name = f"{number}.pdf"
    shutil.move(pdf_path, os.path.join(folder, new_name))
    return True

def process_all_pdfs(input_dir, output_dir, log_box=None):
    count = 0
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, file)
            try:
                img_path = pdf_to_image(pdf_path)
                qr_text = read_qr(img_path)
                success = organize_file(pdf_path, qr_text, output_dir)
                os.remove(img_path)
                count += 1
                if log_box:
                    msg = f"{file} → {qr_text if success else 'QR読み取り失敗'}\n"
                    log_box.insert("end", msg)
            except Exception as e:
                if log_box:
                    log_box.insert("end", f"{file} → エラー: {str(e)}\n")
    return count
