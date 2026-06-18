from flask import render_template, redirect, url_for
from flask.views import View
from werkzeug.wrappers.response import Response

class AddSubscription(View):
    methods = ["GET", "POST"]

    def __init__(self, model_handler, form_handler):
        self.__mh = model_handler
        self.__AddCustomSubForm = form_handler.get_form("AddCustomSubscription")

    def dispatch_request(self) -> str | Response:
        form = self.__AddCustomSubForm(self.__mh)
        CategoryModel = self.__mh.get_model("Category")

        cats = self.__mh.db.session.execute(
            self.__mh.db.select(CategoryModel)
        ).scalars()
        cat_names = [cat.name for cat in cats]
        form.categories.choices = cat_names

        if form.validate_on_submit():
            return redirect(url_for("my_subscriptions"))

        return render_template("add_subscription.html", form=form)