from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timezone as tz


# Create your models here.
class PublishManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False, status=Post.Status.PUBLISHED)

    def get_all(self):
        return super().get_queryset()

    def get_delete(self):
        return super().get_queryset().filter(is_delete=True, status=Post.Status.PUBLISHED)


class SourceModel(models.Model):
    #data
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


# Create your models here.
class Category(SourceModel):
    name = models.CharField(default='sport', max_length=20, verbose_name='Category')

    def __str__(self):
        return self.name


class Post(SourceModel):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECT = 'RJ', 'Rejected'

    # date
    publish = models.DateTimeField(default=timezone.now)
    #relation
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    categories = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='category_post')
    #data fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, verbose_name='slug')
    #choice status
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishManager()

    class Meta:

        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Ticket(SourceModel):
    message = models.TextField(verbose_name='message')
    name = models.CharField(max_length=250, verbose_name='name')
    phone = models.CharField(max_length=11)
    email = models.EmailField(verbose_name='email')
    subject = models.CharField(verbose_name='subject', max_length=10)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Ticket_users'

    def __str__(self):
        return self.name


class PostComment(SourceModel):
    post = models.ForeignKey(to=Post, related_name='comment',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.TextField()
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comment_users'

    def __str__(self):
        return f'{self.name}: {self.post}'


