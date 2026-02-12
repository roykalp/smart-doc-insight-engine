import sys
from fpdf import FPDF

def generate_test_fixture(filename="financial_report.pdf"):
    """
    Generates a synthetic Q3 Financial Report PDF.
    Used as a test fixture for the RAG ingestion pipeline.
    """
    print(f"--- [SYSTEM] Generating Test Artifact: {filename} ---")
    
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # 1. Document Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="Q3 2025 Financial Performance Report", ln=True, align='C')
        pdf.ln(10) # Professional spacing

        # 2. Structured Content Definition
        # (Separating data from presentation logic)
        sections = [
            ("CONFIDENTIAL - INTERNAL USE ONLY", 
             ""),
            
            ("1. Executive Overview", 
             "The company achieved a record revenue of $12.5 Million in Q3 2025, marking a 15% year-over-year growth. "
             "However, net profit margins compressed slightly to 18% due to increased R&D spending in the AI sector."),
            
            ("2. Operational Metrics",
             "- Active Users: 1.2 Million (+8% QoQ)\n"
             "- Customer Churn: Reduced to 4.2% (Target was <5%)\n"
             "- Server Downtime: 0.01% (Met SLA requirements)"),
            
            ("3. Risks & Challenges",
             "The primary risk for Q4 remains the supply chain disruption in the semiconductor division. "
             "We anticipate a potential 3-week delay in hardware shipments if logistics constraints continue.")
        ]

        # 3. Render Loop
        for title, content in sections:
            # Render Section Title (Bold)
            if title:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, title, ln=True)
            
            # Render Section Body (Regular)
            if content:
                pdf.set_font("Arial", '', 12)
                pdf.multi_cell(0, 7, content) # Adjusted line height for readability
                pdf.ln(5)

        # 4. Save to Disk
        pdf.output(filename)
        print(f"[SUCCESS] File created successfully: {filename}")

    except PermissionError:
        print(f"[ERROR] Permission Denied: Could not write to '{filename}'.")
        print("   >> Hint: Close the PDF file if it is currently open in another program.")
    except Exception as e:
        print(f"[CRITICAL] Generation Failed: {e}")

if __name__ == "__main__":
    generate_test_fixture()