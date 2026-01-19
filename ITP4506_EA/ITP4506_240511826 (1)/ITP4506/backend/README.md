# Backend for Second-hand Marketplace

This is the backend API for the second-hand marketplace login system.

## Features Implemented

1. User registration
2. User login with username/password
3. Password hashing for security
4. "Remember me" functionality
5. Session management
6. Forgot password endpoint
7. Google login endpoint (placeholder)
8. 2FA support (placeholder)

## Setup Instructions

### 1) Create and activate a virtual environment (Windows PowerShell)
```powershell
cd ..\..\fyp\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you see an execution policy error, run PowerShell as Administrator once:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Run the server (development)
Option A: python entrypoint
```powershell
python app.py
```

Option B: flask CLI
```powershell
$env:FLASK_APP = "app:create_app"
$env:FLASK_ENV = "development"
flask run --host 0.0.0.0 --port 5000
```

The API will be available at `http://127.0.0.1:5000/`.

### 4) Frontend (static HTML)
Open `frontend/login.html` directly in a browser, or serve the folder with any static server.
