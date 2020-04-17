from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from .models import Tweet
from django.views import generic
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    latest_tweet_list = Tweet.objects.order_by('-pub_date')[:5]
    template = loader.get_template('twitter/home.html')
    context = {
        'latest_tweet_list': latest_tweet_list,
    }
    return render(request, 'twitter/home.html', context)

class TweetListView(ListView):
    model = Tweet
    template_name = 'twitter/home.html'
    context_object_name = 'latest_tweet_list'
    ordering = ['-pub_date']   # want most recent at top of page


def detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    context = {
        'tweet' : tweet,
        'tweet_id' : tweet_id,
    }
    return render(request, 'twitter/detail.html', context)

class TweetDetailView(DetailView):
    model = Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['tweet_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    fields = ['tweet_text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tweet = self.get_object()
        if self.request.user == tweet.author:
            return True
        return False

class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    success_url = '/'   # go home if tweet is deleted 

    def test_func(self):
        tweet = self.get_object()
        if self.request.user == tweet.author:
            return True
        return False
