from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    #order listings which are active from new -> old
    listings = Listing.objects.all().order_by('-time') 
    return render(request, 'auctions/index.html', {
        'listings': listings,
        'title': "Active Listings"
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


@login_required(login_url = "auction/login.html")
def create(request):
    if request.method == 'GET':
        return render(request, "auctions/create.html", {
            "listing_form": NewListingForm()
        })

    if request.method == 'POST':
        form = NewListingForm(request.POST, request.FILES)

        if form.is_valid():
            newListing = form.save(commit = False)
            newListing.user = request.user #assign foreign key
            newListing.save()

            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, "auctions/create.html", {
                "listing_form": form
            })
        

def category_list(request):
    categories = [category[0] for category in Listing._meta.get_field('category').choices]

    return render(request, "auctions/category_list.html", {
        "categories": categories
    })


def category_items(request, category_name):
    listings = Listing.objects.filter(category=category_name)

    return render(request, "auctions/category_items.html", {
        "listings": listings,
        "category_name": category_name
    })


def listing_detail(request, listing_id):
    listing_item = Listing.objects.get(pk = listing_id)
    bid = Bid.objects.filter(item = listing_item)
    comment = Comment.objects.filter(item = listing_item)
    
    #check if highest bidder
    highest_bid = bid.first()
    is_highest_bidder = False
    if highest_bid and highest_bid.user == request.user:
        is_highest_bidder = True

    if request.method == 'POST':
        if not listing_item.closed:
            #if clicked 'Close' button
            if request.POST.get("button") == 'Close':
                if request.user.is_authenticated:
                    listing_item.closed = True
                    listing_item.save()

                else:
                    return HttpResponseRedirect(reverse('login')) #redirect to login page if not logged in


        #if clicked 'Watchlist' button
        if request.POST.get("button") == 'Watchlist':
            if request.user.is_authenticated:
                if not WatchList.objects.filter(user = request.user, item = listing_item):
                    watchlist = WatchList()
                    watchlist.user = request.user
                    watchlist.item = listing_item
                    watchlist.save()
                    message = "Item added to Watchlist."

                else:
                    message = "Item already in Watchlist."

                return render(request, "auctions/listing_detail", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "comment_form": CommentForm(),
                        "bid": bid,
                        "comment": comment,
                        "message": message,
                        "is_highest_bidder": is_highest_bidder
                    })
                
            else:
                return HttpResponseRedirect(reverse('login')) #redirect to login page if not logged in


        
        #if clicked 'Bid' button
        if request.POST.get("button") == 'Place Bid':
            if request.user.is_authenticated:
                bid_form = BidForm(request.POST)

                if bid_form.is_valid():
                    new_bid = bid_form.save(commit=False)
                    new_bid.user = request.user
                    new_bid.item = listing_item
                    new_bid.save()

                    listing_item.currentBid = new_bid.price
                    listing_item.save()

                    return HttpResponseRedirect(reverse('listing_detail', args=(listing_id, )))
            
                else:
                    return render(request, "auctions/listing_detail.html", {
                        "listing": listing_item,
                        "bid_form": bid_form,
                        "comment_form": CommentForm(),
                        "bid": bid,
                        "comment": comment,
                        "is_highest_bidder": is_highest_bidder
                    })
            else:
                return HttpResponseRedirect(reverse('login')) #redirect to login page if not logged in
        

        #if clicked 'Comment' button
        if request.POST.get("button") == "Comment":
            if request.user.is_authenticated:
                comment_form = CommentForm(request.POST)

                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.user = request.user
                    new_comment.item = listing_item
                    new_comment.save()

                    return HttpResponseRedirect(reverse('listing_detail', args=(listing_id, )))
                
                else:
                    return render(request, "auctions/listing_detail.html", {
                        "listing": listing_item,
                        "bid_form": BidForm(),
                        "comment_form": comment_form,
                        "bid": bid,
                        "comment": comment,
                        "is_highest_bidder": is_highest_bidder
                    })
            
            else:
                return HttpResponseRedirect(reverse('login')) #redirect to login page if not logged in

    return render(request, "auctions/listing_detail.html", {
        "listing": listing_item,
        "bid_form": BidForm(),
        "comment_form": CommentForm(),
        "bid": bid,
        "comment": comment,
        "is_highest_bidder": is_highest_bidder
    })