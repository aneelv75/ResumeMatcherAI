
import os
import re
from bs4 import BeautifulSoup
from fpdf import FPDF

def extract_chat_by_keyword(html_path, keyword="AI for Startups"):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    messages = []
    capture = False
    buffer = []

    for tag in soup.find_all(['div', 'section', 'article']):
        text = tag.get_text(separator='\n').strip()
        if keyword.lower() in text.lower():
            capture = True
            buffer.append(tag)

    if not buffer:
        return []

    # Find messages inside the buffer
    for block in buffer[0].find_all(class_=re.compile('^message')):
        role = 'User' if 'user' in block['class'] else 'ChatGPT'
        content = block.get_text(separator='\n').strip()
        messages.append((role, content))

    return messages

def export_to_pdf(messages, output_path='AI_For_Startups.pdf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("AI for Startups Chat Export")
    pdf.set_author("ChatGPT Export Script")

    for role, content in messages:
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 10, f"{role}:", align='L')
        pdf.set_font("Arial", '', 11)
        pdf.multi_cell(0, 8, content)
        pdf.ln(5)

    pdf.output(output_path)
    print(f"✅ PDF saved as: {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract chat section by visible keyword and export to PDF.")
    parser.add_argument("html_path", help="Path to the exported chat.html file")
    parser.add_argument("--keyword", help="Keyword to search in visible chat", default="AI for Startups")
    parser.add_argument("--output", help="Output PDF file name", default="AI_For_Startups.pdf")
    args = parser.parse_args()

    msgs = extract_chat_by_keyword(args.html_path, args.keyword)
    if msgs:
        export_to_pdf(msgs, args.output)
    else:
        print(f"❌ Could not find any section with the keyword: '{args.keyword}'")
