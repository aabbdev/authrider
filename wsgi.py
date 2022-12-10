"""WSGI entry point for authrider."""
import os
import signal
import sys
from waitress import serve
from app import app

def graceful_exit(_signum, _frame):
    """Gracefully exit the application."""
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, graceful_exit)
    signal.signal(signal.SIGINT, graceful_exit)
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
