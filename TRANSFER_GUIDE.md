# Transfer Guide

## Copy to USB

Copy the full `AI-Disaster-platform` folder to your USB drive:

If you want a smaller transfer, you can remove these folders before copying:

- `backend\.venv`
- `frontend\node_modules`
- `backend\__pycache__`

## On your friend's laptop:

1. Copy the project folder from the USB to the desktop or any local folder.
2. Make sure Python and Node.js are installed.
3. Open the project folder.
4. Double-click `start_backend.bat`
5. Open a second terminal or window and double-click `start_frontend.bat`

## Open in browser

- Frontend: `http://localhost:5173`
- Backend docs: `http://127.0.0.1:8000/docs`
- Backend health: `http://127.0.0.1:8000/health`

## If PowerShell blocks scripts:

Use Command Prompt or run the `.bat` files directly by double-clicking them.

## If something fails

- Re-check that Python is installed and available as `python`
- Re-check that Node.js and npm are installed
- Run backend and frontend from VS Code terminal if double-click launching closes too fast
