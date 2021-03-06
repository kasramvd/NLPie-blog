from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    tag_densities = ArrayField(
        ArrayField(models.CharField(max_length=30),
                   size=2)
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(default=0, null=True)
    docfile = models.TextField(blank=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class PostView(models.Model):
    post = models.ForeignKey(Post, related_name='postviews')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)


class Subscribers(models.Model):
    email = models.EmailField(null=True)
    subscribe_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email.split('@')[0]
