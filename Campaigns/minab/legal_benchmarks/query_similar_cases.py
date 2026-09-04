#!/usr/bin/env python3
"""
International Criminal & Humanitarian Law Similar Cases Query Pipeline
People for Peace & Justice ry (PFPJ ry) — Helsinki, Finland

Connects to:
1. European Court of Human Rights (HUDOC) REST API
2. US Federal Case Law & OLC Opinions (CourtListener REST API v4)
3. Local Precedents Database (Campaigns/minab/legal_benchmarks/)
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import argparse

LOCAL_BENCHMARKS_DIR = os.path.dirname(os.path.abspath(__file__))

def query_hudoc(keywords, max_results=10):
    """
    Queries the HUDOC database of the European Court of Human Rights.
    Matches Article 2, targeting errors, military operations, and civilian casualties.
    """
    print(f"\n[HUDOC / ECtHR] Querying for keywords: \"{keywords}\" (limit: {max_results})...")
    base_url = "https://hudoc.echr.coe.int/app/query/results"
    
    query_str = f"({keywords})"
    params = {
        "query": query_str,
        "select": "itemid,docname,appno,decisiondate,conclusion,importance,respondent",
        "sort": "",
        "start": 0,
        "length": max_results
    }
    
    url = base_url + "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) PFPJ-Legal-Research/1.0",
        "Accept": "application/json",
        "Referer": "https://hudoc.echr.coe.int/eng"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            total = data.get("resultcount", 0)
            results = data.get("results", [])
            print(f"✅ HUDOC Query Successful! Found {total} matching cases. Showing top {len(results)}:\n")
            
            output_cases = []
            for idx, item in enumerate(results, 1):
                col = item.get("columns", {})
                item_id = col.get("itemid", "")
                title = col.get("docname", "Untitled")
                app_no = col.get("appno", "N/A")
                date = col.get("decisiondate", "N/A")
                resp_state = col.get("respondent", "N/A")
                hudoc_url = f"https://hudoc.echr.coe.int/eng?i={item_id}"
                
                print(f"  {idx}. {title}")
                print(f"     • App No: {app_no} | Date: {date} | State: {resp_state}")
                print(f"     • Direct Link: {hudoc_url}")
                output_cases.append({
                    "source": "HUDOC",
                    "title": title,
                    "app_no": app_no,
                    "date": date,
                    "respondent": resp_state,
                    "url": hudoc_url
                })
            return output_cases
    except Exception as e:
        print(f"❌ HUDOC API Request Failed: {e}")
        return []

def query_courtlistener(keywords, max_results=10):
    """
    Queries CourtListener API for US Federal, Appellate, and OLC opinions
    on civilian strikes, command negligence, and sovereign immunity.
    """
    print(f"\n[CourtListener / US Jurisprudence] Querying for keywords: \"{keywords}\" (limit: {max_results})...")
    base_url = "https://www.courtlistener.com/api/rest/v4/search/"
    params = {
        "q": keywords,
        "type": "o",
        "format": "json"
    }
    url = base_url + "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": "PFPJ-Legal-Research/1.0 (info@peopleforpeace.live)"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            count = data.get("count", 0)
            results = data.get("results", [])[:max_results]
            print(f"✅ CourtListener Query Successful! Found {count} cases. Showing top {len(results)}:\n")
            
            output_cases = []
            for idx, item in enumerate(results, 1):
                case_name = item.get("caseName", "Untitled")
                court = item.get("court", "Federal Court")
                date_filed = item.get("dateFiled", "N/A")
                docket_url = f"https://www.courtlistener.com{item.get('absolute_url', '')}"
                
                print(f"  {idx}. {case_name}")
                print(f"     • Court: {court} | Date: {date_filed}")
                print(f"     • Docket Link: {docket_url}")
                output_cases.append({
                    "source": "CourtListener",
                    "title": case_name,
                    "court": court,
                    "date": date_filed,
                    "url": docket_url
                })
            return output_cases
    except Exception as e:
        print(f"❌ CourtListener API Request Failed: {e}")
        return []

def list_local_benchmarks():
    """
    Lists the 18 local benchmark precedents in the PFP repository.
    """
    index_file = os.path.join(LOCAL_BENCHMARKS_DIR, "index.md")
    if not os.path.exists(index_file):
        print("Local benchmarks index not found.")
        return
    
    print("\n[PFP Local Legal Benchmarks] (18 International Comparative Cases):")
    print("-" * 75)
    with open(index_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("### Case ") or line.startswith("| **[Case"):
                print(line.strip())
    print("-" * 75)
    print(f"Full details available at: {index_file}")

def main():
    parser = argparse.ArgumentParser(description="Query International Criminal Cases and Benchmarks Pipeline")
    parser.add_argument("--query", "-q", type=str, help="Search keywords (e.g. 'airstrike school', 'collateral damage')")
    parser.add_argument("--source", "-s", choices=["all", "hudoc", "courtlistener", "local"], default="all", help="Target data source")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum results to return per API")
    args = parser.parse_args()

    if args.source == "local" or not args.query:
        list_local_benchmarks()
        if not args.query:
            print("\nTip: Pass --query \"keywords\" to query live international jurisprudence APIs.")
            return

    results = []
    if args.source in ("all", "hudoc"):
        results.extend(query_hudoc(args.query, args.limit))
    if args.source in ("all", "courtlistener"):
        results.extend(query_courtlistener(args.query, args.limit))

if __name__ == "__main__":
    main()
