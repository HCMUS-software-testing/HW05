import os
import sys
import html
import re
import time
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
WS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
REPORT_DIR = os.path.join(WS_ROOT, "submissions", "23127205", "report")
MERMAID_LOCAL = os.path.join(WS_ROOT, "tools", "mermaid.min.js")

def resolve_image_path(img_src, base_dir):
    if img_src.startswith("http://") or img_src.startswith("https://") or img_src.startswith("file://"):
        return img_src
    
    # Relative path resolution
    abs_p = os.path.abspath(os.path.join(base_dir, img_src))
    if os.path.exists(abs_p):
        return f"file:///{abs_p.replace(os.sep, '/')}"
    
    # Check in submissions folder
    alt_p = os.path.join(WS_ROOT, "submissions", "23127205", img_src.lstrip("../"))
    if os.path.exists(alt_p):
        return f"file:///{alt_p.replace(os.sep, '/')}"
        
    return img_src

def markdown_to_simple_clean_html(md_text, base_dir, title="Report"):
    lines = md_text.splitlines()
    html_lines = []
    in_table = False
    table_lines = []
    in_code = False
    code_lines = []
    code_lang = ""
    in_ul = False
    in_ol = False
    
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_lines.append("</ul>")
            in_ul = False
        if in_ol:
            html_lines.append("</ol>")
            in_ol = False

    def process_table(tbl_lines):
        if not tbl_lines:
            return ""
        out = ["<table>"]
        header = True
        for row_idx, r in enumerate(tbl_lines):
            if re.match(r"^\|?\s*[-:]+[-|\s:]*\|?$", r.strip()):
                header = False
                continue
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            tag = "th" if header else "td"
            out.append("<tr>" + "".join(f"<{tag}>{process_inline(c)}</{tag}>" for c in cells) + "</tr>")
            if header and row_idx == 0:
                header = False
        out.append("</table>")
        return "\n".join(out)
    
    def process_inline(text):
        def replace_img(match):
            alt_text = match.group(1)
            src_url = match.group(2)
            resolved_src = resolve_image_path(src_url, base_dir)
            return f'<div class="img-box"><img src="{resolved_src}" alt="{html.escape(alt_text)}" /><div class="img-caption">{html.escape(alt_text)}</div></div>'
            
        img_placeholders = {}
        def save_img(match):
            key = f"__IMG_PH_{len(img_placeholders)}__"
            img_placeholders[key] = replace_img(match)
            return key
            
        text = re.sub(r"!\[(.*?)\]\((.*?)\)", save_img, text)

        # Clean LaTeX formulas if any
        text = re.sub(r"\$([^\$]+)\$", r"\1", text)
        text = re.sub(r"\\text\{([^}]+)\}", r"\1", text)
        text = text.replace(r"\--", "–").replace(r"\%", "%")

        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        text = re.sub(r"\*\*\*(.*?)\*\*\*", r"<strong><em>\1</em></strong>", text)
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', text)
        
        for k, v in img_placeholders.items():
            text = text.replace(k, v)
            
        return text

    for line in lines:
        stripped = line.strip()

        # Handle Code blocks
        if stripped.startswith("```"):
            close_lists()
            if in_code:
                in_code = False
                if code_lang.lower() == "mermaid":
                    mermaid_code = "\n".join(code_lines)
                    html_lines.append(f'<div class="mermaid">\n{mermaid_code}\n</div>')
                else:
                    code_text = html.escape("\n".join(code_lines))
                    html_lines.append(f'<pre><code class="language-{code_lang}">{code_text}</code></pre>')
                code_lines = []
                code_lang = ""
            else:
                if in_table:
                    html_lines.append(process_table(table_lines))
                    table_lines = []
                    in_table = False
                in_code = True
                code_lang = stripped[3:].strip()
            continue
        
        if in_code:
            code_lines.append(line)
            continue
        
        # Handle Tables
        if stripped.startswith("|") and stripped.endswith("|"):
            close_lists()
            in_table = True
            table_lines.append(line)
            continue
        else:
            if in_table:
                html_lines.append(process_table(table_lines))
                table_lines = []
                in_table = False

        # Blank line
        if not stripped:
            close_lists()
            continue

        # Headers
        if line.startswith("# "):
            close_lists()
            html_lines.append(f"<h1>{process_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            close_lists()
            html_lines.append(f"<h2>{process_inline(line[3:])}</h2>")
        elif line.startswith("### "):
            close_lists()
            html_lines.append(f"<h3>{process_inline(line[4:])}</h3>")
        elif line.startswith("#### "):
            close_lists()
            html_lines.append(f"<h4>{process_inline(line[5:])}</h4>")
        elif stripped == "---":
            close_lists()
            html_lines.append("<hr/>")
        
        # Lists: Unordered (- or *)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            item_text = stripped[2:].strip()
            html_lines.append(f"<li>{process_inline(item_text)}</li>")
            
        # Lists: Ordered (1. 2. 3.)
        elif re.match(r"^\d+\.\s+", stripped):
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            m = re.match(r"^\d+\.\s+(.*)", stripped)
            item_text = m.group(1).strip()
            html_lines.append(f"<li>{process_inline(item_text)}</li>")

        # Blockquote (convert to bullet inside ul)
        elif stripped.startswith(">"):
            clean_txt = stripped[1:].strip()
            if clean_txt.startswith("- ") or clean_txt.startswith("* "):
                if in_ol:
                    html_lines.append("</ol>")
                    in_ol = False
                if not in_ul:
                    html_lines.append("<ul>")
                    in_ul = True
                html_lines.append(f"<li>{process_inline(clean_txt[2:].strip())}</li>")
            elif clean_txt:
                if in_ol:
                    html_lines.append("</ol>")
                    in_ol = False
                if not in_ul:
                    html_lines.append("<ul>")
                    in_ul = True
                html_lines.append(f"<li>{process_inline(clean_txt)}</li>")

        # Images
        elif stripped.startswith("!["):
            close_lists()
            html_lines.append(process_inline(stripped))
            
        # Regular Paragraph
        else:
            close_lists()
            html_lines.append(f"<p>{process_inline(stripped)}</p>")
    
    close_lists()
    if in_table:
        html_lines.append(process_table(table_lines))
    if in_code:
        if code_lang.lower() == "mermaid":
            mermaid_code = "\n".join(code_lines)
            html_lines.append(f'<div class="mermaid">\n{mermaid_code}\n</div>')
        else:
            code_text = html.escape("\n".join(code_lines))
            html_lines.append(f'<pre><code>{code_text}</code></pre>')

    body_content = "\n".join(html_lines)
    mermaid_url = f"file:///{MERMAID_LOCAL.replace(os.sep, '/')}"

    full_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<script src="{mermaid_url}"></script>
<style>
    @page {{
        size: A4;
        margin: 15mm 15mm 15mm 15mm;
    }}
    *, *:before, *:after {{
        box-sizing: border-box;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 13.5px;
        line-height: 1.6;
        color: #1f2937;
        background-color: #ffffff;
        padding: 0;
        margin: 0;
    }}
    h1 {{
        font-size: 21px;
        font-weight: 700;
        color: #0f172a;
        border-bottom: 2px solid #334155;
        padding-bottom: 5px;
        margin-top: 10px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }}
    h2 {{
        font-size: 16.5px;
        font-weight: 600;
        color: #1e293b;
        border-bottom: 1px solid #cbd5e1;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    h3 {{
        font-size: 14.5px;
        font-weight: 600;
        color: #334155;
        margin-top: 14px;
        margin-bottom: 6px;
        page-break-after: avoid;
    }}
    h4 {{
        font-size: 13.5px;
        font-weight: 600;
        color: #475569;
        margin-top: 10px;
        margin-bottom: 4px;
    }}
    p {{
        margin-top: 4px;
        margin-bottom: 8px;
    }}
    /* Định dạng chuẩn cho Bullet List và Numbered List */
    ul {{
        list-style-type: disc !important;
        margin: 6px 0 10px 0 !important;
        padding-left: 24px !important;
    }}
    ol {{
        list-style-type: decimal !important;
        margin: 6px 0 10px 0 !important;
        padding-left: 24px !important;
    }}
    li {{
        display: list-item !important;
        list-style-position: outside !important;
        margin-bottom: 4px !important;
        line-height: 1.55 !important;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
        font-size: 12.5px;
    }}
    th, td {{
        border: 1px solid #cbd5e1;
        padding: 6px 10px;
        text-align: left;
        vertical-align: top;
        word-break: break-word;
    }}
    th {{
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 600;
    }}
    tr:nth-child(even) {{
        background-color: #f8fafc;
    }}
    code {{
        font-family: "Consolas", "Courier New", monospace;
        font-size: 12.5px;
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 2px 4px;
        border-radius: 3px;
        border: 1px solid #e2e8f0;
        word-break: break-word;
        white-space: pre-wrap;
    }}
    pre {{
        background-color: #f8fafc;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-left: 3.5px solid #64748b;
        padding: 8px 12px;
        border-radius: 4px;
        font-family: "Consolas", "Courier New", monospace;
        font-size: 12px;
        line-height: 1.5;
        margin: 8px 0;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
    }}
    pre code {{
        background: transparent !important;
        border: none !important;
        color: inherit !important;
        padding: 0 !important;
        font-size: inherit !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }}
    hr {{
        border: 0;
        height: 1px;
        background: #e2e8f0;
        margin: 12px 0;
    }}
    .img-box {{
        text-align: center;
        margin: 10px 0;
    }}
    .img-box img {{
        max-width: 95%;
        max-height: 480px;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        display: inline-block;
    }}
    .img-caption {{
        font-size: 11.5px;
        color: #64748b;
        margin-top: 4px;
        font-style: italic;
    }}
    .mermaid {{
        text-align: center;
        margin: 10px 0;
        background-color: #ffffff;
        padding: 8px;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
    }}
    .mermaid svg {{
        max-width: 100% !important;
        height: auto !important;
    }}
</style>
</head>
<body>
{body_content}
<script>
    if (window.mermaid) {{
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'neutral',
            securityLevel: 'loose',
            themeVariables: {{
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                fontSize: '12px',
                primaryColor: '#f1f5f9',
                primaryBorderColor: '#64748b',
                primaryTextColor: '#0f172a',
                lineColor: '#475569'
            }}
        }});
    }}
</script>
</body>
</html>"""
    return full_html

def convert_md_to_pdf(playwright_browser, md_input):
    if os.path.isabs(md_input):
        md_path = md_input
    elif os.path.exists(os.path.join(REPORT_DIR, md_input)):
        md_path = os.path.join(REPORT_DIR, md_input)
    elif os.path.exists(os.path.join(WS_ROOT, md_input)):
        md_path = os.path.join(WS_ROOT, md_input)
    else:
        md_path = os.path.join(REPORT_DIR, md_input)
        
    if not os.path.exists(md_path):
        print(f"[-] File not found: {md_path}")
        return False
    
    target_dir = os.path.dirname(md_path)
    base_name = os.path.splitext(os.path.basename(md_path))[0]
    html_path = os.path.join(target_dir, f"{base_name}.tmp.html")
    pdf_path = os.path.join(target_dir, f"{base_name}.pdf")
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    rendered_html = markdown_to_simple_clean_html(md_content, target_dir, title=base_name)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    page = playwright_browser.new_page()
    try:
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        
        # Wait for mermaid rendering if any
        page.evaluate("""() => {
            return new Promise((resolve) => {
                if (document.querySelector('.mermaid')) {
                    setTimeout(resolve, 800);
                } else {
                    resolve();
                }
            });
        }""")
        
        # Wait for all images
        page.evaluate("""() => {
            return Promise.all(Array.from(document.images).map(img => {
                if (img.complete) return Promise.resolve();
                return new Promise(resolve => {
                    img.addEventListener('load', resolve);
                    img.addEventListener('error', resolve);
                });
            }));
        }""")
        
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "15mm",
                "bottom": "15mm",
                "left": "15mm",
                "right": "15mm"
            }
        )
        print(f"[+] Successfully created: {os.path.relpath(pdf_path, WS_ROOT)} ({os.path.getsize(pdf_path)} bytes)")
        return True
    except Exception as e:
        print(f"[-] Failed to create PDF for {md_input}: {e}")
        return False
    finally:
        page.close()
        if os.path.exists(html_path):
            os.remove(html_path)

def main():
    md_files = [
        "main-report.md",
        "ai-critique.md",
        "ai-audit-report.md",
        "task2-ai-analysis.md",
        "task3-continuous-performance-testing.md",
        "bug-report.md",
        "workflow-description.md",
        os.path.join(WS_ROOT, "submissions", "23127205", "README.md"),
        os.path.join(WS_ROOT, "README.md")
    ]
    
    print("=" * 70)
    print("    GENERATING PDF REPORTS (FULL <ul> <ol> PROPER BULLETS & NUMBERS)")
    print("=" * 70)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=EDGE_PATH,
            args=["--no-sandbox", "--disable-gpu"]
        )
        success = 0
        for f in md_files:
            if convert_md_to_pdf(browser, f):
                success += 1
        browser.close()
            
    print("\n" + "=" * 70)
    print(f"    SUMMARY: Successfully converted {success}/{len(md_files)} markdown reports to PDF.")
    print("=" * 70)

if __name__ == "__main__":
    main()
