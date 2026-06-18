from flask import render_template
from flask.views import View

class AddSubscription(View):
    def __init__(self, model_handler, form_handler):
        self.__mh = model_handler
        self.__fh = form_handler

    def dispatch_request(self) -> str:
        return render_template("add_subscription.html")