#!/usr/bin/env python3
"""
Minab Platform Backend Adapter
==============================
People for Peace & Justice ry (PFPJ ry)

Converts the unified Minab Incident JSON dataset into:
1. Django fixtures (JSON format) suitable for `python manage.py loaddata` in PFP_Platform/api.
2. Direct seed dictionary payload for API endpoints and ORM models.
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any

def convert_to_django_fixtures(dataset_path: str, output_fixture_path: str):
    """Transforms minab_incident_dataset.json into Django ORM fixture format."""
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset path not found: {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixtures: List[Dict[str, Any]] = []

    # 1. Incident Metadata Fixture
    meta = data.get("incident_metadata", {})
    fixtures.append({
        "model": "campaigns.incident",
        "pk": meta.get("incident_id", "MINAB-2026-0228"),
        "fields": {
            "name_en": meta.get("incident_name_en"),
            "name_fa": meta.get("incident_name_fa"),
            "date": meta.get("incident_date"),
            "time_local": meta.get("incident_time_local"),
            "facility_en": meta.get("target_facility_en"),
            "facility_fa": meta.get("target_facility_fa"),
            "city": meta.get("city"),
            "province": meta.get("province"),
            "country": meta.get("country"),
            "latitude": meta.get("coordinates", {}).get("latitude"),
            "longitude": meta.get("coordinates", {}).get("longitude"),
            "weapon_system": meta.get("weapon_system"),
            "responsible_force": meta.get("responsible_force"),
            "legal_standard_of_proof": meta.get("legal_standard_of_proof"),
            "summary_en": meta.get("summary", {}).get("en") if isinstance(meta.get("summary"), dict) else "",
            "summary_fa": meta.get("summary", {}).get("fa") if isinstance(meta.get("summary"), dict) else ""
        }
    })

    # 2. Source References
    for s in data.get("sources", []):
        fixtures.append({
            "model": "campaigns.sourcereference",
            "pk": s.get("id"),
            "fields": {
                "title": s.get("title"),
                "outlet": s.get("outlet"),
                "url": s.get("url"),
                "publication_date": s.get("publication_date"),
                "tier": str(s.get("tier")),
                "reliability_score": s.get("reliability_score", 0.0),
                "notes": s.get("notes"),
                "archive_hash": s.get("archive_hash")
            }
        })

    # 3. Family Clusters
    for fc in data.get("family_clusters", []):
        desc_en = fc.get("description", {}).get("en") if isinstance(fc.get("description"), dict) else (fc.get("description") or "")
        desc_fa = fc.get("description", {}).get("fa") if isinstance(fc.get("description"), dict) else ""
        fixtures.append({
            "model": "campaigns.familycluster",
            "pk": fc.get("cluster_id"),
            "fields": {
                "surname_en": fc.get("family_surname_en"),
                "surname_fa": fc.get("family_surname_fa"),
                "mother_id": fc.get("mother_id"),
                "total_killed": fc.get("total_killed", 0),
                "total_injured": fc.get("total_injured", 0),
                "member_ids": fc.get("member_ids", []),
                "description_en": desc_en,
                "description_fa": desc_fa,
                "neighborhood": fc.get("neighborhood_or_residence")
            }
        })

    # 4. Mother Profiles
    for m in data.get("mothers", []):
        sum_en = m.get("narrative_summary", {}).get("en") if isinstance(m.get("narrative_summary"), dict) else (m.get("narrative_summary") or "")
        sum_fa = m.get("narrative_summary", {}).get("fa") if isinstance(m.get("narrative_summary"), dict) else ""
        fixtures.append({
            "model": "campaigns.motherprofile",
            "pk": m.get("id"),
            "fields": {
                "full_name_en": m.get("full_name_en"),
                "full_name_fa": m.get("full_name_fa"),
                "spouse_name": m.get("spouse_name"),
                "is_casualty": m.get("is_casualty", False),
                "status": m.get("status"),
                "profession": m.get("profession"),
                "narrative_summary_en": sum_en,
                "narrative_summary_fa": sum_fa,
                "children_ids": m.get("children_ids", []),
                "other_family_member_ids": m.get("other_family_member_ids", []),
                "photo_url": m.get("photo_url"),
                "family_cluster": m.get("family_cluster_id"),
                "sources": m.get("sources", [])
            }
        })

    # 5. Victims
    for v in data.get("victims", []):
        bio_en = v.get("biography", {}).get("en") if isinstance(v.get("biography"), dict) else (v.get("biography") or "")
        bio_fa = v.get("biography", {}).get("fa") if isinstance(v.get("biography"), dict) else ""
        grid_data = v.get("photo_grid") if isinstance(v.get("photo_grid"), dict) else {}

        fixtures.append({
            "model": "campaigns.victim",
            "pk": v.get("id"),
            "fields": {
                "full_name_en": v.get("full_name_en"),
                "full_name_fa": v.get("full_name_fa"),
                "father_name": v.get("father_name"),
                "mother": v.get("mother_id"),
                "age": v.get("age"),
                "gender": v.get("gender"),
                "role": v.get("role"),
                "grade_or_class": v.get("grade_or_class"),
                "status": v.get("status"),
                "identification_method": v.get("identification_method"),
                "burial_location": v.get("burial_location"),
                "photo_url": v.get("photo_url"),
                "grid_index": grid_data.get("grid_index"),
                "border_index": grid_data.get("border_index"),
                "biography_en": bio_en,
                "biography_fa": bio_fa,
                "family_cluster": v.get("family_cluster_id"),
                "sources": v.get("sources", []),
                "injuries_description": v.get("injuries_description"),
                "date_of_death": v.get("date_of_death", "2026-02-28")
            }
        })

    os.makedirs(os.path.dirname(os.path.abspath(output_fixture_path)), exist_ok=True)
    with open(output_fixture_path, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, ensure_ascii=False, indent=2)

    return len(fixtures)

def main():
    parser = argparse.ArgumentParser(description="Convert Minab dataset to Django fixture JSON.")
    parser.add_argument("--data", "-d", default=os.path.join(os.path.dirname(__file__), "minab_incident_dataset.json"),
                        help="Input minab_incident_dataset.json")
    parser.add_argument("--output", "-o", default=os.path.join(os.path.dirname(__file__), "minab_django_fixture.json"),
                        help="Output Django fixture JSON file")

    args = parser.parse_args()
    count = convert_to_django_fixtures(args.data, args.output)
    print(f"[SUCCESS] Generated {count} Django fixture objects at: {args.output}")

if __name__ == "__main__":
    main()
