import os
from PyPDF2 import PdfReader, PdfWriter


def merge_pdfs(folder_path, output):
    pdf_writer = PdfWriter()

    # List all files in the folder and filter for PDFs
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.PDF')]
    pdf_files.sort()  # Optional: sort files if order matters

    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        pdf_reader = PdfReader(pdf_path)
        for page in range(len(pdf_reader.pages)):
            # Add each page to the writer object
            pdf_writer.add_page(pdf_reader.pages[page])

    # Write out the merged PDF to the specified output path
    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
    # Folder containing PDF files
    folder_path = 'data'
    # Output merged PDF
    output = 'merged.pdf'

    merge_pdfs(folder_path, output)
