from django.contrib.auth.models import AbstractUser
from django.db import models
# from . import forms 

#Add date/time aspect later for more complexity 

class User(AbstractUser):
    pass

class Listing(models.Model):
    item_owner = models.ForeignKey(User, related_name="item_owner", on_delete=models.CASCADE)
    highest_bidder = models.ForeignKey(User, blank=True, related_name="highest_bidder", on_delete=models.CASCADE)
    item_name = models.CharField(max_length=120)
    item_description = models.CharField(max_length=1000)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    isActive = models.BooleanField(default=True)
    item_category = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"{self.item_name} : {self.item_price}"

class Comment(models.Model):
    comment_item = models.ForeignKey(Listing, related_name="comment_item", on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name="user_comments", on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.commenter} : {self.comment}"

class Bid(models.Model):
    bid_item = models.ForeignKey(Listing, related_name="bid_item", on_delete=models.CASCADE)
    item_bidder = models.ForeignKey(User, related_name="interested_bids", on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bid_item}, bidder: {self.item_bidder} ${self.bid_amount}"

class WatchList(models.Model):
    user = models.ForeignKey(User, related_name="list_owner", on_delete=models.CASCADE)
    watch_item = models.ForeignKey(Listing, related_name="items_watching", on_delete=models.CASCADE)


class ClosedListing(models.Model):
    user_winner = models.ForeignKey(User, related_name="purchase_owner", on_delete=models.CASCADE)
    sold_item = models.ForeignKey(Listing, related_name="sold_item", on_delete=models.CASCADE)
