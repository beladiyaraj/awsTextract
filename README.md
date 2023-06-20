# Asynchronous PDF to CSV Extraction

This project enables the extraction of data from PDF files and converts them into CSV format. It utilizes AWS Textract, AWS Lambda, and AWS S3 services to automate the extraction process.

## Project Overview

The goal of this project is to extract data from PDF files and save it in CSV format for easy analysis and further processing. The extraction is performed asynchronously using AWS Textract, which accurately extracts text and data from scanned documents.

## Usage

1. **Upload PDF Files:** Place the PDF files in the designated location.
2. **Extraction Process:** The system will automatically trigger the extraction process.
3. **CSV Output:** Extracted data will be saved in CSV format for each PDF file.
4. **Accessing Results:** Retrieve the CSV files for further analysis and use.

## Requirements

- AWS Account with necessary permissions.
- AWS CLI installed and configured.
- Node.js installed for deploying AWS Lambda functions.

## Resources

- [AWS Textract](https://aws.amazon.com/textract/): Service for extracting data from scanned documents.
- [AWS Lambda](https://aws.amazon.com/lambda/): Serverless compute service to run code without managing servers.
- [AWS S3](https://aws.amazon.com/s3/): Scalable object storage service for storing data.

## Contributing

Contributions are welcome! If you encounter issues or have suggestions, please open an issue on the GitHub repository.

