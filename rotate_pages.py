import fitz  # PyMuPDF
import argparse
import os

def rotate_even_pages(pdf_path, output_path):
    try:
        doc = fitz.open(pdf_path)  # Open the PDF file

        for page_number in range(len(doc)):
            if (page_number + 1) % 2 == 0:  # Check if the page is even
                doc[page_number].set_rotation(180)  # Rotate 180 degrees

        doc.save(output_path)  # Save the modified PDF
        doc.close()
        print(f"Successfully rotated even pages in {pdf_path} and saved to {output_path}")
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        if 'doc' in locals():
            doc.close()

def main():
    parser = argparse.ArgumentParser(description='Rotate even pages of a PDF file by 180 degrees')
    parser.add_argument('input_pdf', help='Path to the input PDF file')
    parser.add_argument('--output', '-o', help='Path for the output PDF file (default: input_rotated.pdf)')
    
    args = parser.parse_args()
    
    # If output path is not specified, create a default one
    if not args.output:
        base_name = os.path.splitext(args.input_pdf)[0]
        args.output = f"{base_name}_rotated.pdf"
    
    rotate_even_pages(args.input_pdf, args.output)

if __name__ == "__main__":
    main()
