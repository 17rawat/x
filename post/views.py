from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .forms import PostForm
from .models import Post, Comment
# Create your views here.


@login_required(login_url="/users/signin")
def posts(request):
    # posts = Post.objects.filter(author=request.user)
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "post/dashboard.html", {"posts": posts})


@login_required(login_url="/users/signin")
def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, "post/post_detail.html", {"post": post})


@login_required(login_url="/users/signin")
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        # print(form.errors)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post:posts")

    else:
        form = PostForm()

    return render(request, "post/add_post.html", {"form": form})


@login_required(login_url="/users/signin")
def edit_post(request, id):
    # post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id)

    # print(post)

    if post.author != request.user:
        return redirect("post:posts")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post:post_detail", id=id)

    else:
        form = PostForm(instance=post)

    return render(request, "post/edit_post.html", {"form": form, "post": post})


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
