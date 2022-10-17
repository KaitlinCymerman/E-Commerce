from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comments, Bid

def index(request):
    all_cat = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True),
        "categories": all_cat
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

def create(request):
    if request.method == "POST":
        #Users are able to create and specifiy their listing
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = request.POST["price"]
        category = request.POST["category"]
        user = request.user
        bid = Bid(bid=int(price), user=user)
        bid.save()
        category_data = Category.objects.get(catName=category)
        #After listing is created, users will be able to save their liiting
        newlist = Listing(
            title=title,
            description=descirption,
            url=image_url,
            price=bid,
            category=category_data,
            owner=user,
            is_active=True
        )
        newlist.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render (request, "auctions/create.html", {
            "categories": Category.objects.all()
        })

def display(request):
    if request.method == "POST":
        #Filter out everything in categories and allow users to choose which category to view in active listings
        choose_category = request.POST['category']
        category = Category.objects.get(catName=choose_category)
        all_cat = Category.objects.all()
        active_listings = Listing.objects.filter(is_active=True, category=category)
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_cat
        })

def listing(request, id):
    #Details about listing page
    listing_data = Listing.objects.get(pk=id)
    isListing_InWatchList = request.user in listing_data.watchlist.all()
    allcomments = Comments.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "isListing_InWatchList": isListing_InWatchList,
        "allcomments": allcomments,
        "is_owner": is_owner
    })

def addBid(request, id):
    #Users bid on items
    listing_data = Listing.objects.get(pk=id)
    new_bid = request.POST['new_bid']
    currentBid = listing_data.price.bid
    if int(new_bid) > currentBid:
        updateBid = Bid(user=request.user, bid=int(new_bid))
        updateBid.save()
        listing_data.price = updateBid
        listing_data.save()
        #If bid is greater than starting bid, it will be successful
        return render(request, "auctions/listing.html",{
            "listing": listing_data,
            "message": "Bid was sucessful!",
            "update": True,
        })
    else:
        #Any bid less thn the starting bid would result in an error
        return render(request, "auctions/listing.html",{
            "listing": listing_data,
            "message": "Bidding failed.",
            "update": False,
        })

def add(request, id):
    #Add to watchlist
    listing_data = Listing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def remove(request, id):
    #Remove from watchlist
    listing_data = Listing.objects.get(pk=id)
    user = request.user
    listing_data.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def closeauction(request, id):
    #Creators of the auction have the ability to close the auction
    listing_data = Listing.objects.get(pk=id)
    listing_data.is_active = False
    listing_data.save()
    return render(request, "auctions/listing.html", {
        "listing": listing_data,
        "update": True,
        "message": "Auction is over!"
    })

def addcom(request, id):
    #Allow users to write and add comments to listings
    user = request.user
    listing_data = Listing.objects.get(pk=id)
    text = request.POST["new_comment"]
    new_comment = Comments(
        writer=user,
        listing=listing_data,
        text=text
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def displaywatchlist(request):
    #Watchlist displays all listings added to that page
    return render(request, "auctions/watchlist.html",{
        "listings": request.user.watch_listing.all()
    })

