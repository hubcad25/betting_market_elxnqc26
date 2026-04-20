import os
import json
import re
import unicodedata
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv('.env.local')

supabase_url = os.environ.get("NEXT_PUBLIC_SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_key:
    print("Error: Missing Supabase environment variables.")
    exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

# Load mappings
with open('scripts/qc125_dgeq_mapping.json', 'r', encoding='utf-8') as f:
    qc125_mapping = json.load(f)

with open('scripts/qc125_regions.json', 'r', encoding='utf-8') as f:
    region_mapping = json.load(f)

ridings_to_import = []

for dgeq_code, info in qc125_mapping.items():
    official_name = info['official_name']
    qc125_id = info['qc125_id']
    region = region_mapping.get(qc125_id, "Inconnue")
    
    # Generate ID: slug-code
    slug = slugify(official_name)
    riding_id = f"{slug}-{dgeq_code}"
    
    ridings_to_import.append({
        "id": riding_id,
        "name": official_name,
        "dgeq_code": dgeq_code,
        "region": region,
        "qc125_id": qc125_id,
        "poliwave_id": dgeq_code, # Poliwave uses DGEQ codes
        "metadata": {}
    })

print(f"Preparing to import {len(ridings_to_import)} ridings...")

# Clear existing ridings if any (optional, but good for a fresh start)
# Note: This might fail if there are dependent records in other tables
# supabase.table("ridings").delete().neq("id", "0").execute()

# Batch insert (Supabase handles this well with a list)
try:
    result = supabase.table("ridings").upsert(ridings_to_import).execute()
    print(f"Successfully imported {len(ridings_to_import)} ridings.")
except Exception as e:
    print(f"Error during import: {e}")
