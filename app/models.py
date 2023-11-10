from django.db import models
from django.contrib.auth.models import User
from forum import settings
from django.db.models.functions import Coalesce
from django.db.models import Max



class Category(models.Model):
    name = models.CharField(max_length=50, null = False, blank = False, unique= True)
    description = models.CharField(max_length = 1000, null = False, blank = False)
    slug = models.SlugField(max_length=50, unique=True)
    column = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField()
    bump_limit = models.PositiveIntegerField()
    can_post = models.BooleanField(default = True)


class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=False, null = False)
    text = models.CharField(max_length=2500, blank=False, null = False)
    created_at = models.DateTimeField(auto_now_add= True)
    bump = models.DateTimeField(auto_now_add= True)
    


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2500, blank=False, null = False)
    created_at = models.DateTimeField(auto_now_add= True)
    answer_to = models.ManyToManyField('self', null= True, blank=True)

    def save(self, *args, **kwargs):
        self.topic.bump = self.created_at
        self.topic.save()
        super(Comment, self).save(*args, **kwargs)


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
