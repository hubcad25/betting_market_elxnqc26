import requests
from bs4 import BeautifulSoup
import json
import time
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

regions_urls = {
    "Montréal est": "https://qc125.com/mtlest.htm",
    "Montréal ouest": "https://qc125.com/mtlouest.htm",
    "Laval": "https://qc125.com/laval.htm",
    "Couronne nord": "https://qc125.com/couronnenord.htm",
    "Laurentides-Lanaudière": "https://qc125.com/ll.htm",
    "Montérégie est": "https://qc125.com/monteregieest.htm",
    "Montérégie ouest": "https://qc125.com/monteregieouest.htm",
    "Capitale-Nationale": "https://qc125.com/capitalenationale.htm",
    "Chaudière-Appalaches": "https://qc125.com/chaudiere.htm",
    "Outaouais": "https://qc125.com/outaouais.htm",
    "Centre du Québec et Mauricie": "https://qc125.com/centremauricie.htm",
    "Cantons de l'Est": "https://qc125.com/cantons.htm",
    "Bas-Saint-Laurent–Gaspésie": "https://qc125.com/basstlaurentgaspesie.htm",
    "Sag-Lac": "https://qc125.com/saglac.htm",
    "Abitibi-Côte-Nord et Nord": "https://qc125.com/abitibinord.htm"
}

riding_to_regions = {} # Changed to plural

for region_name, url in regions_urls.items():
    print(f"Fetching {region_name}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            for a in links:
                href = a['href']
                match = re.search(r'([a-z0-9]+)\.htm', href)
                if match:
                    riding_id = match.group(1)
                    if re.match(r'^1[0-9]{3}[a-z]?$', riding_id):
                        if riding_id not in riding_to_regions:
                            riding_to_regions[riding_id] = []
                        if region_name not in riding_to_regions[riding_id]:
                            riding_to_regions[riding_id].append(region_name)
        else:
            print(f"  Failed with status {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")
    time.sleep(1)

print(f"Found {len(riding_to_regions)} unique ridings across regions.")

# Save results
with open('scripts/qc125_regions.json', 'w', encoding='utf-8') as f:
    json.dump(riding_to_regions, f, indent=4, ensure_ascii=False)
