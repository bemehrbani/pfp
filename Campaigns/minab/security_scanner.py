#!/usr/bin/env python3
import os
import re

scan_dirs = ["PFP_Platform", "Campaigns", ".github"]
root_dir = "/Users/mahdifarimani/Documents/PFP"

findings = []

patterns = [
    ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("GitHub Token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}")),
    ("Telegram Bot Token", re.compile(r"\b[0-9]{8,10}:[a-zA-Z0-9_-]{35}\b")),
    ("Private Key Header", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Hardcoded Password", re.compile(r"(password|passwd|pwd|secret)\s*[:=]\s*['\"][^'\"]{4,}['\"]", re.I)),
    ("Django Secret Key Hardcoded", re.compile(r"SECRET_KEY\s*=\s*['\"][^'\"]+['\"]")),
    ("Insecure DOM innerHTML", re.compile(r"\.innerHTML\s*=\s*.*(location|params|search|hash|URLSearchParams)", re.I)),
    ("Exposed Server IP", re.compile(r"65\.109\.198\.200")),
    ("Client-side Password Check", re.compile(r"if\s*\([^)]*(password|pass|pin)\s*===?\s*['\"][^'\"]+['\"]", re.I))
]

for d in scan_dirs:
    full_d = os.path.join(root_dir, d)
    if not os.path.exists(full_d):
        continue
    for root, dirs, files in os.walk(full_d):
        if any(x in root for x in [".git", "venv", "node_modules", ".cache", "screening_media"]):
            continue
        for f in files:
            if f.endswith((".py", ".js", ".ts", ".tsx", ".html", ".yml", ".yaml", ".env", ".sh", ".conf", ".md")):
                p = os.path.join(root, f)
                rel_p = os.path.relpath(p, root_dir)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as file:
                        lines = file.readlines()
                        for idx, line in enumerate(lines, 1):
                            for name, pat in patterns:
                                if pat.search(line):
                                    # Filter obvious false positives (e.g. comments, example files)
                                    if "example" in rel_p or "test" in rel_p or ".env.example" in rel_p:
                                        continue
                                    findings.append({
                                        "type": name,
                                        "file": rel_p,
                                        "line": idx,
                                        "snippet": line.strip()[:120]
                                    })
                except Exception as e:
                    pass

print(f"Total potential security alerts found: {len(findings)}")
for item in findings:
    t = item['type']
    fl = item['file']
    ln = item['line']
    sn = item['snippet']
    print(f"[{t}] {fl}:{ln} -> {sn}")
