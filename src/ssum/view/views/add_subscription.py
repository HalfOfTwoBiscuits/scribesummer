from flask import render_template, redirect, url_for
from flask.views import View
from werkzeug.wrappers.response import Response

from scribesummer.src.ssum.model.interval_enum import IntervalEnum

class AddSubscription(View):
    methods = ["GET", "POST"]

    def __init__(self, model_handler, form_handler):
        self.__mh = model_handler
        self.__AddCustomSubForm = form_handler.get_form("AddCustomSubscription")

    def dispatch_request(self) -> str | Response:
        form = self.__AddCustomSubForm(self.__mh)
        CategoryModel = self.__mh.get_model("Category")

        cats = list(self.__mh.db.session.execute(
            self.__mh.db.select(CategoryModel)
        ).scalars())

        cat_names = [(cat.id, cat.name) for cat in cats]
        form.categories.choices = cat_names

        if form.validate_on_submit():
            CustomSubscription = self.__mh.get_model("CustomSubscription")
            UserModel = self.__mh.get_model("User")
            user = self.__mh.db.get_or_404(UserModel, 1)

            # Get categories selected.
            matching_cats = [cat for cat in cats if cat.id in form.categories.data]

            sub = CustomSubscription(
                name=form.name.data,
                price_in_pence=int(form.price.data * 100),
                interval=IntervalEnum(form.interval.data[0].lower()),
                categories=matching_cats,
                first_renewal=form.date.data,
                user_obj=user
            )
            self.__mh.db.session.add(sub)
            self.__mh.db.session.commit()

            return redirect(url_for("my_subscriptions"))

        return render_template("add_subscription.html", form=form)