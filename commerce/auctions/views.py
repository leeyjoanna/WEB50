from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid, WatchList, ClosedListing
from .forms import NewItemForm, NewCommentForm, NewBidForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive = True),
    })

def categories_view(request):
    return render(request, "auctions/categories.html", {
        "listings": Listing.objects.filter(isActive= True).values('item_category').distinct()
    })

def category_view(request, category):
    listings = Listing.objects.filter(item_category=category)
    return render(request, "auctions/category.html",{
        "listings":listings,
        "category": category
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def item_view(request, listing_id):
    listing = Listing.objects.filter(id=listing_id).first()
    current_user = request.user
    comments = Comment.objects.filter(comment_item= listing)
    bids = Bid.objects.filter(bid_item=listing)
    isOwner = False
    isClosed = False
    if listing in ClosedListing.objects.filter(sold_item=listing):
        isClosed = True
    if current_user == listing.item_owner:
        isOwner = True
    if listing: 
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "isOwner": isOwner,
            "isClosed": isClosed,
            "comments": comments,
            "bids": bids
        })
    return redirect('index')
    

@login_required
def new_item_view(request):
    if request.method == "POST":
         # Attempt to create new listing
        user = request.user
        name = request.POST["item_name"]
        description = request.POST["item_description"]
        price = request.POST["item_price"]
        category = request.POST["item_category"]
        try:
            newListing = Listing.objects.create(
                item_owner = user,
                highest_bidder = user,
                item_name = name, 
                item_description = description, 
                item_price = price,
                isActive = True,
                item_category = category
            )
            newListing.save()
        except IntegrityError:
            return render(request, "auctions/new-item.html", {
                "message": "Oops something went wrong, couldn't list your item!"
            })
        return redirect('index')

    form = NewItemForm()
    return render(request, "auctions/new-item.html", {
        "form": form
    })


@login_required
def item_comment_view(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        form = NewCommentForm()
        return render(request, "auctions/item-comment.html", {
            "listing": listing,
            "form": form
        })
    
    return render('index')


@login_required
def new_item_comment(request):
    if request.method == "POST":
        current_user = request.user
        listing_id = request.POST.get("item")
        listing = Listing.objects.get(pk=listing_id)
        new_comment = request.POST["comment"]
        try: 
            newComment = Comment.objects.create(
                comment_item = listing,
                commenter = current_user,
                comment = new_comment
            )
            newComment.save()
        except IntegrityError:
            return render(request, "auctions/item-comment.html", {
                "message": "Oops something went wrong, couldn't leave your comment!"
            })
        return redirect('index')
    return redirect('index')

@login_required
def item_bid_view(request, listing_id):
    if request.method == "POST": 
        listing = Listing.objects.get(pk=listing_id)
        form = NewBidForm()
        return render(request, "auctions/item-bid.html", {
            "listing": listing,
            "form": form
        })
    return redirect('index')

@login_required
def new_bid_view(request):
    if request.method=="POST":
        bid_amount = float(request.POST["bid_amount"])
        current_user = request.user
        listing_id = request.POST.get("item")
        listing = Listing.objects.get(id=listing_id)
        if (bid_amount <= listing.item_price):
             return render(request, "auctions/item-bid.html", {
                "message": "Oops please place a bid higher than the current price!"
            })
        try: 
            newBid = Bid.objects.create(
                bid_item = listing,
                item_bidder = current_user,
                bid_amount = bid_amount
            )
            newBid.save()
            listing.item_price = bid_amount
            listing.highest_bidder = current_user
            listing.save()
            #need to upgrade listing price 
        except IntegrityError:
            return render(request, "auctions/item-bid.html", {
                "message": "Oops something went wrong, couldn't make your bid!"
            })
        return redirect('index')

    return redirect('index')

        
@login_required
def watchlist_view(request):
    if request.method=="POST":
        current_user = request.user
        listing_id = request.POST.get("item")
        listing = Listing.objects.get(pk=listing_id)
        try: 
            newWatch = WatchList.objects.create(
               user = current_user,
               watch_item = listing
            )
            newWatch.save()
        except IntegrityError:
            return render(request, "auctions/watchlist.html", {
                "message": "Oops something went wrong, couldn't add this to your watchlist!"
            })
        watchlist = WatchList.objects.filter(user=current_user)
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlist

        })
    current_user = request.user
    watchlistQS = WatchList.objects.filter(user=current_user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlistQS
    })

@login_required
def close_listing_view(request):
    if request.method=="POST":
        listing_id = request.POST.get("item")
        listing = Listing.objects.get(pk=listing_id)
        current_user = request.user
        highest_bidder = listing.highest_bidder
        #not delete, add to Closed model (list of closed listings)
        #need to find user_id of person who placed highest bid
        try:
            newClosedListing = ClosedListing.objects.create(
                user_winner = highest_bidder,
                sold_item = listing
            )
            listing.isActive = False
            listing.save()
        except IntegrityError:
            return render(request, "auctions/close-listing.html", {
                "message": "Oops something went wrong! Couldn't close your listing!"
            })
        if current_user == listing.highest_bidder: 
            return render(request, "auctions/close-listing.html", {
                "message": "No sale conducted. Listing successfully closed."
            })
        return render(request, "auctions/close-listing.html", {
            "message": "Congrats on a sale! Listing successfully closed!",
        })
    return redirect('index')

