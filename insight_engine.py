import os
import sys
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader

# Load environment configuration
load_dotenv()

class PDFInsightEngine:
    """
    A robust RAG (Retrieval-Augmented Generation) pipeline for extracting
    insights from unstructured PDF documents using Google's Gemini API.
    """
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.client = None
        self.active_model = None
        
        # Initialize connection on instantiation
        self._initialize_client()

    def _initialize_client(self):
        """Authenticates with the Gemini API and selects the optimal model."""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("Critical Error: GEMINI_API_KEY is missing from .env file.")
            sys.exit(1)
            
        try:
            self.client = genai.Client(api_key=api_key)
            self.active_model = self._resolve_model_version()
            print(f"AI Core Online: Connected to {self.active_model}")
        except Exception as e:
            print(f"Connection Failed: {e}")
            sys.exit(1)

    def _resolve_model_version(self):
        """
        Dynamically selects the best available model version.
        Prioritizes Flash 2.0/1.5 for speed, falls back to Pro for stability.
        """
        priority_queue = [
            "gemini-1.5-flash",  # <--- Put this FIRST
            "gemini-2.0-flash",
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]

        try:
            # Fetch all available models associated with the API key
            available_models = {
                m.name.replace("models/", "") 
                for m in self.client.models.list()
            }
            
            # Match against priority list
            for model in priority_queue:
                if model in available_models:
                    return model
            
            # Fallback: Find any model that supports content generation
            print("Preferred models unavailable. Auto-detecting fallback...")
            for m in self.client.models.list():
                if "generateContent" in (m.supported_generation_methods or []):
                    return m.name.replace("models/", "")
                    
        except Exception as e:
            print(f"Model resolution warning: {e}. Defaulting to 'gemini-1.5-flash'.")
            
        return "gemini-1.5-flash"

    def ingest_document(self):
        """Parses PDF content into a clean text stream."""
        print(f"--- [SYSTEM] Ingesting '{self.pdf_path}' ---")
        
        if not os.path.exists(self.pdf_path):
            print(f"File Not Found: {self.pdf_path}")
            return False

        try:
            reader = PdfReader(self.pdf_path)
            extracted_pages = []
            
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_pages.append(text)
            
            self.raw_text = "\n".join(extracted_pages)
            print(f"Ingestion Complete: {len(extracted_pages)} pages processed.")
            return True
            
        except Exception as e:
            print(f"Parsing Error: {e}")
            return False

    def generate_executive_brief(self):
        """Synthesizes a structured executive summary from the raw text."""
        if not self.raw_text:
            return "Error: No document content loaded."

        print("\n--- [AI ANALYST] Synthesizing Executive Brief... ---")
        
        prompt_structure = f"""
        ROLE: Senior Financial Analyst
        TASK: Synthesize the provided document into a structured Executive Brief.
        
        REQUIRED SECTIONS:
        1.Financial Performance (Revenue, Margins, Growth)
        2.Critical Risks (Operational, Supply Chain, Regulatory)
        3.Strategic Outlook (Future Goals, R&D, Expansion)

        SOURCE MATERIAL:
        {self.raw_text[:40000]}  # Context window safety limit
        """

        try:
            response = self.client.models.generate_content(
                model=self.active_model,
                contents=prompt_structure
            )
            return response.text
        except Exception as e:
            return f"Generation Failed: {e}"

    def query_document(self, user_query):
        """Context-aware Q&A engine for specific document queries."""
        context_prompt = f"""
        CONTEXT: You are an expert analyst reviewing the document below.
        INSTRUCTION: Answer the user's question using ONLY the provided text. Cite specific figures.
        
        DOCUMENT:
        {self.raw_text[:40000]}
        
        QUESTION: {user_query}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.active_model,
                contents=context_prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Query Error: {e}"

# --- APP ENTRY POINT ---
if __name__ == "__main__":
    print("\n===========================================")
    print("   INTELLIGENT DOCUMENT INSIGHT ENGINE")
    print("===========================================")

    target_file = "financial_report.pdf"

    # Initialize Engine
    engine = PDFInsightEngine(target_file)

    # Execution Flow
    if engine.ingest_document():
        # Phase 1: Automated Summary
        summary = engine.generate_executive_brief()
        print("\n" + "="*40)
        print("EXECUTIVE SUMMARY")
        print("="*40)
        print(summary)

        # Phase 2: Interactive Session
        print("\n" + "-"*40)
        print("Interactive Mode Active (Type 'exit' to quit)")
        
        while True:
            query = input("\nAsk a specific question: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("Shutting down insight engine. Goodbye.")
                break
                
            if not query:
                continue

            print(">> Analyzing context...")
            answer = engine.query_document(query)
            print(f"\n💡 INSIGHT: {answer}")