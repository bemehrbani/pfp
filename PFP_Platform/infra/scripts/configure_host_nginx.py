#!/usr/bin/env python3
"""
Inspect and configure host Nginx for Django static assets (peopleforpeace.live).
"""
import glob
import os
import re
import subprocess
import sys

CORRECT_BLOCK = """
    # Django static assets proxy (Admin, DRF, Swagger) - ^~ overrides regex
    location ^~ /static/admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location ^~ /static/rest_framework/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
    }
    location ^~ /static/drf-yasg/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
    }
"""

def main():
    print("=== Host Nginx Inspection ===")
    print("sites-enabled:", os.listdir('/etc/nginx/sites-enabled/') if os.path.exists('/etc/nginx/sites-enabled/') else 'none')
    print("sites-available:", os.listdir('/etc/nginx/sites-available/') if os.path.exists('/etc/nginx/sites-available/') else 'none')

    target_files = []
    for d in ['/etc/nginx/sites-enabled', '/etc/nginx/sites-available', '/etc/nginx/conf.d']:
        if os.path.exists(d):
            for f in os.listdir(d):
                p = os.path.join(d, f)
                if os.path.isfile(p) and not f.endswith('.bak') and not f.startswith('.'):
                    try:
                        content = open(p).read()
                        if 'peopleforpeace.live' in content:
                            real = os.path.realpath(p)
                            if real not in target_files:
                                target_files.append(real)
                    except Exception as e:
                        print(f"Error reading {p}: {e}")

    print(f"PFP Config files found: {target_files}")
    for tf in target_files:
        print(f"\n--- BEGIN {tf} ---")
        with open(tf) as fp:
            content = fp.read()
        print(content)
        print(f"--- END {tf} ---\n")

        # Replace existing static/admin block if it lacks ^~ or points to wrong port
        # or remove old static/admin blocks and inject correct one
        backup = tf + '.bak'
        with open(backup, 'w') as bfp:
            bfp.write(content)

        # Regex remove any existing location [/~^ ]* /static/admin/ { ... }
        # Clean replacement:
        cleaned = re.sub(r'location\s+[\^~]*\s*/static/admin/\s*\{[^}]*\}', '', content)
        cleaned = re.sub(r'location\s+[\^~]*\s*/static/rest_framework/\s*\{[^}]*\}', '', cleaned)
        cleaned = re.sub(r'location\s+[\^~]*\s*/static/drf-yasg/\s*\{[^}]*\}', '', cleaned)

        # Inject CORRECT_BLOCK right before location /admin/ or location /api/ or location /
        if 'location /admin/' in cleaned:
            updated = cleaned.replace('location /admin/', CORRECT_BLOCK + '\n    location /admin/', 1)
        elif 'location /api/' in cleaned:
            updated = cleaned.replace('location /api/', CORRECT_BLOCK + '\n    location /api/', 1)
        elif 'location / {' in cleaned:
            updated = cleaned.replace('location / {', CORRECT_BLOCK + '\n    location / {', 1)
        else:
            idx = cleaned.rfind('}')
            updated = cleaned[:idx] + CORRECT_BLOCK + cleaned[idx:]

        with open(tf, 'w') as ufp:
            ufp.write(updated)
        print(f"Rewrote {tf} with ^~ static proxy to 127.0.0.1:8001")

    # Test and reload
    t = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
    print("nginx -t stdout:", t.stdout)
    print("nginx -t stderr:", t.stderr)
    if t.returncode == 0:
        subprocess.run(['systemctl', 'reload', 'nginx'])
        print("✅ Host Nginx reloaded successfully")
    else:
        print("❌ Nginx config test failed! Restoring backups...")
        for tf in target_files:
            bak = tf + '.bak'
            if os.path.exists(bak):
                open(tf, 'w').write(open(bak).read())
        subprocess.run(['nginx', '-t'])
        sys.exit(1)

    # Now verify locally on host via curl
    print("\n=== Testing local curl via host Nginx ===")
    c1 = subprocess.run(
        ['curl', '-sI', 'http://127.0.0.1/static/admin/css/base.523eb49842a7.css', '-H', 'Host: peopleforpeace.live'],
        capture_output=True, text=True
    )
    print("Host Nginx HTTP response for base.css:")
    print(c1.stdout)

    c2 = subprocess.run(
        ['curl', '-k', '-sI', 'https://127.0.0.1/static/admin/css/base.523eb49842a7.css', '-H', 'Host: peopleforpeace.live'],
        capture_output=True, text=True
    )
    print("Host Nginx HTTPS response for base.css:")
    print(c2.stdout)

if __name__ == '__main__':
    main()
