#!/usr/bin/env python3
import PyPDF2
import sys
import os

def extract_pdf_text(pdf_path):
    """提取PDF文本内容"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return text

def clean_text(text):
    """清理文本，删除业绩表现部分，保留投资组合回顾和市场展望"""
    # 查找关键部分
    # 假设PDF结构：1. 业绩表现 2. 投资组合回顾 3. 市场展望
    # 或者英文：1. Performance 2. Portfolio Review 3. Market Outlook

    lines = text.split('\n')
    cleaned_lines = []

    # 标记是否在需要保留的部分
    in_portfolio_review = False
    in_market_outlook = False
    skip_section = False

    for line in lines:
        line_lower = line.lower()

        # 检测部分标题
        if 'portfolio review' in line_lower or '投资组合回顾' in line:
            in_portfolio_review = True
            in_market_outlook = False
            skip_section = False
            # 不保留标题本身
            continue
        elif 'market outlook' in line_lower or '市场展望' in line:
            in_market_outlook = True
            in_portfolio_review = False
            skip_section = False
            # 不保留标题本身
            continue
        elif 'performance' in line_lower or '业绩表现' in line:
            in_portfolio_review = False
            in_market_outlook = False
            skip_section = True
            continue

        # 如果在新部分开始，重置
        if line.strip() and line[0].isupper() and len(line) < 100:
            # 可能是新章节标题，如果不是我们需要的部分，跳过
            if not (in_portfolio_review or in_market_outlook):
                skip_section = True
                continue

        if skip_section:
            continue

        if in_portfolio_review or in_market_outlook:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_pdf.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    if not os.path.exists(pdf_file):
        print(f"File not found: {pdf_file}")
        sys.exit(1)

    print(f"Extracting text from {pdf_file}...")
    text = extract_pdf_text(pdf_file)

    print("\n=== ORIGINAL TEXT (first 2000 chars) ===")
    print(text[:2000])

    print("\n=== CLEANED TEXT ===")
    cleaned = clean_text(text)
    print(cleaned[:2000])