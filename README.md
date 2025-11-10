# deed_edison_clone

A FastAPI + Jinja2 + SQLAlchemy (async) full-stack template that mirrors the IA/UX of edisonrealestatebd.com (menu structure, sections, forms) with original code and placeholder content.

## Run
```bash
python -m venv .venv
# Windows
. .venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn src.backend.app:app --reload
```
Open http://127.0.0.1:8000/

# PowerShell Command to Remove __pycache__ Directories

```bash
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

```

Run Command:

uvicorn src.backend.app:app --reload --host 127.0.0.1 --port 8000



requirements.txt (put this at repo root)

fastapi==0.115.2
uvicorn[standard]==0.30.6
jinja2==3.1.4
pydantic==2.9.2
pydantic-settings==2.6.0
SQLAlchemy==2.0.36
asyncpg==0.29.0
alembic==1.13.2
python-multipart==0.0.9
email-validator==2.2.0
# Add these to requirements for security hardening
fastapi-csrf-protect==0.3.5
fastapi-limiter==0.1.6
aioredis==2.0.1
argon2-cffi==23.1.0
passlib[argon2]==1.7.4
pip-audit==2.7.3
bandit==1.7.9
ruff==0.6.9
mypy==1.11.2
sentry-sdk==2.14.0
python-dotenv
pytz