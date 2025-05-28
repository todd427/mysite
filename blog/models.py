from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
# blog/models.py

from taggit.models import TagBase, ItemBase


#tags = TaggableManager(through=TaggedPost)

class CustomTag(TagBase):
    slug = models.SlugField(unique=True, max_length=250)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class TaggedPost(ItemBase):
    content_object = models.ForeignKey('Post', on_delete=models.CASCADE)
    tag = models.ForeignKey(CustomTag, related_name="tagged_items", on_delete=models.CASCADE)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    tags = TaggableManager()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    status = models.CharField(
        max_length=250,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
            args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
            ]
        )

    def get_absolute_url(self):
        return reverse('blog:post_detail', 
            args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
            ]
        )   
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
