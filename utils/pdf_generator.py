from fpdf import FPDF
import re
import os

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        # Use standard fonts that support basic characters
        pass
    
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'Investment Portfolio Report', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 51, 102)
        # Remove special characters
        title = self.clean_text(title)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        # Clean the text (remove markdown artifacts and special chars)
        clean_body = re.sub(r'\*\*([^*]+)\*\*', r'\1', body)
        clean_body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_body)
        clean_body = self.clean_text(clean_body)
        self.multi_cell(0, 6, clean_body)
        self.ln(2)
    
    def bullet_point(self, text):
        self.set_font('Arial', '', 11)
        clean_text = self.clean_text(text)
        clean_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', clean_text)
        self.cell(5, 6, '-', 0, 0)
        self.multi_cell(0, 6, clean_text)
    
    def section_break(self):
        self.ln(3)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
    
    def clean_text(self, text):
        """Remove or replace special characters that cause encoding issues"""
        # Replace common special characters
        replacements = {
            '•': '-',
            '★': '*',
            '✓': '[x]',
            '…': '...',
            '–': '-',
            '—': '-',
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
            '€': 'EUR',
            '£': 'GBP',
            '©': '(c)',
            '®': '(r)',
            '™': '(tm)'
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        # Remove any remaining non-ascii characters
        text = text.encode('ascii', 'ignore').decode('ascii')
        return text

def markdown_to_pdf(markdown_text, output_path="portfolio_report.pdf"):
    """Convert markdown report to PDF"""
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    lines = markdown_text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            pdf.ln(2)
            i += 1
            continue
        
        # Headers
        if line.startswith('# ') or line.startswith('## '):
            title = re.sub(r'^#+\s+', '', line)
            pdf.chapter_title(title)
        
        elif line.startswith('### '):
            pdf.set_font('Arial', 'B', 12)
            title = re.sub(r'^###\s+', '', line)
            title = pdf.clean_text(title)
            pdf.cell(0, 8, title, 0, 1)
            pdf.set_font('Arial', '', 11)
            pdf.ln(2)
        
        # Bullet points
        elif line.startswith('- ') or line.startswith('* '):
            pdf.bullet_point(line[2:])
        
        # Separators
        elif line.startswith('---'):
            pdf.section_break()
        
        # Regular text
        elif len(line) > 0 and not line.startswith('#'):
            pdf.chapter_body(line)
        
        i += 1
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)) if os.path.dirname(os.path.abspath(output_path)) else '.', exist_ok=True)
    
    pdf.output(output_path)
    return output_path