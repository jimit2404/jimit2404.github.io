#!/usr/bin/env python3
"""
Avalon Investments — Site Builder
Splits source.html into clean URL folder structure:
  index.html          → avaloninvestments.in/
  research/index.html → avaloninvestments.in/research
  about/index.html    → avaloninvestments.in/about
  contact/index.html  → avaloninvestments.in/contact
"""

import re, os

PAGE_CONFIG = {
    'home':     ('index.html',            'Avalon Investments | Independent Equity Research'),
    'research': ('research/index.html',   'Research | Avalon Investments'),
    'about':    ('about/index.html',      'About | Avalon Investments'),
    'contact':  ('contact/index.html',    'Contact | Avalon Investments'),
}

with open('source.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Fix all internal links to use clean URLs
source = source.replace('href="/research.html"', 'href="/research"')
source = source.replace('href="/about.html"',    'href="/about"')
source = source.replace('href="/contact.html"',  'href="/contact"')

# Extract shared head block (everything before first @@PAGE marker)
head_block = source[:source.index('<!-- @@PAGE:home@@ -->')]

# Extract shared tail block (everything after last @@END marker)
tail_block = source[source.rindex('<!-- @@END:contact@@ -->') + len('<!-- @@END:contact@@ -->'):]

# Extract main content for each page
def extract_page_content(source, page_id):
    start_marker = f'<!-- @@PAGE:{page_id}@@ -->'
    end_marker   = f'<!-- @@END:{page_id}@@ -->'
    start = source.index(start_marker) + len(start_marker)
    end   = source.index(end_marker)
    return source[start:end].strip()

for page_id, (filepath, title) in PAGE_CONFIG.items():
    page_content = extract_page_content(source, page_id)

    # Update <title>
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head_block)

    # Assemble full page
    page_html = f"""{head}
{page_content}
{tail_block}"""

    # Create folder if needed
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(page_html)

    print(f"Built: {filepath} ({len(page_html):,} chars)")

print("\nBuild complete. Clean URLs ready.")
