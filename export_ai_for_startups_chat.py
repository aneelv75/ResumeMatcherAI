
import os
import re
from bs4 import BeautifulSoup
from fpdf import FPDF

def extract_specific_chat(html_path, chat_title="AI For Startups"):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find the container that holds all threads
    all_chats = soup.find_all('div', class_=re.compile('thread'))

    target_messages = []

    for chat in all_chats:
        # Find chat title
        heading = chat.find(['h3', 'h2', 'h1'])
        if heading and chat_title.lower() in heading.text.lower():
            # Extract messages
            for block in chat.find_all(class_=re.compile('^message')):
                role = 'User' if 'user' in block['class'] else 'ChatGPT'
                content = block.get_text(separator='\n').strip()
                target_messages.append((role, content))
            break

    return target_messages

def export_to_pdf(messages, output_path='AI_For_Startups.pdf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("AI For Startups Chat Export")
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
    parser = argparse.ArgumentParser(description="Extract specific ChatGPT thread by title and export to PDF.")
    parser.add_argument("html_path", help="Path to the exported chat.html file")
    parser.add_argument("--title", help="Chat title to extract", default="AI For Startups")
    parser.add_argument("--output", help="Output PDF file name", default="AI_For_Startups.pdf")
    args = parser.parse_args()

    msgs = extract_specific_chat(args.html_path, args.title)
    if msgs:
        export_to_pdf(msgs, args.output)
    else:
        print("❌ Chat titled '{}' not found.".format(args.title))
