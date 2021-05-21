import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import CreatePost
from .models import User, Post, Followers
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    form = CreatePost(request.POST)
    if form.is_valid():
        Post.objects.create(user=request.user, text=form.cleaned_data['text'])
        return HttpResponseRedirect(reverse("index"))

    return render(request, "network/index.html", {
        "form": CreatePost(),
        "posts": posts,
        "page_obj": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def user_page(request, username):
    author_of_post = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user__username=username).order_by('-created_at')
    the_number_of_followers = Followers.objects.filter(whom=author_of_post).count()
    if request.method == "POST":
        is_followed = Followers.objects.filter(whom=author_of_post, who=request.user)
        if is_followed:
            is_followed.delete()
            return HttpResponseRedirect(reverse("user_page", args=[username]))
        else:
            Followers.objects.create(whom=author_of_post, who=request.user)
            return HttpResponseRedirect(reverse("user_page", args=[username]))

    return render(request, "network/user_page.html", {
        "author_of_post": author_of_post,
        "posts": posts,
        "followers": the_number_of_followers,
    })


def following_page(request, username):
    user = User.objects.get(username=username)
    following_users = Followers.objects.filter(who=user).values_list("whom__username", flat=True)
    posts = Post.objects.filter(user__username__in=following_users)
    return render(request, "network/following_page.html", {
        "posts": posts
    })


def edit(request, post_id):
    return render(request, "network/edit.html", {
        "post_id": post_id
    })


def like(request, id):
    post = Post.objects.get(id=id)
    print(post)
    post.update(likes=1)
    post.save()
    return render(request, "network/index.html")