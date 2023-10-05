import PyPDF2
import re
import os
import glob
import configparser

# Initialize the configuration parser
config = configparser.ConfigParser()
config.read('config.conf')  # Update the file path as needed

# Read the download directory from the configuration
download_dir = config.get('General', 'download_dir')

# List all PDF files in the directory (including subdirectories)
pdf_files = glob.glob(os.path.join(download_dir, '**', '*.pdf'), recursive=True)

# Sort the PDF files by modification time to get the most recent one
if pdf_files:
    most_recent_pdf = max(pdf_files, key=os.path.getmtime)
else:
    print("No PDF files found in the specified directory.")

# Replace 'input.pdf' with the path to your input PDF file
input_pdf_path = most_recent_pdf

# Open the input PDF file
pdf_file = open(input_pdf_path, 'rb')

# Create a PDF reader object using PdfReader
pdf_reader = PyPDF2.PdfReader(pdf_file)

# Create a folder to store the output PDFs
output_folder = 'output_pdfs'
os.makedirs(output_folder, exist_ok=True)

# Define a regular expression to match employee names
employee_name_pattern = re.compile(r'Nama\s+(.*?)\n')

# Define a regular expression to match the month and year
month_year_pattern = re.compile(r'Bulan (\w+) (\d{4})')

# Iterate through each page in the PDF
for page_num, page in enumerate(pdf_reader.pages):
    # Extract text content from the current page
    text_content = page.extract_text()
    
    # Use regex to find the employee name
    match_name = employee_name_pattern.search(text_content)
    
    # Use regex to find the month and year
    match_month_year = month_year_pattern.search(text_content)
    
    if match_name and match_month_year:
        # Extract the employee name and clean it up for use in the output file name
        employee_name = match_name.group(1).strip()
        employee_name = ''.join(char for char in employee_name if char.isalnum() or char.isspace())
        
        # Extract the month and year
        month = match_month_year.group(1)
        year = match_month_year.group(2)
        
        # Generate a file name based on employee name, month, and year
        file_name = f'SlipGaji - {month} {year} - {employee_name}.pdf'
        
        # Construct the output PDF file path
        output_pdf_path = os.path.join(output_folder, file_name)
        
        # Create a PDF writer for the current page
        output_pdf = PyPDF2.PdfWriter()
        output_pdf.add_page(page)
        
        # Write the current page to the output PDF file
        with open(output_pdf_path, 'wb') as output_file:
            output_pdf.write(output_file)

# Close the input PDF file
pdf_file.close()
