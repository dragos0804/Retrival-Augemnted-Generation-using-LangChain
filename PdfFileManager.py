import fitz  # PyMuPDF for converting the pages of the PDF into images
import os
import shutil  # For removing directories
import pandas as pd
import re

class PdfFileManager:
    """
    Creates an object that contains all the data from a given pdf, separated and processed
    """
    def __init__(self, pdf_path):
        """
        Constructor used for to initialize the members of the class.
        """
        self.pdf_path = pdf_path

        # Create directories for the output data (if they do not exist)
        self.output_dir = 'output'
        self.text_output_path = os.path.join(self.output_dir, 'pdf_text.txt')
        self.graph_output_dir = os.path.join(self.output_dir, 'graphs')
        self.pages_output_dir = os.path.join(self.output_dir, 'pages_as_images')

        # Clear and recreate output directory (in order to ensure that every time a new pdf is uploaded, we start with no trailing information from previous pdf files)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.graph_output_dir, exist_ok=True)
        os.makedirs(self.pages_output_dir, exist_ok=True)
        
        # Call methods to extract data
        self.extract_text()
        self.convert_pdf_to_images()

    def get_text(self):
        """
            Reads and returns the extracted text from the saved text file.
        """
        with open(self.text_output_path, 'r', encoding='utf-8') as text_file:
            return text_file.read()
        
        """
        Reads all graph data saved as CSV files and returns them in a list of DataFrames.
        """
        graph_dataframes = []
        for csv_file in os.listdir(self.graph_output_dir):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(self.graph_output_dir, csv_file)
                df = pd.read_csv(csv_path)
                graph_dataframes.append(df)
        return graph_dataframes
    
    def clean_text(self, text):
        """
        Convert text to lowercase, remove newlines,
        and reduce multiple spaces to a single space.

        Args:
        - text (str): The text to be cleaned.

        Returns:
        - str: The cleaned text.
        """
        # Convert to lowercase
        cleaned_text = text.lower()
        
        # Remove newlines
        cleaned_text = cleaned_text.replace('\n', ' ')
        
        # Use regex to replace multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Strip leading and trailing spaces
        cleaned_text = cleaned_text.strip()

        return cleaned_text

    def extract_text(self):
        """
        Extracts text from the PDF and saves into a file.
        """
        document = fitz.open(self.pdf_path)
        paragraphs = []

        for page_num in range(len(document)):
            page = document.load_page(page_num)

            # Extract the text blocks from the page
            blocks = page.get_text("dict")["blocks"]
            
            # Iterate through the blocks
            for block in blocks:
                if "lines" in block:  # Ensure it's a text block (not an image or any other object)
                    paragraph = ""
                    for line in block["lines"]:
                        for span in line["spans"]:
                            paragraph += span["text"]  # Collect the text from each span

                        paragraph += " "  # Add a space when iteration over a line inside a block is done
                    paragraphs.append(paragraph.strip())  # Add cleaned paragraph

        # Combine all paragraphs into a single text string
        combined_text = " ".join(paragraphs)  # Join paragraphs with a single space
        
        # Clean the combined text
        cleaned_text = self.clean_text(combined_text)

        # Save the cleaned text to a file without extra newlines
        with open(self.text_output_path, 'w', encoding='utf-8') as text_file:
            text_file.write(cleaned_text)  # Write the cleaned text directly
        document.close()

    def convert_pdf_to_images(self):
        """
        Converts each page of a PDF into JPEG images and saves them in a directory named after the PDF file.
        """
        # Create a directory based on the PDF filename
        document = fitz.open(self.pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            image_path = os.path.join(self.pages_output_dir, f'page_{page_num + 1}.jpg')
            pix.save(image_path)  # Save as JPEG
        document.close()