from django.contrib import admin
from .models import User, Listing, Comment, Bid, WatchList, ClosedListing

class UserAdmin(admin.ModelAdmin):
    list_display= ("id", "username", "email")
# class ListingAdmin(admin.ModelAdmin):
#     list_display = ("id", "item","item_description", "item_price", "item_category")

class ListingAdmin(admin.ModelAdmin):
    list_display=("id", "item_owner", "highest_bidder", "item_name", "item_description", "item_price", "isActive", "item_category")

class CommentAdmin(admin.ModelAdmin):
    list_display=("id", "comment_item", "commenter", "comment")

class BidAdmin(admin.ModelAdmin):
    list_display=("id", "bid_item", "item_bidder", "bid_amount")

class WatchListAdmin(admin.ModelAdmin):
    list_display=("id", "user", "watch_item")

class ClosedListingAdmin(admin.ModelAdmin):
    list_display=("id", "user_winner", "sold_item")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(ClosedListing, ClosedListingAdmin)

