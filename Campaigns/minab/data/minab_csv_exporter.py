#!/usr/bin/env python3
"""
Minab Incident CSV Exporter Utility
===================================
People for Peace & Justice ry (PFPJ ry)

Exports unified Minab Incident JSON records into standard, clean CSV files
formatted for spreadsheets, data analysis, GIS mapping, and legal briefs.

Output Files:
- minab_victims.csv
- minab_mothers.csv
- minab_family_clusters.csv
- minab_sources.csv
"""

import os
import sys
import json
import csv
import argparse
from typing import Dict, Any, Optional

def export_all(data_file: str, output_dir: str):
    """Parses minab_incident_dataset.json and writes 4 formatted CSV files."""
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Dataset file not found: {data_file}")

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)

    # 1. Victims CSV
    victims = data.get("victims", [])
    victims_path = os.path.join(output_dir, "minab_victims.csv")
    with open(victims_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "victim_id", "full_name_en", "full_name_fa", "father_name", "mother_id",
            "age", "gender", "role", "grade_or_class", "status",
            "identification_method", "burial_location", "photo_url",
            "mosaic_grid_index", "mosaic_border_index", "biography_en", "biography_fa",
            "family_cluster_id", "sources", "injuries_description", "date_of_death"
        ])
        for v in victims:
            grid = v.get("photo_grid")
            grid_idx = ""
            border_idx = ""
            if isinstance(grid, dict):
                grid_idx = str(grid.get("grid_index", ""))
                border_idx = str(grid.get("border_index", ""))
            elif isinstance(grid, str):
                grid_idx = grid

            bio = v.get("biography")
            bio_en = ""
            bio_fa = ""
            if isinstance(bio, dict):
                bio_en = bio.get("en", "")
                bio_fa = bio.get("fa", "")
            elif isinstance(bio, str):
                bio_en = bio

            writer.writerow([
                v.get("id", ""),
                v.get("full_name_en", ""),
                v.get("full_name_fa", ""),
                v.get("father_name") or "",
                v.get("mother_id") or "",
                str(v.get("age", "")) if v.get("age") is not None else "",
                v.get("gender") or "",
                v.get("role", ""),
                v.get("grade_or_class") or "",
                v.get("status", ""),
                v.get("identification_method", ""),
                v.get("burial_location") or "",
                v.get("photo_url") or "",
                grid_idx,
                border_idx,
                bio_en,
                bio_fa,
                v.get("family_cluster_id") or "",
                "; ".join(v.get("sources", [])),
                v.get("injuries_description") or "",
                v.get("date_of_death") or "2026-02-28"
            ])

    # 2. Mothers CSV
    mothers = data.get("mothers", [])
    mothers_path = os.path.join(output_dir, "minab_mothers.csv")
    with open(mothers_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "mother_id", "full_name_en", "full_name_fa", "spouse_name", "is_casualty",
            "status", "profession", "narrative_summary_en", "narrative_summary_fa",
            "children_count", "children_ids", "other_family_member_ids",
            "photo_url", "family_cluster_id", "sources"
        ])
        for m in mothers:
            summary = m.get("narrative_summary")
            sum_en = ""
            sum_fa = ""
            if isinstance(summary, dict):
                sum_en = summary.get("en", "")
                sum_fa = summary.get("fa", "")
            elif isinstance(summary, str):
                sum_en = summary

            children = m.get("children_ids", [])
            writer.writerow([
                m.get("id", ""),
                m.get("full_name_en", ""),
                m.get("full_name_fa", ""),
                m.get("spouse_name") or "",
                "YES" if m.get("is_casualty") else "NO",
                m.get("status", ""),
                m.get("profession") or "",
                sum_en,
                sum_fa,
                len(children),
                "; ".join(children),
                "; ".join(m.get("other_family_member_ids", [])),
                m.get("photo_url") or "",
                m.get("family_cluster_id") or "",
                "; ".join(m.get("sources", []))
            ])

    # 3. Family Clusters CSV
    clusters = data.get("family_clusters", [])
    clusters_path = os.path.join(output_dir, "minab_family_clusters.csv")
    with open(clusters_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "cluster_id", "family_surname_en", "family_surname_fa", "mother_id",
            "total_killed", "total_injured", "member_count", "member_ids",
            "description_en", "description_fa", "neighborhood_or_residence", "sources"
        ])
        for c in clusters:
            desc = c.get("description")
            desc_en = ""
            desc_fa = ""
            if isinstance(desc, dict):
                desc_en = desc.get("en", "")
                desc_fa = desc.get("fa", "")
            elif isinstance(desc, str):
                desc_en = desc

            members = c.get("member_ids", [])
            writer.writerow([
                c.get("cluster_id", ""),
                c.get("family_surname_en", ""),
                c.get("family_surname_fa", ""),
                c.get("mother_id") or "",
                c.get("total_killed", 0),
                c.get("total_injured", 0),
                len(members),
                "; ".join(members),
                desc_en,
                desc_fa,
                c.get("neighborhood_or_residence") or "",
                "; ".join(c.get("sources", []))
            ])

    # 4. Sources CSV
    sources = data.get("sources", [])
    sources_path = os.path.join(output_dir, "minab_sources.csv")
    with open(sources_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "source_id", "title", "outlet", "url", "publication_date",
            "tier", "reliability_score", "notes", "archive_hash"
        ])
        for s in sources:
            writer.writerow([
                s.get("id", ""),
                s.get("title", ""),
                s.get("outlet", ""),
                s.get("url") or "",
                s.get("publication_date") or "",
                str(s.get("tier", "")),
                s.get("reliability_score", 0.0),
                s.get("notes") or "",
                s.get("archive_hash") or ""
            ])

    return {
        "victims": victims_path,
        "mothers": mothers_path,
        "family_clusters": clusters_path,
        "sources": sources_path
    }

def main():
    parser = argparse.ArgumentParser(description="Export Minab Incident records to standard CSV files.")
    parser.add_argument("--data", "-d", default=os.path.join(os.path.dirname(__file__), "minab_incident_dataset.json"),
                        help="Path to minab_incident_dataset.json")
    parser.add_argument("--output", "-o", default=os.path.join(os.path.dirname(__file__), "exports"),
                        help="Output directory for generated CSV files")

    args = parser.parse_args()
    exported = export_all(args.data, args.output)
    print(f"[SUCCESS] Exported {len(exported)} CSV tables to: {args.output}")
    for name, path in exported.items():
        print(f"  • {name}: {path}")

if __name__ == "__main__":
    main()
