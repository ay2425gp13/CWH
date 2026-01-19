## Smile & Sunshine Toy — Local Preview

This repo is a front-end prototype. You can run it locally with the included `start.bat`.

### Quick Start (Windows)
1) Ensure you have **one** of the following installed:
   - Python 3 (recommended), or
   - Node.js with `npx`.
2) Double-click `start.bat`.
   - The script tries `python -m http.server 8000`; if Python is missing, it falls back to `npx serve -l 8000 .`.
   - Your default browser will open `http://127.0.0.1:8000/frontend/platform-market.html`.

### Manual Start (if you prefer the terminal)
- Using Python:
  ```bash
  cd E:\ITP4506
  python -m http.server 8000
  ```
  Then open: `http://127.0.0.1:8000/frontend/platform-market.html`

- Using Node (serve):
  ```bash
  cd E:\ITP4506
  npx serve -l 8000 .
  ```
  Then open: `http://127.0.0.1:8000/frontend/platform-market.html`

### Notes
- The project is static; no database is required. Some demo data may be hard-coded or stored in localStorage.
- If port 8000 is occupied, change `PORT` in `start.bat` (first lines) and update the URL accordingly.
- For grading/demo, also include `USERS.TXT` listing predefined usernames/passwords (if required by assignment).

