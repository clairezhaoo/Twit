from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Tweet
from django.utils import reverse

class TweetModelTests(TestCase):
    def test_was_published_recently_with_future_tweet(self):
        # returns false if published in future
        time = timezone.now() + datetime.timedelta(days=30)
        future_tweet = Tweet(pub_date=time)
        self.assertIs(future_tweet.was_published_recently(), False)

    def test_was_published_recently_with_old_tweet(self):
        # returns false if tweet is older than one day
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_tweet = Tweet(pub_date=time)
        self.assertIs(old_tweet.was_published_recently(), False)

    def test_was_published_recently_with_recent_tweet(self):
        # returns true for tweet within the last day
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_tweet = Tweet(pub_date=time)
        self.assertIs(recent_tweet.was_published_recently(), True)

def create_tweet(tweet_text, days):
    """
    create a tweet with the given `tweet_text` and published the
    given number of `days` offset to now (negative for tweets published
    in the past, positive for tweets that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Tweet.objects.create(tweet_text=tweet_text, pub_date=time)

class TweetIndexView(TestCase):
    def test_no_tweets(self):
        """if no tweets exist, display appropriate message"""
        response = self.client.get(reverse('twitter:index'))
        self.assertEqual(response.status_code 200)
        self.assertContains(response, 'No tweets are available')
        self.assertQuerysetEqual(response.context['latest_tweet_list'], [])

    def test_past_tweets(self):
        """tweets with a past pub date are displayed in index page"""
        create_tweet(tweet_text="Past tweet", days=-30)
        response = self.client.get(reverse('twitter:index'))
        self.assertQuerysetEqual(response.context['latest_tweet_list'],
        ['Tweet: Past tweet.'])

    def test_future_tweet(self):
        """tweets with a future pubdate are not displayed on index page"""
        create_tweet(tweet_text="Future tweet", days=30)
        response = self.client.get(reverse('twitter:index'))
        self.assertContains(response, 'No tweets are available')
        self.assertQuerysetEqual(response.context['latest_tweet_list'], [])

    def test_future_tweet_and_past_tweet(self):
        """if both future and past tweets exist, only past tweets are displayed"""
        create_tweet(tweet_text="Past tweet.", days=-30)
        create_tweet(tweet_text="Future tweet.", days=30)
        response = self.client.get(reverse('twitter:index'))
        self.assertQuerysetEqual(
            response.context['latest_tweet_list'],
            ['<Tweet: Past tweet.>']
        )

    def test_two_past_tweets(self):
        """the tweet index page may display multiple tweets"""
        create_tweet(tweet_text="Past tweet 1.", days=-30)
        create_tweet(tweet_text="Past tweet 2.", days=-5)
        response = self.client.get(reverse('twitter:index'))
        self.assertQuerysetEqual(
            response.context['latest_tweet_list'],
            ['<Tweet: Past tweet 2.>', '<Tweet: Past tweet 1.>']
        )

class TweetDetailViewTests(TestCase):
    def test_future_tweet(self):
        """future returns 404 not found"""
        future_tweet = create_tweet(tweet_text='Future tweet', days=5)
        url = reverse('twitter:detail', args=(future_tweet.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_tweet(self):
        """pubdate in past displays the tweet's text"""
        past_tweet = create_tweet(tweet_text='Past tweet', days=-5)
        url = reverse('twitter:detail', args=(past_tweet.id,))
        response = self.client.get(url)
        self.assertContains(response, past_tweet.tweet_text)
