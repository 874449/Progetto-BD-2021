ECHO OFF
ECHO Setting up flask for you...
ECHO [Info] Installing dependencies
pip install -r requirements.txt
ECHO [Info] DONE
ECHO 
ECHO [Info] Setting up environment variables
set FLASK_APP=runner.py
set FLASK_ENV=development
set FLASK_DEBUG=1
ECHO [Info] DONE
ECHO 
ECHO [Info] Creating tables in DB
flask create_tables
ECHO [Info] Setup complete
PAUSE
