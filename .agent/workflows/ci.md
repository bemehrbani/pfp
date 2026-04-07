---
description: Check CI/CD Pipeline Status
---

# CI/CD Pipeline Workflow

## Monitor CI/CD Pipeline

The Continuous Integration/Continuous Deployment (CI/CD) pipeline runs automatically on push to `main` via GitHub Actions (`.github/workflows/ci.yml`).

// turbo
1. Check the status of the latest run:
```bash
cd /Users/mahdifarimani/Documents/PFP && gh run list -w "CI/CD Pipeline" -L 5
```

// turbo
2. View detailed logs of a specific run (replace `[RUN_ID]` with the actual ID from step 1):
```bash
# Example: gh run view 23607983698 --log
cd /Users/mahdifarimani/Documents/PFP && gh run view $(gh run list -w "CI/CD Pipeline" -L 1 --json databaseId -q ".[0].databaseId")
```

## Troubleshooting Failures

If the pipeline fails, it is typically in one of these four jobs:
- **backend-tests**: Check `apps/users/api/views.py` permissions (`is_staff` vs roles) and `ActivityLog` creation logic in signals.
- **frontend-build**: Dependency issues. Run `npm ci --legacy-peer-deps`.
- **docker-build**: Failing health checks. Use `docker-compose logs backend` locally to see what failed to start.
- **security-scan**: Bandit issues. Ensure `bandit -r backend/` ignores safe test fixtures using `# nosec`.

> [!IMPORTANT]
> The codebase enforces strict adherence to PFP's custom role-based (`User.Role`) permissions rather than default Django `is_staff` checks. Always use `apps.users.permissions.IsAdminUser` over the default DRF import.
