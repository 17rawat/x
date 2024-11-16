from django.shortcuts import render, redirect

from .models import Post
# Create your views here.


def posts(request):
    posts = Post.objects.all()
    # print(posts)
    return render(request, "post/dashboard.html", {"posts": posts})


def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, "post/post_detail.html", {"post": post})


def add_post(request):
    if request.method == "POST":
        # print(request)
        title = request.POST["title"]
        content = request.POST["content"]
        Post.objects.create(title=title, content=content)
        return redirect("posts")

    return render(request, "post/add_post.html")


def edit_post(request, id):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        Post.objects.filter(id=id).update(title=title, content=content)
        return redirect("post_detail", id=id)

    post = Post.objects.get(id=id)
    return render(request, "post/edit_post.html", {"post": post})


def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("posts")
