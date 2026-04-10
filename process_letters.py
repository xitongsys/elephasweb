#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

# Add the existing extract_pdf module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_pdf import extract_pdf_text, clean_text

def parse_quarter_from_filename(filename):
    """
    从文件名解析季度信息。
    返回格式： (year, quarter_number)
    例如： (2024, 4) 表示2024年第四季度
    """
    # 中文文件名模式：艾礼象中国能言2024Q4投资者交流.pdf
    # 英文文件名模式：Alphas Investor Letter Q4 2024.pdf
    # 其他：Elephas Alphas Fund Sep 2025.pdf 可能不是季度信

    filename = os.path.basename(filename)

    # 尝试匹配中文模式：年份 + Q + 季度
    match = re.search(r'(\d{4})[Qq](\d)', filename)
    if match:
        year = int(match.group(1))
        quarter = int(match.group(2))
        return year, quarter

    # 尝试匹配英文模式：Q + 季度 + 年份
    match = re.search(r'[Qq](\d)\s*(\d{4})', filename)
    if match:
        quarter = int(match.group(1))
        year = int(match.group(2))
        return year, quarter

    # 尝试匹配月份，但可能不是季度信
    # 暂时返回None
    return None

def generate_html_content(cleaned_text, title):
    """生成简单的HTML页面"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="../web_download/css/style.css">
    <link rel="stylesheet" type="text/css" href="../web_download/css/index.css">
    <style>
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            color: #333;
            line-height: 1.6;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
            background-color: #f9f9f9;
        }}
        .letter-content {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #006561;
            border-bottom: 2px solid #006561;
            padding-bottom: 10px;
        }}
        .back-link {{
            display: inline-block;
            margin-top: 20px;
            color: #006561;
            text-decoration: none;
            font-weight: bold;
        }}
        .back-link:hover {{
            text-decoration: underline;
        }}
        p {{
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <div class="letter-content">
        <h1>{title}</h1>
        <div class="text-content">
{cleaned_text}
        </div>
        <a class="back-link" href="javascript:history.back()">← 返回</a>
    </div>
</body>
</html>"""
    return html

def process_pdf_files(resources_dir='resources', output_dir='quarterly_letters'):
    """处理所有PDF文件并生成HTML页面"""
    resources_path = Path(resources_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    pdf_files = list(resources_path.glob('*.pdf'))
    print(f"找到 {len(pdf_files)} 个PDF文件")

    processed = []

    for pdf_file in pdf_files:
        print(f"\n处理文件: {pdf_file.name}")

        # 解析季度信息
        quarter_info = parse_quarter_from_filename(pdf_file.name)
        if not quarter_info:
            print(f"  警告: 无法从文件名解析季度信息，跳过")
            continue

        year, quarter = quarter_info

        # 生成季度标签（中文）
        quarter_label = f"{year}年第{quarter}季度"

        # 提取并清理文本
        text = extract_pdf_text(str(pdf_file))
        cleaned = clean_text(text)

        if not cleaned.strip():
            print(f"  警告: 清理后的文本为空")
            # 使用原始文本作为后备
            cleaned = text

        # 生成HTML文件名
        html_filename = f"{year}Q{quarter}_letter.html"
        html_file = output_path / html_filename

        # 生成标题
        title = f"{quarter_label} 投资观点摘要"

        # 生成HTML内容
        html_content = generate_html_content(cleaned, title)

        # 写入文件
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  已生成: {html_file}")

        # 记录映射关系
        processed.append({
            'pdf': pdf_file.name,
            'year': year,
            'quarter': quarter,
            'label': quarter_label,
            'html_file': html_filename
        })

    # 生成索引文件
    generate_index_html(processed, output_path)

    return processed

def generate_index_html(processed_list, output_path):
    """生成索引HTML文件，列出所有季度信"""
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>季度交流信索引</title>
    <link rel="stylesheet" type="text/css" href="../web_download/css/style.css">
    <link rel="stylesheet" type="text/css" href="../web_download/css/index.css">
    <style>
        body {
            font-family: "Microsoft YaHei", sans-serif;
            color: #333;
            line-height: 1.6;
            padding: 20px;
            max-width: 900px;
            margin: 0 auto;
            background-color: #f9f9f9;
        }
        h1 {
            color: #006561;
            border-bottom: 2px solid #006561;
            padding-bottom: 10px;
        }
        .quarter-list {
            list-style-type: none;
            padding: 0;
        }
        .quarter-item {
            background-color: white;
            margin-bottom: 15px;
            padding: 15px 20px;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .quarter-item:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        }
        .quarter-link {
            text-decoration: none;
            color: #006561;
            font-weight: bold;
            font-size: 18px;
            display: block;
        }
        .quarter-link:hover {
            color: #004d4a;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #006561;
            text-decoration: none;
            font-weight: bold;
        }
        .back-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="letter-content">
        <h1>季度交流信索引</h1>
        <ul class="quarter-list">
"""

    # 按年份和季度排序
    sorted_list = sorted(processed_list, key=lambda x: (x['year'], x['quarter']), reverse=True)

    for item in sorted_list:
        html += f"""            <li class="quarter-item">
                <a class="quarter-link" href="{item['html_file']}">{item['label']}</a>
                <p>来源文件: {item['pdf']}</p>
            </li>
"""

    html += """        </ul>
        <a class="back-link" href="javascript:history.back()">← 返回</a>
    </div>
</body>
</html>"""

    index_file = output_path / 'index.html'
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n已生成索引文件: {index_file}")

if __name__ == "__main__":
    print("开始处理季度交流信PDF文件...")
    processed = process_pdf_files()
    print(f"\n处理完成！共处理 {len(processed)} 个季度交流信。")
    print(f"HTML文件保存在: quarterly_letters/")