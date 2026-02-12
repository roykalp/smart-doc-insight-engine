# Intelligent Document Insight Generator
A GenAI-powered RAG pipeline that transforms unstructured PDF reports into actionable business intelligence. Automates extraction, summarization, and natural language querying using Google's Gemini Models.

# 🧠 Automated RAG Insight Pipeline

###  Overview 
This project automates the manual, labor-intensive process of reviewing complex financial and technical documents. Instead of relying on human reading speed, I built a scalable Retrieval-Augmented Generation (RAG) Pipeline  capable of ingesting multi-page PDF reports and generating executive-level insights in seconds.

The core objective was to build a system that is  context-aware  and capable of handling "unstructured" data, bridging the gap between raw static files (PDFs) and dynamic intelligence (LLMs).

###  Key Features 
Dynamic Model Resolution:Implemented a "Smart Fallback" mechanism. The system prioritizes high-speed models (`gemini-1.5-flash`) for low latency but automatically switches to robust models (`gemini-1.5-pro`) if rate limits or API errors are detected.
Context-Aware Q&A:Solved the "Keyword Search" limitation by integrating semantic understanding. Users can ask natural questions (e.g.,  "Why did the profit margin drop?" ) and receive citation-backed answers.
Automated Synthesis:Generates structured "Executive Briefs" instantly, categorizing insights into Financial Highlights, Operational Risks, and Strategic Outlooks.
Synthetic Data Testing:Includes a custom  Test Fixture Generator  that produces realistic financial reports on the fly, allowing for rigorous pipeline testing without exposing sensitive real-world data.
Enterprise Security:Enforces environment variable isolation for API keys, preventing credential leakage in version control.

###  Tech Stack 
Language: Python 3.10+
AI Model: Google Gemini 1.5 Flash / Pro (via `google-genai`)
Document Processing: PyPDF
Environment Management: Python Dotenv
Test Data Generation: FPDF

###  The Architecture (RAG Flow) 
1.   Ingest:  Pipeline uses `pypdf` to parse binary PDF files and extract raw text streams.
2.   Contextualize:    Sanitizes text to remove artifacts.
      Fits content into the LLM's context window (optimized for 30k-1M tokens).
3.   Inference: 
      System selects the optimal Gemini model based on availability.
      Injects "Senior Analyst" persona prompts to guide the output.
4.   Insight:  Delivers structured summaries or interactive Q&A responses to the user console.

### ⚙️ How to Run Locally

1.   Clone the repository 
    ```bash
    git clone [https://github.com/roykalp/intelligent-doc-insight-generator.git](https://github.com/roykalp/intelligent-doc-insight-generator.git)
    cd intelligent-doc-insight-generator
    ```

2.   Set Up Environment 
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```ini
    GEMINI_API_KEY=your_api_key_here
    ```

3.   Install dependencies 
    Install the required Python libraries using the requirements file:
    ```bash
    pip install -r requirements.txt
    ```
     (Dependencies: `google-genai`, `pypdf`, `python-dotenv`, `fpdf`) 

4.   Run the Insight Engine 
    First, generate a test document, then run the analysis pipeline:
    ```bash
    # Step 1: Generate a dummy financial report
    python create_dummy_pdf.py

    # Step 2: Launch the Engine
    python insight_engine.py
    ```

5.   View Results 
       Executive Summary:  The terminal will display a structured 3-part brief of the document.
       Interactive Mode:  You can type questions like  "What is the primary risk?"  to chat with the document.

###  Output 
_Automated executive summary generated from a raw financial PDF:_
=== EXECUTIVE SUMMARY ===
1. Financial Highlights: Record revenue of $12.5M (+15% YoY).
2. Operational Risks: Supply chain disruption in semiconductor division.
3. Strategic Outlook: Heavy investment in AI R&D impacting short-term margins.
Author: Kalpataru Roy
