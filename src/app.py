import sys
import os

from dotenv import load_dotenv

from scribesummer.src.ssum import AppFactory

# Add this app to PATH. Necessary for it to deploy on the server.
sys.path.insert(0, os.path.dirname(__file__))

# Load environment files.
load_dotenv()

# Initialise app.
factory = AppFactory()

# On the server WSGI script to deploy the app, 'application' is imported.
app = application = factory.app