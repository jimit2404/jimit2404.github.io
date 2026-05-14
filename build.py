#!/usr/bin/env python3
"""
Avalon Investments — Site Builder
Splits source.html into index.html, research.html, about.html, contact.html
Run locally or via GitHub Actions on every push to source.html
"""

import re, os

PAGE_CONFIG = {
    'home':     ('index.html',    'Avalon Investments | Independent Equity Research', '/'),
    'research': ('research.html', 'Research | Avalon Investments',                   '/research.html'),
    'about':    ('about.html',    'About | Avalon Investments',                      '/about.html'),
    'contact':  ('contact.html',  'Contact | Avalon Investments',                    '/contact.html'),
}

NAV_LINKS = {
    'home':     '/',
    'research': '/research.html',
    'about':    '/about.html',
    'contact':  '/contact.html',
}

with open('source.html', 'r', encoding='utf-8') as f:
    source = f.read()

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

for page_id, (filename, title, active_path) in PAGE_CONFIG.items():
    page_content = extract_page_content(source, page_id)

    # Update <title>
    head = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', head_block)

    # Assemble full page
    page_html = f"""{head}
{page_content}
{tail_block}"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(page_html)

    print(f"Built: {filename} ({len(page_html):,} chars)")

print("\nBuild complete. 4 pages generated.")
