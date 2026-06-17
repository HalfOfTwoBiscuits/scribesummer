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

@app.cli.command("populate")
def populate():
    '''Pre-populate the database with subscription
    presets and categories from model/data/presets.json
    and model/data/categories.json.
    
    If a preset or category already exists then it will be updated
    to match the JSON data.'''

    factory.model_handler.prepopulator.populate()