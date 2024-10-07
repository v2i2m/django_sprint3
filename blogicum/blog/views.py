from datetime import datetime

from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category

MAINPAGE_POST_LIMIT = 5


def get_objects():
    return Post.objects.select_related(
        'category', 'author', 'location')


def index(request):
    post_list = get_objects().filter(
        pub_date__date__lt=datetime.now(),
        is_published=True,
        category__is_published=True).order_by()[:MAINPAGE_POST_LIMIT]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(
        get_objects().filter(
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
    posts = get_objects().filter(
        category=category,
        pub_date__date__lt=datetime.now(),
        is_published=True,)
    context = {
        'category': category,
        'post_list': posts
    }
    return render(request, 'blog/category.html', context)
