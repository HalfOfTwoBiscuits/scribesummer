from flask import render_template
from flask.views import View

class MySubscriptions(View):
    def __init__(self, model_handler, form_handler):
        self.__mh = model_handler

    def dispatch_request(self) -> str:
        UserModel = self.__mh.get_model("User")
        user = self.__mh.db.get_or_404(UserModel, 1)
        subs = user.subscriptions # type: ignore

        if len(subs) == 0:
            return render_template("my_subscriptions_empty.html")
        else:
            CategoryModel = self.__mh.get_model("Category")

            cats = self.__mh.db.session.execute(
                self.__mh.db.select(CategoryModel)
            ).scalars()

            category_ids_by_sub = {sub.id : [cat.id for cat in sub.categories] for sub in subs}

            return render_template(
                "my_subscriptions.html",
                user=user,
                all_subscriptions=subs,
                all_categories=cats,
                category_ids_by_sub=category_ids_by_sub
            )