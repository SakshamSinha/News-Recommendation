# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.utils import timezone

from django.db import models

# Create your models here.
class UserModel(models.Model):
    """User Model Station"""

    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=80)


class UserProfileModel(models.Model):
    """User profile model"""

    profileof_user = models.ForeignKey(UserModel,
                                       on_delete=models.CASCADE)
    static_prefs = models.CharField(max_length=150)
    dynamic_prefs = models.TextField(null=True)


class NewsModel(models.Model):
    """News Model"""

    title = models.TextField()
    description = models.TextField()
    url = models.URLField()
    author = models.CharField(null=True,max_length=50)
    trend_factor = models.FloatField(null=True)
    categories = models.TextField(null=True)
    keywords = models.TextField(null=True)
    published_at = models.DateTimeField(default=timezone.now())


class NewsProfileModel(models.Model):
    """News Profile model"""

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, related_name="news")
    show_more = models.BooleanField(default=False)
    relevance = models.BooleanField(default=False)