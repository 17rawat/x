from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
# Create your views here.


@login_required(login_url="/users/signin")
def posts(request):
    # posts = Post.objects.filter(author=request.user)
    posts = Post.objects.all()
    return render(request, "post/dashboard.html", {"posts": posts})


@login_required(login_url="/users/signin")
def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, "post/post_detail.html", {"post": post})


@login_required(login_url="/users/signin")
def add_post(request):
    if request.method == "POST":
        # print(request)
        title = request.POST["title"]
        content = request.POST["content"]
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect("post:posts")

    return render(request, "post/add_post.html")


@login_required(login_url="/users/signin")
def edit_post(request, id):
    post = Post.objects.get(id=id)

    if post.author != request.user:
        return redirect("post:posts")

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Post.objects.filter(id=id).update(title=title, content=content)
        return redirect("post:post_detail", id=id)

    return render(request, "post/edit_post.html", {"post": post})


@login_required(login_url="/users/signin")
def delete_post(request, id):
    post = Post.objects.get(id=id)

    if post.author != request.user:
        return redirect("post:posts")

    post.delete()
    return redirect("post:posts")


@login_required(login_url="/users/signin")
def add_comment(request, id):
    post = Post.objects.get(id=id)
    Comment.objects.create(
        post=post, author=request.user, content=request.POST["content"]
    )
    return redirect("post:post_detail", id=id)
