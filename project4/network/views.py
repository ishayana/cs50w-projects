from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PostForm
from .models import User, Post, Like, Follow 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.core.paginator import Paginator



def index(request):
   
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            messages.success(request, "Your post submited successfully.", 'success')
            return redirect('network:index')
        messages.error(request, 'Somthing went wrong!', 'error')
        return redirect('network:index')
    
    if request.method == 'GET':
        form = PostForm()
        posts = Post.objects.all().order_by('-created')
        posts_list = []
        for post in posts:
            liked = False
            if request.user.is_authenticated:        
                try:
                    post.likes.get(user=request.user)
                    liked = True
                except Like.DoesNotExist:
                    liked = False
            posts_list.append((post, liked))
        p = Paginator(posts_list, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
    return render(request, "network/index.html", {'posts': page_obj, 'postform' : form, 'postcount' : p.count})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})

@login_required
def userpage(request, user_id):

    user = User.objects.get(pk=user_id)

    try:
        request.user.followings.get(following_id=user)
        followed = True
    except Follow.DoesNotExist:
        followed = False
    
    follower = user.followers.all()
    following = user.followings.all()
    user_posts_list = []
    user_posts = user.posts.all().order_by('-created')
    liked = False
    for post in user_posts:
        try:
            post.likes.get(user=request.user)
            liked = True
        except Like.DoesNotExist:
            liked = False
        user_posts_list.append((post, liked))
        p = Paginator(user_posts_list, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
    return render(request, 'network/user-page.html', {'follower':follower, 'following': following, 'user': user, 'user_posts': page_obj, 'followed' : followed, 'postcount': p.count})


def follow_user(request, user_id):
    user = User.objects.get(pk=user_id)
    
    following, created = request.user.followings.get_or_create(following_id=user.id)
    followed = False
    if not created:
        following.delete()
        followed = False
    else: 
        followed = True
    follower_count = user.followers.all().count()
    return JsonResponse({'followed' : followed, 'follower_count' : follower_count})


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if 'text' in data:
            post.text = data['text']
            post.save()
            return JsonResponse({'status': 'success', 'post': post_id, 'new_text': post.text})

def following_posts(request):
    following = request.user.followings.all().values('following')
    posts = Post.objects.filter(author__in=following).order_by('-created')
    posts_list = []
    for post in posts:
        liked = False
        if request.user.is_authenticated:        
            try:
                post.likes.get(user=request.user)
                liked = True
            except Like.DoesNotExist:
                liked = False
        posts_list.append((post, liked))
        p = Paginator(posts_list, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
    return render(request, 'network/following.html', {'posts':page_obj, 'postcount': p.count})