from django.contrib import admin
from .models import Topic, Category, Comment
admin.site.register(Topic)
admin.site.register(Category)
admin.site.register(Comment)
# Register your models here.
