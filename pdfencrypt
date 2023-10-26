import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
import numpy as np
import cv2
from PIL import Image
import io
import tempfile
import os

def blur_region(pdf_path, output_path, page_number, rect_coordinates):
    # Open the PDF file
    pdf_reader = PdfReader(pdf_path)

    # Create a PDF writer
    pdf_writer = PdfWriter()

    # Get the specified page
    page = pdf_reader.pages[page_number - 1]

    # Get the page dimensions
    width, height = int(page.mediaBox[2]), int(page.mediaBox[3])

    # Print dimensions for debugging
    # print("Width:", width)
    # print("Height:", height)

    if width > 0 and height > 0:
        # Use PyMuPDF to open the PDF and extract the image
        pdf_document = fitz.open(pdf_path)
        pdf_page = pdf_document[page_number - 1]
        img = pdf_page.getPixmap()
        print(img)
        # Convert the image to a NumPy array
        img_array = np.frombuffer(img.samples, dtype=np.uint8)

        # Make a copy of the array to avoid read-only issues
        img_array = img_array.copy()

        # Reshape the array considering RGB channels
        img_array = img_array.reshape((height, width, 3))

        # Define the region to blur
        x1, y1, x2, y2 = rect_coordinates
        region_to_blur = img_array[y1:y2, x1:x2, :].copy()
        region_to_blur = cv2.GaussianBlur(region_to_blur, (55, 55), 0)
        
        # img_pixmap = fitz.getPixmap(img_array.tobytes())
        # Apply Gaussian blur to RGB channels

        # Replace the original region with the blurred region
        image1 = Image.fromarray(region_to_blur)
        image1.save("output_image1.png")
        
        # pdf_page.drawRect((x1, y1, x2, y2), fill = 0, color = 0)
        # pdf_page.insertImage(rect_coordinates, pixmap = img)
        # rect = fitz.Rect(0, 0, 250, 250)
        pdf_page.insertImage(rect_coordinates, filename="output_image1.png")
        
        os.remove("output_image1.png")
        pdf_document.save(output_path)


    else:
        print("Invalid dimensions for the page. Check the dimensions.")

if __name__ == "__main__":
    pdf_path = "D:\\encrypt\\1.pdf"
    output_path = "D:\\encrypt\\processed\\blurred_example18.pdf"
    page_number = 4
    # rect_coordinates = (250, 505, 480, 555)
    rect_coordinates = (225, 502, 495, 558)

    blur_region(pdf_path, output_path, page_number, rect_coordinates)
