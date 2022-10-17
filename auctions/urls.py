from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("display", views.display, name="display"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("remove/<int:id>", views.remove, name="remove"),
    path("add/<int:id>", views.add, name="add"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeauction/<int:id>", views.closeauction, name="closeauction"),
    path("addcom/<int:id>", views.addcom, name="addcom"),
    path("watchlist", views.displaywatchlist, name="watchlist")
]
