import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv('.env.local')
supabase: Client = create_client(os.environ.get("NEXT_PUBLIC_SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))

region_mapping = {
    "Montréal est": "mtlest",
    "Montréal ouest": "mtlouest",
    "Laval": "laval",
    "Couronne nord": "couronnenord",
    "Laurentides-Lanaudière": "laurentides-lanaudiere",
    "Montérégie est": "monteregieest",
    "Montérégie ouest": "monteregieouest",
    "Capitale-Nationale": "capitalenationale",
    "Chaudière-Appalaches": "chaudiere",
    "Outaouais": "outaouais",
    "Centre du Québec et Mauricie": "centremauricie",
    "Cantons de l'Est": "cantons-est",
    "Bas-Saint-Laurent–Gaspésie": "bsl-gaspesie",
    "Sag-Lac": "saglac",
    "Abitibi-Côte-Nord et Nord": "abitibinord"
}

# 1. Insert Regions
regions_data = [{"id": slug, "name": name} for name, slug in region_mapping.items()]
print(f"Upserting {len(regions_data)} regions...")
supabase.table("regions").upsert(regions_data).execute()

# 2. Update Riding-Regions Junction Table
print("Updating riding_regions junction table...")
# Load the new mapping from json
with open('scripts/qc125_regions.json', 'r', encoding='utf-8') as f:
    qc125_regions_mapping = json.load(f)

# Fetch all ridings to map qc125_id to riding_id (slug-code)
ridings = supabase.table("ridings").select("id", "qc125_id").execute().data
qc125_to_internal_id = {r['qc125_id']: r['id'] for r in ridings}

junction_data = []
for qc125_id, regions in qc125_regions_mapping.items():
    internal_id = qc125_to_internal_id.get(qc125_id)
    if internal_id:
        for r_name in regions:
            region_id = region_mapping.get(r_name)
            if region_id:
                junction_data.append({
                    "riding_id": internal_id,
                    "region_id": region_id
                })

if junction_data:
    print(f"Inserting {len(junction_data)} associations into riding_regions...")
    supabase.table("riding_regions").upsert(junction_data).execute()

print("Migration complete.")
