from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import truncatechars


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    category = models.ManyToManyField(
        Category, blank=True, related_name='posts')
    excerpt = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    image = models.FileField(
        upload_to='static/thumbnail/', default='static/thumbnail/default/default.jpg')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    content = RichTextUploadingField(null=True)
    status = models.CharField(max_length=10, choices=options, default='draft')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    bookmark = models.ManyToManyField(
        User, blank=True, related_name='bookmark')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

    def get_absolute_url(self):
        return reverse('blog:post_single', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    @property
    def Title(self):
        return truncatechars(self.title, 50)

    @property
    def Slug(self):
        return truncatechars(self.slug, 50)


class Comment(models.Model):

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='comments_made')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return f'Comment by {self.name}'

    @property
    def Content(self):
        return truncatechars(self.content, 50)

    @property
    def Post(self):
        return truncatechars(self.post, 50)
