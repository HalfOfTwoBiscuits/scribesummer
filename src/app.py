import sys
import os

from dotenv import load_dotenv

from scribesummer.src.ssum import create_app

# Add this app to PATH. Necessary for it to deploy on the server.
sys.path.insert(0, os.path.dirname(__file__))

# Load environment files.
load_dotenv()

# On the server WSGI script to deploy the app, 'application' is imported.
app = application = create_app()