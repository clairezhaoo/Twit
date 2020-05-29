from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect

class Tweet(models.Model):
    tweet_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    replies = models.IntegerField(default=0)
    def __str__(self):
        return self.tweet_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def get_absolute_url(self):
        return reverse('twitter:detail', kwargs={'pk': self.pk})

"""
class Reply(models.Model):
    reply_text = models.CharField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.reply_text


"""
