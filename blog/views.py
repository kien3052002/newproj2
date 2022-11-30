from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Post, Comment, Category
from .forms import NewCommentForm, PostSearchForm
from django.views.generic import ListView
from django.db.models import Q

# Create your views here.


def home(request):

    all_posts = Post.newmanager.all()
    all_categorys = Category.objects.all()
    return render(request, 'blog/index.html', {'posts': all_posts, 'categorys': all_categorys})


def post_single(request, post):

    post = get_object_or_404(Post, slug=post, status='published')
    comments = post.comments.filter(status=True)

    user_comment = None

    if request.method == 'POST':
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/' + post.slug)
    else:
        comment_form = NewCommentForm()
    return render(request, 'blog/single.html', {'post': post, 'comments':  user_comment, 'comments': comments, 'comment_form': comment_form,})


# class CatListView(ListView):
#     template_name = 'blog/category.html'
#     context_object_name = 'catlist'

#     def get_queryset(self):
#         content = {
#             'cat': self.kwargs['category'],
#             'posts': Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
#         }
#         return content


def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()
    form = PostSearchForm(request.GET)
    if form.is_valid():
        q = form.cleaned_data['q']
        c = form.data.getlist('c')
        if q is not None:
            query &= Q(title__contains=q)
        results = Post.objects.filter(query)
        for tag in c:
            results = results.filter(tag in Post.category)

    return render(request, 'blog/search.html', {'form': form, 'q': q, 'results': results, })
