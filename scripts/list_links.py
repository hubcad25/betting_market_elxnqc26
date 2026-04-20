from bs4 import BeautifulSoup
import re

html_path = "/home/hubcad25/.local/share/opencode/tool-output/tool_dac986877001T3fVH6ITi01Sry"
with open(html_path, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.htm') and 'qc125.com' not in href:
        links.append(href)

print(sorted(list(set(links))))
