from flask import send_file
from flask.views import View

class PWAManifest(View):
    def __init__(self, model_handler, form_handler):
        pass

    def dispatch_request(self) -> str:
        return send_file('manifest.json', mimetype='application/manifest+json')