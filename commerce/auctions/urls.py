from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-item", views.new_item_view, name="new-item"),
    path("new-comment", views.new_item_comment, name="new-comment"),
    path("new-bid", views.new_bid_view, name="new-bid"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("close-listing", views.close_listing_view, name="close-listing"),
    path("categories", views.categories_view, name="categories"),
    path("categories-<str:category>", views.category_view, name="category"),
    path("<int:listing_id>", views.item_view, name="item"),
    path("<int:listing_id>-comment", views.item_comment_view, name="item-edit"),
    path("<int:listing_id>-bid", views.item_bid_view, name="item-bid"),
]
