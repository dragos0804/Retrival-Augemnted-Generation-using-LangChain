# Given Task

You will be given a PDF document that contains both textual and graphical data. Your task is to:

* Extract the textual and graphical information from the PDF pages.
* Convert the extracted graphical data (such as charts or graphs) into a structured, queryable format.
* Implement a system where users can ask questions and receive meaningful responses based on the extracted data.


Requirements:
* Document your approach and display your results in a Jupyter notebook (.ipynb)
* Your solution should allow users to query both the extracted text and any data that was derived from the graphical elements (such as tables).
* Provide brief explanations of your approach, choices made, and any challenges you encountered.
<hr>

# PDF Data Extraction and Query System

This project implements a system for extracting and querying both textual and graphical data from PDF documents. The solution provides two different approaches to handle PDF data extraction and user queries.

## Project Structure

```
├── input/                  # Directory for input PDF files
├── output/                 # Directory for extracted data
├── models/                 # Contains attempted models for graphical data extraction
├── PdfFileManager.py       # Custom class for PDF data handling
├── solution.ipynb         # Main solution notebook
└── environment.yaml       # Conda environment configuration
```

## Approaches

### Approach 1: Direct PDF Processing with RAG
The first approach uses a straightforward method that:
1. Processes the PDF directly using UnstructuredPDFLoader
2. Creates embeddings using HuggingFaceEmbeddings
3. Implements a RAG (Retrieval-Augmented Generation) system using:
   - Langchain for document processing
   - Mistral-7B-Instruct-v0.2 as the language model
   - FAISS for vector storage and retrieval

This approach proved effective at interpreting both textual content and statistical data from text-based and SVG-based charts.

### Approach 2: Manual Extraction Pipeline
The second approach implements a more detailed extraction pipeline using:
1. Custom PdfFileManager class for:
   - Text extraction
   - Page-to-image conversion
   - Output management
2. Same RAG system as Approach 1 but applied to manually extracted content

## Key Components

### PdfFileManager Class
- Handles PDF processing and data extraction
- Creates organized output directory structure
- Implements text cleaning and processing
- Converts PDF pages to images for potential graphical analysis

### Machine Learning Models
The project experimented with two models for graphical data extraction:
- Donut model (naver-clova-ix/donut-base-finetuned-docvqa)
- GPT-Vision-1-ft
However, these were not used in the final implementation due to limitations in accurately extracting graphical data.

## Dependencies
All required dependencies are listed in the environment.yaml file. To set up the environment:
```bash
conda env create -f _ECMX_.yaml
```

## Key Libraries
- langchain: For document processing and RAG implementation
- PyMuPDF (fitz): For PDF processing
- HuggingFace transformers: For embeddings and language model
- FAISS: For vector storage and similarity search

## Implementation Notes

### Text Processing
- Implements thorough text cleaning and normalization
- Handles PDF text extraction with proper formatting
- Maintains structural integrity of extracted content

### Query System
- Uses RetrievalQA chain for processing queries
- Implements similarity search for relevant context retrieval
- Provides natural language responses to user queries

### Limitations
- While the system successfully handles text and SVG-based charts, manual extraction of complex graphical data remains a challenge
- The attempted use of vision models for chart interpretation was not successful
- Future improvements could include implementing specialized chart recognition systems

## Future Improvements
- Implementation of chart segmentation network
- Integration with GPT-4 Vision for better chart interpretation
- Enhanced graph data extraction capabilities
- Improved queryable format for graphical data

## Usage
1. Place PDF files in the input/ directory
2. Run the notebook cells sequentially
3. Use the query system to ask questions about the document content

The system can handle various types of queries about both textual content and basic statistical information present in the documents.
