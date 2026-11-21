# CyberSakhi — Digital Safety Companion

A runnable Django starter project for digital-safety awareness, scam checking, incident reporting and learning.

## Included features
- User registration, login and logout
- Dashboard with the user's submitted reports
- Heuristic scam checker for URLs, messages and emails (educational screening, not a guarantee)
- Private incident reports with reference IDs and status tracking
- Awareness library with searchable scam guides
- Cybersecurity quiz with score feedback
- Safety recommendations
- Admin panel for managing reports and awareness articles
- Community scam-trend summaries using aggregate counts only
- Personal safety checklist with a self-assessment score
- Save/bookmark awareness guides to a personal library

## Requirements
- Python 3.10 or newer
- VS Code
- Internet connection only for installing Django (the app itself runs locally)

## Run on Windows (PowerShell)

Open this folder in VS Code, then open Terminal → New Terminal.

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/

If PowerShell blocks activation, use Command Prompt terminal instead:
```cmd
venv\Scripts\activate.bat
```
Then run the pip/migrate/seed/runserver commands above.

## Admin account
Create your own administrator:
```powershell
python manage.py createsuperuser
```
Then visit http://127.0.0.1:8000/admin/

## Important notes
- The detector uses transparent, rule-based indicators. It is not a trained AI model and cannot confirm whether something is safe or fraudulent.
- Do not submit passwords, OTPs, bank details, identity documents or other sensitive information.
- Reports are private to the account that submitted them; administrators can review them.
- After extracting this updated version, run `makemigrations core` and `migrate` before using the new features. If you already have a database from an older version, keep your `db.sqlite3` and apply migrations; do not delete it.
- This is a college/portfolio prototype. Before public deployment, add HTTPS, secure production settings, rate limiting, stronger file/evidence handling, privacy notices, retention controls and professional security review.
