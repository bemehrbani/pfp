#!/usr/bin/env python3
"""
scripts/download_dropsite_images.py
-------------------------------------------------------------------------------
Download and cryptographically verify all primary visual exhibits and child survivor
drawings from the Drop Site News investigation (Jeremy Scahill et al., 2026-09-30)
into Campaigns/minab/data/sources_archive/images/dropsite/.
-------------------------------------------------------------------------------
"""

import os
import sys
import hashlib
import json
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "Campaigns" / "minab" / "data" / "sources_archive" / "images" / "dropsite"
MANIFEST_FILE = OUTPUT_DIR / "images_manifest.json"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "id": "IMG-DROPSITE-01",
        "filename": "01_fatemeh_zahra_drawing_cemetery.jpeg",
        "description": "Fatemeh Zahra Bahrami (survivor) drawing: school bombing with martyrs cemetery in background",
        "url": "https://substackcdn.com/image/fetch/$s_!_dXh!,w_1600,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff77f0cbd-b4d0-4b4c-b863-952b4b5b7410_1600x800.jpeg"
    },
    {
        "id": "IMG-DROPSITE-02",
        "filename": "02_fatemeh_yazdanpanah_and_father.jpg",
        "description": "Fatemeh Yazdanpanah (6 yo victim) and with her father Yaghoub Yazdanpanah",
        "url": "https://substackcdn.com/image/fetch/$s_!80nA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F925d3679-139b-4a5d-89c2-bacc8e97cac1_2100x1500.tif"
    },
    {
        "id": "IMG-DROPSITE-03",
        "filename": "03_hossniyeh_salem_teacher.jpeg",
        "description": "Hossniyeh Salem, Shajareh Tayyebeh preschool teacher, with her niece",
        "url": "https://substackcdn.com/image/fetch/$s_!Xx6b!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F76bf3f0d-e52e-4f1e-9526-8e69e7ce6923_1600x915.jpeg"
    },
    {
        "id": "IMG-DROPSITE-04",
        "filename": "04_destroyed_school_exterior_august2026.jpeg",
        "description": "Destroyed Shajareh Tayyebeh school building surrounded by rubble (Atta Kenare / AFP)",
        "url": "https://substackcdn.com/image/fetch/$s_!HamH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa4c4f90c-c50f-4c39-beb2-bbb149e814dc_6000x4000.jpeg"
    },
    {
        "id": "IMG-DROPSITE-05",
        "filename": "05_father_talking_to_child_backpack.jpeg",
        "description": "Father talking to child's backpack in rubble after strike (Photo: Majid Dadania / Red Crescent)",
        "url": "https://substackcdn.com/image/fetch/$s_!BZBy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2dca5318-4563-44ac-898c-e8333fbfb458_900x977.jpeg"
    },
    {
        "id": "IMG-DROPSITE-06",
        "filename": "06_recovered_raytheon_missile_fragments.jpeg",
        "description": "Tomahawk missile fragments recovered from Minab showing Raytheon CAGE code components",
        "url": "https://substackcdn.com/image/fetch/$s_!0UX6!,w_800,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1f3218d3-238e-42a7-a057-23c7aee39ca8_1532x2048.jpeg"
    },
    {
        "id": "IMG-DROPSITE-07",
        "filename": "07_hegseth_caine_press_briefing.jpeg",
        "description": "Pete Hegseth and Gen. Dan Caine Pentagon press conference March 2, 2026 (AFP)",
        "url": "https://substackcdn.com/image/fetch/$s_!Sv5D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24bbc57f-4fed-47ed-a858-804d4f9c5d6f_5073x3382.jpeg"
    },
    {
        "id": "IMG-DROPSITE-08",
        "filename": "08_trump_monitoring_iran_strikes.jpeg",
        "description": "Donald Trump monitoring military operations against Iran in Washington March 2, 2026 (Anadolu)",
        "url": "https://substackcdn.com/image/fetch/$s_!bP1H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbdad9fb9-b4b8-46dc-a40d-2c6b04f8d168_4096x2730.jpeg"
    },
    {
        "id": "IMG-DROPSITE-09",
        "filename": "09_trump_hegseth_air_force_one.jpeg",
        "description": "Trump and Hegseth stepping off Air Force One March 18, 2026 (Jim Watson / AFP)",
        "url": "https://substackcdn.com/image/fetch/$s_!C8_x!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F291ddc6f-a9b8-4fe6-8665-906f4d7a3c1a_2430x1619.jpeg"
    },
    {
        "id": "IMG-DROPSITE-10",
        "filename": "10_destroyed_classroom_interior.jpeg",
        "description": "View from inside destroyed classroom at Shajareh Tayyebeh (Atta Kenare / AFP)",
        "url": "https://substackcdn.com/image/fetch/$s_!pJFq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe94b9b73-154d-4bf2-acdf-8eda2422ee3c_6000x4000.jpeg"
    },
    {
        "id": "IMG-DROPSITE-11",
        "filename": "11_mohammad_sharafi_drawing.jpeg",
        "description": "Drawing by child survivor Mohammad Sharafi (hands burned, sister/aunt killed)",
        "url": "https://substackcdn.com/image/fetch/$s_!ZvDy!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F67b38a5c-27cb-46e5-82b5-b954e3fc2918_1010x720.jpeg"
    },
    {
        "id": "IMG-DROPSITE-12",
        "filename": "12_fatemeh_zahra_drawing_missile_strike.jpeg",
        "description": "Drawing by survivor Fatemeh Zahra Bahrami: Tomahawk missile hitting schoolyard",
        "url": "https://substackcdn.com/image/fetch/$s_!DPVp!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F99643379-00c8-4c48-bbea-0ffb7af4b740_722x1038.jpeg"
    },
    {
        "id": "IMG-DROPSITE-13",
        "filename": "13_funeral_fatemeh_and_asra.jpeg",
        "description": "Mourners holding portrait of Fatemeh Yazdanpanah and cousin Asra at funeral ceremony (Anadolu)",
        "url": "https://substackcdn.com/image/fetch/$s_!sdXG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf2de28c-9a20-4326-afcf-a6643e7518f9_2560x1920.jpeg"
    },
    {
        "id": "IMG-DROPSITE-14",
        "filename": "14_fatemeh_zahra_drawing_trump_serpent.jpeg",
        "description": "Drawing by survivor Fatemeh Zahra Bahrami: Trump, missile with Israeli flag, and serpent",
        "url": "https://substackcdn.com/image/fetch/$s_!1BZY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9bd02269-ae0f-4b0d-9328-b82e59657f6a_842x595.jpeg"
    },
    {
        "id": "IMG-DROPSITE-15",
        "filename": "15_teacher_salem_and_son_at_site.png",
        "description": "Teacher Hossniyeh Salem and her surviving son Yassin at site of bombing (Reuters Connect)",
        "url": "https://substackcdn.com/image/fetch/$s_!39gk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2d0ea0e1-6922-4e62-a183-18d19f59521a_3826x2141.png"
    },
    {
        "id": "IMG-DROPSITE-16",
        "filename": "16_asra_child_survivor_drawing.jpeg",
        "description": "Drawing by child survivor Asra (depicting severed hand seen during strike)",
        "url": "https://substackcdn.com/image/fetch/$s_!jBYo!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52285be0-a176-4e15-a20a-4efd8c8991e5_842x595.jpeg"
    },
    {
        "id": "IMG-DROPSITE-17",
        "filename": "17_backpack_and_books_memorial.jpeg",
        "description": "Women holding up schoolbooks and backpack of martyred children (Photo: Morteza Akhondi)",
        "url": "https://substackcdn.com/image/fetch/$s_!dzvd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd65feaa4-ce1d-4b14-8f69-1a9cc3e711ae_2560x1440.jpeg"
    },
    {
        "id": "IMG-DROPSITE-18",
        "filename": "18_yazdanpanah_parents_in_gurzang.jpeg",
        "description": "Yaghoub Yazdanpanah and Masoumeh Farahi Zadeh (parents of Fatemeh) in Gurzang (Zohreh Saberi)",
        "url": "https://substackcdn.com/image/fetch/$s_!eKkJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f17d055-d9fa-444a-92c2-f6f5bd245c04_5472x3648.jpeg"
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
}

manifest_records = []

print(f"Downloading {len(IMAGES)} Drop Site News images to {OUTPUT_DIR}...")

for item in IMAGES:
    target_path = OUTPUT_DIR / item["filename"]
    print(f"-> Fetching {item['id']}: {item['filename']}...")
    try:
        req = urllib.request.Request(item["url"], headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(target_path, "wb") as f:
                f.write(data)
            
            sha256 = hashlib.sha256(data).hexdigest()
            size = len(data)
            print(f"   [OK] Size: {size} bytes, SHA-256: {sha256[:12]}...")
            
            manifest_records.append({
                "id": item["id"],
                "filename": item["filename"],
                "description": item["description"],
                "size_bytes": size,
                "sha256": sha256,
                "source_url": item["url"]
            })
    except Exception as e:
        print(f"   [ERROR] Failed to fetch {item['filename']}: {e}")

with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump({
        "collection": "Drop Site News Minab Massacre Photo Archive",
        "total_images": len(manifest_records),
        "source_investigation": "https://www.dropsitenews.com/p/minab-school-massacre-iran-war-children-families",
        "images": manifest_records
    }, f, indent=2, ensure_ascii=False)

print(f"\nCompleted! Manifest written to {MANIFEST_FILE}")
