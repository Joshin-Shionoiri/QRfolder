import os
import shutil

def organize_file(pdf_path, qr_text, output_dir):
    if not qr_text or "-" not in qr_text:
        return False
    venue, number = qr_text.split("-")
    folder = os.path.join(output_dir, venue)
    os.makedirs(folder, exist_ok=True)
    new_name = f"{number}.pdf"
    shutil.move(pdf_path, os.path.join(folder, new_name))
    return True
