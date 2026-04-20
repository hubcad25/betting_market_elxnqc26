import os
import json
import urllib.request
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

# Mapping DGEQ Party Numbers to our DB IDs
PARTY_MAP = {
    27: "CAQ",
    6: "PLQ",
    8: "PQ",
    40: "QS",
    10: "PVQ",
    22: "PCQ"
}

URLS = {
    2022: "https://donnees.electionsquebec.qc.ca/production/provincial/resultats/archives/gen2022-10-03/resultats.json",
    2018: "https://donnees.electionsquebec.qc.ca/production/provincial/resultats/archives/gen2018-10-01/resultats.json"
}

def fetch_json(url):
    print(f"Fetching data from {url}...")
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode('utf-8'))

def process_election(year, data):
    print(f"Processing results for {year}...")
    
    # Get ridings to map DGEQ code to ID
    ridings_res = supabase.table("ridings").select("id, dgeq_code").execute()
    riding_map = {r['dgeq_code']: r['id'] for r in ridings_res.data}
    
    historical_records = []
    
    for circ in data.get("circonscriptions", []):
        code = str(circ.get("numeroCirconscription"))
        if code not in riding_map:
            print(f"Warning: Riding code {code} ({circ.get('nomCirconscription')}) not found in DB.")
            continue
            
        riding_id = riding_map[code]
        turnout = float(circ.get("tauxParticipation", 0))
        
        # Sort candidates by votes to find winner and margin
        candidates = sorted(circ.get("candidats", []), key=lambda x: x.get("nbVoteTotal", 0), reverse=True)
        
        if not candidates:
            continue
            
        winner = candidates[0]
        runner_up = candidates[1] if len(candidates) > 1 else None
        
        winning_party_num = winner.get("numeroPartiPolitique")
        winning_party_id = PARTY_MAP.get(winning_party_num, "IND")
        
        margin = winner.get("tauxVote", 0) - (runner_up.get("tauxVote", 0) if runner_up else 0)
        
        # Aggregate all party scores for the 'votes' JSONB column
        votes_detail = {}
        others_total = 0.0
        
        for cand in candidates:
            p_num = cand.get("numeroPartiPolitique")
            p_id = PARTY_MAP.get(p_num)
            p_score = float(cand.get("tauxVote", 0))
            
            if p_id:
                # Add to specific party (handle duplicates just in case)
                votes_detail[p_id] = votes_detail.get(p_id, 0.0) + p_score
            else:
                others_total += p_score
        
        if others_total > 0:
            votes_detail["IND"] = round(votes_detail.get("IND", 0.0) + others_total, 2)
            
        # Round all scores to 2 decimal places
        votes_detail = {k: round(v, 2) for k, v in votes_detail.items()}
        
        historical_records.append({
            "riding_id": riding_id,
            "election_year": year,
            "winning_party_id": winning_party_id,
            "margin_percent": round(margin, 2),
            "turnout_percent": round(turnout, 2),
            "votes": votes_detail
        })
        
    if historical_records:
        try:
            # Upsert into riding_historical_results
            supabase.table("riding_historical_results").upsert(
                historical_records, 
                on_conflict="riding_id, election_year"
            ).execute()
            print(f"Successfully imported {len(historical_records)} ridings for {year}.")
        except Exception as e:
            print(f"Error during upsert for {year}: {e}")

if __name__ == "__main__":
    for year, url in URLS.items():
        data = fetch_json(url)
        process_election(year, data)
