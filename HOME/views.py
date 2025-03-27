from django.http import HttpResponse
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):
    post_list = Blog.objects.order_by('-id')
    main_post = Blog.objects.order_by('-id').filter(Main_post=True)[0:1]
    cat = Category.objects.all()

    # Pagination
    paginator = Paginator(post_list, 2)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        post = paginator.page(paginator.num_pages)

    context = {
        'post': post,
        'main_post': main_post,
        'cat': cat,
    }

    return render(request, 'HOME/index.html', context)

def blog_detail(request, slug):
    posts = Blog.objects.order_by('-id')[:5]
    cat = Category.objects.all()
    post = get_object_or_404(Blog, blog_slug = slug)
    comments = Comment.objects.filter(blog_id = post.id).order_by('-date')

    context = {
        'posts': posts,
        'cat': cat,
        'post': post,
        'comments': comments
    }

    return render (request, 'HOME/blog_detail.html', context)


def category(request, slug):
    cat = Category.objects.all()
    category_obj = get_object_or_404(Category, slug=slug)
    blog_list = Blog.objects.filter(category=category_obj)
    
    # Pagination
    paginator = Paginator(blog_list, 2)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        blog_cat = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blog_cat = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        blog_cat = paginator.page(paginator.num_pages)

    context = {
        'cat': cat,
        'active_category': slug,
        'blog_cat': blog_cat,
    }
    
    return render(request, 'HOME/category.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Blog, blog_slug = slug)
        comment_text = request.POST.get('InputComment')
        name = request.POST.get('InputName')
        email = request.POST.get('InputEmail')
        parent_id = request.POST.get('parent_id')
        parent_comment = None

        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id)

        Comment.objects.create(
            post = post,
            name = name,
            email = email,
            comment = comment_text,
            parent = parent_comment

        )
        return redirect('blog_detail', slug=post.blog_slug)
    return redirect('blog_detail')