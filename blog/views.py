from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, HttpResponse
from .models import Post, Category
from .forms import NewCommentForm, PostSearchForm
from django.db.models import Q
from django.core.paginator import Paginator
from random import shuffle
from django.urls import reverse

# Create your views here.


def pagination(request, posts):
    obj = posts
    page_n = request.GET.get('page')
    p = Paginator(obj, 5)
    list = p.get_page(page_n)
    return list


def like(request, post):
    referer = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Post, slug=post)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(referer)


def bookmark(request, post):
    referer = request.META.get('HTTP_REFERER')
    post = get_object_or_404(Post, slug=post)
    if post.bookmark.filter(id=request.user.id).exists():
        post.bookmark.remove(request.user)
    else:
        post.bookmark.add(request.user)
    return HttpResponseRedirect(referer)


def home(request):
    posts = Post.newmanager.all()
    list = pagination(request, posts)
    return render(request, 'blog/index.html', {'posts': Post.newmanager.all(), 'categorys': Category.objects.all(), 'list': list})


def check_like(request, post):
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    return is_liked


def check_bookmark(request, post):
    is_marked = False
    if post.bookmark.filter(id=request.user.id).exists():
        is_marked = True
    return is_marked


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    user_comment = None
    suggestions = suggest(post)
    is_liked = check_like(request, post)
    is_marked = check_bookmark(request, post)
    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.name = request.user
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    comments = post.comments.filter(status=True)
    return render(request, 'blog/single.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'suggestions_list': suggestions, 'is_liked': is_liked, 'is_marked': is_marked})


def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    form = PostSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        c = form.cleaned_data['c']
        results = Post.newmanager.filter(
            Q(title__contains=q, status='published'))
        for tag in c:
            results = results.filter(category=tag.id)
    list = pagination(request, results)
    return render(request, 'blog/search.html', {'categorys': Category.objects.all(), 'posts': results, 'total_results': results.count, 'q': str(q), 'c': c, 'list': list})


def suggest(post):
    tags = post.category.all()
    suggestions = []
    query = Q()
    for tag in tags:
        query = query or Q(category=tag.id)
    suggestions = list(Post.newmanager.filter(query))
    if post in suggestions:
        suggestions.remove(post)
    shuffle(suggestions)
    if len(suggestions) > 3:
        suggestions = suggestions[0:3]
    return suggestions
