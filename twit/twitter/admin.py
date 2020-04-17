from django.contrib import admin

from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'tweet_text', 'author']

admin.site.register(Tweet, TweetAdmin)
