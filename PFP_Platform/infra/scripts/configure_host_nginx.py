#!/usr/bin/env python3
"""
Configure host Nginx to proxy Django admin static assets to backend container (127.0.0.1:8001).
Idempotent and safe: creates backups before modifications and rolls back if nginx -t fails.
"""
import glob
import os
import re
import subprocess
import sys

BLOCK = """
    # Django static assets proxy (Admin, DRF, Swagger)
    location ^~ /static/admin/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        expires 30d;
        add_header Cache-Control "public";
    }

    location ^~ /static/rest_framework/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        expires 30d;
        add_header Cache-Control "public";
    }

    location ^~ /static/drf-yasg/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        expires 30d;
        add_header Cache-Control "public";
    }
"""

def main():
    candidate_files = (
        glob.glob('/etc/nginx/sites-enabled/*') +
        glob.glob('/etc/nginx/sites-available/*') +
        glob.glob('/etc/nginx/conf.d/*.conf')
    )

    pfp_files = []
    for f in candidate_files:
        try:
            if os.path.isfile(f) and not f.endswith('.bak'):
                with open(f, 'r') as fp:
                    content = fp.read()
                if 'peopleforpeace.live' in content or '8001' in content or '8080' in content:
                    real_path = os.path.realpath(f)
                    if real_path not in pfp_files:
                        pfp_files.append(real_path)
        except Exception as e:
            print(f"Skipping {f}: {e}")

    print(f"Target Nginx config files: {pfp_files}")
    if not pfp_files:
        print("No target Nginx config files found. Checking default...")
        for f in ['/etc/nginx/sites-available/default', '/etc/nginx/conf.d/default.conf']:
            if os.path.exists(f):
                pfp_files.append(os.path.realpath(f))

    modified_files = []
    for f in pfp_files:
        with open(f, 'r') as fp:
            content = fp.read()

        if '/static/admin/' in content:
            print(f"Rule already present in {f}")
            continue

        backup_path = f + '.bak'
        with open(backup_path, 'w') as fp:
            fp.write(content)

        if 'location /admin/' in content:
            new_content = content.replace('location /admin/', BLOCK + '\n    location /admin/', 1)
        elif 'location /api/' in content:
            new_content = content.replace('location /api/', BLOCK + '\n    location /api/', 1)
        elif 'location / {' in content:
            new_content = content.replace('location / {', BLOCK + '\n    location / {', 1)
        else:
            last_brace = content.rfind('}')
            if last_brace != -1:
                new_content = content[:last_brace] + BLOCK + content[last_brace:]
            else:
                new_content = content + '\n' + BLOCK

        with open(f, 'w') as fp:
            fp.write(new_content)
        modified_files.append((f, backup_path))
        print(f"Injected /static/admin/ rules into {f}")

    if not modified_files:
        print("No Nginx configs needed modifications.")
    else:
        # Test configuration
        test_res = subprocess.run(['nginx', '-t'], capture_output=True, text=True)
        print("nginx -t output:")
        print(test_res.stdout)
        print(test_res.stderr)

        if test_res.returncode == 0:
            reload_res = subprocess.run(['systemctl', 'reload', 'nginx'], capture_output=True, text=True)
            if reload_res.returncode != 0:
                subprocess.run(['nginx', '-s', 'reload'])
            print("✅ Host Nginx reloaded successfully")
        else:
            print("❌ Nginx test failed! Restoring backups...")
            for f, bak in modified_files:
                if os.path.exists(bak):
                    with open(bak, 'r') as bfp, open(f, 'w') as orig_fp:
                        orig_fp.write(bfp.read())
            subprocess.run(['nginx', '-t'])
            sys.exit(1)

if __name__ == '__main__':
    main()
