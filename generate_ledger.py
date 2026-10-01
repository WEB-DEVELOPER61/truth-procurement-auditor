import hashlib
import json
from datetime import datetime

def compute_sha256(data_str: str) -> str:
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

def compute_merkle_root(hash_list: list) -> str:
    if not hash_list:
        return ""
    current_level = sorted(hash_list)
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            combined = hashlib.sha256((left + right).encode("utf-8")).hexdigest()
            next_level.append(combined)
        current_level = next_level
    return current_level[0]

RAW_RECORDS = [
    {"tender_id": "2026_CEPWD_60212_1", "nit_no": "NIT 07/2026-27 Item 1", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 18.50, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_60212_2", "nit_no": "NIT 07/2026-27 Item 2", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 14.20, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_60212_3", "nit_no": "NIT 07/2026-27 Item 3", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 22.00, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_60212_4", "nit_no": "NIT 07/2026-27 Item 4", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 19.80, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_60212_5", "nit_no": "NIT 07/2026-27 Item 5", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 12.10, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_60212_6", "nit_no": "NIT 07/2026-27 Item 6", "division": "Chirawa Sub-Division", "district": "Jhunjhunu", "cost_lac": 12.00, "published": "2026-09-30 15:30:00", "closing": "2026-10-04 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_59901_1", "nit_no": "NIT 04/2026-27 Item 1", "division": "Khetri Sub-Division", "district": "Jhunjhunu", "cost_lac": 28.40, "published": "2026-09-28 11:00:00", "closing": "2026-10-02 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_59901_2", "nit_no": "NIT 04/2026-27 Item 2", "division": "Khetri Sub-Division", "district": "Jhunjhunu", "cost_lac": 31.00, "published": "2026-09-28 11:00:00", "closing": "2026-10-02 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_58412_1", "nit_no": "NIT 09/2026-27 Item 1", "division": "Mundawar Sub-Division", "district": "Alwar", "cost_lac": 45.00, "published": "2026-09-25 10:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_58412_2", "nit_no": "NIT 09/2026-27 Item 2", "division": "Mundawar Sub-Division", "district": "Alwar", "cost_lac": 38.50, "published": "2026-09-25 10:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_57102_1", "nit_no": "NIT 12/2026-27 Item 1", "division": "Jhunjhunu Division HQ", "district": "Jhunjhunu", "cost_lac": 85.00, "published": "2026-09-20 10:00:00", "closing": "2026-09-30 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_57102_2", "nit_no": "NIT 12/2026-27 Item 2", "division": "Jhunjhunu Division HQ", "district": "Jhunjhunu", "cost_lac": 92.50, "published": "2026-09-20 10:00:00", "closing": "2026-09-30 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_56219_1", "nit_no": "NIT 03/2026-27 Item 1", "division": "Sikar Circle Office", "district": "Sikar", "cost_lac": 145.00, "published": "2026-09-15 09:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_56219_2", "nit_no": "NIT 03/2026-27 Item 2", "division": "Sikar Circle Office", "district": "Sikar", "cost_lac": 110.00, "published": "2026-09-15 09:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_55481_1", "nit_no": "NIT 15/2026-27 Item 1", "division": "Churu Division", "district": "Churu", "cost_lac": 48.00, "published": "2026-09-21 12:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_55481_2", "nit_no": "NIT 15/2026-27 Item 2", "division": "Churu Division", "district": "Churu", "cost_lac": 35.20, "published": "2026-09-21 12:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_54902_1", "nit_no": "NIT 02/2026-27 Item 1", "division": "Jaipur Circle I", "district": "Jaipur", "cost_lac": 320.00, "published": "2026-09-10 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 15},
    {"tender_id": "2026_CEPWD_54902_2", "nit_no": "NIT 02/2026-27 Item 2", "division": "Jaipur Circle I", "district": "Jaipur", "cost_lac": 410.00, "published": "2026-09-10 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 15},
    {"tender_id": "2026_CEPWD_53811_1", "nit_no": "NIT 08/2026-27 Item 1", "division": "Jaipur Rural Div", "district": "Jaipur", "cost_lac": 65.00, "published": "2026-09-18 10:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_53811_2", "nit_no": "NIT 08/2026-27 Item 2", "division": "Jaipur Rural Div", "district": "Jaipur", "cost_lac": 72.00, "published": "2026-09-18 10:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_52981_1", "nit_no": "NIT 06/2026-27 Item 1", "division": "Alwar City Division", "district": "Alwar", "cost_lac": 88.00, "published": "2026-09-16 11:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_52981_2", "nit_no": "NIT 06/2026-27 Item 2", "division": "Alwar City Division", "district": "Alwar", "cost_lac": 95.00, "published": "2026-09-16 11:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_51829_1", "nit_no": "NIT 11/2026-27 Item 1", "division": "Nagaur Division", "district": "Nagaur", "cost_lac": 54.00, "published": "2026-09-19 10:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_51829_2", "nit_no": "NIT 11/2026-27 Item 2", "division": "Nagaur Division", "district": "Nagaur", "cost_lac": 42.00, "published": "2026-09-19 10:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_50412_1", "nit_no": "NIT 05/2026-27 Item 1", "division": "Bikaner Division I", "district": "Bikaner", "cost_lac": 160.00, "published": "2026-09-12 10:00:00", "closing": "2026-09-24 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_50412_2", "nit_no": "NIT 05/2026-27 Item 2", "division": "Bikaner Division I", "district": "Bikaner", "cost_lac": 180.00, "published": "2026-09-12 10:00:00", "closing": "2026-09-24 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_49821_1", "nit_no": "NIT 01/2026-27 Item 1", "division": "Kota Circle", "district": "Kota", "cost_lac": 210.00, "published": "2026-09-08 10:00:00", "closing": "2026-09-20 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_49821_2", "nit_no": "NIT 01/2026-27 Item 2", "division": "Kota Circle", "district": "Kota", "cost_lac": 195.00, "published": "2026-09-08 10:00:00", "closing": "2026-09-20 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_48910_1", "nit_no": "NIT 07/2026-27 Item 1", "division": "Ajmer Division II", "district": "Ajmer", "cost_lac": 74.00, "published": "2026-09-17 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_48910_2", "nit_no": "NIT 07/2026-27 Item 2", "division": "Ajmer Division II", "district": "Ajmer", "cost_lac": 68.00, "published": "2026-09-17 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_47812_1", "nit_no": "NIT 10/2026-27 Item 1", "division": "Dausa Division", "district": "Dausa", "cost_lac": 58.00, "published": "2026-09-20 11:00:00", "closing": "2026-09-28 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_47812_2", "nit_no": "NIT 10/2026-27 Item 2", "division": "Dausa Division", "district": "Dausa", "cost_lac": 61.50, "published": "2026-09-20 11:00:00", "closing": "2026-09-28 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_46901_1", "nit_no": "NIT 04/2026-27 Item 1", "division": "Bharatpur Circle", "district": "Bharatpur", "cost_lac": 130.00, "published": "2026-09-14 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_46901_2", "nit_no": "NIT 04/2026-27 Item 2", "division": "Bharatpur Circle", "district": "Bharatpur", "cost_lac": 115.00, "published": "2026-09-14 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_45819_1", "nit_no": "NIT 14/2026-27 Item 1", "division": "Tonk Division", "district": "Tonk", "cost_lac": 49.00, "published": "2026-09-19 12:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_45819_2", "nit_no": "NIT 14/2026-27 Item 2", "division": "Tonk Division", "district": "Tonk", "cost_lac": 52.00, "published": "2026-09-19 12:00:00", "closing": "2026-09-27 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_44901_1", "nit_no": "NIT 03/2026-27 Item 1", "division": "Udaipur Circle", "district": "Udaipur", "cost_lac": 240.00, "published": "2026-09-09 10:00:00", "closing": "2026-09-21 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_44901_2", "nit_no": "NIT 03/2026-27 Item 2", "division": "Udaipur Circle", "district": "Udaipur", "cost_lac": 310.00, "published": "2026-09-09 10:00:00", "closing": "2026-09-21 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_43810_1", "nit_no": "NIT 09/2026-27 Item 1", "division": "Bhilwara Division", "district": "Bhilwara", "cost_lac": 63.00, "published": "2026-09-18 10:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_43810_2", "nit_no": "NIT 09/2026-27 Item 2", "division": "Bhilwara Division", "district": "Bhilwara", "cost_lac": 59.00, "published": "2026-09-18 10:00:00", "closing": "2026-09-26 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_42918_1", "nit_no": "NIT 02/2026-27 Item 1", "division": "Pali Division", "district": "Pali", "cost_lac": 77.00, "published": "2026-09-16 11:00:00", "closing": "2026-09-24 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_42918_2", "nit_no": "NIT 02/2026-27 Item 2", "division": "Pali Division", "district": "Pali", "cost_lac": 81.00, "published": "2026-09-16 11:00:00", "closing": "2026-09-24 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_41829_1", "nit_no": "NIT 05/2026-27 Item 1", "division": "Hanumangarh Div", "district": "Hanumangarh", "cost_lac": 55.00, "published": "2026-09-21 10:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_41829_2", "nit_no": "NIT 05/2026-27 Item 2", "division": "Hanumangarh Div", "district": "Hanumangarh", "cost_lac": 47.50, "published": "2026-09-21 10:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_40918_1", "nit_no": "NIT 08/2026-27 Item 1", "division": "Sri Ganganagar", "district": "Sri Ganganagar", "cost_lac": 90.00, "published": "2026-09-15 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_40918_2", "nit_no": "NIT 08/2026-27 Item 2", "division": "Sri Ganganagar", "district": "Sri Ganganagar", "cost_lac": 94.00, "published": "2026-09-15 10:00:00", "closing": "2026-09-25 18:00:00", "statutory_days": 10},
    {"tender_id": "2026_CEPWD_39812_1", "nit_no": "NIT 13/2026-27 Item 1", "division": "Jhunjhunu Rural Div", "district": "Jhunjhunu", "cost_lac": 34.00, "published": "2026-09-22 10:00:00", "closing": "2026-09-30 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_39812_2", "nit_no": "NIT 13/2026-27 Item 2", "division": "Jhunjhunu Rural Div", "district": "Jhunjhunu", "cost_lac": 39.50, "published": "2026-09-22 10:00:00", "closing": "2026-09-30 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_38901_1", "nit_no": "NIT 06/2026-27 Item 1", "division": "Sikar Rural Div", "district": "Sikar", "cost_lac": 41.00, "published": "2026-09-21 11:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7},
    {"tender_id": "2026_CEPWD_38901_2", "nit_no": "NIT 06/2026-27 Item 2", "division": "Sikar Rural Div", "district": "Sikar", "cost_lac": 44.00, "published": "2026-09-21 11:00:00", "closing": "2026-09-29 18:00:00", "statutory_days": 7}
]

def generate_cryptographic_manifest():
    ledger_entries = []
    hash_list = []

    for item in RAW_RECORDS:
        canonical_payload = (
            f"{item['tender_id']}|"
            f"{item['nit_no']}|"
            f"{item['published']}|"
            f"{item['closing']}|"
            f"{item['cost_lac']:.2f}|"
            f"{item['division']}"
        )
        digest = compute_sha256(canonical_payload)
        hash_list.append(digest)
        
        entry = {
            "tender_id": item["tender_id"],
            "nit_no": item["nit_no"],
            "division": item["division"],
            "district": item["district"],
            "cost_lac": item["cost_lac"],
            "canonical_payload": canonical_payload,
            "sha256_digest": digest
        }
        ledger_entries.append(entry)

    merkle_root = compute_merkle_root(hash_list)

    output_manifest = {
        "metadata": {
            "system": "Project TRUTH Forensic Auditor",
            "statutory_act": "Rajasthan Transparency in Public Procurement Act, 2012",
            "audited_records_count": len(ledger_entries),
            "generated_at": datetime.now().isoformat(),
            "merkle_root": merkle_root,
            "hash_algorithm": "SHA-256"
        },
        "evidence_ledger": ledger_entries
    }

    with open("forensic_ledger.json", "w", encoding="utf-8") as f:
        json.dump(output_manifest, f, indent=2)

    print("Success: Generated forensic_ledger.json")
    print(f"Merkle Root: {merkle_root}")

if __name__ == "__main__":
    generate_cryptographic_manifest()
