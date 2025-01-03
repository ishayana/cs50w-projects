from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CreateListinForm, BidForm, CommentForm
from .models import User, Listing, Bids, Comment, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError


def index(request):
    listings = Listing.objects.filter(active=True)
    listing_list = []
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    for listing in listings:
        is_watchlisted = False
        if request.user in listing.watchlist.all():
            is_watchlisted = True
        listing_list.append((listing, is_watchlisted))

    return render(request, "auctions/index.html", {'listsing_list' : listing_list, 'whatchlist_count': whatchlist_count})


def listing_details(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid_form = BidForm()
    bids = listing.bids.all()
    winner_user = None
    if bids:
        winner_user = Bids.objects.filter(listing=listing_id).order_by('-amount').latest('created').user
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing).order_by('-created')

    if request.method == 'POST':
        if 'bid_submit' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                if listing.bid >= bid_form.cleaned_data['amount']:
                    messages.warning(request, 'Your bid must be grater than current bid!', 'warning')
                    return redirect('auctions:listing_details', listing_id=listing.id)
                new_bid = bid_form.save(commit=False)
                new_bid.user = request.user
                new_bid.listing = listing
                new_bid.save()
                listing.bid = new_bid.amount
                listing.save()
                messages.success(request, 'Your bid submited successfully.', 'success')
                return redirect('auctions:index')
        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, 'Your commetn submited successfully.')
            else:
                messages.warning(request, 'Somthing went wrong!.')
            return redirect('auctions:listing_details', listing.id)

                
    return render(request, 'auctions/listing-details.html', {
                                                            'listing':listing,
                                                            'bid_form' : bid_form,
                                                            'comment_form': comment_form,
                                                            'comments' : comments,
                                                            'winner_user':winner_user,
                                                            'comments' : comments,
                                                            'whatchlist_count' : whatchlist_count
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    form = CreateListinForm()
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    if request.method == 'POST':
        form = CreateListinForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            # Category.objects.create(name=listing.category)
            messages.success(request, 'Your list created successfully!', 'success')
            return redirect('auctions:index')
        else:
            print(form.errors)
            messages.warning(request, 'Somthing wrong!', 'warning')
            return redirect('auctions:create')
            

    return render(request, 'auctions/create.html', {'form' : form, 'whatchlist_count' : whatchlist_count})

@login_required
def whatchlist(request):
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    watchlists = request.user.watchlists.all
    return render(request, 'auctions/watchlist.html', {'watchlists' : watchlists, 'whatchlist_count':whatchlist_count})


@login_required
def add_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)

    if request.user in listing.watchlist.all():
        listing.watchlist.remove(request.user)
        messages.success(request, f'{listing.title} removed from your watchlist!')
    else:
        listing.watchlist.add(request.user)
        messages.success(request, f'{listing.title} added to your watchlist.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def listing_close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.author == request.user:
        listing.active = False
        listing.save()
        messages.success(request, 'Your acutions closed!', 'success')
        return redirect('auctions:watchlist')
    return render(request, 'auctions/listing-details.html')

def category(request):
    categorys =  Category.objects.all()
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    return render(request, 'auctions/category.html', {'categorys' : categorys, 'whatchlist_count':whatchlist_count})

def category_details(request, category_id):
    whatchlist_count = ''
    if request.user.is_authenticated:
        whatchlist_count = request.user.watchlists.all().count
    category_lisings =  Listing.objects.filter(category=category_id)
    listing_list = []
    for listing in category_lisings:
        is_watchlisted = False
        if request.user in listing.watchlist.all():
            is_watchlisted = True
        listing_list.append((listing, is_watchlisted))
    print(listing_list)
    return render(request, 'auctions/category-details.html', {'listing_list' : listing_list, 'whatchlist_count':whatchlist_count})

