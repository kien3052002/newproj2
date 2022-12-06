from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Category
from .forms import NewCommentForm, PostSearchForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from random import shuffle
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
# Create your views here.


def pagination(request, posts):
    obj = posts
    page_n = request.GET.get('page')
    p = Paginator(obj, 5)
    list = p.get_page(page_n)
    return list


def like(request, post):
    post = get_object_or_404(Post, slug=post)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:post_single', args=[post.slug]))


def home(request):
    posts = Post.newmanager.all()
    list = pagination(request, posts)
    return render(request, 'blog/index.html', {'posts': Post.newmanager.all(), 'categorys': Category.objects.all(), 'list': list})


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')
    user_comment = None
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
    suggestions = None
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    return render(request, 'blog/single.html', {'post': post, 'comments': comments, 'comment_form': comment_form, 'suggestions': suggestions, 'is_liked': is_liked})


def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    form = PostSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        c = form.cleaned_data['c']
        results = Post.objects.filter(Q(title__contains=q, status='published'))
        for tag in c:
            results = results.filter(category=tag.id)
    list = pagination(request, results)
    return render(request, 'blog/search.html', {'categorys': Category.objects.all(), 'posts': results, 'total_results': results.count, 'q': str(q), 'c': c, 'list': list})


def suggest(post):
    tags = post.category.all()
    suggestions = {}
    for tag in tags:
        s = list(tag.posts.all())
        suggestions.update(s)
    suggestions = list(suggestions)
    shuffle(suggestions)
    return suggestions[0:3]
