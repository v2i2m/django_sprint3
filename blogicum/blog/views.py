from django.shortcuts import get_object_or_404, render
from blog.models import Post, Category
from datetime import datetime


def index(request):
    post_list = Post.objects.select_related(
        'category', 'author', 'location').filter(
        pub_date__date__lt=datetime.now(),
        is_published=True,
        category__is_published=True).order_by(
        'pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author', 'location').filter(
            id=post_id,
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )
    )
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    posts = Post.objects.select_related(
        'category', 'author', 'location').filter(
        category=category, is_published=True,
        pub_date__date__lt=datetime.now())
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, 'blog/category.html', context)
