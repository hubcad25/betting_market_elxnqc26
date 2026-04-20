import json
import re
import unicodedata

def normalize(text):
    if not text:
        return ""
    # Normalize unicode characters
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    # Remove special characters and lowercase
    text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    # Special cases for Qc125 mismatches
    if text == "arthabaskalerable": return "arthabaska"
    if text == "montroyaloutremont": return "montroyaloutremont"
    return text

# Load DGEQ data
with open('scripts/dgeq_2017.json', 'r', encoding='utf-8') as f:
    dgeq_raw = json.load(f)
    dgeq_list = dgeq_raw['circ2017']

dgeq_map = {}
for code, info in dgeq_list.items():
    norm_name = normalize(info['nomCirc'])
    dgeq_map[norm_name] = {
        "code": code,
        "official_name": info['nomCirc']
    }

# Load Qc125 districts HTML (from the saved file)
html_path = "/home/hubcad25/.local/share/opencode/tool-output/tool_dac986877001T3fVH6ITi01Sry"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract the 'source' variable content using regex
# var source = [{value:"https://qc125.com/1001f.htm", label: "Abitibi-Est"}, ...]
matches = re.findall(r'\{value:"https://qc125\.com/([a-z0-9]+)\.htm", label: "([^"]+)"\}', html_content)

mapping = {}
unmapped = []

for qc125_id, qc125_label in matches:
    # Skip labels that look like candidates (often at the end of the list)
    # The first 125 are usually the ridings
    norm_qc125 = normalize(qc125_label)
    
    if norm_qc125 in dgeq_map:
        dgeq_info = dgeq_map[norm_qc125]
        mapping[dgeq_info['code']] = {
            "qc125_id": qc125_id,
            "official_name": dgeq_info['official_name'],
            "qc125_label": qc125_label
        }
    else:
        # Check if it's already in mapping (to avoid candidate names which repeat the ID)
        if norm_qc125 not in [normalize(v['official_name']) for v in mapping.values()]:
            unmapped.append((qc125_id, qc125_label))

print(f"Mapped {len(mapping)} ridings out of 125.")
if len(mapping) < 125:
    print("Unmapped Qc125 entries (potential ridings):")
    for qid, qlab in unmapped[:10]: # Show only first 10
        print(f"  {qid}: {qlab}")

# Save the mapping
with open('scripts/qc125_dgeq_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=4, ensure_ascii=False)
