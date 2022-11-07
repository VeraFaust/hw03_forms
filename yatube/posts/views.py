from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post, Group, User

User = get_user_model()


LIMIT = 10


def get_paginator(posts, request):
    paginator = Paginator(posts, LIMIT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    post_list = Post.objects.select_related('author', 'group')
    page_obj = get_paginator(post_list, request)
    template = 'posts/index.html'
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group)
    page_obj = get_paginator(post_list, request)
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    page_obj = get_paginator(post_list, request)
    template = 'posts/profile.html'
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    template = 'posts/post_detail.html'
    context = {
        'post': post,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        template = 'posts/create_post.html'
        context = {
            'form': form,
        }
        return render(request, template, context)

    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=post.author.username)


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        context = {
            'form': form,
            'post_id': post_id,
            'is_edit': True,
        }
        return render(request, 'posts/create_post.html', context)
    form.save()
    return redirect('posts:post_detail', post_id=post_id)
